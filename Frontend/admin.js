document.addEventListener("DOMContentLoaded", () => {
  fetchExitRequests();
  fetchDamageReports();
  attachLogoutHandler();
});

// -------------------------------
// Fetch & Render Exit Requests
// -------------------------------
async function fetchExitRequests() {
  try {
    const res = await fetch("http://127.0.0.1:8000/admin/exit-requests", {
      credentials: "include"
    });

    if (!res.ok) throw new Error("Failed to fetch exit requests");

    const data = await res.json();
    const tbody = document.getElementById("exitBody");
    tbody.innerHTML = "";

    data.forEach((item) => {
      const checklist = (item.moveout_checklist || []).join(", ") || "N/A";
      const badgeClass = {
        Pending: "bg-yellow-100 text-yellow-700",
        Approved: "bg-green-100 text-green-700",
        Rejected: "bg-red-100 text-red-700",
        InReview: "bg-blue-100 text-blue-700"
      }[item.request_status] || "bg-gray-100 text-gray-700";

      const row = document.createElement("tr");
      row.classList.add("hover:bg-gray-50", "transition");

      row.innerHTML = `
        <td class="px-4 py-3 text-sm font-medium text-gray-900">${item.request_id}</td>
        <td class="px-4 py-3 text-sm text-gray-700">${item.name}<br><span class="text-xs text-gray-500">${item.tenant_id}</span></td>
        <td class="px-4 py-3 text-sm text-gray-700">${item.room_number}</td>
        <td class="px-4 py-3 text-sm text-gray-700">${item.exit_reason}</td>
        <td class="px-4 py-3 text-sm text-gray-700" title="${checklist}">
          ${checklist.length > 40 ? checklist.substring(0, 40) + "..." : checklist}
        </td>
        <td class="px-4 py-3 text-sm">
          <span class="px-2 py-1 rounded-full text-xs font-semibold ${badgeClass}">
            ${item.request_status}
          </span>
        </td>
        <td class="px-4 py-3 text-sm">
          <button onclick="updateStatus('${item.request_id}')" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs px-3 py-1 rounded">
            Update
          </button>
        </td>
      `;

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching exit requests:", err);
    Swal.fire("Error", "Failed to load exit requests", "error");
  }
}

// -------------------------------
// Fetch & Render Damage Reports
// -------------------------------
async function fetchDamageReports() {
  try {
    const res = await fetch("http://127.0.0.1:8000/admin/damage-reports", {
      credentials: "include"
    });

    if (!res.ok) throw new Error("Failed to fetch damage reports");

    const data = await res.json();
    const tbody = document.getElementById("damageBody");
    tbody.innerHTML = "";

    data.forEach((item) => {
      const row = document.createElement("tr");
      row.classList.add("hover:bg-gray-50", "transition");

      row.innerHTML = `
        <td class="px-4 py-3 text-sm font-medium text-gray-900">${item.report_id}</td>
        <td class="px-4 py-3 text-sm text-gray-700">${item.tenant_id}</td>
        <td class="px-4 py-3 text-sm text-gray-700">${item.room_number}</td>
        <td class="px-4 py-3 text-sm text-gray-700">${item.damage_description || item.description || "N/A"}</td>
        <td class="px-4 py-3 text-sm text-green-600 font-semibold">₹${item.estimated_cost || 0}</td>
        <td class="px-4 py-3 text-sm text-gray-500">${item.reported_at ? new Date(item.reported_at).toLocaleDateString() : "N/A"}</td>
      `;

      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching damage reports:", err);
    Swal.fire("Error", "Failed to load damage reports", "error");
  }
}

// -------------------------------
// Update Exit Request Status
// -------------------------------
async function updateStatus(requestId) {
  const { value: status } = await Swal.fire({
    title: "Update Exit Request Status",
    input: "select",
    inputOptions: {
      Pending: "Pending",
      Approved: "Approved",
      InReview: "In Review",
      Rejected: "Rejected"
    },
    inputPlaceholder: "Choose new status",
    showCancelButton: true,
    confirmButtonText: "Update",
    cancelButtonText: "Cancel"
  });

  if (status) {
    try {
      const res = await fetch("http://127.0.0.1:8000/admin/update-exit-status", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
          request_id: requestId,
          new_status: status
        })
      });

      const result = await res.json();
      if (res.ok) {
        Swal.fire("Success", result.message || "Status updated successfully", "success");
        fetchExitRequests();
      } else {
        throw new Error(result.detail || "Unknown error");
      }
    } catch (err) {
      console.error("Update failed:", err);
      Swal.fire("Error", "Status update failed", "error");
    }
  }
}

// -------------------------------
// Logout Functionality
// -------------------------------
function attachLogoutHandler() {
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/logout", {
          method: "POST",
          credentials: "include"
        });
        const data = await res.json();
        Swal.fire({
          icon: "success",
          title: "Logged Out",
          text: data.message,
          confirmButtonColor: "#1e40af"
        }).then(() => {
          window.location.href = "login.html";
        });
      } catch (err) {
        console.error("Logout failed:", err);
        Swal.fire("Error", "Logout failed. Please try again.", "error");
      }
    });
  }
}
