/**
 * API Client for Life OS Backend
 * Provides type-safe API calls to Flask server
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// ==================== TYPES ====================

export interface Category {
  id: number;
  name: string;
  description?: string;
  parent_id?: number | null;
  sort_order?: number;
  children?: Category[]; // For tree structure
}

export interface Task {
  id: number;
  category_id?: number;
  category_name?: string;
  content: string;
  due_date?: string;
  completed: boolean;
  created_date: string;
}

export interface Note {
  id: number;
  category_id?: number;
  category_name?: string;
  content: string;
  created_date: string;
}

export interface SearchResult {
  query: string;
  answer: string;
}

export interface HealthStatus {
  status: string;
  database: string;
  timestamp: string;
}

// ==================== API CLIENT ====================

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // ==================== HEALTH ====================

  async health(): Promise<HealthStatus> {
    return this.request<HealthStatus>('/health');
  }

  // ==================== CATEGORIES ====================

  async getCategories(): Promise<Category[]> {
    return this.request<Category[]>('/categories');
  }

  async getCategoriesTree(): Promise<Category[]> {
    return this.request<Category[]>('/categories/tree');
  }

  async getCategoryTaskCounts(): Promise<Record<number, number>> {
    return this.request<Record<number, number>>('/categories/task-counts');
  }

  async getCategoryNoteCounts(): Promise<Record<number, number>> {
    return this.request<Record<number, number>>('/categories/note-counts');
  }

  async createCategory(data: Partial<Category>): Promise<Category> {
    return this.request<Category>('/categories', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateCategory(id: number, data: Partial<Category>): Promise<Category> {
    return this.request<Category>(`/categories/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteCategory(id: number, options?: { reassign_to?: number; delete_tasks?: boolean }): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/categories/${id}`, {
      method: 'DELETE',
      body: options ? JSON.stringify(options) : undefined,
    });
  }

  // ==================== TASKS ====================

  async getTasks(filters?: { category_id?: number; completed?: boolean; include_children?: boolean }): Promise<Task[]> {
    const params = new URLSearchParams();
    if (filters?.category_id) params.append('category_id', filters.category_id.toString());
    if (filters?.completed !== undefined) params.append('completed', filters.completed.toString());
    if (filters?.include_children) params.append('include_children', 'true');

    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request<Task[]>(`/tasks${query}`);
  }

  async getTask(id: number): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`);
  }

  async createTask(data: Partial<Task>): Promise<Task> {
    return this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateTask(id: number, data: Partial<Task>): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async toggleTaskCompletion(id: number): Promise<Task> {
    return this.request<Task>(`/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }

  async deleteTask(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  // ==================== NOTES ====================

  async getNotes(filters?: { category_id?: number }): Promise<Note[]> {
    const params = new URLSearchParams();
    if (filters?.category_id) params.append('category_id', filters.category_id.toString());

    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request<Note[]>(`/notes${query}`);
  }

  async getNote(id: number): Promise<Note> {
    return this.request<Note>(`/notes/${id}`);
  }

  async createNote(data: Partial<Note>): Promise<Note> {
    return this.request<Note>('/notes', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateNote(id: number, data: Partial<Note>): Promise<Note> {
    return this.request<Note>(`/notes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteNote(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/notes/${id}`, {
      method: 'DELETE',
    });
  }

  // ==================== SEARCH ====================

  async search(query: string): Promise<SearchResult> {
    const params = new URLSearchParams({ q: query });
    return this.request<SearchResult>(`/search?${params.toString()}`);
  }

  // ==================== HEALTH ====================

  async getHealthSummary(): Promise<any> {
    return this.request<any>('/health/summary');
  }

  async getInBodyData(): Promise<any[]> {
    return this.request<any[]>('/health/inbody');
  }

  async getSleepData(params?: { start_date?: string; end_date?: string }): Promise<any[]> {
    const query = params ? `?${new URLSearchParams(params as any).toString()}` : '';
    return this.request<any[]>(`/health/sleep${query}`);
  }

  async getWaterData(params?: { start_date?: string; end_date?: string }): Promise<any[]> {
    const query = params ? `?${new URLSearchParams(params as any).toString()}` : '';
    return this.request<any[]>(`/health/water${query}`);
  }

  async getExerciseData(params?: { start_date?: string; end_date?: string }): Promise<any[]> {
    const query = params ? `?${new URLSearchParams(params as any).toString()}` : '';
    return this.request<any[]>(`/health/exercise${query}`);
  }

  async getSaunaData(params?: { start_date?: string; end_date?: string }): Promise<any[]> {
    const query = params ? `?${new URLSearchParams(params as any).toString()}` : '';
    return this.request<any[]>(`/health/sauna${query}`);
  }
}

export const api = new ApiClient(API_BASE_URL);
