import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Cloud, CloudRain, CloudSnow, Sun, Wind, Loader2 } from 'lucide-react';

const API_KEY = '5dd9f6966bc21ea6f112dd6b69dc3e6d';
const CITY = 'Lawrenceville,NJ,US';

interface HourlyWeather {
  time: string;
  temp: number;
  condition: string;
  icon: string;
}

export function WeatherWidget() {
  const [hourlyWeather, setHourlyWeather] = useState<HourlyWeather[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetchWeather();
    // Refresh every 30 minutes
    const interval = setInterval(fetchWeather, 30 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  async function fetchWeather() {
    try {
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/forecast?q=${CITY}&appid=${API_KEY}&units=imperial`
      );

      if (!response.ok) throw new Error('Weather fetch failed');

      const data = await response.json();

      // Get next 6 forecast periods (18 hours with 3-hour intervals)
      const forecasts = data.list.slice(0, 6).map((item: any) => {
        const date = new Date(item.dt * 1000);
        const hours = date.getHours();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        const displayHour = hours % 12 || 12;

        return {
          time: `${displayHour}${ampm}`,
          temp: Math.round(item.main.temp),
          condition: item.weather[0].main,
          icon: item.weather[0].icon,
        };
      });

      setHourlyWeather(forecasts);
      setLoading(false);
      setError(false);
    } catch (err) {
      console.error('Weather fetch error:', err);
      setError(true);
      setLoading(false);
    }
  }

  function getWeatherIcon(condition: string) {
    switch (condition.toLowerCase()) {
      case 'clear':
        return <Sun className="h-6 w-6 text-yellow-500" />;
      case 'clouds':
        return <Cloud className="h-6 w-6 text-gray-400" />;
      case 'rain':
      case 'drizzle':
        return <CloudRain className="h-6 w-6 text-blue-400" />;
      case 'snow':
        return <CloudSnow className="h-6 w-6 text-blue-200" />;
      default:
        return <Wind className="h-6 w-6 text-gray-400" />;
    }
  }

  return (
    <Card className="bg-gradient-to-br from-sky-500/10 to-blue-500/10 border-sky-500/20">
      <CardContent className="pt-3 pb-3 px-2">
        {loading ? (
          <div className="flex items-center justify-center gap-2 py-2">
            <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
            <span className="text-xs text-muted-foreground">Loading...</span>
          </div>
        ) : error ? (
          <div className="text-xs text-muted-foreground text-center py-2">
            Weather unavailable
          </div>
        ) : (
          <div className="space-y-2">
            {/* Header */}
            <div className="flex items-center justify-between px-2">
              <span className="text-xs font-medium text-muted-foreground">
                Lawrenceville, NJ
              </span>
              <span className="text-xs text-muted-foreground">Next 18hrs</span>
            </div>

            {/* Horizontal Scroll of Hourly Forecasts */}
            <div className="flex gap-2 overflow-x-auto scrollbar-hide">
              {hourlyWeather.map((forecast, idx) => (
                <div
                  key={idx}
                  className="flex flex-col items-center gap-1 min-w-[60px] p-2 rounded-lg bg-background/50 border border-sky-500/10 transition-all duration-300 hover:bg-sky-500/10 hover:border-sky-500/30 hover:scale-105 hover:shadow-md cursor-pointer"
                  style={{ animationDelay: `${idx * 50}ms` }}
                >
                  <span className="text-xs font-medium text-muted-foreground">
                    {forecast.time}
                  </span>
                  {getWeatherIcon(forecast.condition)}
                  <span className="text-sm font-bold">{forecast.temp}°</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
