import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import type {components} from '@denge-atlasi/api-client';

import type {AnalysisResponse} from '../validation/analysisResponse';
import {AskScreen} from '../screens/AskScreen';
import {HomeScreen} from '../screens/HomeScreen';
import {ResultScreen} from '../screens/ResultScreen';
import {SourceDetailScreen} from '../screens/SourceDetailScreen';

export type RootStackParamList = {
  Home: undefined;
  Ask: undefined;
  Result: {result: AnalysisResponse};
  SourceDetail: {citation: components['schemas']['RetrievalResult']};
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
