import {z} from 'zod';
import type {components} from '@denge-atlasi/api-client';

export type HealthResponse = components['schemas']['HealthResponse'];

export const healthResponseSchema: z.ZodType<HealthResponse> = z
  .object({
    status: z.literal('ok'),
    service: z.string().min(1),
    version: z.string().min(1),
    timestamp: z.iso.datetime({offset: true}),
  })
  .strict();
