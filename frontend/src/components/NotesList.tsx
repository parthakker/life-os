import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api, type Note } from '@/lib/api';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { NoteCard } from './NoteCard';
import { NoteEditDialog } from './NoteEditDialog';

interface NotesListProps {
  categoryId: number | null;
}

export function NotesList({ categoryId }: NotesListProps) {
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingNote, setEditingNote] = useState<Note | undefined>(undefined);

  const { data: notes = [], isLoading, error } = useQuery({
    queryKey: ['notes', { category_id: categoryId }],
    queryFn: () => {
      if (categoryId === null) {
        return api.getNotes();
      }
      return api.getNotes({ category_id: categoryId });
    },
  });

  const handleEdit = (note: Note) => {
    setEditingNote(note);
    setEditDialogOpen(true);
  };

  const handleNewNote = () => {
    setEditingNote(undefined);
    setEditDialogOpen(true);
  };

  const handleDialogClose = (open: boolean) => {
    setEditDialogOpen(open);
    if (!open) {
      setEditingNote(undefined);
    }
  };

  if (isLoading) {
    return <div className="text-muted-foreground">Loading notes...</div>;
  }

  if (error) {
    return <div className="text-destructive">Error loading notes</div>;
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">
            {categoryId ? 'Category Notes' : 'All Notes'}
          </h2>
          <p className="text-sm text-muted-foreground mt-1">
            {notes.length} {notes.length === 1 ? 'note' : 'notes'}
          </p>
        </div>
        <Button onClick={handleNewNote} size="sm">
          <Plus className="h-4 w-4 mr-2" />
          New Note
        </Button>
      </div>

      {/* Notes List */}
      {notes.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          <p>No notes yet</p>
          <p className="text-sm mt-2">Click "New Note" to create one</p>
        </div>
      ) : (
        <div className="space-y-4">
          {notes.map((note) => (
            <NoteCard key={note.id} note={note} onEdit={handleEdit} />
          ))}
        </div>
      )}

      {/* Edit Dialog */}
      <NoteEditDialog
        note={editingNote}
        open={editDialogOpen}
        onOpenChange={handleDialogClose}
      />
    </div>
  );
}
