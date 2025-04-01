// content_script.js

// Listen for message from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "SCRAPE_TEXT") {
    try {
      // Clone the document for processing
      const articleDoc = document.cloneNode(true);
      const reader = new Readability(articleDoc);
      const article = reader.parse();

      // Extract title and content
      const title = article?.title || document.title;
      const content = article?.content || "";

      // Strip HTML tags from content
      const tempElement = document.createElement("div");
      tempElement.innerHTML = content;
      const plainText = tempElement.innerText.trim();

      // ✅ Clean the domain URL
      const fullUrl = window.location.href;
      const urlObj = new URL(fullUrl);
      const hostname = urlObj.hostname.replace(/^www\./, ""); // removes 'www.'
      const cleanedUrl = hostname; // final result: 'livemint.com'

      console.log("[FactFlow] Title:", title);
      console.log("[FactFlow] Cleaned Content:", plainText.slice(0, 3000));
      console.log("[FactFlow] Domain URL:", cleanedUrl);

      // Send response back to popup
      sendResponse({
        scrapedText: `${title}\n\n${plainText}`,
        domain: cleanedUrl,
      });
    } catch (error) {
      console.error("Readability failed:", error);
      sendResponse({ scrapedText: "", domain: "" });
    }

    // Indicate async response
    return true;
  }
});
