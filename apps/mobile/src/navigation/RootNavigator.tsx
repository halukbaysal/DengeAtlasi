import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import type {components} from '@denge-atlasi/api-client';

import type {AnalysisResponse} from '../validation/analysisResponse';
import type {TemperamentResponse} from '../validation/temperamentResponse';
import {AskScreen} from '../screens/AskScreen';
import {HomeScreen} from '../screens/HomeScreen';
import {ResultScreen} from '../screens/ResultScreen';
import {SourceDetailScreen} from '../screens/SourceDetailScreen';
import {TemperamentConsentScreen} from '../screens/TemperamentConsentScreen';
import {TemperamentInputScreen} from '../screens/TemperamentInputScreen';
import {TemperamentResultScreen} from '../screens/TemperamentResultScreen';

export type RootStackParamList = {
  Home: undefined;
  Ask: undefined;
  Result: {result: AnalysisResponse};
  SourceDetail: {citation: components['schemas']['RetrievalResult']};
  TemperamentConsent: undefined;
  TemperamentInput: undefined;
  TemperamentResult: {result: TemperamentResponse};
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export function RootNavigator(): React.JSX.Element {
  return (
    <Stack.Navigator>
      <Stack.Screen
        component={HomeScreen}
        name="Home"
        options={{title: 'Denge Atlası'}}
      />
      <Stack.Screen
        component={TemperamentConsentScreen}
        name="TemperamentConsent"
        options={{title: 'Açıklama ve Onay'}}
      />
      <Stack.Screen
        component={TemperamentInputScreen}
        name="TemperamentInput"
        options={{title: 'Mizaç Öz-Düşünümü'}}
      />
      <Stack.Screen
        component={TemperamentResultScreen}
        name="TemperamentResult"
        options={{title: 'Temalar'}}
      />
      <Stack.Screen component={AskScreen} name="Ask" options={{title: 'Kaynaklara Sor'}} />
      <Stack.Screen component={ResultScreen} name="Result" options={{title: 'Sonuç'}} />
      <Stack.Screen
        component={SourceDetailScreen}
        name="SourceDetail"
        options={{title: 'Kaynak Ayrıntısı'}}
      />
    </Stack.Navigator>
  );
}
