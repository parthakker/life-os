/**
 * TaskCard Component
 * Displays a single task with actions
 */

import type { Task } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
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
      });
    } catch {
      return dateString;
    }
  };

  const isOverdue = task.due_date && !task.completed && new Date(task.due_date) < new Date();

  return (
    <Card className={task.completed ? 'opacity-60' : ''}>
      <CardContent className="py-2.5 px-3">
        <div className="flex items-start gap-2">
          <Checkbox
            checked={task.completed}
            onCheckedChange={() => onToggleComplete(task.id)}
            className="mt-0.5"
          />
          <div className="flex-1 min-w-0">
            <p className={`text-sm ${task.completed ? 'line-through text-muted-foreground' : ''}`}>
              {task.content}
            </p>

            <div className="flex flex-wrap items-center gap-1.5 mt-1">
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

          {/* Action buttons and created date on the right */}
          <div className="flex items-start gap-1 flex-shrink-0">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit(task)}
              className="h-6 w-6 p-0"
            >
              <Edit2 className="h-3.5 w-3.5" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(task.id)}
              className="h-6 w-6 p-0 text-destructive hover:text-destructive"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>

        {/* Created date at bottom right */}
        <div className="flex justify-end mt-1">
          <span className="text-xs text-muted-foreground">
            {formatDate(task.created_date)}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
