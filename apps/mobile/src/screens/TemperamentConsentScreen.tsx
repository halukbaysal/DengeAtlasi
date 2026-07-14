import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import React, {useState} from 'react';
import {Pressable, StyleSheet, Switch, Text, View} from 'react-native';

import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'TemperamentConsent'>;

export function TemperamentConsentScreen({navigation}: Props): React.JSX.Element {
  const [education, setEducation] = useState(false);
  const [adult, setAdult] = useState(false);
  const [selfReport, setSelfReport] = useState(false);
  const eligible = education && adult && selfReport;
  return (
    <View style={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>Mizaç öz-düşünümü</Text>
      <Text style={styles.notice}>
        Bu akış tarihsel ve tematik bir öz-düşünüm aracıdır; kişilik testi, kesin sınıflandırma
        veya tıbbi değerlendirme değildir.
      </Text>
      <ConsentRow label="Eğitim ve güvenlik açıklamasını kabul ediyorum" value={education} onChange={setEducation} />
      <ConsentRow label="18 yaş veya üzerindeyim" value={adult} onChange={setAdult} />
      <ConsentRow label="Yalnızca kendim için yanıtlıyorum" value={selfReport} onChange={setSelfReport} />
      <Pressable
        accessibilityRole="button"
        disabled={!eligible}
        onPress={() => navigation.navigate('TemperamentInput')}
        style={[styles.button, !eligible && styles.disabled]}>
        <Text style={styles.buttonText}>Devam et</Text>
      </Pressable>
    </View>
  );
}

function ConsentRow({label, value, onChange}: {label: string; value: boolean; onChange: (value: boolean) => void}) {
  return (
    <View style={styles.row}>
      <Text style={styles.rowText}>{label}</Text>
      <Switch accessibilityLabel={label} onValueChange={onChange} value={value} />
    </View>
  );
}

const styles = StyleSheet.create({
  button: {alignItems: 'center', backgroundColor: '#1D5147', borderRadius: 10, minHeight: 48, padding: 14},
  buttonText: {color: '#FFFFFF', fontSize: 17, fontWeight: '700'},
  container: {backgroundColor: '#F7F4ED', flex: 1, gap: 16, padding: 24},
  disabled: {opacity: 0.45},
  notice: {color: '#273A36', fontSize: 17, lineHeight: 26},
  row: {alignItems: 'center', flexDirection: 'row', gap: 12, justifyContent: 'space-between', minHeight: 52},
  rowText: {color: '#273A36', flex: 1, fontSize: 16},
  title: {color: '#173C35', fontSize: 26, fontWeight: '700'},
});
