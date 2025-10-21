/**
 * TaskEditDialog Component
 * Modal dialog for creating/editing tasks
 */

import { useState, useEffect } from 'react';
import type { Task, Category } from '@/lib/api';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';

interface TaskEditDialogProps {
  task?: Task | null;
  categories: Category[];
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSave: (data: Partial<Task>) => void;
  isLoading?: boolean;
}

export function TaskEditDialog({
  task,
  categories,
  open,
  onOpenChange,
  onSave,
  isLoading = false,
}: TaskEditDialogProps) {
  const [content, setContent] = useState('');
  const [categoryId, setCategoryId] = useState<string>('');
  const [dueDate, setDueDate] = useState('');

  // Initialize form with task data when dialog opens
  useEffect(() => {
    if (open) {
      setContent(task?.content || '');
      setCategoryId(task?.category_id?.toString() || '');
      // Format date for input[type="date"]
      setDueDate(
        task?.due_date
          ? new Date(task.due_date).toISOString().split('T')[0]
          : ''
      );
    }
  }, [open, task]);

  const handleSave = () => {
    const data: Partial<Task> = {
      content: content.trim(),
      category_id: categoryId ? parseInt(categoryId) : undefined,
      due_date: dueDate || undefined,
    };

    // If editing, include the ID
    if (task) {
      onSave({ ...data, id: task.id });
    } else {
      onSave(data);
    }
  };

  const handleClose = () => {
    if (!isLoading) {
      onOpenChange(false);
    }
  };

  const isValid = content.trim().length > 0;

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[525px]">
        <DialogHeader>
          <DialogTitle>{task ? 'Edit Task' : 'Create New Task'}</DialogTitle>
          <DialogDescription>
            {task
              ? 'Update the task details below.'
              : 'Fill in the details to create a new task.'}
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          {/* Content */}
          <div className="grid gap-2">
            <Label htmlFor="content">Task Content *</Label>
            <Textarea
              id="content"
              placeholder="Enter task description..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={4}
              disabled={isLoading}
            />
          </div>

          {/* Category */}
          <div className="grid gap-2">
            <Label htmlFor="category">Category</Label>
            <Select
              value={categoryId}
              onValueChange={setCategoryId}
              disabled={isLoading}
            >
              <SelectTrigger id="category">
                <SelectValue placeholder="Select a category (optional)" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">None</SelectItem>
                {categories.map((cat) => (
                  <SelectItem key={cat.id} value={cat.id.toString()}>
                    {cat.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Due Date */}
          <div className="grid gap-2">
            <Label htmlFor="due-date">Due Date</Label>
            <Input
              id="due-date"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              disabled={isLoading}
            />
          </div>
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            onClick={handleClose}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button
            onClick={handleSave}
            disabled={!isValid || isLoading}
          >
            {isLoading ? 'Saving...' : task ? 'Update' : 'Create'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
