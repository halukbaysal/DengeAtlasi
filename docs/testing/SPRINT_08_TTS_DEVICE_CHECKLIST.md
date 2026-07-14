# Sprint 08 Native TTS Device Checklist

Run on one current iOS device/simulator and one supported Android device/emulator.

- Open a grounded result and confirm no speech starts automatically.
- Activate **Oynat** and confirm visible Turkish text is read on device.
- Activate **Duraklat**. If native pause is unavailable, confirm playback stops safely.
- Activate **Devam et** where pause is supported, then activate **Durdur**.
- Cycle speech rate through 0.4, 0.5, and 0.6 and confirm the audible change.
- Navigate away during playback and confirm speech stops.
- Background the app during playback and confirm speech stops.
- Remove/disable the Turkish voice and confirm an error appears while text stays visible.
- Navigate all controls with VoiceOver/TalkBack and verify their labels and touch targets.
- Inspect network traffic and confirm TTS creates no HTTP request or audio upload.
- Confirm no audio file is created and no background playback continues.
