import React from 'react';
import ReactTestRenderer from 'react-test-renderer';

import App from '../App';

jest.mock('react-native-nitro-sqlite', () => ({open: jest.fn()}));

test('renders the navigation shell', async () => {
  await ReactTestRenderer.act(() => {
    ReactTestRenderer.create(<App />);
  });
});
