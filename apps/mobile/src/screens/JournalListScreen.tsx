import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import {useFocusEffect} from '@react-navigation/native';
import React, {useCallback, useState} from 'react';
import {Alert, Pressable, ScrollView, Share, StyleSheet, Text, View} from 'react-native';

import {getJournalRepository} from '../features/journal/service';
import type {JournalEntry} from '../features/journal/types';
import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'JournalList'>;

export function JournalListScreen({navigation}: Props): React.JSX.Element {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const load = useCallback(() => {
    getJournalRepository().then(repository => repository.list()).then(setEntries, () => setEntries([]));
  }, []);
  useFocusEffect(load);

  const exportEntries = async () => {
    const content = await (await getJournalRepository()).exportAll();
    await Share.share({message: content || 'Henüz dışa aktarılacak günlük kaydı yok.'});
    load();
  };
  const confirmDeleteAll = () => {
    Alert.alert('Tüm yerel veriyi sil', 'Bu işlem tüm günlük kayıtlarını kalıcı olarak siler.', [
      {style: 'cancel', text: 'Vazgeç'},
      {
        style: 'destructive',
        text: 'Tümünü sil',
        onPress: () => {
          getJournalRepository().then(repository => repository.deleteAll()).then(load);
        },
      },
    ]);
  };
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>Özel günlük</Text>
      <Text style={styles.privacy}>Kayıtlarınız bu cihazdaki SQLite veritabanında kalır. Hesap, bulut eşitleme veya otomatik analiz yoktur.</Text>
      <Pressable accessibilityRole="button" onPress={() => navigation.navigate('JournalEdit', {})} style={styles.primary}><Text style={styles.primaryText}>Yeni kayıt</Text></Pressable>
      {entries.length ? entries.map(entry => (
        <Pressable accessibilityLabel={`Günlük kaydı: ${entry.title}`} accessibilityRole="button" key={entry.id} onPress={() => navigation.navigate('JournalDetail', {entryId: entry.id})} style={styles.card}>
          <Text style={styles.cardTitle}>{entry.title}</Text>
          <Text style={styles.meta}>{new Date(entry.updatedAt).toLocaleDateString()}</Text>
        </Pressable>
      )) : <Text accessibilityLabel="Boş günlük">Henüz günlük kaydı yok.</Text>}
      <View style={styles.actions}>
        <Pressable accessibilityRole="button" onPress={exportEntries} style={styles.secondary}><Text>Dışa aktar</Text></Pressable>
        <Pressable accessibilityRole="button" onPress={confirmDeleteAll} style={styles.danger}><Text>Tüm yerel veriyi sil</Text></Pressable>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  actions: {gap: 12, marginTop: 12},
  card: {backgroundColor: '#FFFFFF', borderRadius: 10, gap: 6, minHeight: 60, padding: 16},
  cardTitle: {color: '#173C35', fontSize: 18, fontWeight: '700'},
  container: {backgroundColor: '#F7F4ED', gap: 14, padding: 20},
  danger: {alignItems: 'center', borderColor: '#8A2E2E', borderRadius: 10, borderWidth: 1, minHeight: 48, padding: 14},
  meta: {color: '#536761', fontSize: 14},
  primary: {alignItems: 'center', backgroundColor: '#1D5147', borderRadius: 10, minHeight: 48, padding: 14},
  primaryText: {color: '#FFFFFF', fontSize: 17, fontWeight: '700'},
  privacy: {color: '#40534E', fontSize: 16, lineHeight: 24},
  secondary: {alignItems: 'center', borderColor: '#1D5147', borderRadius: 10, borderWidth: 1, minHeight: 48, padding: 14},
  title: {color: '#173C35', fontSize: 27, fontWeight: '700'},
});
