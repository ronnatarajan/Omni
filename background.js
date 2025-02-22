// Function to get Google OAuth token
function getGoogleOAuthToken() {
  chrome.identity.getAuthToken({ interactive: true }, function (token) {
      if (chrome.runtime.lastError) {
          console.error("Google OAuth failed:", chrome.runtime.lastError);
          return;
      }
      console.log("Google OAuth token:", token);

      // Store token in Chrome storage
      chrome.storage.local.set({ google_token: token }, function () {
          console.log("Stored Google Calendar token.");
      });
  });
}

// Function to capture a screenshot
function captureScreenshot() {
  chrome.tabs.captureVisibleTab(null, { format: "png" }, function (screenshotUrl) {
      if (chrome.runtime.lastError) {
          console.error("Screenshot capture failed:", chrome.runtime.lastError);
          return;
      }

      console.log("Screenshot captured:", screenshotUrl);

      // Open the cropper window with the screenshot
      chrome.windows.create({
          url: `cropper.html?image=${encodeURIComponent(screenshotUrl)}`,
          type: "popup",
          width: 800,
          height: 600
      });
  });
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "get_google_token") {
      getGoogleOAuthToken();
  }
  if (request.action === "capture_screen") {
      captureScreenshot();
  }
});
