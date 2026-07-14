import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import {useFocusEffect} from '@react-navigation/native';
import React, {useCallback, useState} from 'react';
import {Alert, Platform, Pressable, ScrollView, StyleSheet, Text} from 'react-native';

import {requestAnalysis} from '../api/analysisApi';
import {getJournalRepository} from '../features/journal/service';
import type {JournalEntry} from '../features/journal/types';
import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'JournalDetail'>;
const API_BASE_URL = Platform.OS === 'android' ? 'http://10.0.2.2:8000' : 'http://127.0.0.1:8000';

export function JournalDetailScreen({navigation, route}: Props): React.JSX.Element {
  const [entry, setEntry] = useState<JournalEntry | null>(null);
  const [analysisState, setAnalysisState] = useState<'idle' | 'loading' | 'error'>('idle');
  const load = useCallback(() => {
    getJournalRepository()
      .then(repository => repository.get(route.params.entryId))
      .then(setEntry, () => setEntry(null));
  }, [route.params.entryId]);
  useFocusEffect(load);
  if (!entry) return <Text accessibilityLabel="Günlük kaydı yükleniyor">Kayıt yükleniyor…</Text>;

  const analyzeExplicitly = async () => {
    if (entry.body.trim().length < 2 || entry.body.length > 1000) {
      setAnalysisState('error');
      return;
    }
    setAnalysisState('loading');
    try {
      const result = await requestAnalysis({query: entry.body, topK: 5}, {baseUrl: API_BASE_URL});
      setAnalysisState('idle');
      navigation.navigate('Result', {result});
    } catch {
      setAnalysisState('error');
    }
  };
  const confirmDelete = () => Alert.alert('Kaydı sil', 'Bu yerel kayıt kalıcı olarak silinecek.', [
    {style: 'cancel', text: 'Vazgeç'},
    {
      style: 'destructive',
      text: 'Sil',
      onPress: () => {
        getJournalRepository()
          .then(repository => repository.delete(entry.id))
          .then(() => navigation.goBack());
      },
    },
  ]);
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>{entry.title}</Text>
      <Text style={styles.meta}>Son güncelleme: {new Date(entry.updatedAt).toLocaleString()}</Text>
      <Text accessibilityLabel="Özel günlük metni" style={styles.body}>{entry.body}</Text>
      <Text style={styles.privacy}>Bu metin yalnızca “Bu kaydı analiz et” düğmesine bastığınızda gönderilir. Başarısız istek otomatik tekrarlanmaz.</Text>
      {analysisState === 'error' ? <Text accessibilityRole="alert">Analiz gönderilemedi veya metin API sınırlarını aşıyor.</Text> : null}
      <Pressable accessibilityRole="button" disabled={analysisState === 'loading'} onPress={analyzeExplicitly} style={styles.primary}><Text style={styles.primaryText}>{analysisState === 'loading' ? 'Gönderiliyor…' : 'Bu kaydı analiz et'}</Text></Pressable>
      <Pressable accessibilityRole="button" onPress={() => navigation.navigate('JournalEdit', {entryId: entry.id})} style={styles.secondary}><Text>Kaydı düzenle</Text></Pressable>
      <Pressable accessibilityRole="button" onPress={confirmDelete} style={styles.danger}><Text>Kaydı sil</Text></Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  body: {backgroundColor: '#FFFFFF', borderRadius: 10, color: '#273A36', fontSize: 18, lineHeight: 28, padding: 16},
  container: {backgroundColor: '#F7F4ED', gap: 14, padding: 20},
  danger: {alignItems: 'center', borderColor: '#8A2E2E', borderRadius: 10, borderWidth: 1, minHeight: 48, padding: 14},
  meta: {color: '#536761', fontSize: 14},
  primary: {alignItems: 'center', backgroundColor: '#1D5147', borderRadius: 10, minHeight: 48, padding: 14},
  primaryText: {color: '#FFFFFF', fontSize: 17, fontWeight: '700'},
  privacy: {color: '#40534E', fontSize: 15, lineHeight: 22},
  secondary: {alignItems: 'center', borderColor: '#1D5147', borderRadius: 10, borderWidth: 1, minHeight: 48, padding: 14},
  title: {color: '#173C35', fontSize: 26, fontWeight: '700'},
});
