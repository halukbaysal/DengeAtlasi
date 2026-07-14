import React from 'react';
import {StyleSheet, Text, View} from 'react-native';

export function SourceLimitNotice({text}: {text: string}): React.JSX.Element {
  return (
    <View accessibilityLabel="Kaynak sınırlaması" style={styles.source}>
      <Text style={styles.title}>Kaynak sınırı</Text>
      <Text style={styles.text}>{text}</Text>
    </View>
  );
}

export function MedicalSafetyNotice({text}: {text: string}): React.JSX.Element {
  return (
    <View accessibilityLabel="Tıbbi güvenlik uyarısı" accessibilityRole="summary" style={styles.medical}>
      <Text style={styles.title}>Sağlık uyarısı</Text>
      <Text style={styles.text}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  medical: {backgroundColor: '#FFF3D6', borderRadius: 10, gap: 6, padding: 16},
  source: {backgroundColor: '#EDF1F0', borderRadius: 10, gap: 6, padding: 16},
  text: {color: '#273A36', fontSize: 16, lineHeight: 24},
  title: {color: '#173C35', fontSize: 17, fontWeight: '700'},
});
