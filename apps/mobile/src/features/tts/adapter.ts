import Tts from 'react-native-tts';

export interface TtsAdapter {
  initialize(): Promise<void>;
  speak(text: string, rate: number): Promise<void>;
  pause(): Promise<boolean>;
  resume(): Promise<boolean>;
  stop(): Promise<void>;
}

export class NativeTtsAdapter implements TtsAdapter {
  async initialize(): Promise<void> {
    await Tts.getInitStatus();
    const voices = await Tts.voices();
    const localTurkishVoice = voices.find(
      voice =>
        voice.language.toLocaleLowerCase().startsWith('tr') &&
        !voice.networkConnectionRequired &&
        !voice.notInstalled,
    );
    if (voices.length && !localTurkishVoice) {
      throw new Error('Bu cihazda çevrimdışı Türkçe ses bulunamadı.');
    }
    await Tts.setDefaultLanguage('tr-TR');
    if (localTurkishVoice) await Tts.setDefaultVoice(localTurkishVoice.id);
  }

  async speak(text: string, rate: number): Promise<void> {
    await Tts.setDefaultRate(rate);
    Tts.speak(text);
  }

  async pause(): Promise<boolean> {
    try {
      return await Tts.pause();
    } catch {
      return false;
    }
  }

  async resume(): Promise<boolean> {
    try {
      return await Tts.resume();
    } catch {
      return false;
    }
  }

  async stop(): Promise<void> {
    await Tts.stop();
  }
}
