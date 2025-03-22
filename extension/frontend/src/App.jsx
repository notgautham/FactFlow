import React, { useEffect, useState } from "react";
import { ThemeProvider } from "next-themes";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";

const AppContent = () => {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // To avoid hydration mismatch error
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="w-[400px] min-h-[400px] p-4 bg-background text-foreground">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h1 className="text-xl font-bold">🧠 FactFlow</h1>
          <p className="text-sm text-muted-foreground">
            AI-powered fake news detection
          </p>
        </div>
        <Button
          variant="outline"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {theme === "dark" ? "☀ Light" : "🌙 Dark"}
        </Button>
      </div>

      {/* Content placeholder for the rest of the extension UI */}
      <div className="mt-4">
        <p className="text-xs">🔗 Sample content will go here.</p>
        <Button className="mt-2">Analyze Page</Button>
      </div>
    </div>
  );
};

// Root wraps AppContent with ThemeProvider
const App = () => {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <AppContent />
    </ThemeProvider>
  );
};

export default App;
