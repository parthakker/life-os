import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api, type Note } from '@/lib/api';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface NoteEditDialogProps {
  note?: Note;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function NoteEditDialog({ note, open, onOpenChange }: NoteEditDialogProps) {
  const [content, setContent] = useState('');
  const [categoryId, setCategoryId] = useState<string>('');
  const queryClient = useQueryClient();

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.getCategories(),
  });

  // Initialize form when dialog opens
  useEffect(() => {
    if (open) {
      if (note) {
        setContent(note.content);
        setCategoryId(note.category_id?.toString() || '');
      } else {
        setContent('');
        setCategoryId('');
      }
    }
  }, [open, note]);

  const createMutation = useMutation({
    mutationFn: (data: Partial<Note>) => api.createNote(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes'] });
      onOpenChange(false);
      setContent('');
      setCategoryId('');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Note> }) =>
      api.updateNote(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes'] });
      onOpenChange(false);
    },
  });

  const handleSubmit = () => {
    const noteData: Partial<Note> = {
      content: content.trim(),
      category_id: categoryId ? parseInt(categoryId) : undefined,
    };

    if (note) {
      updateMutation.mutate({ id: note.id, data: noteData });
    } else {
      createMutation.mutate(noteData);
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;
  const canSubmit = content.trim().length > 0 && categoryId;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{note ? 'Edit Note' : 'Create Note'}</DialogTitle>
          <DialogDescription>
            {note ? 'Edit your note below' : 'Create a new note'}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* Category Selection */}
          <div className="space-y-2">
            <Label htmlFor="category">Category</Label>
            <Select value={categoryId} onValueChange={setCategoryId}>
              <SelectTrigger id="category">
                <SelectValue placeholder="Select a category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat.id} value={cat.id.toString()}>
                    {cat.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Content */}
          <div className="space-y-2">
            <Label htmlFor="content">Content</Label>
            <Textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write your note here..."
              rows={12}
              className="resize-none font-mono text-sm"
            />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={!canSubmit || isLoading}>
            {isLoading ? 'Saving...' : note ? 'Save' : 'Create'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
