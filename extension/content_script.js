// content_script.js

function extractVisibleText() {
  const bodyText = document.body.innerText;
  return bodyText;
}

// Listen for messages from background/popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "SCRAPE_TEXT") {
    const text = extractVisibleText();
    sendResponse({ scrapedText: text });
  }
});

console.log("✅ FactFlow content script loaded.");

