import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import React, {useState} from 'react';
import {
  ActivityIndicator,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import {disabledAnalytics as analytics} from '../analytics/analytics';
import {requestAnalysis, OfflineAnalysisError} from '../api/analysisApi';
import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'Ask'>;
const API_BASE_URL = Platform.OS === 'android' ? 'http://10.0.2.2:8000' : 'http://127.0.0.1:8000';

export function validateQuestion(value: string): string | null {
  const length = value.trim().length;
  if (length < 2) return 'Lütfen en az iki karakter girin.';
  if (length > 1000) return 'Soru 1000 karakterden kısa olmalıdır.';
  return null;
}

export function AskScreen({navigation}: Props): React.JSX.Element {
  const [query, setQuery] = useState('');
  const [state, setState] = useState<'idle' | 'loading' | 'offline' | 'error'>('idle');
  const [validation, setValidation] = useState<string | null>(null);

  const submit = async () => {
    const issue = validateQuestion(query);
    setValidation(issue);
    if (issue) return;
    setState('loading');
    analytics.track('analysis_started', {screen: 'ask'});
    try {
      const result = await requestAnalysis(
        {query: query.trim(), topK: 5},
        {baseUrl: API_BASE_URL},
      );
      setState('idle');
      analytics.track('analysis_completed', {
        outcome: result.status === 'ANSWER' ? 'answer' : 'source_limited',
        screen: 'result',
      });
      navigation.navigate('Result', {result});
    } catch (error) {
      if (error instanceof OfflineAnalysisError) {
        setState('offline');
        analytics.track('offline_state_seen', {screen: 'ask'});
      } else {
        setState('error');
        analytics.track('analysis_failed', {outcome: 'error', screen: 'ask'});
      }
    }
  };

  return (
    <View style={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>Kaynaklara sor</Text>
      <TextInput
        accessibilityLabel="Sorunuz"
        multiline
        onChangeText={setQuery}
        placeholder="Tarihsel kaynaklarda bir tema sorun"
        style={styles.input}
        value={query}
      />
      {validation ? <Text accessibilityRole="alert" style={styles.error}>{validation}</Text> : null}
      {state === 'loading' ? <ActivityIndicator accessibilityLabel="Analiz yükleniyor" /> : null}
      {state === 'offline' ? <Text accessibilityRole="alert">Çevrimdışısınız. Yeni analiz için bağlantı gerekir.</Text> : null}
      {state === 'error' ? <Text accessibilityRole="alert">Analiz tamamlanamadı. Lütfen yeniden deneyin.</Text> : null}
      <Pressable accessibilityRole="button" disabled={state === 'loading'} onPress={submit} style={styles.button}>
        <Text style={styles.buttonText}>Soruyu gönder</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  button: {alignItems: 'center', backgroundColor: '#1D5147', borderRadius: 10, minHeight: 48, padding: 14},
  buttonText: {color: '#FFFFFF', fontSize: 17, fontWeight: '700'},
  container: {backgroundColor: '#F7F4ED', flex: 1, gap: 16, padding: 24},
  error: {color: '#8A2E2E', fontSize: 15},
  input: {backgroundColor: '#FFFFFF', borderColor: '#55736C', borderRadius: 10, borderWidth: 1, fontSize: 17, minHeight: 140, padding: 14, textAlignVertical: 'top'},
  title: {color: '#173C35', fontSize: 26, fontWeight: '700'},
});
