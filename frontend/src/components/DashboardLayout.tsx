import { useState } from 'react';
import { CategorySidebar } from './CategorySidebar';
import { TaskList } from './TaskList';
import { NotesList } from './NotesList';
import { StatsBar } from './StatsBar';

type Tab = 'home' | 'search' | 'calendar';

interface DashboardLayoutProps {
  currentTab: Tab;
}

export function DashboardLayout({ currentTab }: DashboardLayoutProps) {
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(null);

  return (
    <div className="flex h-[calc(100vh-57px)]"> {/* 57px = header height */}
      {/* Category Sidebar - Fixed width */}
      <aside className="w-[280px] border-r bg-card flex-shrink-0">
        <CategorySidebar onCategorySelect={setSelectedCategoryId} />
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {currentTab === 'home' ? (
          <>
            {/* Stats Bar - Horizontal across top */}
            <StatsBar categoryId={selectedCategoryId} />

            {/* Tasks and Notes Grid */}
            <div className="flex-1 grid grid-cols-2 gap-px bg-border overflow-hidden">
              {/* Tasks Panel */}
              <div className="bg-background overflow-y-auto">
                <div className="px-4 py-3">
                  <TaskList categoryId={selectedCategoryId} />
                </div>
              </div>

              {/* Notes Panel */}
              <div className="bg-background overflow-y-auto">
                <div className="px-4 py-3">
                  <NotesList categoryId={selectedCategoryId} />
                </div>
              </div>
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
