/**
 * API Client for Life OS Backend
 * Provides type-safe API calls to Flask server
 */

const API_BASE_URL = 'http://localhost:5000/api';

// ==================== TYPES ====================

export interface Category {
  id: number;
  name: string;
  parent_category?: string;
  sort_order?: number;
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

  // ==================== TASKS ====================

  async getTasks(filters?: { category_id?: number; completed?: boolean }): Promise<Task[]> {
    const params = new URLSearchParams();
    if (filters?.category_id) params.append('category_id', filters.category_id.toString());
    if (filters?.completed !== undefined) params.append('completed', filters.completed.toString());

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
}

export const api = new ApiClient(API_BASE_URL);
