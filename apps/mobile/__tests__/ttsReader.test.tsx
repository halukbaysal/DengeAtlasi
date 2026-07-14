import React from 'react';
import ReactTestRenderer from 'react-test-renderer';
import {AppState, Text} from 'react-native';

import {TtsReader} from '../src/components/TtsReader';
import type {TtsAdapter} from '../src/features/tts/adapter';

function adapter(overrides: Partial<TtsAdapter> = {}): TtsAdapter {
  return {
    initialize: jest.fn().mockResolvedValue(undefined),
    pause: jest.fn().mockResolvedValue(true),
    resume: jest.fn().mockResolvedValue(true),
    speak: jest.fn().mockResolvedValue(undefined),
    stop: jest.fn().mockResolvedValue(undefined),
    ...overrides,
  };
}

test('does not autoplay and exposes accessible play, pause, stop, and rate controls', async () => {
  const engine = adapter();
  let renderer!: ReactTestRenderer.ReactTestRenderer;
  await ReactTestRenderer.act(() => {
    renderer = ReactTestRenderer.create(<TtsReader adapter={engine} text="Okunacak metin" />);
  });
  expect(engine.speak).not.toHaveBeenCalled();
  const play = renderer.root.findByProps({accessibilityLabel: 'Oynat'});
  await ReactTestRenderer.act(() => play.props.onPress());
  expect(engine.speak).toHaveBeenCalledWith('Okunacak metin', 0.5);
  await ReactTestRenderer.act(() =>
    renderer.root.findByProps({accessibilityLabel: 'Duraklat'}).props.onPress(),
  );
  expect(engine.pause).toHaveBeenCalled();
  await ReactTestRenderer.act(() =>
    renderer.root.findByProps({accessibilityLabel: 'Durdur'}).props.onPress(),
  );
  expect(engine.stop).toHaveBeenCalled();
  await ReactTestRenderer.act(() =>
    renderer.root.findByProps({accessibilityLabel: 'Hız 0.5'}).props.onPress(),
  );
  expect(renderer.root.findByProps({accessibilityLabel: 'Hız 0.6'})).toBeTruthy();
});

test('stops on navigation cleanup and leaves visible text when initialization fails', async () => {
  const engine = adapter({initialize: jest.fn().mockRejectedValue(new Error('unsupported'))});
  let renderer!: ReactTestRenderer.ReactTestRenderer;
  await ReactTestRenderer.act(() => {
    renderer = ReactTestRenderer.create(
      <><TtsReader adapter={engine} text="Metin" /><Text>Metin görünür kalır</Text></>,
    );
  });
  await ReactTestRenderer.act(() =>
    renderer.root.findByProps({accessibilityLabel: 'Oynat'}).props.onPress(),
  );
  expect(renderer.root.findByProps({accessibilityRole: 'alert'})).toBeTruthy();
  expect(JSON.stringify(renderer.toJSON())).toContain('Metin görünür kalır');
  await ReactTestRenderer.act(() => renderer.unmount());
  expect(engine.stop).toHaveBeenCalled();
});

test('stops playback when the app moves to the background', async () => {
  const engine = adapter();
  let lifecycleHandler: ((state: string) => void) | undefined;
  const appStateSpy = jest.spyOn(AppState, 'addEventListener').mockImplementation(
    (_event, handler) => {
      lifecycleHandler = handler as (state: string) => void;
      return {remove: jest.fn()};
    },
  );
  let renderer!: ReactTestRenderer.ReactTestRenderer;
  await ReactTestRenderer.act(() => {
    renderer = ReactTestRenderer.create(<TtsReader adapter={engine} text="Metin" />);
  });
  await ReactTestRenderer.act(() => lifecycleHandler?.('background'));
  expect(engine.stop).toHaveBeenCalled();
  await ReactTestRenderer.act(() => renderer.unmount());
  appStateSpy.mockRestore();
});
