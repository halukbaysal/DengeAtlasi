import type {components} from '@denge-atlasi/api-client';
import {z} from 'zod';

export type AnalysisResponse = components['schemas']['AnalysisResponse'];

const retrievalResultSchema = z
  .object({
    author: z.string().min(1),
    category: z.string().min(1),
    chunkId: z.string().min(1),
    edition: z.string().min(1),
    excerpt: z.string().min(1),
    pageNumber: z.number().int().positive(),
    score: z.number().min(0).max(1),
    section: z.string().min(1),
    sourceId: z.string().min(1),
    workTitle: z.string().min(1),
  })
  .strict();

const generatedClaimSchema = z
  .object({
    citationIds: z.array(z.string().min(1)).min(1),
    text: z.string().min(1),
  })
  .strict();

export const analysisResponseSchema: z.ZodType<AnalysisResponse> = z
  .object({
    citations: z.array(retrievalResultSchema).optional(),
    correlationId: z.string().uuid(),
    generalSymbolicInterpretation: z.string().min(1).nullable().optional(),
    medicalNotice: z.string().min(1).nullable().optional(),
    message: z.string().min(1).nullable().optional(),
    promptId: z.string().min(1).nullable().optional(),
    promptVersion: z.string().min(1).nullable().optional(),
    sourceLimitNote: z.string().min(1).nullable().optional(),
    sourcedClaims: z.array(generatedClaimSchema).optional(),
    status: z.enum([
      'ANSWER',
      'SOURCE_LIMITED',
      'OUT_OF_SCOPE',
      'SAFETY_REDIRECT',
      'MEDICAL_REDIRECT',
      'PROVIDER_UNAVAILABLE',
      'CITATION_VALIDATION_FAILED',
    ]),
  })
  .strict()
  .superRefine((response, context) => {
    if (response.status === 'ANSWER') {
      if (!response.sourcedClaims?.length || !response.citations?.length) {
        context.addIssue({
          code: 'custom',
          message: 'Grounded answers require claims and citations.',
        });
      }
      const citationIds = new Set(
        response.citations?.map(citation => citation.chunkId) ?? [],
      );
      for (const claim of response.sourcedClaims ?? []) {
        if (claim.citationIds.some(id => !citationIds.has(id))) {
          context.addIssue({
            code: 'custom',
            message: 'Claim references an unavailable citation.',
          });
        }
      }
    }
  });
