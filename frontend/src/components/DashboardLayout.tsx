import { useState } from 'react';
import { CategorySidebar } from './CategorySidebar';
import { TaskList } from './TaskList';
import { NotesList } from './NotesList';
import { HealthVisualsPanel } from './HealthVisualsPanel';

type Tab = 'home' | 'search' | 'calendar';

interface DashboardLayoutProps {
  currentTab: Tab;
}

export function DashboardLayout({ currentTab }: DashboardLayoutProps) {
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(null);
  const [selectedCategoryName, setSelectedCategoryName] = useState<string | null>(null);

  const handleCategorySelect = (categoryId: number | null, categoryName: string | null) => {
    setSelectedCategoryId(categoryId);
    setSelectedCategoryName(categoryName);
  };

  const categoryDisplayName = selectedCategoryName || 'All';

  return (
    <div className="flex h-[calc(100vh-57px)]"> {/* 57px = header height */}
      {/* Category Sidebar - Fixed width */}
      <aside className="w-[280px] border-r bg-card flex-shrink-0">
        <CategorySidebar onCategorySelect={handleCategorySelect} />
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex overflow-hidden">
        {currentTab === 'home' ? (
          <>
            {/* Left Column: Tasks and Notes */}
            <div className="flex-1 flex flex-col overflow-hidden border-r">
              {/* Category Context Header */}
              <div className="border-b bg-muted/30 px-4 py-2">
                <p className="text-sm text-muted-foreground">
                  Viewing: <span className="font-semibold text-foreground">{categoryDisplayName}</span>
                </p>
              </div>

              {/* Tasks and Notes Stacked */}
              <div className="flex-1 flex flex-col overflow-hidden">
                {/* Tasks Panel - Top Half */}
                <div className="flex-1 overflow-y-auto border-b">
                  <div className="px-4 py-3">
                    <TaskList categoryId={selectedCategoryId} />
                  </div>
                </div>

                {/* Notes Panel - Bottom Half */}
                <div className="flex-1 overflow-y-auto">
                  <div className="px-4 py-3">
                    <NotesList categoryId={selectedCategoryId} />
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column: Health Visuals */}
            <div className="flex-1 overflow-hidden">
              <HealthVisualsPanel />
            </div>
          </>
        ) : currentTab === 'search' ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center text-muted-foreground">
              <p className="text-2xl font-bold mb-2">Search</p>
              <p>Coming soon...</p>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center text-muted-foreground">
              <p className="text-2xl font-bold mb-2">Calendar</p>
              <p>Coming soon...</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
