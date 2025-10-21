/**
 * TaskList Component
 * Displays a list of tasks with filtering and CRUD operations
 */

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  useTasksQuery,
  useToggleTaskCompletion,
  useUpdateTask,
  useDeleteTask,
  useCreateTask,
} from '@/hooks/useTasks';
import { api } from '@/lib/api';
import type { Task } from '@/lib/api';
import { TaskCard } from './TaskCard';
import { TaskEditDialog } from './TaskEditDialog';
import { Button } from '@/components/ui/button';
import { Plus, Loader2 } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface TaskListProps {
  categoryId?: number | null;
}

export function TaskList({ categoryId }: TaskListProps) {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [completedFilter, setCompletedFilter] = useState<string>('all');

  // Fetch categories for the dialog
  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.getCategories(),
  });

  // Build filter object based on props and local state
  const filters =
    categoryId === null && completedFilter === 'all'
      ? undefined
      : {
          category_id: categoryId === null ? undefined : categoryId,
          completed: completedFilter === 'all' ? undefined : completedFilter === 'true',
          include_children: categoryId !== null && categoryId !== undefined,
        };

  // Fetch tasks with filters
  const { data: tasks = [], isLoading, error } = useTasksQuery(filters);

  // Mutations
  const toggleCompletion = useToggleTaskCompletion();
  const updateTask = useUpdateTask();
  const deleteTask = useDeleteTask();
  const createTask = useCreateTask();

  // Handlers
  const handleToggleComplete = (id: number) => {
    toggleCompletion.mutate(id);
  };

  const handleEdit = (task: Task) => {
    setSelectedTask(task);
    setDialogOpen(true);
  };

  const handleDelete = (id: number) => {
    if (confirm('Are you sure you want to delete this task?')) {
      deleteTask.mutate(id);
    }
  };

  const handleCreateNew = () => {
    setSelectedTask(null);
    setDialogOpen(true);
  };

  const handleSaveTask = (data: Partial<Task>) => {
    if (selectedTask) {
      // Update existing task
      updateTask.mutate(
        { id: selectedTask.id, data },
        {
          onSuccess: () => {
            setDialogOpen(false);
            setSelectedTask(null);
          },
        }
      );
    } else {
      // Create new task
      createTask.mutate(data, {
        onSuccess: () => {
          setDialogOpen(false);
        },
      });
    }
  };

  const isMutating =
    updateTask.isPending || createTask.isPending || toggleCompletion.isPending || deleteTask.isPending;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tasks</h1>
        <Button onClick={handleCreateNew}>
          <Plus className="h-4 w-4 mr-2" />
          New Task
        </Button>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <Select value={completedFilter} onValueChange={setCompletedFilter}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="All Tasks" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Tasks</SelectItem>
            <SelectItem value="false">Active</SelectItem>
            <SelectItem value="true">Completed</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Task List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-destructive">Error loading tasks: {error.message}</p>
            <Button variant="outline" onClick={() => window.location.reload()} className="mt-4">
              Retry
            </Button>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            <p className="text-lg">No tasks found</p>
            <p className="text-sm mt-2">Create your first task to get started!</p>
          </div>
        ) : (
          tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))
        )}
      </div>

      {/* Edit/Create Dialog */}
      <TaskEditDialog
        task={selectedTask}
        categories={categories}
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        onSave={handleSaveTask}
        isLoading={isMutating}
      />
    </div>
  );
}
