/**
 * React Query hooks for Task operations
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { Task } from '@/lib/api';

// Query keys
export const taskKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskKeys.all, 'list'] as const,
  list: (filters?: { category_id?: number; completed?: boolean; include_children?: boolean }) =>
    [...taskKeys.lists(), filters] as const,
  details: () => [...taskKeys.all, 'detail'] as const,
  detail: (id: number) => [...taskKeys.details(), id] as const,
};

// ==================== QUERIES ====================

/**
 * Fetch all tasks with optional filters
 */
export function useTasksQuery(filters?: { category_id?: number; completed?: boolean; include_children?: boolean }) {
  return useQuery({
    queryKey: taskKeys.list(filters),
    queryFn: () => api.getTasks(filters),
  });
}

/**
 * Fetch a single task by ID
 */
export function useTaskQuery(id: number) {
  return useQuery({
    queryKey: taskKeys.detail(id),
    queryFn: () => api.getTask(id),
    enabled: !!id,
  });
}

// ==================== MUTATIONS ====================

/**
 * Create a new task
 */
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Partial<Task>) => api.createTask(data),
    onSuccess: () => {
      // Invalidate all task lists to refetch
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}

/**
 * Update an existing task
 */
export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Task> }) =>
      api.updateTask(id, data),
    onSuccess: (updatedTask) => {
      // Invalidate task lists
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
      // Update the specific task detail
      queryClient.setQueryData(taskKeys.detail(updatedTask.id), updatedTask);
    },
  });
}

/**
 * Toggle task completion status
 */
export function useToggleTaskCompletion() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => api.toggleTaskCompletion(id),
    onSuccess: (updatedTask) => {
      // Invalidate task lists to refetch with new completion status
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
      // Update the specific task detail
      queryClient.setQueryData(taskKeys.detail(updatedTask.id), updatedTask);
    },
  });
}

/**
 * Delete a task
 */
export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => api.deleteTask(id),
    onSuccess: () => {
      // Invalidate all task queries
      queryClient.invalidateQueries({ queryKey: taskKeys.all });
    },
  });
}
