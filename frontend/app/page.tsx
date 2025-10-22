'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, CheckCircle2, Circle, Clock } from 'lucide-react';

export default function HomePage() {
  const { data: tasks, isLoading: tasksLoading, error: tasksError } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => api.getTasks(),
  });

  const { data: categories, isLoading: categoriesLoading, error: categoriesError } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.getCategories(),
  });

  const { data: healthStatus, error: healthError } = useQuery({
    queryKey: ['health'],
    queryFn: () => api.health(),
  });

  const activeTasks = tasks?.filter((t) => !t.completed) || [];
  const completedTasks = tasks?.filter((t) => t.completed) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Header */}
      <header className="border-b bg-white/50 dark:bg-slate-950/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Life OS</h1>
              <p className="text-sm text-muted-foreground">Your Personal Dashboard</p>
            </div>
            {healthStatus && (
              <Badge variant={healthStatus.status === 'healthy' ? 'default' : 'destructive'}>
                {healthStatus.status}
              </Badge>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {/* Stats */}
          <Card>
            <CardHeader>
              <CardTitle>Tasks</CardTitle>
              <CardDescription>Your task overview</CardDescription>
            </CardHeader>
            <CardContent>
              {tasksLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                </div>
              ) : tasksError ? (
                <div className="flex flex-col items-center justify-center py-8 text-center">
                  <p className="text-sm text-destructive">Error loading tasks</p>
                  <p className="text-xs text-muted-foreground mt-1">{(tasksError as Error).message}</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Circle className="h-5 w-5 text-blue-500" />
                      <span className="text-sm">Active</span>
                    </div>
                    <span className="text-2xl font-bold">{activeTasks.length}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-5 w-5 text-green-500" />
                      <span className="text-sm">Completed</span>
                    </div>
                    <span className="text-2xl font-bold">{completedTasks.length}</span>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Categories */}
          <Card>
            <CardHeader>
              <CardTitle>Categories</CardTitle>
              <CardDescription>Organization structure</CardDescription>
            </CardHeader>
            <CardContent>
              {categoriesLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                </div>
              ) : categoriesError ? (
                <div className="flex flex-col items-center justify-center py-8 text-center">
                  <p className="text-sm text-destructive">Error loading categories</p>
                  <p className="text-xs text-muted-foreground mt-1">{(categoriesError as Error).message}</p>
                </div>
              ) : (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Total categories</span>
                  <span className="text-3xl font-bold">{categories?.length || 0}</span>
                </div>
              )}
            </CardContent>
          </Card>

          {/* API Status */}
          <Card>
            <CardHeader>
              <CardTitle>System Status</CardTitle>
              <CardDescription>Backend health</CardDescription>
            </CardHeader>
            <CardContent>
              {healthError ? (
                <div className="flex flex-col items-center justify-center py-8 text-center">
                  <p className="text-sm text-destructive">Error loading health status</p>
                  <p className="text-xs text-muted-foreground mt-1">{(healthError as Error).message}</p>
                </div>
              ) : healthStatus ? (
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Database</span>
                    <Badge variant="outline">{healthStatus.database}</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Status</span>
                    <Badge variant="default">{healthStatus.status}</Badge>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Recent Tasks */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Recent Tasks</CardTitle>
            <CardDescription>Your latest active tasks</CardDescription>
          </CardHeader>
          <CardContent>
            {tasksLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
              </div>
            ) : activeTasks.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <CheckCircle2 className="h-12 w-12 text-muted-foreground mb-2" />
                <p className="text-lg font-medium">All caught up!</p>
                <p className="text-sm text-muted-foreground">No active tasks</p>
              </div>
            ) : (
              <div className="space-y-3">
                {activeTasks.slice(0, 10).map((task) => (
                  <div
                    key={task.id}
                    className="flex items-start gap-3 p-3 rounded-lg border bg-card hover:bg-accent transition-colors"
                  >
                    <Circle className="h-5 w-5 mt-0.5 text-muted-foreground" />
                    <div className="flex-1 space-y-1">
                      <p className="text-sm font-medium leading-none">{task.content}</p>
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        {task.category_name && (
                          <Badge variant="secondary" className="text-xs">
                            {task.category_name}
                          </Badge>
                        )}
                        {task.due_date && (
                          <span className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {new Date(task.due_date).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
