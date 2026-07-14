import type {
  AnalyticsEvent,
  AnalyticsProperties,
} from '../src/analytics/analytics';

test('analytics contract contains only allowlisted non-sensitive metadata', () => {
  const event: AnalyticsEvent = 'analysis_completed';
  const properties: AnalyticsProperties = {
    outcome: 'answer',
    screen: 'result',
    sourceRole: 'primary',
  };

  expect(event).toBe('analysis_completed');
  expect(Object.keys(properties).sort()).toEqual([
    'outcome',
    'screen',
    'sourceRole',
  ]);
  expect(JSON.stringify(properties)).not.toMatch(/query|prompt|excerpt|health/i);
  expect(JSON.stringify(properties)).not.toMatch(/journal|body|note|private/i);
});
