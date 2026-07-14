import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import React from 'react';
import {Pressable, ScrollView, StyleSheet, Text, View} from 'react-native';

import {MedicalSafetyNotice, SourceLimitNotice} from '../components/Notices';
import {SourceCard} from '../components/SourceCard';
import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'TemperamentResult'>;

export function TemperamentResultScreen({navigation, route}: Props): React.JSX.Element {
  const {result} = route.params;
  const primary = (result.citations ?? []).filter(item => item.category === 'PRIMARY');
  const supplementary = (result.citations ?? []).filter(item => item.category !== 'PRIMARY');
  const open = (citation: (typeof primary)[number]) => navigation.navigate('SourceDetail', {citation});
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>Olası mizaç temaları</Text>
      <Text accessibilityLabel="Eğitim amaçlı açıklama" style={styles.disclaimer}>{result.educationalDisclaimer}</Text>
      {result.sourceLimitNote ? <SourceLimitNotice text={result.sourceLimitNote} /> : null}
      {result.primarySourceFindings?.length ? <Section title="Marifetname — birincil bulgular" values={result.primarySourceFindings.map(item => item.text)} /> : null}
      {result.supplementaryFindings?.length ? (
        <>
          <Section title="Ibn Sina — ayrı ek kaynak" values={result.supplementaryFindings.map(item => item.text)} />
          {result.supplementReason ? <Text style={styles.reason}>{result.supplementReason}</Text> : null}
        </>
      ) : null}
      {result.symbolicThemes?.length ? <Section title="Sembolik düşünme temaları" values={result.symbolicThemes} /> : null}
      {result.safeWellbeingSuggestions?.length ? <Section title="Genel ve düşük riskli öneriler" values={result.safeWellbeingSuggestions} /> : null}
      {result.reflectionQuestions?.length ? <Section title="Düşünme soruları" values={result.reflectionQuestions} /> : null}
      {result.medicalSafetyNotice ? <MedicalSafetyNotice text={result.medicalSafetyNotice} /> : null}
      <Pressable
        accessibilityRole="button"
        onPress={() =>
          navigation.navigate('JournalEdit', {
            initialBody: [
              ...(result.primarySourceFindings?.map(item => item.text) ?? []),
              ...(result.reflectionQuestions ?? []),
            ].join('\n\n'),
            linkedAnalysisId: result.correlationId,
          })
        }
        style={styles.saveButton}>
        <Text style={styles.saveButtonText}>Temaları özel günlüğe kaydet</Text>
      </Pressable>
      {primary.length ? <Text accessibilityRole="header" style={styles.sectionTitle}>Marifetname kaynakları</Text> : null}
      {primary.map(item => <SourceCard citation={item} key={item.chunkId} onOpen={open} />)}
      {supplementary.length ? <Text accessibilityRole="header" style={styles.sectionTitle}>Ek kaynaklar</Text> : null}
      {supplementary.map(item => <SourceCard citation={item} key={item.chunkId} onOpen={open} />)}
    </ScrollView>
  );
}

function Section({title, values}: {title: string; values: string[]}) {
  return <View style={styles.section}><Text accessibilityRole="header" style={styles.sectionTitle}>{title}</Text>{values.map(value => <Text key={value} style={styles.body}>• {value}</Text>)}</View>;
}

const styles = StyleSheet.create({
  body: {color: '#273A36', fontSize: 17, lineHeight: 26},
  container: {backgroundColor: '#F7F4ED', gap: 16, padding: 20},
  disclaimer: {backgroundColor: '#EDF1F0', color: '#273A36', fontSize: 16, lineHeight: 24, padding: 14},
  reason: {color: '#40534E', fontSize: 15, fontStyle: 'italic'},
  saveButton: {alignItems: 'center', borderColor: '#1D5147', borderRadius: 10, borderWidth: 1, minHeight: 48, padding: 14},
  saveButtonText: {color: '#1D5147', fontSize: 16, fontWeight: '700'},
  section: {gap: 8},
  sectionTitle: {color: '#173C35', fontSize: 20, fontWeight: '700'},
  title: {color: '#173C35', fontSize: 27, fontWeight: '700'},
});
