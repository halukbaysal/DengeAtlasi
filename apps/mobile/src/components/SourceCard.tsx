import type {components} from '@denge-atlasi/api-client';
import React from 'react';
import {StyleSheet, Text, View} from 'react-native';

import {CitationBadge} from './CitationBadge';

type Citation = components['schemas']['RetrievalResult'];
type Props = {citation: Citation; onOpen: (citation: Citation) => void};

export function SourceCard({citation, onOpen}: Props): React.JSX.Element {
  return (
    <View accessibilityLabel={`Kaynak: ${citation.workTitle}`} style={styles.card}>
      <Text accessibilityRole="header" style={styles.title}>
        {citation.workTitle}
      </Text>
      <Text style={styles.metadata}>{citation.author}</Text>
      <Text style={styles.metadata}>
        {citation.edition} · Sayfa {citation.pageNumber} · {citation.section}
      </Text>
      <Text numberOfLines={4} style={styles.excerpt}>
        {citation.excerpt}
      </Text>
      <CitationBadge label={`Sayfa ${citation.pageNumber}`} onPress={() => onOpen(citation)} />
    </View>
  );
}

const styles = StyleSheet.create({
  card: {backgroundColor: '#FFFFFF', borderRadius: 12, gap: 8, padding: 16},
  excerpt: {color: '#273A36', fontSize: 16, lineHeight: 24},
  metadata: {color: '#536761', fontSize: 14},
  title: {color: '#173C35', fontSize: 19, fontWeight: '700'},
});
