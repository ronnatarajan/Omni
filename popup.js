document.getElementById("sign-in").addEventListener("click", function () {
  chrome.runtime.sendMessage({ action: "sign_in" }, (response) => {
      if (response && response.success) {
          console.log("Signed in successfully. Token:", response.token);
          alert("Signed in successfully!");
      } else {
          console.error("Sign-in failed.");
      }
  });
});

document.getElementById("capture-button").addEventListener("click", function () {
  chrome.runtime.sendMessage({ action: "capture_screen" }, (response) => {
      if (response && response.success) {
          console.log("Screenshot captured successfully.");
          window.open("cropper.html", "_blank", "width=800,height=600");
      } else {
          console.error("Failed to capture screenshot.");
      }
  });
});
