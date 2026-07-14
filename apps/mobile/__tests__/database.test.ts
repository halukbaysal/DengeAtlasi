import {DATABASE_NAME, initializeDatabase} from '../src/storage/database';

jest.mock('react-native-nitro-sqlite', () => ({open: jest.fn()}));

test('initializes only the SQLite schema version', async () => {
  const execute = jest.fn();
  const factory = jest.fn(() => ({execute}));

  const connection = await initializeDatabase(factory);

  expect(factory).toHaveBeenCalledWith(DATABASE_NAME);
  expect(execute).toHaveBeenCalledWith('PRAGMA user_version = 1');
  expect(connection).toEqual({execute});
});
