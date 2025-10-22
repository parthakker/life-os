import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Droplet, Moon, Dumbbell, Scale } from 'lucide-react';
import { WeddingCountdown } from './WeddingCountdown';
import { WeatherWidget } from './WeatherWidget';
import { CalendarPreview } from './CalendarPreview';

export function StatsBar() {
  // Fetch health summary data
  const { data: healthSummary } = useQuery({
    queryKey: ['health', 'summary'],
    queryFn: () => api.getHealthSummary(),
  });

  // Fetch latest InBody data for weight
  const { data: inbodyData } = useQuery({
    queryKey: ['health', 'inbody'],
    queryFn: () => api.getInBodyData(),
  });

  const latestWeight = inbodyData?.[0]?.weight;

  return (
    <div className="grid grid-cols-8 gap-3 p-3 border-b bg-gradient-to-r from-background via-accent/5 to-background">
      {/* Water Intake */}
      <Card className="col-span-1 bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border-blue-500/20 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20 hover:-translate-y-1 hover:border-blue-500/40 cursor-pointer">
        <CardContent className="pt-4 pb-3">
          <div className="flex items-center gap-2 mb-2">
            <Droplet className="h-4 w-4 text-blue-500 transition-transform duration-300 hover:scale-110" />
            <span className="text-xs font-medium text-muted-foreground">Water</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-blue-600 dark:text-blue-400 transition-all duration-300">
              {healthSummary?.water_cups || 0}
            </span>
            <span className="text-xs text-muted-foreground">cups</span>
          </div>
        </CardContent>
      </Card>

      {/* Sleep */}
      <Card className="col-span-1 bg-gradient-to-br from-purple-500/10 to-indigo-500/10 border-purple-500/20 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/20 hover:-translate-y-1 hover:border-purple-500/40 cursor-pointer">
        <CardContent className="pt-4 pb-3">
          <div className="flex items-center gap-2 mb-2">
            <Moon className="h-4 w-4 text-purple-500 transition-transform duration-300 hover:scale-110" />
            <span className="text-xs font-medium text-muted-foreground">Sleep</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-purple-600 dark:text-purple-400 transition-all duration-300">
              {healthSummary?.sleep_hours || 0}
            </span>
            <span className="text-xs text-muted-foreground">hours</span>
          </div>
        </CardContent>
      </Card>

      {/* Exercise */}
      <Card className="col-span-1 bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-500/20 transition-all duration-300 hover:shadow-lg hover:shadow-green-500/20 hover:-translate-y-1 hover:border-green-500/40 cursor-pointer">
        <CardContent className="pt-4 pb-3">
          <div className="flex items-center gap-2 mb-2">
            <Dumbbell className="h-4 w-4 text-green-500 transition-transform duration-300 hover:scale-110" />
            <span className="text-xs font-medium text-muted-foreground">Exercise</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-green-600 dark:text-green-400 transition-all duration-300">
              {healthSummary?.exercise_minutes || 0}
            </span>
            <span className="text-xs text-muted-foreground">mins</span>
          </div>
        </CardContent>
      </Card>

      {/* Weight */}
      <Card className="col-span-1 bg-gradient-to-br from-orange-500/10 to-amber-500/10 border-orange-500/20 transition-all duration-300 hover:shadow-lg hover:shadow-orange-500/20 hover:-translate-y-1 hover:border-orange-500/40 cursor-pointer">
        <CardContent className="pt-4 pb-3">
          <div className="flex items-center gap-2 mb-2">
            <Scale className="h-4 w-4 text-orange-500 transition-transform duration-300 hover:scale-110" />
            <span className="text-xs font-medium text-muted-foreground">Weight</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-orange-600 dark:text-orange-400 transition-all duration-300">
              {latestWeight || '-'}
            </span>
            <span className="text-xs text-muted-foreground">lbs</span>
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
