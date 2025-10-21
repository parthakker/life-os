import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface InBodyData {
  date: string;
  weight: number;
  smm: number;
  pbf: number;
  ecw_tbw_ratio: number;
}

interface InBodyChartProps {
  data: InBodyData[];
}

export function InBodyChart({ data }: InBodyChartProps) {
  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>InBody Trends</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No data available</p>
        </CardContent>
      </Card>
    );
  }

  // Format data for the chart (reverse to show oldest to newest)
  const chartData = [...data].reverse().map(item => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    Weight: item.weight,
    SMM: item.smm,
    'PBF (%)': item.pbf,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>InBody Trends</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="date"
              className="text-xs"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
            />
            <YAxis
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
            />
            <Legend
              wrapperStyle={{ paddingTop: '20px' }}
              iconType="line"
            />
            <Line
              type="monotone"
              dataKey="Weight"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--primary))' }}
            />
            <Line
              type="monotone"
              dataKey="SMM"
              stroke="hsl(142, 76%, 36%)"
              strokeWidth={2}
              dot={{ fill: 'hsl(142, 76%, 36%)' }}
            />
            <Line
              type="monotone"
              dataKey="PBF (%)"
              stroke="hsl(24, 95%, 53%)"
              strokeWidth={2}
              dot={{ fill: 'hsl(24, 95%, 53%)' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
