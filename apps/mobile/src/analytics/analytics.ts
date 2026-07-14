export type AnalyticsEvent =
  | 'screen_viewed'
  | 'analysis_started'
  | 'analysis_completed'
  | 'analysis_failed'
  | 'citation_opened'
  | 'reflection_saved'
  | 'tts_started'
  | 'offline_state_seen';

export type AnalyticsProperties = Readonly<{
  screen?: 'home' | 'ask' | 'result' | 'source_detail';
  outcome?:
    | 'answer'
    | 'source_limited'
    | 'medical_redirect'
    | 'safety_redirect'
    | 'error';
  sourceRole?: 'primary' | 'supplementary';
}>;

export interface Analytics {
  track(event: AnalyticsEvent, properties?: AnalyticsProperties): void;
}

const EVENTS = new Set<AnalyticsEvent>([
  'screen_viewed',
  'analysis_started',
  'analysis_completed',
  'analysis_failed',
  'citation_opened',
  'reflection_saved',
  'tts_started',
  'offline_state_seen',
]);
const PROPERTY_VALUES = {
  screen: new Set(['home', 'ask', 'result', 'source_detail']),
  outcome: new Set([
    'answer',
    'source_limited',
    'medical_redirect',
    'safety_redirect',
    'error',
  ]),
  sourceRole: new Set(['primary', 'supplementary']),
} as const;

export function validateAnalyticsEvent(
  event: string,
  properties: Readonly<Record<string, unknown>> = {},
): void {
  if (!EVENTS.has(event as AnalyticsEvent)) {
    throw new Error('Analytics event is not allowlisted.');
  }
  for (const [key, value] of Object.entries(properties)) {
    const allowed = PROPERTY_VALUES[key as keyof typeof PROPERTY_VALUES];
    if (!allowed || typeof value !== 'string' || !allowed.has(value as never)) {
      throw new Error('Analytics property is not allowlisted.');
    }
  }
}

export const disabledAnalytics: Analytics = {
  track: (event, properties) => validateAnalyticsEvent(event, properties),
};
