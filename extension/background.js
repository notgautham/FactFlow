chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "scrape") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.scripting.executeScript(
          {
            target: { tabId: tabs[0].id },
            func: () => {
              return document.body.innerText || "";
            },
          },
          (results) => {
            if (chrome.runtime.lastError || !results || !results[0]) {
              console.error("Scraping failed:", chrome.runtime.lastError);
              sendResponse({ success: false });
              return;
            }
            sendResponse({ success: true, data: results[0].result });
          }
        );
      }
    });
    return true; // Important: Keeps sendResponse alive
  }
});
