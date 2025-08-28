// ---------- Utility Functions ----------

// Generate random UUID (simplified v4)
function generateId(prefix) {
  return prefix + '_' + Math.random().toString(36).substring(2, 10);
}

// Show/hide loader
function toggleLoader(show = true) {
  const loader = document.getElementById('loader');
  loader?.classList.toggle('hidden', !show);
}

// ---------- Exit Request Submission ----------
document.getElementById('exitForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  toggleLoader(true);

  const tenantId = document.getElementById('tenantId').value.trim();
  const name = document.getElementById('name').value.trim();
  const roomNumber = document.getElementById('roomNumber').value.trim();
  const exitDate = document.getElementById('exitDate').value.trim();
  const exitReason = document.getElementById('reason').value.trim();
  const email = document.getElementById('email').value.trim();
  const fileInput = document.getElementById('supportingDoc');

  const checklistItems = Array.from(
    document.querySelectorAll('input[name="moveout_checklist"]:checked')
  ).map(cb => cb.value);

  if (!tenantId || !name || !roomNumber || !exitReason || !email || !exitDate) {
    toggleLoader(false);
    Swal.fire("Missing Fields", "Please fill in all required fields.", "warning");
    return;
  }

  const formData = new FormData();
  formData.append("tenant_id", tenantId);
  formData.append("name", name);
  formData.append("room_number", roomNumber);
  formData.append("exit_reason", exitReason);
  formData.append("email", email);
  formData.append("exit_date", exitDate);
  checklistItems.forEach(item => formData.append("moveout_checklist", item));

  if (fileInput && fileInput.files.length > 0) {
    formData.append("supporting_document", fileInput.files[0]);
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/exit-request/submit', {
      method: 'POST',
      body: formData
    });

    if (res.ok) {
      Swal.fire("Success", "Exit request submitted successfully!", "success");
      e.target.reset();
    } else {
      const errorData = await res.json();
      Swal.fire("Error", errorData.detail || "Failed to submit exit request.", "error");
    }
  } catch (err) {
    console.error("Exit Request Error:", err);
    Swal.fire("Network Error", "Unable to submit exit request.", "error");
  } finally {
    toggleLoader(false);
  }
});

// ---------- Damage Report Submission ----------
document.getElementById('damageForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  toggleLoader(true);

  const tenantId = document.getElementById('tenantIdDamage').value.trim();
  const description = document.getElementById('description').value.trim();
  const amount = parseFloat(document.getElementById('amount').value.trim());

  if (!tenantId || !description || isNaN(amount)) {
    toggleLoader(false);
    Swal.fire("Missing Fields", "Please fill in all required fields.", "warning");
    return;
  }

  const data = {
    report_id: generateId("damage"),
    tenant_id: tenantId,
    room_number: document.getElementById('roomNumberDamage')?.value || "N/A",
    description,
    estimated_cost: amount,
    reported_at: new Date().toISOString()
  };

  try {
    const res = await fetch('http://127.0.0.1:8000/damage-report/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (res.ok) {
      Swal.fire("Success", "Damage report submitted successfully!", "success");
      e.target.reset();
    } else {
      const errorData = await res.json();
      Swal.fire("Error", errorData.detail || "Failed to submit damage report.", "error");
    }
  } catch (err) {
    console.error("Damage Report Error:", err);
    Swal.fire("Network Error", "Unable to submit damage report.", "error");
  } finally {
    toggleLoader(false);
  }
});

// ---------- Update Exit Request Status ----------
async function updateStatus(requestId, newStatus) {
  toggleLoader(true);
  try {
    const res = await fetch('http://127.0.0.1:8000/exit-request/update-status', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: requestId, new_status: newStatus })
    });

    if (res.ok) {
      Swal.fire("Updated", `Request marked as '${newStatus}'`, "success");
      fetchRequests(); // Refresh list
    } else {
      const data = await res.json();
      Swal.fire("Error", data.detail || "Failed to update status.", "error");
    }
  } catch (err) {
    console.error("Update Status Error:", err);
    Swal.fire("Network Error", "Could not update request status.", "error");
  } finally {
    toggleLoader(false);
  }
}

// ---------- Fetch Exit + Damage Requests ----------
async function fetchRequests() {
  const tenantId = document.getElementById('lookupTenantId').value.trim();
  const exitList = document.getElementById('exitList');
  const damageList = document.getElementById('damageList');

  exitList.innerHTML = "";
  damageList.innerHTML = "";

  if (!tenantId) {
    Swal.fire("Missing Field", "Please enter a Tenant ID.", "warning");
    return;
  }

  toggleLoader(true);

  try {
    const res = await fetch(`http://127.0.0.1:8000/exit-request/list/${tenantId}`);
    const data = await res.json();

    if (Array.isArray(data) && data.length > 0) {
      data.forEach(item => {
        const li = document.createElement('li');
        const statusColor = {
          "Pending": "status-pending",
          "Approved": "status-approved",
          "Needs Action": "status-needs-action"
        }[item.request_status] || "status-pending";

        li.innerHTML = `
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
            <div>
              <span class="font-semibold">#${item.request_id}</span> | 
              Room: ${item.room_number} | 
              <span class="status-pill ${statusColor}">${item.request_status}</span> | 
              ${new Date(item.submitted_at).toLocaleDateString()}
            </div>
            <div class="flex gap-2">
              <button onclick="updateStatus('${item.request_id}', 'Approved')" class="text-sm bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded-md">Approve</button>
              <button onclick="updateStatus('${item.request_id}', 'Needs Action')" class="text-sm bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded-md">Needs Action</button>
            </div>
          </div>`;
        exitList.appendChild(li);
      });
    } else {
      exitList.innerHTML = '<li>No exit requests found.</li>';
    }
  } catch (err) {
    console.error("Fetch exit requests error:", err);
    exitList.innerHTML = '<li>Error fetching exit requests.</li>';
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/damage-report/list/${tenantId}`);
    const data = await res.json();

    if (Array.isArray(data) && data.length > 0) {
      data.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
          <div class="flex justify-between items-start bg-white rounded-lg shadow-sm p-3 border">
            <div>
              <div class="font-semibold text-red-700">#${item.report_id}</div>
              <div class="text-sm">Room: ${item.room_number} | ₹${item.estimated_cost}</div>
              <div class="text-xs text-gray-700 mt-1">${item.damage_description}</div>
              <div class="text-xs text-gray-500 mt-1">${new Date(item.reported_at).toLocaleString()}</div>
            </div>
          </div>
        `;
        damageList.appendChild(li);
      });
    } else {
      damageList.innerHTML = '<li class="text-gray-500 text-sm">No damage reports found.</li>';
    }
  } catch (err) {
    console.error("Fetch damage reports error:", err);
    damageList.innerHTML = '<li class="text-red-600 text-sm">Error fetching damage reports.</li>';
  }


  toggleLoader(false);
}

// ---------- CSV Report Download ----------
async function downloadReport() {
  const tenantId = document.getElementById('lookupTenantId').value.trim();
  if (!tenantId) {
    Swal.fire("Missing Field", "Enter Tenant ID to download report.", "warning");
    return;
  }

  toggleLoader(true);
  try {
    const res = await fetch(`http://127.0.0.1:8000/exit-request/report/${tenantId}`);
    if (!res.ok) throw new Error("Download failed");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exit_report_${tenantId}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    Swal.fire("Downloaded", "CSV report downloaded successfully!", "success");
  } catch (err) {
    Swal.fire("Error", "Error downloading report.", "error");
    console.error("CSV Download Error:", err);
  } finally {
    toggleLoader(false);
  }
}
