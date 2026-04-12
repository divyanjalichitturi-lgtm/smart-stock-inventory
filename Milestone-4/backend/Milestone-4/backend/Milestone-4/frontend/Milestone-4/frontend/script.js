const API_BASE_URL = "http://127.0.0.1:5000/api";

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard`);
        const data = await response.json();

        document.getElementById("totalProducts").textContent =
            data.totalProducts;

        document.getElementById("totalSales").textContent =
            data.totalSales.toLocaleString("en-IN");

        document.getElementById("activeAlerts").textContent =
            data.activeAlerts;

        document.getElementById("revenue").textContent =
            data.revenue.toLocaleString("en-IN");
    } catch (error) {
        console.error("Error loading dashboard:", error);
    }
}

async function loadAlerts() {
    try {
        const response = await fetch(`${API_BASE_URL}/alerts`);
        const alerts = await response.json();

        const tbody = document.getElementById("alerts-table-body");
        tbody.innerHTML = "";

        alerts.forEach(item => {
            const row = `
                <tr>
                    <td>${item.sku}</td>
                    <td>${item.product}</td>
                    <td>${item.category}</td>
                    <td>${item.qty}</td>
                    <td>${item.status}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error("Error loading alerts:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
    loadAlerts();
});
