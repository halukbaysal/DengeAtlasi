import React from 'react';
import ReactTestRenderer from 'react-test-renderer';

import {MedicalSafetyNotice, SourceLimitNotice} from '../src/components/Notices';
import {SourceCard} from '../src/components/SourceCard';
import {validateQuestion} from '../src/screens/AskScreen';

const citation = {
  author: 'Synthetic Author',
  category: 'PRIMARY',
  chunkId: 'chunk-1',
  edition: 'Test Edition',
  excerpt: 'Synthetic excerpt',
  pageNumber: 12,
  score: 0.9,
  section: 'Balance',
  sourceId: 'SRC-1',
  workTitle: 'Marifetname',
};

test('question form validation enforces API limits', () => {
  expect(validateQuestion(' ')).toBeTruthy();
  expect(validateQuestion('x'.repeat(1001))).toBeTruthy();
  expect(validateQuestion('denge')).toBeNull();
});

test('citation is accessible and navigates on activation', async () => {
  const onOpen = jest.fn();
  let renderer!: ReactTestRenderer.ReactTestRenderer;
  await ReactTestRenderer.act(() => {
    renderer = ReactTestRenderer.create(<SourceCard citation={citation} onOpen={onOpen} />);
  });
  const button = renderer.root.findByProps({accessibilityRole: 'button'});
  await ReactTestRenderer.act(() => button.props.onPress());
  expect(button.props.accessibilityLabel).toContain('Sayfa 12');
  expect(onOpen).toHaveBeenCalledWith(citation);
});

test('medical and source-limit notices remain visible and labeled', async () => {
  let renderer!: ReactTestRenderer.ReactTestRenderer;
  await ReactTestRenderer.act(() => {
    renderer = ReactTestRenderer.create(
      <>
        <SourceLimitNotice text="Kaynak sınırlı" />
        <MedicalSafetyNotice text="Hekime danışın" />
      </>,
    );
  });
  expect(renderer.root.findByProps({accessibilityLabel: 'Kaynak sınırlaması'})).toBeTruthy();
  expect(renderer.root.findByProps({accessibilityLabel: 'Tıbbi güvenlik uyarısı'})).toBeTruthy();
});
