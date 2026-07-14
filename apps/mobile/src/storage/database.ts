import {open} from 'react-native-nitro-sqlite';

export const DATABASE_NAME = 'denge_atlasi.db';

export type DatabaseConnection = {
  execute: (statement: string) => unknown | Promise<unknown>;
};

export type DatabaseFactory = (name: string) => DatabaseConnection;

const nativeDatabaseFactory: DatabaseFactory = name => open({name});

export async function initializeDatabase(
  factory: DatabaseFactory = nativeDatabaseFactory,
): Promise<DatabaseConnection> {
  const database = factory(DATABASE_NAME);
  await database.execute('PRAGMA user_version = 1');
  return database;
}
