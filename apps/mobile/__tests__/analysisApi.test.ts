import {
  AnalysisApiError,
  InvalidAnalysisResponseError,
  OfflineAnalysisError,
  requestAnalysis,
} from '../src/api/analysisApi';

const validResponse = {
  status: 'ANSWER',
  sourcedClaims: [{text: 'Supported', citationIds: ['chunk-1']}],
  citations: [
    {
      author: 'Author',
      category: 'PRIMARY',
      chunkId: 'chunk-1',
      edition: 'Edition',
      excerpt: 'Excerpt',
      pageNumber: 1,
      score: 0.8,
      section: 'Section',
      sourceId: 'SRC-1',
      workTitle: 'Marifetname',
    },
  ],
  correlationId: '6f49ad7f-1a51-4ad7-a8d9-d044a4fc4ac5',
};

test('submits analysis and validates successful API data', async () => {
  const fetcher = jest.fn().mockResolvedValue({ok: true, json: async () => validResponse});
  const result = await requestAnalysis(
    {query: 'denge', topK: 5},
    {baseUrl: 'https://example.test', fetcher},
  );
  expect(result.status).toBe('ANSWER');
  expect(fetcher).toHaveBeenCalledWith(
    'https://example.test/api/v1/analyze/reflection',
    expect.objectContaining({method: 'POST'}),
  );
});

test('blocks malformed data and reports offline failures', async () => {
  const malformed = jest.fn().mockResolvedValue({ok: true, json: async () => ({status: 'ANSWER'})});
  await expect(
    requestAnalysis({query: 'denge', topK: 5}, {baseUrl: '', fetcher: malformed}),
  ).rejects.toBeInstanceOf(InvalidAnalysisResponseError);

  const offline = jest.fn().mockRejectedValue(new TypeError('network'));
  await expect(
    requestAnalysis({query: 'denge', topK: 5}, {baseUrl: '', fetcher: offline}),
  ).rejects.toBeInstanceOf(OfflineAnalysisError);
});

test('maps non-success HTTP responses to a safe API error', async () => {
  const fetcher = jest.fn().mockResolvedValue({ok: false, status: 503});
  await expect(
    requestAnalysis({query: 'denge', topK: 5}, {baseUrl: '', fetcher}),
  ).rejects.toBeInstanceOf(AnalysisApiError);
});
