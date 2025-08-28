document.addEventListener("DOMContentLoaded", () => {
  fetchApprovedExits();
  fetchRoomHistory();
  fetchMoveTimeline();
  attachLogoutHandler();
});

// -----------------------------
// Fetch Approved Exit Requests
// -----------------------------
async function fetchApprovedExits() {
  try {
    const response = await fetch("http://127.0.0.1:8000/landlord/approved-exits", {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) throw new Error("Failed to fetch approved exits");

    const data = await response.json();
    const exitContainer = document.getElementById("approvedExitList");
    if (!exitContainer) return;

    exitContainer.innerHTML = "";

    if (data.length === 0) {
      exitContainer.innerHTML = `<p class="text-gray-500">No approved exits found.</p>`;
      return;
    }

    data.forEach((exit, index) => {
      const card = `
        <div class="bg-white p-4 rounded-lg shadow-md mb-4">
          <h4 class="font-bold text-lg">Exit ${index + 1}</h4>
          <p><strong>Tenant:</strong> ${exit.name}</p>
          <p><strong>Room:</strong> ${exit.room_number}</p>
          <p><strong>Date:</strong> ${exit.exit_date}</p>
        </div>
      `;
      exitContainer.innerHTML += card;
    });
  } catch (err) {
    console.error("Error loading approved exits:", err);
    Swal.fire("Error", "Failed to load approved exits", "error");
  }
}

// -----------------------------
// Fetch Room History
// -----------------------------
async function fetchRoomHistory() {
  try {
    const response = await fetch("http://127.0.0.1:8000/landlord/room-history", {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) throw new Error("Failed to fetch room history");

    const data = await response.json();
    const historyContainer = document.getElementById("roomHistoryList");
    if (!historyContainer) return;

    historyContainer.innerHTML = "";

    if (data.length === 0) {
      historyContainer.innerHTML = `<tr><td colspan="4" class="text-center text-gray-500 py-2">No room history found.</td></tr>`;
      return;
    }

    data.forEach((entry) => {
      const row = `
        <tr class="border-b">
          <td class="py-2 px-4">${entry.room_number}</td>
          <td class="py-2 px-4">${entry.tenant_name}</td>
          <td class="py-2 px-4">${entry.move_in}</td>
          <td class="py-2 px-4">${entry.move_out}</td>
        </tr>
      `;
      historyContainer.innerHTML += row;
    });
  } catch (err) {
    console.error("Error loading room history:", err);
    Swal.fire("Error", "Failed to load room history", "error");
  }
}

// -----------------------------
// Fetch Move-in/Out Timeline
// -----------------------------
async function fetchMoveTimeline() {
  try {
    const response = await fetch("http://127.0.0.1:8000/landlord/move-timeline", {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) throw new Error("Failed to fetch timeline");

    const data = await response.json();
    const timelineContainer = document.getElementById("moveTimelineList");
    if (!timelineContainer) return;

    timelineContainer.innerHTML = "";

    if (data.length === 0) {
      timelineContainer.innerHTML = `<p class="text-gray-500">No movement events found.</p>`;
      return;
    }

    data.forEach((event) => {
      const timelineItem = `
        <div class="border-l-4 border-blue-500 pl-4 mb-4">
          <p class="text-sm text-gray-600">${event.date}</p>
          <p class="text-md font-semibold">${event.description}</p>
        </div>
      `;
      timelineContainer.innerHTML += timelineItem;
    });
  } catch (err) {
    console.error("Error loading timeline:", err);
    Swal.fire("Error", "Failed to load move-in/out timeline", "error");
  }
}

// -----------------------------
// Logout Button Handler
// -----------------------------
function attachLogoutHandler() {
  const logoutBtn = document.getElementById("logoutBtn");
  if (!logoutBtn) return;

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
        text: data.message,
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
