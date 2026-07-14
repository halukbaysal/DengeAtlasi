import {initializeDatabase} from '../../storage/database';
import {JournalRepository} from './repository';

let repositoryPromise: Promise<JournalRepository> | undefined;

export function getJournalRepository(): Promise<JournalRepository> {
  repositoryPromise ??= initializeDatabase().then(database => new JournalRepository(database));
  return repositoryPromise;
}
