document.addEventListener("DOMContentLoaded", () => {
  handleExitFormSubmit();
  attachLogoutHandler();
});

// -----------------------------
// Submit Exit Request
// -----------------------------
function handleExitFormSubmit() {
  const form = document.getElementById("tenantExitForm");
  const statusEl = document.getElementById("tenantExitStatus");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const tenantId = document.getElementById("tenantId").value;

    formData.append("tenant_id", tenantId);
    formData.append("name", document.getElementById("name").value);
    formData.append("room_number", document.getElementById("roomNumber").value);
    formData.append("exit_reason", document.getElementById("reason").value);
    formData.append("email", document.getElementById("email").value);

    // Checklist (optional multi-select)
    const checklistOptions = document.querySelectorAll('input[name="checklist"]:checked');
    checklistOptions.forEach((item) => {
      formData.append("moveout_checklist", item.value);
    });

    // Supporting document (optional)
    const fileInput = document.getElementById("supportingDoc");
    if (fileInput && fileInput.files.length > 0) {
      formData.append("supporting_document", fileInput.files[0]);
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/exit-request/submit", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to submit exit request.");

      const result = await response.json();
      statusEl.textContent = result.message || "✅ Exit request submitted successfully!";
      statusEl.className = "text-green-600 font-semibold";

      form.reset();

      setTimeout(() => fetchMyExitRequests(tenantId), 300);
    } catch (error) {
      statusEl.textContent = "❌ Failed to submit request. Try again.";
      statusEl.className = "text-red-600 font-semibold";
      console.error(error);
    }
  });

  // Fetch requests if Tenant ID is already pre-filled
  const tenantIdField = document.getElementById("tenantId");
  if (tenantIdField && tenantIdField.value) {
    fetchMyExitRequests(tenantIdField.value);
  }

  // Optional: refetch on blur
  tenantIdField?.addEventListener("blur", () => {
    if (tenantIdField.value.trim() !== "") {
      fetchMyExitRequests(tenantIdField.value.trim());
    }
  });
}

// -----------------------------
// Fetch Exit Requests by Tenant ID
// -----------------------------
async function fetchMyExitRequests(tenantId) {
  const container = document.getElementById("myExitRequests");
  if (!tenantId || !container) return;

  try {
    const res = await fetch(`http://127.0.0.1:8000/exit-request/by-tenant/${tenantId}`);
    const data = await res.json();

    container.innerHTML = "";

    if (data.length === 0) {
      container.innerHTML = "<p class='text-gray-500'>No requests submitted yet.</p>";
      return;
    }

    data.forEach((req, index) => {
      const checklistHTML = req.moveout_checklist?.length
        ? `<p><strong>Checklist:</strong> ${req.moveout_checklist.join(", ")}</p>`
        : "";

      const card = `
        <div class="bg-white p-4 rounded-xl shadow-md mb-4">
          <h4 class="text-lg font-semibold">Request ${index + 1}</h4>
          <p><strong>Room:</strong> ${req.room_number}</p>
          <p><strong>Status:</strong> 
            <span class="font-bold ${
              req.request_status === "Approved"
                ? "text-green-600"
                : req.request_status === "Rejected"
                ? "text-red-600"
                : "text-yellow-600"
            }">${req.request_status}</span>
          </p>
          <p><strong>Reason:</strong> ${req.exit_reason}</p>
          <p><strong>Date:</strong> ${req.submitted_at || "N/A"}</p>
          ${checklistHTML}
          ${
            req.supporting_document_url
              ? `<a href="${req.supporting_document_url}" target="_blank" class="text-blue-600 underline">Download Document</a>`
              : ""
          }
        </div>
      `;
      container.innerHTML += card;
    });
  } catch (err) {
    container.innerHTML = "<p class='text-red-600'>Error fetching requests. Try again later.</p>";
    console.error(err);
  }
}

// -----------------------------
// Logout Functionality
// -----------------------------
function attachLogoutHandler() {
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/logout", {
          method: "POST",
          credentials: "include",
        });

        const data = await res.json();

        Swal.fire({
          icon: "success",
          title: "Logged Out",
          text: data.message || "You have been logged out.",
          confirmButtonColor: "#1e40af",
        }).then(() => {
          window.location.href = "login.html";
        });
      } catch (err) {
        console.error("Logout error:", err);
        Swal.fire("Error", "Logout failed. Try again.", "error");
      }
    });
  }
}
