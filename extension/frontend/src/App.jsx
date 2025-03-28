import React, { useState, useEffect } from "react";
//import { ThemeProvider, useTheme } from "@/components/theme-provider";
import CircularProgress from "@/components/ui/circular-progress";
import { ThemeProvider } from "@/components/theme-provider";
import { useTheme } from "next-themes";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import "@/App.css";

const LoadingTasks = [
  "Scraping visible webpage content...",
  "Analyzing sentence structure...",
  "Detecting bias indicators...",
  "Checking headline exaggeration...",
  "Cross-referencing factual claims...",
  "Calculating credibility score...",
];

const AppContent = () => {
  const { theme, setTheme } = useTheme();
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [taskIndex, setTaskIndex] = useState(0);
  const [showResult, setShowResult] = useState(false);
  

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setProgress((prev) => {
          const next = Math.min(prev + Math.random() * 20, 100);
          if (next >= 100) {
            clearInterval(interval);
            setTimeout(() => {
              setLoading(false);
              setShowResult(true);
            }, 500);
          }
          return next;
        });
        setTaskIndex((prev) => (prev + 1) % LoadingTasks.length);
      }, 800);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleAnalyze = () => {
    setProgress(0);
    setTaskIndex(0);
    setShowResult(false);
    setLoading(true);
  };

  return (
    <div className="min-h-[400px] w-[300px] px-3 py-3 bg-background text-foreground rounded-xl border border-violet-500 shadow-lg flex flex-col justify-between transition-all duration-500 mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 px-1">
        <h1 className="text-[30px] font-semibold tracking-tight bg-gradient-to-r from-violet-400 to-violet-600 text-transparent bg-clip-text transition-all hover:scale-110 hover:brightness-125">
          FactFlow
        </h1>
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="border p-1.5 rounded-md hover:bg-muted transition"
          aria-label="Toggle Theme"
        >
          {theme === "dark" ? "🌞" : "🌙"}
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col gap-4 items-center justify-center text-center px-2">
        {!loading && !showResult && (
          <>
            <p className="text-base font-medium text-muted-foreground hover:text-violet-400 transition">
              Your personal AI fact checker
            </p>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li className="transition hover:text-violet-400">
                ✔️ Pattern-based content scan
              </li>
              <li className="transition hover:text-violet-400">
                ✔️ Source credibility check
              </li>
              <li className="transition hover:text-violet-400">
                ✔️ Cross-referenced verification
              </li>
            </ul>
          </>
        )}

        {loading && (
          <div className="w-full animate-in fade-in duration-500 px-1">
            <CardHeader>
              <CardTitle className="text-lg">Analyzing Page...</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center justify-center space-y-2 mt-2">
              <CircularProgress progress={progress} />
              <p className="text-xs text-muted-foreground mt-2">
                {LoadingTasks[taskIndex]}
              </p>
            </CardContent>
          </div>
        )}

        {showResult && (
          <Card className="w-full animate-in fade-in duration-500 px-1">
            <CardHeader>
              <CardTitle className="text-lg">Credibility Score</CardTitle>
              <CardDescription className="text-sm">
                Based on content analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-2 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-2 bg-red-500 rounded-full transition-all"
                  style={{ width: "74%" }}
                />
              </div>
              <p className="text-sm mt-2 font-semibold text-red-500">
                74% chance of being fake
              </p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Footer / CTA */}
      <div className="mt-6 flex flex-col items-center gap-2 px-1">
        {!loading && !showResult && (
          <Button
            onClick={handleAnalyze}
            className="group w-[90%] bg-violet-600 hover:bg-violet-700 transition-all relative overflow-hidden"
          >
            <span className="relative z-10">Analyze Page</span>
            <span className="absolute inset-0 bg-violet-300 opacity-0 group-hover:opacity-20 blur-md transition-all duration-500" />
          </Button>
        )}
        <p className="text-xs text-muted-foreground italic mt-1">
          🔍 Results powered by AI
        </p>
      </div>
    </div>
  );
};

const App = () => (
  <ThemeProvider defaultTheme="dark">
    <AppContent />
  </ThemeProvider>
);

export default App;
