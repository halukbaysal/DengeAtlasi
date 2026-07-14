import type {components} from '@denge-atlasi/api-client';

import {
  AnalysisResponse,
  analysisResponseSchema,
} from '../validation/analysisResponse';

type AnalysisRequest = components['schemas']['AnalysisRequest'];

export class OfflineAnalysisError extends Error {}
export class InvalidAnalysisResponseError extends Error {}
export class AnalysisApiError extends Error {}

export async function requestAnalysis(
  request: AnalysisRequest,
  options: {baseUrl: string; fetcher?: typeof fetch},
): Promise<AnalysisResponse> {
  const fetcher = options.fetcher ?? fetch;
  let response: Response;
  try {
    response = await fetcher(`${options.baseUrl}/api/v1/analyze/reflection`, {
      body: JSON.stringify(request),
      headers: {'Content-Type': 'application/json'},
      method: 'POST',
    });
  } catch {
    throw new OfflineAnalysisError('Yeni analiz için ağ bağlantısı gerekiyor.');
  }
  if (!response.ok) {
    throw new AnalysisApiError('Analiz şu anda tamamlanamadı.');
  }
  const parsed = analysisResponseSchema.safeParse(await response.json());
  if (!parsed.success) {
    throw new InvalidAnalysisResponseError('Geçersiz API yanıtı güvenli biçimde engellendi.');
  }
  return parsed.data;
}
