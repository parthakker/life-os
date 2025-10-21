import { useState } from 'react';
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
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { AlertTriangle } from 'lucide-react';

interface DeleteCategoryDialogProps {
  category: Category | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function DeleteCategoryDialog({ category, open, onOpenChange }: DeleteCategoryDialogProps) {
  const [reassignTo, setReassignTo] = useState<string>('none');
  const [deleteTasks, setDeleteTasks] = useState(false);
  const queryClient = useQueryClient();

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.getCategories(),
    enabled: open,
  });

  const { data: tasks = [] } = useQuery({
    queryKey: ['tasks', { category_id: category?.id }],
    queryFn: () => api.getTasks({ category_id: category!.id }),
    enabled: open && category !== null,
  });

  const deleteMutation = useMutation({
    mutationFn: ({ id, options }: { id: number; options?: { reassign_to?: number; delete_tasks?: boolean } }) =>
      api.deleteCategory(id, options),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
      queryClient.invalidateQueries({ queryKey: ['categories', 'tree'] });
      queryClient.invalidateQueries({ queryKey: ['categories', 'task-counts'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      onOpenChange(false);
      setReassignTo('none');
      setDeleteTasks(false);
    },
  });

  if (!category) return null;

  // Check if category has children
  const hasChildren = categories.some((cat) => cat.parent_id === category.id);
  const taskCount = tasks.length;
  const hasTasks = taskCount > 0;

  // Available categories to reassign tasks to (excluding the one being deleted)
  const availableCategories = categories.filter((cat) => cat.id !== category.id);

  const handleDelete = () => {
    if (hasChildren) {
      return; // Shouldn't happen if button is disabled
    }

    const options: { reassign_to?: number; delete_tasks?: boolean } = {};

    if (hasTasks) {
      if (deleteTasks) {
        options.delete_tasks = true;
      } else if (reassignTo !== 'none') {
        options.reassign_to = parseInt(reassignTo);
      } else {
        // User must choose an option
        return;
      }
    }

    deleteMutation.mutate({ id: category.id, options });
  };

  const canDelete = !hasChildren && (!hasTasks || deleteTasks || reassignTo !== 'none');

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-destructive" />
            Delete Category
          </DialogTitle>
          <DialogDescription>
            Are you sure you want to delete "{category.name}"?
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {hasChildren && (
            <div className="p-3 border border-destructive/50 bg-destructive/10 rounded-md">
              <p className="text-sm text-destructive font-medium">Cannot delete this category</p>
              <p className="text-sm text-muted-foreground mt-1">
                This category has subcategories. Please delete or move them first.
              </p>
            </div>
          )}

          {hasTasks && !hasChildren && (
            <div className="space-y-3">
              <div className="p-3 border border-amber-500/50 bg-amber-500/10 rounded-md">
                <p className="text-sm text-amber-700 dark:text-amber-400 font-medium">
                  This category has {taskCount} task{taskCount !== 1 ? 's' : ''}
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Choose what to do with {taskCount === 1 ? 'it' : 'them'}:
                </p>
              </div>

              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    id="reassign"
                    name="taskAction"
                    checked={!deleteTasks}
                    onChange={() => setDeleteTasks(false)}
                    className="h-4 w-4"
                  />
                  <Label htmlFor="reassign" className="flex-1 cursor-pointer">
                    Reassign tasks to another category
                  </Label>
                </div>

                {!deleteTasks && (
                  <div className="ml-6">
                    <Select value={reassignTo} onValueChange={setReassignTo}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select category" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="none">Select a category</SelectItem>
                        {availableCategories.map((cat) => (
                          <SelectItem key={cat.id} value={cat.id.toString()}>
                            {cat.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}

                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    id="delete"
                    name="taskAction"
                    checked={deleteTasks}
                    onChange={() => {
                      setDeleteTasks(true);
                      setReassignTo('none');
                    }}
                    className="h-4 w-4"
                  />
                  <Label htmlFor="delete" className="flex-1 cursor-pointer text-destructive">
                    Delete all tasks permanently
                  </Label>
                </div>
              </div>
            </div>
          )}

          {!hasTasks && !hasChildren && (
            <p className="text-sm text-muted-foreground">
              This category is empty and can be safely deleted.
            </p>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={deleteMutation.isPending}>
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={handleDelete}
            disabled={!canDelete || deleteMutation.isPending}
          >
            {deleteMutation.isPending ? 'Deleting...' : 'Delete Category'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
