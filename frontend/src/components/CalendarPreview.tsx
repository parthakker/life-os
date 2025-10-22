import { useState } from 'react';
import Calendar from 'react-calendar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Calendar as CalendarIcon } from 'lucide-react';
import 'react-calendar/dist/Calendar.css';
import './CalendarPreview.css';

export function CalendarPreview() {
  const [value, setValue] = useState(new Date());

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-center gap-2">
          <CalendarIcon className="h-4 w-4 text-primary" />
          <CardTitle className="text-sm font-medium">Calendar</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="calendar-preview-container">
          <Calendar
            onChange={(date) => setValue(date as Date)}
            value={value}
            locale="en-US"
            minDetail="month"
            prev2Label={null}
            next2Label={null}
            showNeighboringMonth={false}
          />
        </div>
      </CardContent>
    </Card>
  );
}
