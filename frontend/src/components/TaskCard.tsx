/**
 * TaskCard Component
 * Displays a single task with actions
 */

import type { Task } from '@/lib/api';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Calendar, Edit2, Trash2 } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

export function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  const isOverdue = task.due_date && !task.completed && new Date(task.due_date) < new Date();

  return (
    <Card className={task.completed ? 'opacity-60' : ''}>
      <CardContent className="pt-6">
        <div className="flex items-start gap-3">
          <Checkbox
            checked={task.completed}
            onCheckedChange={() => onToggleComplete(task.id)}
            className="mt-1"
          />
          <div className="flex-1 space-y-2">
            <p className={`text-sm ${task.completed ? 'line-through text-muted-foreground' : ''}`}>
              {task.content}
            </p>

            <div className="flex flex-wrap items-center gap-2">
              {task.category_name && (
                <Badge variant="secondary" className="text-xs">
                  {task.category_name}
                </Badge>
              )}

              {task.due_date && (
                <Badge
                  variant={isOverdue ? 'destructive' : 'outline'}
                  className="text-xs flex items-center gap-1"
                >
                  <Calendar className="h-3 w-3" />
                  {formatDate(task.due_date)}
                </Badge>
              )}
            </div>
          </div>
        </div>
      </CardContent>

      <CardFooter className="flex justify-end gap-2 pt-0 pb-4">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onEdit(task)}
          className="h-8 px-2"
        >
          <Edit2 className="h-4 w-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onDelete(task.id)}
          className="h-8 px-2 text-destructive hover:text-destructive"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
}
