from __future__ import annotations

import logging
import time
from collections import defaultdict, deque
from collections.abc import Callable
from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("denge_atlasi.http")


class SecurityMiddleware:
    """Payload-safe API guard that never records request or response content."""

    def __init__(
        self,
        app: ASGIApp,
        *,
        max_body_bytes: int,
        rate_limit_requests: int,
        rate_limit_window_seconds: int,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.app = app
        self.max_body_bytes = max_body_bytes
        self.rate_limit_requests = rate_limit_requests
        self.rate_limit_window_seconds = rate_limit_window_seconds
        self.clock = clock
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not scope.get("path", "").startswith("/api/"):
            await self.app(scope, receive, send)
            return

        started = self.clock()
        correlation_id = self._correlation_id(scope)
        client = scope.get("client")
        client_key = str(client[0]) if client else "unknown"
        if self._rate_limited(client_key, started):
            await self._json_error(send, 429, "RATE_LIMITED", correlation_id)
            self._log(scope, 429, correlation_id, started)
            return

        body = await self._read_body(receive)
        if body is None:
            await self._json_error(send, 413, "PAYLOAD_TOO_LARGE", correlation_id)
            self._log(scope, 413, correlation_id, started)
            return

        status_code = 500

        async def replay() -> Message:
            return {"type": "http.request", "body": body, "more_body": False}

        async def guarded_send(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
                headers = list(message.get("headers", []))
                headers.append((b"x-correlation-id", correlation_id.encode("ascii")))
                message = {**message, "headers": headers}
            await send(message)

        await self.app(scope, replay, guarded_send)
        self._log(scope, status_code, correlation_id, started)

    async def _read_body(self, receive: Receive) -> bytes | None:
        chunks = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return bytes(chunks)
            chunks.extend(message.get("body", b""))
            if len(chunks) > self.max_body_bytes:
                return None
            if not message.get("more_body", False):
                return bytes(chunks)

    def _rate_limited(self, client: str, now: float) -> bool:
        requests = self._requests[client]
        cutoff = now - self.rate_limit_window_seconds
        while requests and requests[0] <= cutoff:
            requests.popleft()
        if len(requests) >= self.rate_limit_requests:
            return True
        requests.append(now)
        return False

    @staticmethod
    def _correlation_id(scope: Scope) -> str:
        headers = dict(scope.get("headers", []))
        supplied = headers.get(b"x-correlation-id", b"").decode("ascii", "ignore")
        if supplied and len(supplied) <= 64 and supplied.replace("-", "").isalnum():
            return supplied
        return str(uuid4())

    @staticmethod
    async def _json_error(
        send: Send, status_code: int, error_code: str, correlation_id: str
    ) -> None:
        body = (
            f'{{"detail":"{error_code}","correlationId":"{correlation_id}"}}'
        ).encode()
        await send(
            {
                "type": "http.response.start",
                "status": status_code,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(body)).encode()),
                    (b"x-correlation-id", correlation_id.encode()),
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})

    def _log(
        self, scope: Scope, status_code: int, correlation_id: str, started: float
    ) -> None:
        logger.info(
            "api_request endpoint=%s method=%s status=%d correlation_id=%s latency_ms=%d",
            scope.get("path"),
            scope.get("method"),
            status_code,
            correlation_id,
            int((self.clock() - started) * 1000),
        )
