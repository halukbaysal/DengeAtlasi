import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import React, {useEffect, useState} from 'react';
import {Pressable, StyleSheet, Text, TextInput, View} from 'react-native';

import {disabledAnalytics as analytics} from '../analytics/analytics';
import {getJournalRepository} from '../features/journal/service';
import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'JournalEdit'>;

export function JournalEditScreen({navigation, route}: Props): React.JSX.Element {
  const {entryId, initialBody = '', linkedAnalysisId = null} = route.params;
  const [title, setTitle] = useState('');
  const [body, setBody] = useState(initialBody);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    if (entryId) {
      getJournalRepository().then(repository => repository.get(entryId)).then(entry => {
        if (entry) { setTitle(entry.title); setBody(entry.body); }
      });
    }
  }, [entryId]);
  const save = async () => {
    if (!title.trim() || title.trim().length > 200 || body.length > 10000) {
      setError('Başlık zorunludur; başlık 200, metin 10000 karakteri aşamaz.');
      return;
    }
    const repository = await getJournalRepository();
    const entry = entryId
      ? await repository.update(entryId, {body, linkedAnalysisId, title})
      : await repository.create({body, linkedAnalysisId, title});
    if (entry) {
      analytics.track('reflection_saved');
      navigation.replace('JournalDetail', {entryId: entry.id});
    }
  };
  return (
    <View style={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>{entryId ? 'Kaydı düzenle' : 'Yeni günlük kaydı'}</Text>
      <TextInput accessibilityLabel="Günlük başlığı" maxLength={200} onChangeText={setTitle} placeholder="Başlık" style={styles.titleInput} value={title} />
      <TextInput accessibilityLabel="Günlük metni" maxLength={10000} multiline onChangeText={setBody} placeholder="Yalnızca cihazınızda saklanacak düşünceleriniz" style={styles.bodyInput} value={body} />
      {error ? <Text accessibilityRole="alert">{error}</Text> : null}
      <Pressable accessibilityRole="button" onPress={save} style={styles.button}><Text style={styles.buttonText}>Yerel olarak kaydet</Text></Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  bodyInput: {backgroundColor: '#FFFFFF', borderRadius: 10, flex: 1, fontSize: 17, padding: 14, textAlignVertical: 'top'},
  button: {alignItems: 'center', backgroundColor: '#1D5147', borderRadius: 10, minHeight: 48, padding: 14},
  buttonText: {color: '#FFFFFF', fontSize: 17, fontWeight: '700'},
  container: {backgroundColor: '#F7F4ED', flex: 1, gap: 14, padding: 20},
  title: {color: '#173C35', fontSize: 25, fontWeight: '700'},
  titleInput: {backgroundColor: '#FFFFFF', borderRadius: 10, fontSize: 18, padding: 14},
});
