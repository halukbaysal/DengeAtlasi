import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import React from 'react';
import {ScrollView, StyleSheet, Text} from 'react-native';

import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'SourceDetail'>;

export function SourceDetailScreen({route}: Props): React.JSX.Element {
  const {citation} = route.params;
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>{citation.workTitle}</Text>
      <Text style={styles.metadata}>Yazar: {citation.author}</Text>
      <Text style={styles.metadata}>Baskı: {citation.edition}</Text>
      <Text style={styles.metadata}>Sayfa: {citation.pageNumber}</Text>
      <Text style={styles.metadata}>Bölüm: {citation.section}</Text>
      <Text accessibilityLabel="Kaynak alıntısı" style={styles.excerpt}>{citation.excerpt}</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {backgroundColor: '#F7F4ED', gap: 12, padding: 24},
  excerpt: {color: '#273A36', fontSize: 18, lineHeight: 28, marginTop: 12},
  metadata: {color: '#465D57', fontSize: 16},
  title: {color: '#173C35', fontSize: 26, fontWeight: '700'},
});
