import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Heart } from 'lucide-react';

const WEDDING_DATE = new Date('2026-05-03T00:00:00');

export function WeddingCountdown() {
  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());

  function calculateTimeLeft() {
    const now = new Date();
    const diff = WEDDING_DATE.getTime() - now.getTime();

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    return { days, hours, minutes };
  }

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft());
    }, 60000); // Update every minute

    return () => clearInterval(timer);
  }, []);

  return (
    <Card className="bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-rose-500/10 border-pink-500/20">
      <CardContent className="pt-4 pb-3">
        <div className="flex items-center gap-2 mb-2">
          <Heart className="h-4 w-4 text-pink-500 fill-pink-500" />
          <span className="text-xs font-medium text-muted-foreground">Wedding Countdown</span>
        </div>
        <div className="flex flex-col">
          <span className="text-3xl font-bold bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent">
            {timeLeft.days}
          </span>
          <span className="text-xs text-muted-foreground mt-0.5">
            days to go!
          </span>
        </div>
        <div className="text-xs text-muted-foreground mt-1">
          May 3, 2026
        </div>
      </CardContent>
    </Card>
  );
}
