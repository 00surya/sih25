function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return match[2];
}

const draftModal = document.getElementById("draftModal");
const submitBtn = document.getElementById("submitDraftBtn");
const csvUrlField = document.getElementById("csvUrl");
const csrfToken = getCookie('csrf_access_token');

// Modal open/close
document.getElementById("openDraftModal").onclick = () => draftModal.style.display = "flex";
document.getElementById("closeDraftModal").onclick = () => closeModal();
document.getElementById("cancelDraft").onclick = () => closeModal();
window.onclick = (e) => { if (e.target === draftModal) closeModal(); };

function closeModal() {
  draftModal.style.display = "none";
  resetUploadBox();
  document.getElementById("draftForm").reset();
}

function resetUploadBox() {
  csvUrlField.value = "";
  submitBtn.disabled = true;
  document.getElementById("uploadBox").textContent = "📂 Drop CSV here or click to upload";
}

// Enable submit button after CSV upload
function enableDraftSubmit() {
  if (csvUrlField.value) submitBtn.disabled = false;
}
window.enableDraftSubmit = enableDraftSubmit;

// Form submit
document.getElementById("draftForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!csvUrlField.value) {
    showNotification("Error", "⚠️ Please upload a CSV first!", "error");
    return;
  }

  const payload = {
    title: document.getElementById("draftTitle").value,
    description: document.getElementById("draftDesc").value,
    csv_url: csvUrlField.value
  };

  try {
    const res = await fetch("/u/draft/api/add", {
      method: "POST",
      credentials: 'include',
      headers: { 
        "Content-Type": "application/json",
        'X-CSRF-TOKEN': csrfToken
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok) {
      showNotification("Success", "Draft submitted successfully!", "success");

      // Close modal
      closeModal();

      // Add new draft to UI immediately with processing = true
      const container = document.getElementById("draftsContainer");
      const newDraftCard = createDraftCard({
        id: data.data.id,       // assuming your API returns the new draft id
        title: payload.title,
        desc: payload.description
      }, true); // processing = true
      container.prepend(newDraftCard);

    } else {
      showNotification("Error", "Failed: " + (data.message || "Server error"), "error");
    }
  } catch (err) {
    showNotification("Error", "⚠️ Error: " + err.message, "error");
  }
});
