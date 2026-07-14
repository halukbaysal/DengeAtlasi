import React from 'react';
import type {NativeStackScreenProps} from '@react-navigation/native-stack';
import {Pressable, StyleSheet, Text, View} from 'react-native';

import type {RootStackParamList} from '../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

export function HomeScreen({navigation}: Props): React.JSX.Element {
  return (
    <View style={styles.container}>
      <Text accessibilityRole="header" style={styles.title}>
        Denge Atlası
      </Text>
      <Text style={styles.subtitle}>
        Onaylı tarihsel kaynaklarda düşünme ve denge temalarını keşfedin.
      </Text>
      <Pressable
        accessibilityHint="Soru formunu açar"
        accessibilityLabel="Kaynaklara soru sor"
        accessibilityRole="button"
        onPress={() => navigation.navigate('Ask')}
        style={styles.button}>
        <Text style={styles.buttonText}>Kaynaklara Sor</Text>
      </Pressable>
      <Pressable
        accessibilityHint="Eğitim ve onay ekranını açar"
        accessibilityLabel="Mizaç öz-düşünümünü başlat"
        accessibilityRole="button"
        onPress={() => navigation.navigate('TemperamentConsent')}
        style={styles.secondaryButton}>
        <Text style={styles.secondaryButtonText}>Mizaç Temalarını İncele</Text>
      </Pressable>
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
  button: {
    backgroundColor: '#1D5147',
    borderRadius: 10,
    marginTop: 24,
    minHeight: 48,
    padding: 14,
  },
  buttonText: {color: '#FFFFFF', fontSize: 17, fontWeight: '700'},
  title: {
    color: '#1D3B35',
    fontSize: 28,
    fontWeight: '700',
  },
  subtitle: {
    color: '#40534E',
    fontSize: 16,
    marginTop: 8,
    textAlign: 'center',
  },
  secondaryButton: {
    borderColor: '#1D5147',
    borderRadius: 10,
    borderWidth: 1,
    marginTop: 12,
    minHeight: 48,
    padding: 14,
  },
  secondaryButtonText: {color: '#1D5147', fontSize: 17, fontWeight: '700'},
});
