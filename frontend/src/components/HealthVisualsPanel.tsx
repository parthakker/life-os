import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Legend,
} from 'recharts';
import { WeatherWidget } from './WeatherWidget';
import { CalendarPreview } from './CalendarPreview';
import { WeddingCountdown } from './WeddingCountdown';

type TimeRange = '7d' | '1m' | '6m';

const TIME_RANGE_DAYS: Record<TimeRange, number> = {
  '7d': 7,
  '1m': 30,
  '6m': 180,
};

export function HealthVisualsPanel() {
  const [timeRange, setTimeRange] = useState<TimeRange>('7d');
  const days = TIME_RANGE_DAYS[timeRange];

  // Fetch all health data with proper error handling
  const { data: sleepData } = useQuery({
    queryKey: ['health', 'sleep'],
    queryFn: () => api.getSleepData(),
  });

  const { data: waterData } = useQuery({
    queryKey: ['health', 'water'],
    queryFn: () => api.getWaterData(),
    retry: false, // Don't retry if endpoint doesn't exist
  });

  const { data: exerciseData } = useQuery({
    queryKey: ['health', 'exercise'],
    queryFn: () => api.getExerciseData(),
  });

  const { data: inbodyData } = useQuery({
    queryKey: ['health', 'inbody'],
    queryFn: () => api.getInBodyData(),
  });

  // Process sleep data
  const sleepChartData = Array.isArray(sleepData)
    ? sleepData
        .slice(0, days)
        .reverse()
        .map(item => ({
          date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          hours: item.hours,
        }))
    : [];

  const avgSleep = sleepChartData.length
    ? sleepChartData.reduce((sum, item) => sum + item.hours, 0) / sleepChartData.length
    : 0;

  // Process water data
  const waterChartData = Array.isArray(waterData)
    ? waterData
        .slice(0, days)
        .reverse()
        .map(item => ({
          date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          cups: item.cups,
        }))
    : [];

  const avgWater = waterChartData.length
    ? waterChartData.reduce((sum, item) => sum + item.cups, 0) / waterChartData.length
    : 0;

  // Process exercise data
  const exerciseChartData = Array.isArray(exerciseData)
    ? exerciseData
        .slice(0, days)
        .reverse()
        .map(item => ({
          date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          minutes: item.duration_minutes,
        }))
    : [];

  const avgExercise = exerciseChartData.length
    ? exerciseChartData.reduce((sum, item) => sum + item.minutes, 0) / exerciseChartData.length
    : 0;

  // Process InBody data
  const inbodyChartData = Array.isArray(inbodyData)
    ? inbodyData
        .slice(0, Math.min(days, inbodyData.length))
        .reverse()
        .map(item => ({
          date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          Weight: item.weight,
          SMM: item.smm,
          'PBF (%)': item.pbf,
        }))
    : [];

  return (
    <div className="h-full flex flex-col overflow-y-auto">
      <div className="space-y-4 p-4">
        {/* Time Range Selector */}
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold">Health Trends</h2>
          <Tabs value={timeRange} onValueChange={(value) => setTimeRange(value as TimeRange)}>
            <TabsList>
              <TabsTrigger value="7d">7 Days</TabsTrigger>
              <TabsTrigger value="1m">1 Month</TabsTrigger>
              <TabsTrigger value="6m">6 Months</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-2 gap-4">
          {/* Sleep Chart */}
          <Card className="transition-all duration-300 hover:shadow-lg">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center justify-between text-base">
                <span>Sleep</span>
                {avgSleep > 0 && (
                  <span className="text-sm font-normal text-muted-foreground">
                    Avg: {avgSleep.toFixed(1)} hrs
                  </span>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {sleepChartData.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-8">No data available</p>
              ) : (
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={sleepChartData}>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis
                      dataKey="date"
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                    />
                    <YAxis
                      domain={[0, 10]}
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
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
                    {avgSleep > 0 && (
                      <ReferenceLine
                        y={avgSleep}
                        stroke="hsl(var(--muted-foreground))"
                        strokeDasharray="3 3"
                        label={{ value: 'Avg', position: 'right', fill: 'hsl(var(--muted-foreground))' }}
                      />
                    )}
                    <Bar dataKey="hours" fill="hsl(262, 83%, 58%)" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>

          {/* Water Chart */}
          <Card className="transition-all duration-300 hover:shadow-lg">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center justify-between text-base">
                <span>Water Intake</span>
                {avgWater > 0 && (
                  <span className="text-sm font-normal text-muted-foreground">
                    Avg: {avgWater.toFixed(1)} cups
                  </span>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {waterChartData.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-8">No data available</p>
              ) : (
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={waterChartData}>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis
                      dataKey="date"
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                    />
                    <YAxis
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '6px',
                      }}
                      labelStyle={{ color: 'hsl(var(--foreground))' }}
                      formatter={(value: number) => [`${value} cups`, 'Water']}
                    />
                    {avgWater > 0 && (
                      <ReferenceLine
                        y={avgWater}
                        stroke="hsl(var(--muted-foreground))"
                        strokeDasharray="3 3"
                        label={{ value: 'Avg', position: 'right', fill: 'hsl(var(--muted-foreground))' }}
                      />
                    )}
                    <Bar dataKey="cups" fill="hsl(199, 89%, 48%)" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>

          {/* Exercise Chart */}
          <Card className="transition-all duration-300 hover:shadow-lg">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center justify-between text-base">
                <span>Exercise</span>
                {avgExercise > 0 && (
                  <span className="text-sm font-normal text-muted-foreground">
                    Avg: {avgExercise.toFixed(0)} mins
                  </span>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {exerciseChartData.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-8">No data available</p>
              ) : (
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={exerciseChartData}>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis
                      dataKey="date"
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                    />
                    <YAxis
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '6px',
                      }}
                      labelStyle={{ color: 'hsl(var(--foreground))' }}
                      formatter={(value: number) => [`${value} mins`, 'Exercise']}
                    />
                    {avgExercise > 0 && (
                      <ReferenceLine
                        y={avgExercise}
                        stroke="hsl(var(--muted-foreground))"
                        strokeDasharray="3 3"
                        label={{ value: 'Avg', position: 'right', fill: 'hsl(var(--muted-foreground))' }}
                      />
                    )}
                    <Bar dataKey="minutes" fill="hsl(142, 76%, 36%)" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>

          {/* Weight / InBody Chart */}
          <Card className="transition-all duration-300 hover:shadow-lg">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Body Composition</CardTitle>
            </CardHeader>
            <CardContent>
              {inbodyChartData.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-8">No data available</p>
              ) : (
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={inbodyChartData}>
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis
                      dataKey="date"
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                    />
                    <YAxis
                      className="text-xs"
                      tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '6px',
                      }}
                      labelStyle={{ color: 'hsl(var(--foreground))' }}
                    />
                    <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '12px' }} iconType="line" />
                    <Line
                      type="monotone"
                      dataKey="Weight"
                      stroke="hsl(24, 95%, 53%)"
                      strokeWidth={2}
                      dot={{ fill: 'hsl(24, 95%, 53%)' }}
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
                      stroke="hsl(199, 89%, 48%)"
                      strokeWidth={2}
                      dot={{ fill: 'hsl(199, 89%, 48%)' }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Widgets Section */}
        <div className="space-y-3">
          <h3 className="text-lg font-semibold">Quick View</h3>
          <div className="grid grid-cols-1 gap-3">
            <WeddingCountdown />
            <WeatherWidget />
            <CalendarPreview />
          </div>
        </div>
      </div>
    </div>
  );
}
