document.addEventListener("DOMContentLoaded", function () {
  let screenshotDataUrl = null;

  // Capture Screenshot
  document.getElementById("capture").addEventListener("click", function () {
      chrome.runtime.sendMessage({ action: "take_screenshot" }, (response) => {
          if (response.screenshot) {
              screenshotDataUrl = response.screenshot;

              // Open the cropping window
              chrome.runtime.sendMessage({
                  action: "open_cropper",
                  image: screenshotDataUrl
              });

              // Close the popup
              window.close();
          }
      });
  });
});
