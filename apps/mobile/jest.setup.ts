jest.mock('react-native-tts', () => ({
  __esModule: true,
  default: {
    getInitStatus: jest.fn().mockResolvedValue('success'),
    pause: jest.fn().mockResolvedValue(true),
    resume: jest.fn().mockResolvedValue(true),
    setDefaultLanguage: jest.fn().mockResolvedValue('success'),
    setDefaultRate: jest.fn().mockResolvedValue('success'),
    setDefaultVoice: jest.fn().mockResolvedValue('success'),
    speak: jest.fn(),
    stop: jest.fn().mockResolvedValue(true),
    voices: jest.fn().mockResolvedValue([]),
  },
}));
