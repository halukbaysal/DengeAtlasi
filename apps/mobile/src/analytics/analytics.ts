export type AnalyticsEvent =
  | 'screen_viewed'
  | 'analysis_started'
  | 'analysis_completed'
  | 'analysis_failed'
  | 'citation_opened'
  | 'reflection_saved'
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

export const disabledAnalytics: Analytics = {
  track: () => undefined,
};
