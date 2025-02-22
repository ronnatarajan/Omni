document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("googleSignIn").addEventListener("click", function () {
      chrome.runtime.sendMessage({ action: "get_google_token" });
  });

  document.getElementById("captureScreen").addEventListener("click", function () {
      chrome.runtime.sendMessage({ action: "capture_screen" });
  });
});
