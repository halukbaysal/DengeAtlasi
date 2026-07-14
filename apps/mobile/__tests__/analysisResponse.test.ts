import {analysisResponseSchema} from '../src/validation/analysisResponse';

const citation = {
  author: 'Synthetic Author',
  category: 'PRIMARY',
  chunkId: 'chunk-1',
  edition: 'Synthetic test edition',
  excerpt: 'Synthetic excerpt',
  pageNumber: 1,
  score: 0.9,
  section: 'Test section',
  sourceId: 'SRC-TEST-1',
  workTitle: 'Synthetic Work',
};

test('accepts a grounded response matching the generated contract', () => {
  const result = analysisResponseSchema.safeParse({
    status: 'ANSWER',
    sourcedClaims: [{text: 'Supported claim', citationIds: ['chunk-1']}],
    citations: [citation],
    correlationId: '6f49ad7f-1a51-4ad7-a8d9-d044a4fc4ac5',
  });
  expect(result.success).toBe(true);
});

test('rejects malformed and citation-spoofed responses', () => {
  const result = analysisResponseSchema.safeParse({
    status: 'ANSWER',
    sourcedClaims: [{text: 'Unsupported claim', citationIds: ['fake-id']}],
    citations: [citation],
    correlationId: 'not-a-uuid',
    rawProviderOutput: 'must never reach mobile',
  });
  expect(result.success).toBe(false);
});
