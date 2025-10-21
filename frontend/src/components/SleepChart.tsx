import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface SleepData {
  date: string;
  hours: number;
}

interface SleepChartProps {
  data: SleepData[];
  days?: number; // Number of days to show (default: 7)
}

export function SleepChart({ data, days = 7 }: SleepChartProps) {
  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Sleep Trends ({days} Days)</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No data available</p>
        </CardContent>
      </Card>
    );
  }

  // Take the most recent N days and reverse for chronological order
  const chartData = [...data]
    .slice(0, days)
    .reverse()
    .map(item => ({
      date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      hours: item.hours,
    }));

  // Calculate average
  const avgHours = chartData.reduce((sum, item) => sum + item.hours, 0) / chartData.length;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Sleep Trends ({days} Days)</span>
          <span className="text-sm font-normal text-muted-foreground">
            Avg: {avgHours.toFixed(1)} hrs
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="date"
              className="text-xs"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
            />
            <YAxis
              domain={[0, 10]}
              className="text-xs"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '6px',
              }}
              labelStyle={{ color: 'hsl(var(--foreground))' }}
              formatter={(value: number) => [`${value} hrs`, 'Sleep']}
            />
            <ReferenceLine
              y={avgHours}
              stroke="hsl(var(--muted-foreground))"
              strokeDasharray="3 3"
              label={{ value: 'Avg', position: 'right', fill: 'hsl(var(--muted-foreground))' }}
            />
            <Bar
              dataKey="hours"
              fill="hsl(var(--primary))"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
