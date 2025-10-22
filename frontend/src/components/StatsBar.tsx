import { useTasksQuery } from '@/hooks/useTasks';
import { Card, CardContent } from '@/components/ui/card';
import { Circle, CheckCircle2, Clock, ListTodo } from 'lucide-react';
import { WeddingCountdown } from './WeddingCountdown';
import { WeatherWidget } from './WeatherWidget';
import { CalendarPreview } from './CalendarPreview';

interface StatsBarProps {
  categoryId?: number | null;
}

export function StatsBar({ categoryId }: StatsBarProps) {
  const filters =
    categoryId === null
      ? undefined
      : {
          category_id: categoryId,
          include_children: categoryId !== null && categoryId !== undefined,
        };

  const { data: tasks = [] } = useTasksQuery(filters);

  const stats = {
    total: tasks.length,
    completed: tasks.filter((t) => t.completed).length,
    pending: tasks.filter((t) => !t.completed).length,
    overdue: tasks.filter(
      (t) => !t.completed && t.due_date && new Date(t.due_date) < new Date()
    ).length,
    dueToday: tasks.filter((t) => {
      if (!t.due_date || t.completed) return false;
      const today = new Date();
      const dueDate = new Date(t.due_date);
      return (
        dueDate.getDate() === today.getDate() &&
        dueDate.getMonth() === today.getMonth() &&
        dueDate.getFullYear() === today.getFullYear()
      );
    }).length,
  };

  return (
    <div className="grid grid-cols-6 gap-3 p-3 border-b bg-card/50">
      {/* Tasks Overview */}
      <Card className="col-span-1">
        <CardContent className="pt-4 pb-3">
          <div className="flex items-center gap-2 mb-2">
            <ListTodo className="h-4 w-4 text-blue-500" />
            <span className="text-xs font-medium text-muted-foreground">Tasks</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold">{stats.total}</span>
            <span className="text-xs text-muted-foreground">total</span>
          </div>
        </CardContent>
      </Card>

      {/* Overdue & Due Today */}
      <Card className="col-span-1">
        <CardContent className="pt-4 pb-3">
          <div className="flex flex-col gap-1.5">
            {stats.overdue > 0 && (
              <div className="flex items-center gap-2">
                <Clock className="h-3.5 w-3.5 text-destructive" />
                <span className="text-sm font-semibold text-destructive">{stats.overdue}</span>
                <span className="text-xs text-muted-foreground">overdue</span>
              </div>
            )}
            {stats.dueToday > 0 && (
              <div className="flex items-center gap-2">
                <Circle className="h-3.5 w-3.5 text-yellow-500" />
                <span className="text-sm font-semibold text-yellow-500">{stats.dueToday}</span>
                <span className="text-xs text-muted-foreground">due today</span>
              </div>
            )}
            {stats.overdue === 0 && stats.dueToday === 0 && (
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
                <span className="text-xs text-muted-foreground">All caught up!</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Wedding Countdown */}
      <div className="col-span-1">
        <WeddingCountdown />
      </div>

      {/* Weather Widget */}
      <div className="col-span-1">
        <WeatherWidget />
      </div>

      {/* Calendar Preview */}
      <div className="col-span-2">
        <CalendarPreview />
      </div>
    </div>
  );
}
