chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "sign_in") {
      chrome.identity.getAuthToken({ interactive: true }, (token) => {
          if (chrome.runtime.lastError) {
              console.error("OAuth Error:", chrome.runtime.lastError);
              sendResponse({ success: false, error: chrome.runtime.lastError });
              return;
          }
          // Store OAuth token
          chrome.storage.local.set({ googleToken: token }, () => {
              console.log("Google OAuth Token stored:", token);
              sendResponse({ success: true, token });
          });
      });
      return true;
  }

  if (request.action === "capture_screen") {
      chrome.tabs.captureVisibleTab(null, { format: "png" }, (imageUri) => {
          if (chrome.runtime.lastError) {
              console.error("Capture failed:", chrome.runtime.lastError);
              sendResponse({ success: false });
              return;
          }
          chrome.storage.local.set({ capturedImage: imageUri }, () => {
              console.log("Screenshot saved to storage.");
              sendResponse({ success: true });
          });
      });
      return true;
  }
});
