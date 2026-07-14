import React from 'react';
import ReactTestRenderer from 'react-test-renderer';
import {Switch} from 'react-native';

import {requestTemperament} from '../src/api/temperamentApi';
import {TemperamentConsentScreen} from '../src/screens/TemperamentConsentScreen';
import {temperamentResponseSchema} from '../src/validation/temperamentResponse';

const citation = {
  author: 'Synthetic Author',
  category: 'PRIMARY',
  chunkId: 'chunk-1',
  edition: 'Test Edition',
  excerpt: 'Synthetic excerpt',
  pageNumber: 1,
  score: 0.9,
  section: 'Balance',
  sourceId: 'SRC-1',
  workTitle: 'Marifetname',
};
const response = {
  status: 'THEMES_FOUND',
  primarySourceFindings: [{text: 'Bu tema ilgili olabilir.', citationIds: ['chunk-1']}],
  citations: [citation],
  educationalDisclaimer: 'Bu bir kişilik testi değildir.',
  correlationId: '6f49ad7f-1a51-4ad7-a8d9-d044a4fc4ac5',
};

test('consent flow blocks continuation until all requirements are accepted', async () => {
  const navigate = jest.fn();
  let renderer!: ReactTestRenderer.ReactTestRenderer;
  await ReactTestRenderer.act(() => {
    renderer = ReactTestRenderer.create(
      <TemperamentConsentScreen navigation={{navigate} as never} route={{} as never} />,
    );
  });
  const continueButton = renderer.root.findAllByProps({accessibilityRole: 'button'})[0];
  expect(continueButton.props.disabled).toBe(true);
  const switches = renderer.root.findAllByType(Switch);
  for (const item of switches) {
    await ReactTestRenderer.act(() => item.props.onValueChange(true));
  }
  const enabledButton = renderer.root.findAllByProps({accessibilityRole: 'button'})[0];
  expect(enabledButton.props.disabled).toBe(false);
  await ReactTestRenderer.act(() => enabledButton.props.onPress());
  expect(navigate).toHaveBeenCalledWith('TemperamentInput');
});

test('validates thematic output and rejects definitive uncited output', () => {
  expect(temperamentResponseSchema.safeParse(response).success).toBe(true);
  expect(
    temperamentResponseSchema.safeParse({
      ...response,
      primarySourceFindings: [{text: 'Kesin tipin budur.', citationIds: ['fake']}],
    }).success,
  ).toBe(false);
});

test('temperament API uses generated request shape', async () => {
  const fetcher = jest.fn().mockResolvedValue({ok: true, json: async () => response});
  const result = await requestTemperament(
    {
      observations: 'denge',
      consentAccepted: true,
      confirmsAdult: true,
      confirmsSelfReport: true,
      includeLifestyleContext: false,
    },
    {baseUrl: 'https://example.test', fetcher},
  );
  expect(result.status).toBe('THEMES_FOUND');
  expect(fetcher).toHaveBeenCalledWith(
    'https://example.test/api/v1/analyze/temperament',
    expect.objectContaining({method: 'POST'}),
  );
});
