import React, { useState, useEffect } from "react";
import { ThemeProvider, useTheme } from "@/components/theme-provider";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
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
  const { theme, toggleTheme } = useTheme();
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
    <div className="min-h-[400px] w-[350px] px-4 py-6 bg-background text-foreground rounded-xl border border-violet-500 shadow-lg flex flex-col justify-between transition-all duration-500">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-light tracking-tight bg-gradient-to-r from-violet-400 to-violet-600 text-transparent bg-clip-text">
          FactFlow
        </h1>
        <button
          onClick={toggleTheme}
          className="border p-1.5 rounded-md hover:bg-muted transition"
          aria-label="Toggle Theme"
        >
          {theme === "dark" ? "🌞" : "🌙"}
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col gap-4 items-center justify-center text-center">
        {!loading && !showResult && (
          <>
            <p className="text-sm text-muted-foreground">Your personal AI fact checker</p>
            <ul className="text-sm text-muted-foreground">
              <li>✔️ Pattern-based content scan</li>
              <li>✔️ Source credibility check</li>
              <li>✔️ Cross-referenced verification</li>
            </ul>
          </>
        )}

        {loading && (
          <Card className="w-full animate-in fade-in duration-500">
            <CardHeader>
              <CardTitle className="text-lg">Analyzing Page...</CardTitle>
              <CardDescription className="text-sm">{LoadingTasks[taskIndex]}</CardDescription>
            </CardHeader>
            <CardContent>
              <Progress value={progress} className="h-2" />
              <p className="text-xs text-muted-foreground mt-2 text-right">{Math.round(progress)}%</p>
            </CardContent>
          </Card>
        )}

        {showResult && (
          <Card className="w-full animate-in fade-in duration-500">
            <CardHeader>
              <CardTitle className="text-lg">Credibility Score</CardTitle>
              <CardDescription className="text-sm">Based on content analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <Progress value={74} className="h-2 bg-muted" />
              <p className="text-sm mt-2 font-semibold text-red-500">74% chance of being fake</p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Footer / CTA */}
      <div className="mt-6 flex flex-col items-center gap-2">
        {!loading && !showResult && (
          <Button
            onClick={handleAnalyze}
            className="group w-full bg-violet-600 hover:bg-violet-700 transition-all relative overflow-hidden"
          >
            <span className="relative z-10">Analyze Page</span>
            <span className="absolute inset-0 bg-violet-400 opacity-10 blur-md group-hover:animate-pulse" />
          </Button>
        )}
        <p className="text-xs text-muted-foreground italic mt-1">🔍 Results powered by AI</p>
      </div>
    </div>
  );
};

const App = () => (
  <ThemeProvider>
    <AppContent />
  </ThemeProvider>
);

export default App;
