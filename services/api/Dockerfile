FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade --yes \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir --upgrade pip==26.0.1

RUN addgroup --system api && adduser --system --ingroup api api

COPY services/api/requirements.txt ./services/api/requirements.txt
RUN python -m pip install --requirement services/api/requirements.txt

COPY services/__init__.py ./services/__init__.py
COPY services/api ./services/api

USER api
EXPOSE 8000
CMD ["uvicorn", "services.api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
