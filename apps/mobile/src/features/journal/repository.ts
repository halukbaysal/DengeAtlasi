import type {DatabaseConnection} from '../../storage/database';
import type {JournalDraft, JournalEntry} from './types';

type JournalRow = Record<string, unknown> & {
  id: string;
  created_at: string;
  updated_at: string;
  title: string;
  body: string;
  linked_analysis_id: string | null;
  tags_json: string;
  is_exported: number;
};

export class JournalRepository {
  constructor(
    private readonly database: DatabaseConnection,
    private readonly now: () => string = () => new Date().toISOString(),
    private readonly createId: () => string = () => createLocalId(),
  ) {}

  async create(draft: JournalDraft): Promise<JournalEntry> {
    validateDraft(draft);
    const timestamp = this.now();
    const entry: JournalEntry = {
      id: this.createId(),
      createdAt: timestamp,
      updatedAt: timestamp,
      title: draft.title.trim(),
      body: draft.body,
      linkedAnalysisId: draft.linkedAnalysisId ?? null,
      tags: sanitizeTags(draft.tags ?? []),
      isExported: false,
    };
    await this.database.execute(
      `INSERT INTO journal_entries
       (id, created_at, updated_at, title, body, linked_analysis_id, tags_json, is_exported)
       VALUES (?, ?, ?, ?, ?, ?, ?, 0)`,
      [
        entry.id,
        entry.createdAt,
        entry.updatedAt,
        entry.title,
        entry.body,
        entry.linkedAnalysisId,
        JSON.stringify(entry.tags),
      ],
    );
    return entry;
  }

  async list(): Promise<JournalEntry[]> {
    const result = await this.database.execute(
      'SELECT * FROM journal_entries ORDER BY updated_at DESC',
    );
    return (result.results ?? []).map(row => mapRow(row as JournalRow));
  }

  async get(id: string): Promise<JournalEntry | null> {
    const result = await this.database.execute(
      'SELECT * FROM journal_entries WHERE id = ? LIMIT 1',
      [id],
    );
    const row = result.results?.[0];
    return row ? mapRow(row as JournalRow) : null;
  }

  async update(id: string, draft: JournalDraft): Promise<JournalEntry | null> {
    validateDraft(draft);
    const existing = await this.get(id);
    if (!existing) return null;
    const entry: JournalEntry = {
      ...existing,
      updatedAt: this.now(),
      title: draft.title.trim(),
      body: draft.body,
      linkedAnalysisId: draft.linkedAnalysisId ?? existing.linkedAnalysisId,
      tags: sanitizeTags(draft.tags ?? existing.tags),
      isExported: false,
    };
    await this.database.execute(
      `UPDATE journal_entries SET updated_at = ?, title = ?, body = ?,
       linked_analysis_id = ?, tags_json = ?, is_exported = 0 WHERE id = ?`,
      [
        entry.updatedAt,
        entry.title,
        entry.body,
        entry.linkedAnalysisId,
        JSON.stringify(entry.tags),
        id,
      ],
    );
    return entry;
  }

  async delete(id: string): Promise<void> {
    await this.database.execute('DELETE FROM journal_entries WHERE id = ?', [id]);
  }

  async deleteAll(): Promise<void> {
    await this.database.execute('DELETE FROM journal_entries');
  }

  async exportAll(): Promise<string> {
    const entries = await this.list();
    const content = entries
      .map(
        entry =>
          `# ${entry.title}\nCreated: ${entry.createdAt}\nUpdated: ${entry.updatedAt}\n\n${entry.body}`,
      )
      .join('\n\n---\n\n');
    if (entries.length) {
      await this.database.execute('UPDATE journal_entries SET is_exported = 1');
    }
    return content;
  }
}

function validateDraft(draft: JournalDraft): void {
  const titleLength = draft.title.trim().length;
  if (titleLength < 1 || titleLength > 200) throw new Error('Invalid journal title.');
  if (draft.body.length > 10000) throw new Error('Journal body is too long.');
}

function sanitizeTags(tags: string[]): string[] {
  return [...new Set(tags.map(tag => tag.trim()).filter(Boolean))].slice(0, 10);
}

function mapRow(row: JournalRow): JournalEntry {
  let tags: string[] = [];
  try {
    const parsed: unknown = JSON.parse(row.tags_json);
    if (Array.isArray(parsed)) tags = parsed.filter(item => typeof item === 'string');
  } catch {
    tags = [];
  }
  return {
    id: row.id,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    title: row.title,
    body: row.body,
    linkedAnalysisId: row.linked_analysis_id,
    tags,
    isExported: row.is_exported === 1,
  };
}

function createLocalId(): string {
  return `journal-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}
