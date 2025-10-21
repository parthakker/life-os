import { useState, useEffect, useRef } from 'react';
import { CategorySidebar } from './CategorySidebar';
import { TaskList } from './TaskList';
import { NotesList } from './NotesList';
import { DashboardPanel } from './DashboardPanel';

const MIN_SIDEBAR_WIDTH = 200;
const MAX_SIDEBAR_WIDTH = 500;
const DEFAULT_SIDEBAR_WIDTH = 256;

const MIN_DASHBOARD_WIDTH = 30; // Minimum 30% for dashboard panel
const DEFAULT_DASHBOARD_WIDTH = 40; // 40% dashboard

const MIN_SPLIT_WIDTH = 30; // Minimum 30% for either panel
const DEFAULT_SPLIT_POSITION = 50; // 50% tasks, 50% notes (in the right panel)

type Tab = 'home' | 'search' | 'calendar';

interface DashboardLayoutProps {
  currentTab: Tab;
}

export function DashboardLayout({ currentTab }: DashboardLayoutProps) {
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(null);
  const [sidebarWidth, setSidebarWidth] = useState(() => {
    const saved = localStorage.getItem('sidebarWidth');
    return saved ? parseInt(saved, 10) : DEFAULT_SIDEBAR_WIDTH;
  });
  const [dashboardWidth, setDashboardWidth] = useState(() => {
    const saved = localStorage.getItem('dashboardWidth');
    return saved ? parseInt(saved, 10) : DEFAULT_DASHBOARD_WIDTH;
  });
  const [splitPosition, setSplitPosition] = useState(() => {
    const saved = localStorage.getItem('splitPosition');
    return saved ? parseInt(saved, 10) : DEFAULT_SPLIT_POSITION;
  });
  const [isResizingSidebar, setIsResizingSidebar] = useState(false);
  const [isResizingDashboard, setIsResizingDashboard] = useState(false);
  const [isResizingSplit, setIsResizingSplit] = useState(false);
  const sidebarRef = useRef<HTMLDivElement>(null);
  const mainRef = useRef<HTMLDivElement>(null);
  const rightPanelRef = useRef<HTMLDivElement>(null);

  // Sidebar resize handler
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizingSidebar) return;

      const newWidth = e.clientX;
      if (newWidth >= MIN_SIDEBAR_WIDTH && newWidth <= MAX_SIDEBAR_WIDTH) {
        setSidebarWidth(newWidth);
        localStorage.setItem('sidebarWidth', newWidth.toString());
      }
    };

    const handleMouseUp = () => {
      setIsResizingSidebar(false);
    };

    if (isResizingSidebar) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isResizingSidebar]);

  // Dashboard resize handler
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizingDashboard || !mainRef.current) return;

      const mainRect = mainRef.current.getBoundingClientRect();
      const relativeX = e.clientX - mainRect.left;
      const percentage = (relativeX / mainRect.width) * 100;

      if (percentage >= MIN_DASHBOARD_WIDTH && percentage <= (100 - MIN_DASHBOARD_WIDTH)) {
        setDashboardWidth(percentage);
        localStorage.setItem('dashboardWidth', percentage.toString());
      }
    };

    const handleMouseUp = () => {
      setIsResizingDashboard(false);
    };

    if (isResizingDashboard) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isResizingDashboard]);

  // Split panel resize handler (for tasks/notes within right panel)
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizingSplit || !rightPanelRef.current) return;

      const panelRect = rightPanelRef.current.getBoundingClientRect();
      const relativeX = e.clientX - panelRect.left;
      const percentage = (relativeX / panelRect.width) * 100;

      if (percentage >= MIN_SPLIT_WIDTH && percentage <= (100 - MIN_SPLIT_WIDTH)) {
        setSplitPosition(percentage);
        localStorage.setItem('splitPosition', percentage.toString());
      }
    };

    const handleMouseUp = () => {
      setIsResizingSplit(false);
    };

    if (isResizingSplit) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isResizingSplit]);

  return (
    <div className="flex h-[calc(100vh-73px)]"> {/* 73px = header height */}
      {/* Sidebar */}
      <aside
        ref={sidebarRef}
        className="border-r bg-card flex-shrink-0 relative"
        style={{ width: `${sidebarWidth}px` }}
      >
        <CategorySidebar onCategorySelect={setSelectedCategoryId} />

        {/* Sidebar Resize Handle */}
        <div
          className="absolute top-0 right-0 w-1 h-full cursor-col-resize hover:bg-primary/20 transition-colors"
          onMouseDown={() => setIsResizingSidebar(true)}
        />
      </aside>

      {/* Main Content */}
      <main ref={mainRef} className="flex-1 overflow-hidden flex">
        {currentTab === 'home' ? (
          <>
            {/* Left Panel (Tasks + Notes) */}
            <div
              ref={rightPanelRef}
              className="flex-1 overflow-hidden flex"
            >
              {/* Tasks Panel */}
              <div
                className="overflow-y-auto border-r"
                style={{ width: `${splitPosition}%` }}
              >
                <div className="px-4 py-8">
                  <TaskList categoryId={selectedCategoryId} />
                </div>
              </div>

              {/* Split Resize Handle */}
              <div
                className="w-1 cursor-col-resize hover:bg-primary/20 transition-colors flex-shrink-0"
                onMouseDown={() => setIsResizingSplit(true)}
              />

              {/* Notes Panel */}
              <div
                className="overflow-y-auto"
                style={{ width: `${100 - splitPosition}%` }}
              >
                <div className="px-4 py-8">
                  <NotesList categoryId={selectedCategoryId} />
                </div>
              </div>
            </div>

            {/* Dashboard Resize Handle */}
            <div
              className="w-1 cursor-col-resize hover:bg-primary/20 transition-colors flex-shrink-0"
              onMouseDown={() => setIsResizingDashboard(true)}
            />

            {/* Dashboard Panel (Right) */}
            <div
              className="overflow-y-auto border-l"
              style={{ width: `${dashboardWidth}%` }}
            >
              <div className="px-4 py-8">
                <DashboardPanel />
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
