import React, {useEffect, useRef, useState} from 'react';
import {AppState, Pressable, StyleSheet, Text, View} from 'react-native';

import {disabledAnalytics as analytics} from '../analytics/analytics';
import {NativeTtsAdapter, TtsAdapter} from '../features/tts/adapter';

type Props = {text: string; adapter?: TtsAdapter};
const RATES = [0.4, 0.5, 0.6] as const;

export function TtsReader({text, adapter}: Props): React.JSX.Element {
  const engine = useRef(adapter ?? new NativeTtsAdapter()).current;
  const [state, setState] = useState<'idle' | 'playing' | 'paused' | 'error'>('idle');
  const [rateIndex, setRateIndex] = useState(1);
  const rate = RATES[rateIndex];

  useEffect(() => {
    const subscription = AppState.addEventListener('change', nextState => {
      if (nextState !== 'active') {
        engine.stop().catch(() => undefined);
        setState('idle');
      }
    });
    return () => {
      subscription.remove();
      engine.stop().catch(() => undefined);
    };
  }, [engine]);

  const play = async () => {
    try {
      if (state === 'paused' && (await engine.resume())) {
        setState('playing');
        return;
      }
      await engine.initialize();
      await engine.speak(text, rate);
      analytics.track('tts_started');
      setState('playing');
    } catch {
      setState('error');
    }
  };
  const pause = async () => {
    if (await engine.pause()) setState('paused');
    else {
      await engine.stop();
      setState('idle');
    }
  };
  const stop = async () => {
    await engine.stop();
    setState('idle');
  };
  const cycleRate = () => setRateIndex(index => (index + 1) % RATES.length);

  return (
    <View accessibilityLabel="Cihaz içi sesli okuma" style={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>Sesli okuma</Text>
      <Text style={styles.note}>Ses cihazınızda üretilir; metin veya ses yüklenmez.</Text>
      {state === 'error' ? <Text accessibilityRole="alert">Sesli okuma kullanılamıyor. Metin aşağıda görünür kalır.</Text> : null}
      <View style={styles.controls}>
        <Control label={state === 'paused' ? 'Devam et' : 'Oynat'} onPress={play} />
        <Control label="Duraklat" onPress={pause} />
        <Control label="Durdur" onPress={stop} />
        <Control label={`Hız ${rate.toFixed(1)}`} onPress={cycleRate} />
      </View>
    </View>
  );
}

function Control({label, onPress}: {label: string; onPress: () => void | Promise<void>}) {
  return (
    <Pressable accessibilityLabel={label} accessibilityRole="button" onPress={onPress} style={styles.button}>
      <Text style={styles.buttonText}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {alignItems: 'center', borderColor: '#1D5147', borderRadius: 8, borderWidth: 1, minHeight: 44, padding: 11},
  buttonText: {color: '#1D5147', fontSize: 15, fontWeight: '700'},
  container: {backgroundColor: '#EDF1F0', borderRadius: 10, gap: 10, padding: 14},
  controls: {flexDirection: 'row', flexWrap: 'wrap', gap: 8},
  note: {color: '#40534E', fontSize: 14, lineHeight: 20},
  title: {color: '#173C35', fontSize: 18, fontWeight: '700'},
});
