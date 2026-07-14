import type {
  AnalyticsEvent,
  AnalyticsProperties,
} from '../src/analytics/analytics';
import {validateAnalyticsEvent} from '../src/analytics/analytics';

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

test('runtime analytics allowlist rejects sensitive or unknown payloads', () => {
  expect(() => validateAnalyticsEvent('journal_text')).toThrow('not allowlisted');
  expect(() =>
    validateAnalyticsEvent('analysis_started', {prompt_text: 'private'}),
  ).toThrow('not allowlisted');
  expect(() =>
    validateAnalyticsEvent('analysis_completed', {outcome: 'diagnosis'}),
  ).toThrow('not allowlisted');
});
