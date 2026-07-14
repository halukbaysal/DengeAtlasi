import React from 'react';
import {Pressable, StyleSheet, Text} from 'react-native';

type Props = {label: string; onPress: () => void};

export function CitationBadge({label, onPress}: Props): React.JSX.Element {
  return (
    <Pressable
      accessibilityHint="Kaynak ayrıntılarını açar"
      accessibilityLabel={`Atıf: ${label}`}
      accessibilityRole="button"
      onPress={onPress}
      style={styles.badge}>
      <Text style={styles.text}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  badge: {backgroundColor: '#E3ECE8', borderRadius: 16, minHeight: 44, padding: 12},
  text: {color: '#173C35', fontSize: 16, fontWeight: '600'},
});
