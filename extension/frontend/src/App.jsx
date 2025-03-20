// extension/frontend/src/App.jsx
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [scrapedText, setScrapedText] = useState("");
  const [result, setResult] = useState(null);

  // Function to trigger web scraping on the active tab
  const getScrapedText = () => {
    // This uses Chrome's scripting API to execute a function in the context of the active tab.
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript(
        {
          target: { tabId: tabs[0].id },
          // This function is injected into the active page to extract its visible text.
          func: () => {
            // You can improve this function to target specific elements.
            return document.body.innerText;
          },
        },
        (injectionResults) => {
          if (injectionResults && injectionResults.length > 0) {
            setScrapedText(injectionResults[0].result);
          }
        }
      );
    });
  };

  // Function to send the scraped text to your backend for analysis
  const analyzeText = async () => {
    try {
      // Replace with your actual backend URL and endpoint.
      const response = await axios.post("http://localhost:5000/api/analyze", { text: scrapedText });
      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing text", error);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>FactFlow Fake News Detector</h1>
      <button onClick={getScrapedText}>Scrape Current Page</button>
      <textarea
        value={scrapedText}
        onChange={(e) => setScrapedText(e.target.value)}
        placeholder="Scraped text will appear here..."
        style={{ width: "100%", height: "150px", marginTop: "10px" }}
      />
      <button onClick={analyzeText} style={{ marginTop: "10px" }}>
        Analyze Text
      </button>
      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Analysis Result</h2>
          <p>Fake Probability: {result.fake_probability}</p>
          <p>Real Probability: {result.real_probability}</p>
        </div>
      )}
    </div>
  );
}

export default App;
