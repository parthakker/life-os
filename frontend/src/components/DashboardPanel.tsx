import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { InBodyChart } from './InBodyChart';
import { SleepChart } from './SleepChart';
import { ExerciseBreakdown } from './ExerciseBreakdown';

export function DashboardPanel() {
  const { data: healthSummary } = useQuery({
    queryKey: ['health', 'summary'],
    queryFn: () => api.getHealthSummary(),
  });

  const { data: inbodyData } = useQuery({
    queryKey: ['health', 'inbody'],
    queryFn: () => api.getInBodyData(),
  });

  const { data: sleepData } = useQuery({
    queryKey: ['health', 'sleep'],
    queryFn: () => api.getSleepData(),
  });

  const { data: exerciseData } = useQuery({
    queryKey: ['health', 'exercise'],
    queryFn: () => api.getExerciseData(),
  });

  const latestInBody = inbodyData?.[0];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Dashboard</h2>

      <div className="space-y-4">
        {/* Calendar Placeholder */}
        <Card>
          <CardHeader>
            <CardTitle>Calendar Preview</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">Coming soon...</p>
          </CardContent>
        </Card>

        {/* Health Widgets */}
        <div className="grid grid-cols-2 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Sleep</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {healthSummary?.sleep_hours ? `${healthSummary.sleep_hours} hrs` : '-'}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Water</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {healthSummary?.water_cups ? `${healthSummary.water_cups} cups` : '-'}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Exercise</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {healthSummary?.exercise_minutes ? `${healthSummary.exercise_minutes} min` : '-'}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Sauna</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {healthSummary?.sauna?.duration_minutes ? `${healthSummary.sauna.duration_minutes} min` : '-'}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sleep Trends */}
        <SleepChart data={sleepData || []} days={7} />

        {/* Exercise Breakdown */}
        <ExerciseBreakdown data={exerciseData || []} days={30} />

        {/* InBody Latest */}
        {latestInBody && (
          <Card>
            <CardHeader>
              <CardTitle>Latest InBody</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Weight</p>
                  <p className="text-xl font-bold">{latestInBody.weight} lbs</p>
                </div>
                <div>
                  <p className="text-muted-foreground">SMM</p>
                  <p className="text-xl font-bold">{latestInBody.smm} lbs</p>
                </div>
                <div>
                  <p className="text-muted-foreground">PBF</p>
                  <p className="text-xl font-bold">{latestInBody.pbf}%</p>
                </div>
                <div>
                  <p className="text-muted-foreground">ECW/TBW</p>
                  <p className="text-xl font-bold">{latestInBody.ecw_tbw_ratio}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* InBody Trends Chart */}
        <InBodyChart data={inbodyData || []} />

        {/* Top Categories Placeholder */}
        <Card>
          <CardHeader>
            <CardTitle>Top Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">Coming soon...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
