import Tts from 'react-native-tts';

import {NativeTtsAdapter} from '../src/features/tts/adapter';

const mockedTts = Tts as jest.Mocked<typeof Tts>;

beforeEach(() => jest.clearAllMocks());

test('initializes a local Turkish voice and controls playback without network', async () => {
  mockedTts.voices.mockResolvedValueOnce([
    {
      id: 'tr-local',
      language: 'tr-TR',
      name: 'Turkish',
      quality: 300,
      latency: 100,
      networkConnectionRequired: false,
      notInstalled: false,
    },
  ]);
  const fetchSpy = jest.spyOn(globalThis, 'fetch');
  const adapter = new NativeTtsAdapter();
  await adapter.initialize();
  await adapter.speak('Görünür yerel metin', 0.5);
  await adapter.pause();
  await adapter.resume();
  await adapter.stop();
  expect(mockedTts.setDefaultLanguage).toHaveBeenCalledWith('tr-TR');
  expect(mockedTts.setDefaultVoice).toHaveBeenCalledWith('tr-local');
  expect(mockedTts.setDefaultRate).toHaveBeenCalledWith(0.5);
  expect(mockedTts.speak).toHaveBeenCalledWith('Görünür yerel metin');
  expect(fetchSpy).not.toHaveBeenCalled();
  fetchSpy.mockRestore();
});

test('rejects network-only or missing Turkish voice availability', async () => {
  mockedTts.voices.mockResolvedValueOnce([
    {
      id: 'tr-cloud',
      language: 'tr-TR',
      name: 'Cloud Turkish',
      quality: 300,
      latency: 100,
      networkConnectionRequired: true,
      notInstalled: false,
    },
  ]);
  await expect(new NativeTtsAdapter().initialize()).rejects.toThrow(
    'çevrimdışı Türkçe ses',
  );
});

test('reports unsupported pause and resume without throwing', async () => {
  mockedTts.pause.mockRejectedValueOnce(new Error('unsupported'));
  mockedTts.resume.mockRejectedValueOnce(new Error('unsupported'));
  const adapter = new NativeTtsAdapter();
  await expect(adapter.pause()).resolves.toBe(false);
  await expect(adapter.resume()).resolves.toBe(false);
});
