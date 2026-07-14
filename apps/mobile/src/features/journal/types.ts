export type JournalEntry = Readonly<{
  id: string;
  createdAt: string;
  updatedAt: string;
  title: string;
  body: string;
  linkedAnalysisId: string | null;
  tags: string[];
  isExported: boolean;
}>;

export type JournalDraft = Readonly<{
  title: string;
  body: string;
  linkedAnalysisId?: string | null;
  tags?: string[];
}>;
