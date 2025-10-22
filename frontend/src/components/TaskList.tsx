/**
 * TaskList Component
 * Displays a list of tasks with filtering and CRUD operations
 */

import { useState, useMemo } from 'react';
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
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Plus, Loader2, Search } from 'lucide-react';
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

type SortOption = 'due_date' | 'created_date' | 'alphabetical';
type GroupOption = 'none' | 'category' | 'status';

export function TaskList({ categoryId }: TaskListProps) {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [completedFilter, setCompletedFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<SortOption>('due_date');
  const [groupBy, setGroupBy] = useState<GroupOption>('none');
  const [searchQuery, setSearchQuery] = useState('');

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

  // Filter, sort, and group tasks
  const processedTasks = useMemo(() => {
    let filtered = [...tasks];

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter((task) =>
        task.content.toLowerCase().includes(query) ||
        task.category_name?.toLowerCase().includes(query)
      );
    }

    // Sort tasks
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'due_date':
          // Put tasks without due date at the end
          if (!a.due_date && !b.due_date) return 0;
          if (!a.due_date) return 1;
          if (!b.due_date) return -1;
          return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();

        case 'created_date':
          return new Date(b.created_date).getTime() - new Date(a.created_date).getTime();

        case 'alphabetical':
          return a.content.localeCompare(b.content);

        default:
          return 0;
      }
    });

    return filtered;
  }, [tasks, searchQuery, sortBy]);

  // Group tasks if needed
  const groupedTasks = useMemo(() => {
    if (groupBy === 'none') {
      return { 'All Tasks': processedTasks };
    }

    if (groupBy === 'category') {
      const groups: Record<string, Task[]> = {};
      processedTasks.forEach((task) => {
        const category = task.category_name || 'Uncategorized';
        if (!groups[category]) groups[category] = [];
        groups[category].push(task);
      });
      return groups;
    }

    if (groupBy === 'status') {
      return {
        'Open': processedTasks.filter((t) => !t.completed),
        'Completed': processedTasks.filter((t) => t.completed),
      };
    }

    return { 'All Tasks': processedTasks };
  }, [processedTasks, groupBy]);

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
    <div className="space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Tasks</h2>
        <Button size="sm" onClick={handleCreateNew}>
          <Plus className="h-3.5 w-3.5 mr-1.5" />
          New
        </Button>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col gap-2.5">
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        {/* Filter Controls */}
        <div className="flex gap-2 flex-wrap">
          <Select value={completedFilter} onValueChange={setCompletedFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Tasks</SelectItem>
              <SelectItem value="false">Active</SelectItem>
              <SelectItem value="true">Completed</SelectItem>
            </SelectContent>
          </Select>

          <Select value={sortBy} onValueChange={(val) => setSortBy(val as SortOption)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="due_date">Due Date</SelectItem>
              <SelectItem value="created_date">Created Date</SelectItem>
              <SelectItem value="alphabetical">Alphabetical</SelectItem>
            </SelectContent>
          </Select>

          <Select value={groupBy} onValueChange={(val) => setGroupBy(val as GroupOption)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Group by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="none">No Grouping</SelectItem>
              <SelectItem value="category">By Category</SelectItem>
              <SelectItem value="status">By Status</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Task List */}
      <div className="space-y-3">
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
        ) : processedTasks.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            <p className="text-lg">
              {searchQuery ? 'No tasks match your search' : 'No tasks found'}
            </p>
            <p className="text-sm mt-2">
              {searchQuery ? 'Try a different search term' : 'Create your first task to get started!'}
            </p>
          </div>
        ) : (
          Object.entries(groupedTasks).map(([groupName, groupTasks]) => (
            <div key={groupName} className="space-y-2">
              {/* Group Header */}
              {groupBy !== 'none' && (
                <div className="flex items-center gap-3">
                  <h2 className="text-lg font-semibold">{groupName}</h2>
                  <Badge variant="secondary">{groupTasks.length}</Badge>
                </div>
              )}

              {/* Tasks in Group */}
              <div className="space-y-2">
                {groupTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onToggleComplete={handleToggleComplete}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                  />
                ))}
              </div>
            </div>
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
