window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const imageUrl = params.get("image");

  const image = document.getElementById("imageToCrop");
  image.src = decodeURIComponent(imageUrl);

  // Wait for the image to load before initializing Cropper
  image.onload = function () {
      const cropper = new Cropper(image, {
          aspectRatio: 0,
          viewMode: 2, // Ensure the whole image fits in the window
          autoCropArea: 1, // Ensure the default crop area is large
          responsive: true,
          background: false,
          scalable: false, 
          zoomable: true,
          movable: false
      });
  };

  document.getElementById("confirmCrop").addEventListener("click", () => {
      const croppedCanvas = cropper.getCroppedCanvas();
      const croppedImage = croppedCanvas.toDataURL("image/png").split(",")[1]; // Remove Base64 prefix

      // Retrieve stored Google OAuth token
      chrome.storage.local.get(["google_token"], function (data) {
          if (!data.google_token) {
              console.error("No Google OAuth token found.");
              return;
          }

          fetch("http://127.0.0.1:5000/upload_image", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                  image: croppedImage,
                  token: data.google_token
              })
          })
          .then(response => response.json())
          .then(data => console.log("API Response:", data))
          .catch(error => console.error("API Error:", error));

          window.close();
      });
  });
});
