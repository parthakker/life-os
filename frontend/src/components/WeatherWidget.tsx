import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Cloud, CloudRain, CloudSnow, Sun, Wind, Loader2 } from 'lucide-react';

const API_KEY = '5dd9f6966bc21ea6f112dd6b69dc3e6d';
const CITY = 'New York'; // Default city - can be made configurable

interface WeatherData {
  temp: number;
  condition: string;
  description: string;
  icon: string;
}

export function WeatherWidget() {
  const [weather, setWeather] = useState<WeatherData | null>(null);
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
        `https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}&units=imperial`
      );

      if (!response.ok) throw new Error('Weather fetch failed');

      const data = await response.json();
      setWeather({
        temp: Math.round(data.main.temp),
        condition: data.weather[0].main,
        description: data.weather[0].description,
        icon: data.weather[0].icon,
      });
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
      <CardContent className="pt-4 pb-3">
        <div className="flex items-center justify-between">
          {loading ? (
            <div className="flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
              <span className="text-xs text-muted-foreground">Loading...</span>
            </div>
          ) : error ? (
            <div className="text-xs text-muted-foreground">Weather unavailable</div>
          ) : weather ? (
            <>
              <div className="flex flex-col">
                <span className="text-3xl font-bold">{weather.temp}°</span>
                <span className="text-xs text-muted-foreground capitalize">
                  {weather.description}
                </span>
              </div>
              <div className="flex flex-col items-end gap-1">
                {getWeatherIcon(weather.condition)}
                <span className="text-xs text-muted-foreground">{CITY}</span>
              </div>
            </>
          ) : null}
        </div>
      </CardContent>
    </Card>
  );
}
