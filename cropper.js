let cropper;

document.addEventListener("DOMContentLoaded", function () {
    let imageElement = document.getElementById("image-to-crop");

    chrome.storage.local.get(["capturedImage", "googleToken"], function (result) {
        if (result.capturedImage) {
            console.log("Image retrieved from storage.");
            loadImageAndResize(result.capturedImage);
        } else {
            console.error("No image found in storage.");
        }

        window.googleToken = result.googleToken || null;
    });

    document.getElementById("crop-button").addEventListener("click", function () {
        let croppedCanvas = cropper.getCroppedCanvas();
        if (!croppedCanvas) {
            console.error("Cropping failed.");
            return;
        }

        let croppedImageDataURL = croppedCanvas.toDataURL("image/png");

        if (!window.googleToken) {
            console.error("Google OAuth token not found.");
            alert("You need to sign in with Google first!");
            return;
        }

        fetch("http://127.0.0.1:5000/upload_image", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                image: croppedImageDataURL
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data);
            alert("Image and token sent successfully!");
            window.close();
        })
        .catch(error => {
            console.error("Error sending image:", error);
            alert("Failed to send image.");
        });
    });
});

// ✅ Resize Image to Fit Window Before Initializing Cropper
function loadImageAndResize(imageSrc) {
    let imageElement = document.getElementById("image-to-crop");
    let tempImg = new Image();
    tempImg.src = imageSrc;

    tempImg.onload = function () {
        // Get the actual image dimensions
        let originalWidth = tempImg.width;
        let originalHeight = tempImg.height;

        // Get window dimensions
        let maxWidth = window.innerWidth * 0.8; // 80% of window width
        let maxHeight = window.innerHeight * 0.8; // 80% of window height

        // Calculate scaling ratio to fit inside window
        let scale = Math.min(maxWidth / originalWidth, maxHeight / originalHeight);

        imageElement.width = originalWidth * scale;
        imageElement.height = originalHeight * scale;
        imageElement.src = imageSrc;

        // Initialize Cropper **AFTER** the image is loaded & resized
        cropper = new Cropper(imageElement, {
            viewMode: 2, // Ensures it fits within container
            autoCropArea: 1,
            movable: true,
            zoomable: false, // Disable zoom
            rotatable: true,
            scalable: true
        });
    };
}
