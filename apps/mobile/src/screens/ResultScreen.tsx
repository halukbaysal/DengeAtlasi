import type {components} from '@denge-atlasi/api-client';
import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import React from 'react';
import {Pressable, ScrollView, StyleSheet, Text, View} from 'react-native';

import {disabledAnalytics as analytics} from '../analytics/analytics';
import {MedicalSafetyNotice, SourceLimitNotice} from '../components/Notices';
import {SourceCard} from '../components/SourceCard';
import {TtsReader} from '../components/TtsReader';
import type {RootStackParamList} from '../navigation/RootNavigator';

type Citation = components['schemas']['RetrievalResult'];
type Props = NativeStackScreenProps<RootStackParamList, 'Result'>;

export function ResultScreen({navigation, route}: Props): React.JSX.Element {
  const {result} = route.params;
  const citations = [...(result.citations ?? [])].sort((left, right) =>
    left.category === right.category ? 0 : left.category === 'PRIMARY' ? -1 : 1,
  );
  const openCitation = (citation: Citation) => {
    analytics.track('citation_opened', {
      screen: 'result',
      sourceRole: citation.category === 'PRIMARY' ? 'primary' : 'supplementary',
    });
    navigation.navigate('SourceDetail', {citation});
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>Kaynaklandırılmış sonuç</Text>
      <TtsReader
        text={[
          ...(result.sourcedClaims?.map(claim => claim.text) ?? []),
          result.generalSymbolicInterpretation ?? '',
          result.medicalNotice ?? '',
        ]
          .filter(Boolean)
          .join('\n\n')}
      />
      {result.message ? <Text accessibilityRole="alert" style={styles.body}>{result.message}</Text> : null}
      {result.sourcedClaims?.map((claim, index) => (
        <View key={`${index}-${claim.text}`} style={styles.claim}>
          <Text style={styles.body}>{claim.text}</Text>
        </View>
      ))}
      {result.generalSymbolicInterpretation ? (
        <View style={styles.symbolic}>
          <Text accessibilityRole="header" style={styles.sectionTitle}>Genel sembolik yorum</Text>
          <Text style={styles.body}>{result.generalSymbolicInterpretation}</Text>
        </View>
      ) : null}
      {result.sourceLimitNote ? <SourceLimitNotice text={result.sourceLimitNote} /> : null}
      {result.medicalNotice ? <MedicalSafetyNotice text={result.medicalNotice} /> : null}
      <Pressable
        accessibilityRole="button"
        onPress={() =>
          navigation.navigate('JournalEdit', {
            initialBody: [
              ...(result.sourcedClaims?.map(claim => claim.text) ?? []),
              result.generalSymbolicInterpretation ?? '',
            ]
              .filter(Boolean)
              .join('\n\n'),
            linkedAnalysisId: result.correlationId,
          })
        }
        style={styles.saveButton}>
        <Text style={styles.saveButtonText}>Düşünümü özel günlüğe kaydet</Text>
      </Pressable>
      {citations.length ? (
        <>
          <Text accessibilityRole="header" style={styles.sectionTitle}>Kaynaklar</Text>
          {citations.map(citation => (
            <SourceCard citation={citation} key={citation.chunkId} onOpen={openCitation} />
          ))}
        </>
      ) : (
        <Text accessibilityLabel="Boş sonuç">Gösterilecek onaylı kaynak bulunamadı.</Text>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  body: {color: '#273A36', fontSize: 17, lineHeight: 26},
  claim: {backgroundColor: '#FFFFFF', borderRadius: 10, padding: 16},
  container: {backgroundColor: '#F7F4ED', gap: 16, padding: 20},
  sectionTitle: {color: '#173C35', fontSize: 21, fontWeight: '700'},
  saveButton: {alignItems: 'center', borderColor: '#1D5147', borderRadius: 10, borderWidth: 1, minHeight: 48, padding: 14},
  saveButtonText: {color: '#1D5147', fontSize: 16, fontWeight: '700'},
  symbolic: {borderLeftColor: '#718B84', borderLeftWidth: 4, gap: 8, padding: 14},
  title: {color: '#173C35', fontSize: 27, fontWeight: '700'},
});
