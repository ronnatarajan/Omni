let cropper;

document.addEventListener("DOMContentLoaded", function () {
    const imageElement = document.getElementById("cropImage");

    // Get the image URL from query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const imageUrl = urlParams.get("image");

    if (imageUrl) {
        imageElement.src = imageUrl;

        // Wait for the image to load before initializing Cropper.js
        imageElement.onload = function () {
            cropper = new Cropper(imageElement, {
                aspectRatio: 0, 
                viewMode: 2, 
                autoCropArea: 1,
                scalable: false, 
                zoomable: true,
                movable: false,
                background: false
            });
        };
    }

    // Confirm crop and send the image to API
    document.getElementById("confirmCrop").addEventListener("click", function () {
        if (cropper) {
            const croppedCanvas = cropper.getCroppedCanvas();
            if (croppedCanvas) {
                const croppedDataUrl = croppedCanvas.toDataURL("image/png");

                // Send image to API via background script
                chrome.runtime.sendMessage({
                    action: "send_to_api",
                    croppedImage: croppedDataUrl
                });

                // Close the cropping window
                window.close();
            }
        }
    });

    // Cancel cropping and close only the cropping window
    document.getElementById("cancelCrop").addEventListener("click", function () {
        window.close();
    });
});
