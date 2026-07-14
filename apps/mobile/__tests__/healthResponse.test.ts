import {healthResponseSchema} from '../src/validation/healthResponse';

test('accepts a valid backend health response', () => {
  const result = healthResponseSchema.parse({
    status: 'ok',
    service: 'denge-atlasi-api',
    version: '0.1.0',
    timestamp: '2026-07-13T12:00:00+00:00',
  });

  expect(result.status).toBe('ok');
});

test('rejects contract drift', () => {
  expect(() =>
    healthResponseSchema.parse({
      status: 'healthy',
      service: 'denge-atlasi-api',
      version: '0.1.0',
      timestamp: 'not-a-date',
    }),
  ).toThrow();
});
