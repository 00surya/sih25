// Reusable function to create a draft card
function createDraftCard(draft) {
  const card = document.createElement("div");
  card.className = "draft-card";
  card.style.border = "1px solid #ddd";
  card.style.borderRadius = "10px";
  card.style.padding = "1rem";
  card.style.marginBottom = "1rem";
  card.style.position = "relative";
  card.style.background = "#fff";
  card.style.boxShadow = "0 4px 12px rgba(0,0,0,0.1)";

  // Header
  const header = document.createElement("div");
  header.style.display = "flex";
  header.style.justifyContent = "space-between";
  header.style.alignItems = "center";
  header.style.marginBottom = "0.8rem";

  const icon = document.createElement("div");
  icon.textContent = "📝";
  icon.style.fontSize = "1.2rem";

  const optionsContainer = document.createElement("div");
  optionsContainer.style.position = "relative";
  optionsContainer.style.cursor = "pointer";
  optionsContainer.textContent = "⋮";

  const menu = document.createElement("div");
  menu.style.display = "none";
  menu.style.position = "absolute";
  menu.style.top = "100%";
  menu.style.right = "0";
  menu.style.background = "#fff";
  menu.style.border = "1px solid #ccc";
  menu.style.borderRadius = "6px";
  menu.style.boxShadow = "0 4px 8px rgba(0,0,0,0.1)";
  menu.style.zIndex = "10";

  const edit = document.createElement("div");
  edit.textContent = "Edit";
  edit.style.padding = "0.5rem 1rem";
  edit.style.cursor = "pointer";
  edit.onclick = () => editDraft(draft.id);

  const del = document.createElement("div");
  del.textContent = "Delete";
  del.style.padding = "0.5rem 1rem";
  del.style.cursor = "pointer";
  del.onclick = () => deleteDraft(draft.id);

  menu.appendChild(edit);
  menu.appendChild(del);
  optionsContainer.appendChild(menu);

  optionsContainer.onclick = (e) => {
    e.stopPropagation();
    menu.style.display = menu.style.display === "block" ? "none" : "block";
  };

  window.addEventListener("click", () => menu.style.display = "none");

  header.appendChild(icon);
  header.appendChild(optionsContainer);

  // Title & Description
  const title = document.createElement("div");
  title.textContent = draft.title;
  title.style.fontWeight = "600";
  title.style.marginBottom = "0.5rem";

  const desc = document.createElement("div");
  desc.textContent = draft.desc;
  desc.style.color = "#555";
  desc.style.marginBottom = "1rem";

  // View Results button
  let viewBtn;
  if (draft.processing) {
    // Show disabled button with Processing...
    viewBtn = document.createElement("button");
    viewBtn.className = "btn";
    viewBtn.style.border = "none";
    viewBtn.style.borderRadius = "6px";
    viewBtn.style.padding = "0.6rem 1rem";
    viewBtn.style.cursor = "not-allowed";
    viewBtn.style.color = "#fff";
    viewBtn.style.background = "#dc3545"; // red
    viewBtn.textContent = "Processing...";
    viewBtn.disabled = true;
  } else {
    // Show anchor tag to dashboard
    viewBtn = document.createElement("a");
    viewBtn.href = `/u/draft/${draft.id}/dashboard`;
    viewBtn.className = "btn";
    viewBtn.style.display = "inline-block";
    viewBtn.style.textDecoration = "none";
    viewBtn.style.borderRadius = "6px";
    viewBtn.style.padding = "0.6rem 1rem";
    viewBtn.style.color = "#fff";
    viewBtn.style.background = "#28a745"; // green
    viewBtn.textContent = "View Results";
  }

  // Append everything
  card.appendChild(header);
  card.appendChild(title);
  card.appendChild(desc);
  card.appendChild(viewBtn);

  return card;
}

// Fetch drafts and add to UI
async function fetchDrafts() {
  showNotification("Info", "Fetching drafts", "info");
  try {
    const res = await fetch("/u/draft/list", { credentials: 'include' });
    const data = await res.json();
    const container = document.getElementById("draftsContainer");
    container.innerHTML = "";

    if (res.ok && data.status) {
      data.data.forEach(d => {
        console.log(d, 'dddd');
        const card = createDraftCard(d); // processing = false
        container.appendChild(card);
        
      });
      showNotification("Info", "Drafted loaded succefully!", "success");
    }
  } catch (err) {
    showNotification("Error", "⚠️ Could not fetch drafts: " + err.message, "error");
  }
}

// Example placeholders
async function viewResults(id) {
  await new Promise(resolve => setTimeout(resolve, 1500));
  showNotification("Info", "Results ready for draft: " + id, "success");
}

function editDraft(id) {
  showNotification("Info", "Edit draft: " + id, "success");
}

function deleteDraft(id) {
  showNotification("Info", "Delete draft: " + id, "warning");
}

// Call on page load
fetchDrafts();
