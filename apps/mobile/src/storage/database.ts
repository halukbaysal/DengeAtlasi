import {open} from 'react-native-nitro-sqlite';

export const DATABASE_NAME = 'denge_atlasi.db';
export const DATABASE_VERSION = 2;

type DatabaseResult = {
  results?: Array<Record<string, unknown>>;
};

export type DatabaseConnection = {
  execute: (
    statement: string,
    params?: Array<boolean | number | string | ArrayBuffer | null>,
  ) => DatabaseResult | Promise<DatabaseResult>;
};

export type DatabaseFactory = (name: string) => DatabaseConnection;

const nativeDatabaseFactory: DatabaseFactory = name => open({name});

export async function initializeDatabase(
  factory: DatabaseFactory = nativeDatabaseFactory,
): Promise<DatabaseConnection> {
  const database = factory(DATABASE_NAME);
  const versionResult = await database.execute('PRAGMA user_version');
  const currentVersion = Number(versionResult.results?.[0]?.user_version ?? 0);
  if (currentVersion < 2) {
    await database.execute(`
      CREATE TABLE IF NOT EXISTS journal_entries (
        id TEXT PRIMARY KEY NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
        body TEXT NOT NULL CHECK(length(body) <= 10000),
        linked_analysis_id TEXT,
        tags_json TEXT NOT NULL DEFAULT '[]',
        is_exported INTEGER NOT NULL DEFAULT 0 CHECK(is_exported IN (0, 1))
      )
    `);
    await database.execute(
      'CREATE INDEX IF NOT EXISTS idx_journal_entries_updated_at ON journal_entries(updated_at DESC)',
    );
    await database.execute(`PRAGMA user_version = ${DATABASE_VERSION}`);
  }
  return database;
}
