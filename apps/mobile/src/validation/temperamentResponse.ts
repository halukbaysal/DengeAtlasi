import type {components} from '@denge-atlasi/api-client';
import {z} from 'zod';

import {retrievalResultSchema} from './analysisResponse';

export type TemperamentResponse = components['schemas']['TemperamentResponse'];

const findingSchema = z
  .object({citationIds: z.array(z.string().min(1)).min(1), text: z.string().min(1)})
  .strict();

export const temperamentResponseSchema: z.ZodType<TemperamentResponse> = z
  .object({
    citations: z.array(retrievalResultSchema).optional(),
    correlationId: z.string().uuid(),
    educationalDisclaimer: z.string().min(1),
    medicalSafetyNotice: z.string().min(1).nullable().optional(),
    primarySourceFindings: z.array(findingSchema).optional(),
    reflectionQuestions: z.array(z.string().min(1)).optional(),
    safeWellbeingSuggestions: z.array(z.string().min(1)).optional(),
    sourceLimitNote: z.string().min(1).nullable().optional(),
    status: z.enum([
      'THEMES_FOUND',
      'SOURCE_LIMITED',
      'MEDICAL_REDIRECT',
      'SAFETY_REDIRECT',
    ]),
    supplementReason: z.string().min(1).nullable().optional(),
    supplementaryFindings: z.array(findingSchema).optional(),
    symbolicThemes: z.array(z.string().min(1)).optional(),
  })
  .strict()
  .superRefine((response, context) => {
    if (response.status === 'THEMES_FOUND' && !response.primarySourceFindings?.length) {
      context.addIssue({code: 'custom', message: 'Temperament themes require a primary source.'});
    }
    const citations = new Set(response.citations?.map(item => item.chunkId) ?? []);
    const findings = [
      ...(response.primarySourceFindings ?? []),
      ...(response.supplementaryFindings ?? []),
    ];
    if (findings.some(finding => finding.citationIds.some(id => !citations.has(id)))) {
      context.addIssue({code: 'custom', message: 'Temperament citation is unavailable.'});
    }
  });
