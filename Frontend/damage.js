document.addEventListener("DOMContentLoaded", () => {
  const estimatedAmount = document.getElementById("estimatedAmount");
  const damageForm = document.getElementById("damageForm");

  // ✅ Predefined item prices
  const itemPrices = {
    fan: 50,
    table: 100,
    chair: 200,
    bed: 500,
    bulb: 30,
  };

  // 🔁 Update total cost based on checked items
  const updateTotal = () => {
    const checkedItems = document.querySelectorAll('input[name="item"]:checked');
    let total = 0;

    checkedItems.forEach((checkbox) => {
      const value = checkbox.value;
      total += itemPrices[value] || 0;
    });

    estimatedAmount.value = total.toFixed(2);
  };

  // 🔄 Listen to checkbox changes
  const itemCheckboxes = document.querySelectorAll('input[name="item"]');
  itemCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", updateTotal);
  });

  // 📤 Handle damage report submission
  damageForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const tenantId = document.getElementById("tenantId").value.trim();
    const description = document.getElementById("description").value.trim();
    const estimatedCost = parseFloat(estimatedAmount.value);
    const roomNumber = "ROOM123"; // 🔄 Replace with actual logic if needed

    if (!tenantId || !description || isNaN(estimatedCost) || estimatedCost <= 0) {
      alert("⚠️ Please fill in all fields and select at least one item.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("tenant_id", tenantId);
      formData.append("room_number", roomNumber);
      formData.append("description", description);
      formData.append("estimated_cost", estimatedCost);

      const response = await fetch("http://127.0.0.1:8000/damage-report/submit", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        alert("✅ Damage report submitted successfully.\nReport ID: " + result.report_id);
        damageForm.reset();
        estimatedAmount.value = "0.00";
      } else {
        alert("❌ Submission failed: " + result.detail);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("🚫 Network or server error occurred.");
    }
  });

  // 🔃 Set default on page load
  estimatedAmount.value = "0.00";
});
