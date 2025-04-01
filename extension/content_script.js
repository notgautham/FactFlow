// content_script.js

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "SCRAPE_TEXT") {
    try {
      // Clone document for readability
      const articleDoc = document.cloneNode(true);
      const reader = new Readability(articleDoc);
      const article = reader.parse();

      // Extract title and content
      const title = article?.title || document.title;
      const content = article?.content || "";

      // Strip HTML tags
      const tempElement = document.createElement("div");
      tempElement.innerHTML = content;
      const plainText = tempElement.innerText.trim();

      // Clean domain URL
      const fullUrl = window.location.href;
      const urlObj = new URL(fullUrl);
      const hostname = urlObj.hostname.replace(/^www\./, "");
      const cleanedUrl = hostname;

      // 🗓️ Attempt to extract publish date from meta tags or page
      let publishDate = "";

      const metaTags = [
        'meta[property="article:published_time"]',
        'meta[name="pubdate"]',
        'meta[name="publish-date"]',
        'meta[name="date"]',
        'meta[itemprop="datePublished"]',
      ];

      for (const selector of metaTags) {
        const tag = document.querySelector(selector);
        if (tag?.content) {
          publishDate = tag.content;
          break;
        }
      }

      // Fallback to regex
      if (!publishDate) {
        const bodyText = document.body.innerText;
        const dateMatch = bodyText.match(
          /\b(?:\d{1,2}[\/\-th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,\-]*(?:\d{1,2}[,\s]*)?\d{4}\b/i
        );
        if (dateMatch) {
          publishDate = dateMatch[0];
        }
      }

      // Final fallback
      publishDate = publishDate || "Not found";

      // Prepend date to content text block
      const formattedText = `[📅 Published On: ${publishDate}]\n\n${plainText}`;

      sendResponse({
        scrapedText: `${title}\n\n${formattedText}`,
        domain: cleanedUrl,
        publishDate: publishDate,
      });

      // ✅ Logging for debug
      console.log("[FactFlow] Title:", title);
      console.log("[FactFlow] Cleaned Content:", formattedText.slice(0, 200));
      console.log("[FactFlow] Domain URL:", cleanedUrl);
      console.log("[FactFlow] Publish Date:", publishDate);

    } catch (error) {
      console.error("Readability failed:", error);
      sendResponse({ scrapedText: "", domain: "", publishDate: "" });
    }

    return true; // enable async sendResponse
  }
});
