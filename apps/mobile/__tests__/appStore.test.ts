import {useAppStore} from '../src/state/appStore';

beforeEach(() => useAppStore.setState({isReady: false}));

test('marks the application as ready', () => {
  useAppStore.getState().markReady();
  expect(useAppStore.getState().isReady).toBe(true);
});
