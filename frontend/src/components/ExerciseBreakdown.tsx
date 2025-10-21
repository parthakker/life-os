import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ExerciseData {
  date: string;
  activity_type: string;
  duration_minutes: number;
}

interface ExerciseBreakdownProps {
  data: ExerciseData[];
  days?: number; // Number of days to analyze (default: 30)
}

const ACTIVITY_COLORS: Record<string, string> = {
  'Pickleball': 'hsl(142, 76%, 36%)',
  'Gym': 'hsl(var(--primary))',
  'BJJ': 'hsl(24, 95%, 53%)',
  'Yoga': 'hsl(280, 65%, 60%)',
  'Running': 'hsl(200, 98%, 39%)',
  'Other': 'hsl(var(--muted-foreground))',
};

export function ExerciseBreakdown({ data, days = 30 }: ExerciseBreakdownProps) {
  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Exercise Breakdown</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No data available</p>
        </CardContent>
      </Card>
    );
  }

  // Filter to recent days
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - days);
  const recentData = data.filter(item => new Date(item.date) >= cutoffDate);

  // Aggregate by activity type
  const activityTotals = recentData.reduce((acc, item) => {
    const type = item.activity_type || 'Other';
    acc[type] = (acc[type] || 0) + item.duration_minutes;
    return acc;
  }, {} as Record<string, number>);

  // Convert to chart format
  const chartData = Object.entries(activityTotals).map(([name, value]) => ({
    name,
    value,
    hours: (value / 60).toFixed(1),
  }));

  const totalMinutes = chartData.reduce((sum, item) => sum + item.value, 0);
  const totalHours = (totalMinutes / 60).toFixed(1);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Exercise Breakdown</span>
          <span className="text-sm font-normal text-muted-foreground">
            Total: {totalHours} hrs
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="hsl(var(--primary))"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={ACTIVITY_COLORS[entry.name] || ACTIVITY_COLORS['Other']}
                />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '6px',
              }}
              labelStyle={{ color: 'hsl(var(--foreground))' }}
              formatter={(value: number, name: string, props: any) => [
                `${props.payload.hours} hrs (${value} min)`,
                name,
              ]}
            />
          </PieChart>
        </ResponsiveContainer>

        {/* Activity List */}
        <div className="mt-4 space-y-2">
          {chartData.map((item) => (
            <div key={item.name} className="flex justify-between text-sm">
              <div className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: ACTIVITY_COLORS[item.name] || ACTIVITY_COLORS['Other'] }}
                />
                <span>{item.name}</span>
              </div>
              <span className="text-muted-foreground">{item.hours} hrs</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
