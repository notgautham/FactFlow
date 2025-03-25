import React, { useEffect, useState } from "react";
import { ThemeProvider } from "@/components/theme-provider";
import { useTheme } from "next-themes";
import { SunIcon, MoonIcon } from "@radix-ui/react-icons";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import "@/App.css"; // Inter font imported here

const AppContent = () => {
  const { theme, setTheme } = useTheme();
  const [isDarkMode, setIsDarkMode] = useState(theme === "dark");
  const [fakeProbability, setFakeProbability] = useState(74); // test value

  useEffect(() => {
    setTheme(isDarkMode ? "dark" : "light");
  }, [isDarkMode, setTheme]);

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-background text-foreground font-sans">
      <div className="w-[350px] rounded-xl border border-violet-500 shadow-md p-4 bg-card space-y-4">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-pink-500 text-xl">🧠</span>
            <h1 className="text-transparent bg-gradient-to-r from-violet-400 to-violet-600 bg-clip-text text-xl font-light tracking-wide">
              FactFlow
            </h1>
          </div>
          <Button
            variant="outline"
            size="icon"
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="border-muted"
          >
            {isDarkMode ? <SunIcon /> : <MoonIcon />}
          </Button>
        </div>

        <p className="text-muted-foreground text-sm text-left">
          AI-powered fake news detection
        </p>

        {/* Score Card */}
        <Card className="bg-muted/50">
          <CardHeader>
            <CardTitle className="text-lg text-center">Credibility Score</CardTitle>
            <CardDescription className="text-center text-xs">
              Fake Probability Based on Content
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <Progress value={fakeProbability} />
            <p className="text-sm text-center">{fakeProbability}% chance of being fake</p>
          </CardContent>
        </Card>

        <p className="text-sm text-muted-foreground text-center">
          Scanning the current page for deceptive or misleading content patterns.
        </p>

        <Button className="w-full" disabled>
          Analyze Page
        </Button>

        <p className="text-[10px] text-muted-foreground text-center">
          🧠 Results powered by AI
        </p>
      </div>
    </div>
  );
};

const App = () => {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      <AppContent />
    </ThemeProvider>
  );
};

export default App;
