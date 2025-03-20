chrome.runtime.onInstalled.addListener(() => {
  console.log("FactFlow Extension Installed");
});

chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content_script.js"]
  });
});
