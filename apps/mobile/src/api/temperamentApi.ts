import type {components} from '@denge-atlasi/api-client';

import {
  TemperamentResponse,
  temperamentResponseSchema,
} from '../validation/temperamentResponse';
import {AnalysisApiError, InvalidAnalysisResponseError, OfflineAnalysisError} from './analysisApi';

type TemperamentRequest = components['schemas']['TemperamentRequest'];

export async function requestTemperament(
  request: TemperamentRequest,
  options: {baseUrl: string; fetcher?: typeof fetch},
): Promise<TemperamentResponse> {
  let response: Response;
  try {
    response = await (options.fetcher ?? fetch)(
      `${options.baseUrl}/api/v1/analyze/temperament`,
      {
        body: JSON.stringify(request),
        headers: {'Content-Type': 'application/json'},
        method: 'POST',
      },
    );
  } catch {
    throw new OfflineAnalysisError('Mizaç öz-düşünümü için ağ bağlantısı gerekiyor.');
  }
  if (!response.ok) throw new AnalysisApiError('Mizaç öz-düşünümü tamamlanamadı.');
  const parsed = temperamentResponseSchema.safeParse(await response.json());
  if (!parsed.success) throw new InvalidAnalysisResponseError('Geçersiz mizaç yanıtı engellendi.');
  return parsed.data;
}
