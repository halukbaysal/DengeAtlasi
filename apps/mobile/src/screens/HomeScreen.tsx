import React from 'react';
import {StyleSheet, Text, View} from 'react-native';

export function HomeScreen(): React.JSX.Element {
  return (
    <View style={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>
        Denge Atlası
      </Text>
      <Text style={styles.subtitle}>Mühendislik temeli hazır.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    backgroundColor: '#F7F4ED',
    flex: 1,
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    color: '#1D3B35',
    fontSize: 28,
    fontWeight: '700',
  },
  subtitle: {
    color: '#40534E',
    fontSize: 16,
    marginTop: 8,
  },
});
