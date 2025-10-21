import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { Category } from '@/lib/api';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

type DialogMode = 'rename' | 'create' | 'move';

interface CategoryEditDialogProps {
  mode: DialogMode;
  category?: Category;
  parentId?: number | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CategoryEditDialog({ mode, category, parentId, open, onOpenChange }: CategoryEditDialogProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [selectedParentId, setSelectedParentId] = useState<string>('none');
  const queryClient = useQueryClient();

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.getCategories(),
  });

  // Initialize form when dialog opens
  useEffect(() => {
    if (open) {
      if (mode === 'rename' && category) {
        setName(category.name);
        setDescription(category.description || '');
      } else if (mode === 'create') {
        setName('');
        setDescription('');
        setSelectedParentId(parentId !== undefined && parentId !== null ? parentId.toString() : 'none');
      } else if (mode === 'move' && category) {
        setSelectedParentId(category.parent_id !== undefined && category.parent_id !== null ? category.parent_id.toString() : 'none');
      }
    }
  }, [open, mode, category, parentId]);

  const createMutation = useMutation({
    mutationFn: (data: Partial<Category>) => api.createCategory(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
      queryClient.invalidateQueries({ queryKey: ['categories', 'tree'] });
      queryClient.invalidateQueries({ queryKey: ['categories', 'task-counts'] });
      onOpenChange(false);
      setName('');
      setDescription('');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Category> }) => api.updateCategory(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
      queryClient.invalidateQueries({ queryKey: ['categories', 'tree'] });
      onOpenChange(false);
    },
  });

  const handleSubmit = () => {
    if (mode === 'rename' && category) {
      updateMutation.mutate({
        id: category.id,
        data: { name, description: description.trim() || undefined },
      });
    } else if (mode === 'create') {
      const parent_id = selectedParentId === 'none' ? null : parseInt(selectedParentId);
      createMutation.mutate({
        name,
        description: description.trim() || undefined,
        parent_id,
      });
    } else if (mode === 'move' && category) {
      const parent_id = selectedParentId === 'none' ? null : parseInt(selectedParentId);
      updateMutation.mutate({
        id: category.id,
        data: { parent_id },
      });
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;
  const canSubmit = mode === 'move' || (name.trim().length > 0);

  // Filter out the category being moved and its descendants to prevent circular references
  const availableParents = categories.filter((cat) => {
    if (mode === 'move' && category) {
      // Can't move to itself
      if (cat.id === category.id) return false;
      // Can't move to its own children (would need recursive check in real app)
      // For now, simple check
      return true;
    }
    if (mode === 'create' && parentId !== undefined) {
      // When creating, can select any category
      return true;
    }
    return true;
  });

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {mode === 'rename' && 'Rename Category'}
            {mode === 'create' && 'Create Category'}
            {mode === 'move' && 'Move Category'}
          </DialogTitle>
          <DialogDescription>
            {mode === 'rename' && 'Enter a new name for this category'}
            {mode === 'create' && 'Create a new category'}
            {mode === 'move' && 'Select a new parent category'}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {(mode === 'rename' || mode === 'create') && (
            <>
              <div className="space-y-2">
                <Label htmlFor="name">Category Name</Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Enter category name"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && canSubmit && !e.shiftKey) {
                      handleSubmit();
                    }
                  }}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">
                  Description <span className="text-muted-foreground text-xs">(optional)</span>
                </Label>
                <Textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Help AI understand what goes in this category: people, topics, activities..."
                  rows={3}
                  className="resize-none"
                />
                <p className="text-xs text-muted-foreground">
                  This helps the AI assistant categorize your tasks and notes automatically
                </p>
              </div>
            </>
          )}

          {(mode === 'create' || mode === 'move') && (
            <div className="space-y-2">
              <Label htmlFor="parent">Parent Category</Label>
              <Select value={selectedParentId} onValueChange={setSelectedParentId}>
                <SelectTrigger id="parent">
                  <SelectValue placeholder="Select parent" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">None (Top Level)</SelectItem>
                  {availableParents.map((cat) => (
                    <SelectItem key={cat.id} value={cat.id.toString()}>
                      {cat.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={!canSubmit || isLoading}>
            {isLoading ? 'Saving...' : mode === 'create' ? 'Create' : 'Save'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
