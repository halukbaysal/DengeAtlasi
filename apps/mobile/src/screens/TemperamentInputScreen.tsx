import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import React, {useState} from 'react';
import {ActivityIndicator, Platform, Pressable, StyleSheet, Switch, Text, TextInput, View} from 'react-native';

import {OfflineAnalysisError} from '../api/analysisApi';
import {requestTemperament} from '../api/temperamentApi';
import type {RootStackParamList} from '../navigation/RootNavigator';
import {validateQuestion} from './AskScreen';

type Props = NativeStackScreenProps<RootStackParamList, 'TemperamentInput'>;
const API_BASE_URL = Platform.OS === 'android' ? 'http://10.0.2.2:8000' : 'http://127.0.0.1:8000';

export function TemperamentInputScreen({navigation}: Props): React.JSX.Element {
  const [observations, setObservations] = useState('');
  const [lifestyle, setLifestyle] = useState(false);
  const [state, setState] = useState<'idle' | 'loading' | 'offline' | 'error'>('idle');
  const [validation, setValidation] = useState<string | null>(null);
  const submit = async () => {
    const issue = validateQuestion(observations);
    setValidation(issue);
    if (issue) return;
    setState('loading');
    try {
      const result = await requestTemperament(
        {
          observations: observations.trim(),
          consentAccepted: true,
          confirmsAdult: true,
          confirmsSelfReport: true,
          includeLifestyleContext: lifestyle,
        },
        {baseUrl: API_BASE_URL},
      );
      setState('idle');
      navigation.navigate('TemperamentResult', {result});
    } catch (error) {
      setState(error instanceof OfflineAnalysisError ? 'offline' : 'error');
    }
  };
  return (
    <View style={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>Gözlemlerinizi paylaşın</Text>
      <Text style={styles.help}>Kendinizde fark ettiğiniz günlük eğilimleri yargısız ve genel biçimde yazın.</Text>
      <TextInput accessibilityLabel="Kişisel gözlemler" multiline onChangeText={setObservations} style={styles.input} value={observations} />
      <View style={styles.row}>
        <Text style={styles.rowText}>Uyku, hareket ve yaşam tarzı bağlamını ayrıca incele</Text>
        <Switch accessibilityLabel="Yaşam tarzı ek kaynağı" onValueChange={setLifestyle} value={lifestyle} />
      </View>
      {validation ? <Text accessibilityRole="alert">{validation}</Text> : null}
      {state === 'loading' ? <ActivityIndicator accessibilityLabel="Mizaç temaları yükleniyor" /> : null}
      {state === 'offline' ? <Text accessibilityRole="alert">Çevrimdışısınız; yeni analiz için bağlantı gerekir.</Text> : null}
      {state === 'error' ? <Text accessibilityRole="alert">Öz-düşünüm tamamlanamadı.</Text> : null}
      <Pressable accessibilityRole="button" disabled={state === 'loading'} onPress={submit} style={styles.button}>
        <Text style={styles.buttonText}>Temaları incele</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  button: {alignItems: 'center', backgroundColor: '#1D5147', borderRadius: 10, minHeight: 48, padding: 14},
  buttonText: {color: '#FFFFFF', fontSize: 17, fontWeight: '700'},
  container: {backgroundColor: '#F7F4ED', flex: 1, gap: 14, padding: 24},
  help: {color: '#40534E', fontSize: 16, lineHeight: 24},
  input: {backgroundColor: '#FFFFFF', borderColor: '#55736C', borderRadius: 10, borderWidth: 1, fontSize: 17, minHeight: 130, padding: 14, textAlignVertical: 'top'},
  row: {alignItems: 'center', flexDirection: 'row', gap: 12, minHeight: 52},
  rowText: {color: '#273A36', flex: 1, fontSize: 16},
  title: {color: '#173C35', fontSize: 25, fontWeight: '700'},
});
