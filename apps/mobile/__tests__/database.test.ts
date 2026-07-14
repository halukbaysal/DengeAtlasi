import {
  DATABASE_NAME,
  DATABASE_VERSION,
  initializeDatabase,
} from '../src/storage/database';

jest.mock('react-native-nitro-sqlite', () => ({open: jest.fn()}));

test('migrates a fresh database to the journal schema', async () => {
  const execute = jest
    .fn()
    .mockResolvedValueOnce({results: [{user_version: 1}]})
    .mockResolvedValue({results: []});
  const factory = jest.fn(() => ({execute}));

  const connection = await initializeDatabase(factory);

  expect(factory).toHaveBeenCalledWith(DATABASE_NAME);
  expect(execute).toHaveBeenNthCalledWith(1, 'PRAGMA user_version');
  expect(execute.mock.calls.some(([sql]) => sql.includes('CREATE TABLE IF NOT EXISTS journal_entries'))).toBe(true);
  expect(execute).toHaveBeenLastCalledWith(
    `PRAGMA user_version = ${DATABASE_VERSION}`,
  );
  expect(connection).toEqual({execute});
});

test('does not rerun migrations after restart at the current version', async () => {
  const execute = jest.fn().mockResolvedValue({results: [{user_version: DATABASE_VERSION}]});
  await initializeDatabase(() => ({execute}));
  expect(execute).toHaveBeenCalledTimes(1);
  expect(execute).toHaveBeenCalledWith('PRAGMA user_version');
});
