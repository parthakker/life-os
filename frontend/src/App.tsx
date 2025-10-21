import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DashboardLayout } from './components/DashboardLayout';
import { ThemeProvider } from './components/ThemeProvider';
import { ThemeToggle } from './components/ThemeToggle';
import { cn } from './lib/utils';
import './App.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

type Tab = 'home' | 'search' | 'calendar';

function App() {
  const [currentTab, setCurrentTab] = useState<Tab>('home');

  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      <QueryClientProvider client={queryClient}>
        <div className="min-h-screen bg-background text-foreground">
          {/* Header */}
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold">Life OS</h1>
                <div className="flex items-center gap-4">
                  <nav className="flex gap-4">
                    <button
                      onClick={() => setCurrentTab('home')}
                      className={cn(
                        "text-sm font-medium transition-colors",
                        currentTab === 'home'
                          ? "text-primary"
                          : "text-muted-foreground hover:text-primary"
                      )}
                    >
                      Home
                    </button>
                    <button
                      onClick={() => setCurrentTab('search')}
                      className={cn(
                        "text-sm font-medium transition-colors",
                        currentTab === 'search'
                          ? "text-primary"
                          : "text-muted-foreground hover:text-primary"
                      )}
                    >
                      Search
                    </button>
                    <button
                      onClick={() => setCurrentTab('calendar')}
                      className={cn(
                        "text-sm font-medium transition-colors",
                        currentTab === 'calendar'
                          ? "text-primary"
                          : "text-muted-foreground hover:text-primary"
                      )}
                    >
                      Calendar
                    </button>
                  </nav>
                  <ThemeToggle />
                </div>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <DashboardLayout currentTab={currentTab} />
        </div>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

export default App;
