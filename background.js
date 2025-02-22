let cropperWindowId = null; // Store the cropping window ID

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "take_screenshot") {
        chrome.tabs.captureVisibleTab(null, { format: "png" }, (dataUrl) => {
            sendResponse({ screenshot: dataUrl });
        });
        return true;
    }

    if (request.action === "open_cropper") {
        chrome.windows.create({
            url: `cropper.html?image=${encodeURIComponent(request.image)}`,
            type: "popup",
            width: 1000,
            height: 800
        }, function (window) {
            cropperWindowId = window.id; // Store cropping window ID
        });
    }

    if (request.action === "send_to_api") {
        fetch("https://your-api-endpoint.com/process-image", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: request.croppedImage })
        })
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data);
            sendResponse({ success: true });
        })
        .catch(error => {
            console.error("API Error:", error);
            sendResponse({ success: false, error: error });
        });

        if (cropperWindowId) {
            // Check if the window still exists before removing it
            chrome.windows.get(cropperWindowId, function (window) {
                if (chrome.runtime.lastError) {
                    console.warn("Cropping window was already closed.");
                } else {
                    chrome.windows.remove(cropperWindowId, () => {
                        cropperWindowId = null;
                    });
                }
            });
        }

        return true; // Keeps the async response alive
    }
});
