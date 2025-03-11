// background.js
// Handles background tasks for the browser extension.

chrome.runtime.onInstalled.addListener(() => {
    console.log("Fake News Detector extension installed.");
});
