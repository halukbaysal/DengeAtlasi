import {JournalRepository} from '../src/features/journal/repository';

const row = {
  id: 'entry-1',
  created_at: '2026-07-13T10:00:00.000Z',
  updated_at: '2026-07-13T10:00:00.000Z',
  title: 'Denge notu',
  body: 'Yalnızca yerel içerik',
  linked_analysis_id: null,
  tags_json: '["denge"]',
  is_exported: 0,
};

test('creates a local journal entry with parameterized SQL', async () => {
  const execute = jest.fn().mockResolvedValue({results: []});
  const repository = new JournalRepository(
    {execute},
    () => row.created_at,
    () => row.id,
  );
  const entry = await repository.create({title: ' Denge notu ', body: row.body, tags: ['denge']});
  expect(entry.id).toBe(row.id);
  expect(entry.title).toBe('Denge notu');
  expect(execute).toHaveBeenCalledWith(expect.stringContaining('INSERT INTO journal_entries'), [
    row.id,
    row.created_at,
    row.created_at,
    row.title,
    row.body,
    null,
    '["denge"]',
  ]);
});

test('lists and restores entries after a repository restart', async () => {
  const execute = jest.fn().mockResolvedValue({results: [row]});
  const firstInstance = new JournalRepository({execute});
  const secondInstance = new JournalRepository({execute});
  expect((await firstInstance.list())[0].body).toBe(row.body);
  expect((await secondInstance.list())[0].id).toBe(row.id);
});

test('updates, deletes one, deletes all, and exports readable content', async () => {
  const execute = jest
    .fn()
    .mockResolvedValueOnce({results: [row]})
    .mockResolvedValueOnce({results: []})
    .mockResolvedValueOnce({results: []})
    .mockResolvedValueOnce({results: []})
    .mockResolvedValueOnce({results: [row]})
    .mockResolvedValueOnce({results: []});
  const repository = new JournalRepository({execute}, () => '2026-07-14T00:00:00.000Z');
  const updated = await repository.update(row.id, {title: 'Yeni başlık', body: 'Yeni metin'});
  expect(updated?.title).toBe('Yeni başlık');
  await repository.delete(row.id);
  await repository.deleteAll();
  const exported = await repository.exportAll();
  expect(exported).toContain('# Denge notu');
  expect(exported).toContain(row.body);
  expect(execute).toHaveBeenCalledWith('DELETE FROM journal_entries WHERE id = ?', [row.id]);
  expect(execute).toHaveBeenCalledWith('DELETE FROM journal_entries');
  expect(execute).toHaveBeenLastCalledWith('UPDATE journal_entries SET is_exported = 1');
});

test('rejects oversized content before SQLite and does not log content', async () => {
  const execute = jest.fn().mockResolvedValue({results: []});
  const repository = new JournalRepository({execute});
  await expect(repository.create({title: 'x', body: 'x'.repeat(10001)})).rejects.toThrow();
  expect(execute).not.toHaveBeenCalled();
});
