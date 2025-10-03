const uploadBox = document.getElementById("uploadBox");
const csvFileInput = document.getElementById("csvFile");

// Show loading state
function showLoading(isLoading) {
  if (isLoading) {
    uploadBox.classList.add("loading");
    uploadBox.textContent = "⏳ Uploading CSV...";
  } else {
    uploadBox.classList.remove("loading");
  }
}

// Upload file to backend
async function uploadFile(file) {
  showLoading(true);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/upload/csv", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    if (response.ok && data.data.url) {
      // Set hidden input
      document.getElementById("csvUrl").value = data.data.url;

      // Change label to uploaded file
      uploadBox.textContent = `✅ ${file.name} uploaded`;

      // Enable submit button
      if (typeof window.enableDraftSubmit === "function") {
        window.enableDraftSubmit();
      }
    } else {
      uploadBox.textContent = "❌ Upload failed! Try again";
    }
  } catch (err) {
    uploadBox.textContent = "⚠️ Upload error!";
  } finally {
    showLoading(false);
  }
}

// File picker
uploadBox.addEventListener("click", () => csvFileInput.click());
csvFileInput.addEventListener("change", () => {
  const file = csvFileInput.files[0];
  if (file) uploadFile(file);
});

// Drag & drop
uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.classList.add("dragover");
});
uploadBox.addEventListener("dragleave", () => uploadBox.classList.remove("dragover"));
uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadBox.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  if (file) uploadFile(file);
});
