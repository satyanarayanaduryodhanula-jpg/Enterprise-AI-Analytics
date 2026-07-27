// ===============================
// Global Chart Variable
// ===============================

let salesChart = null;

// ===============================
// Load KPI Cards
// ===============================

async function loadDashboard(){

    const response = await fetch("/kpi-data");

    const data = await response.json();

    document.getElementById("revenue").innerHTML =
        "₹" + Number(data.revenue).toLocaleString();

    document.getElementById("orders").innerHTML =
        data.orders;

    document.getElementById("customers").innerHTML =
        data.customers;

    document.getElementById("avg").innerHTML =
        "₹" + Number(data.average_order).toLocaleString();

}

// ===============================
// Load Revenue Chart
// ===============================

async function loadChart(){

    const response = await fetch("/sales-chart");

    const data = await response.json();

    const labels = data.map(item => item.product);

    const revenue = data.map(item => item.revenue);

    if(salesChart){

        salesChart.destroy();

    }

    salesChart = new Chart(

        document.getElementById("salesChart"),

        {

            type:"bar",

            data:{

                labels:labels,

                datasets:[{

                    label:"Revenue",

                    data:revenue

                }]

            },

            options:{

                responsive:true,

                maintainAspectRatio:false,

                animation:false,

                plugins:{

                    legend:{
                        display:false
                    }

                }

            }

        }

    );

}

// ===============================
// Load AI Summary
// ===============================

async function loadAIReport(){

    const response = await fetch("/latest-ai-report");

    const data = await response.json();

    document.getElementById("aiReport").innerHTML = `

<h2>🤖 AI Executive Summary</h2>

<p>🟢 <b>Business Health :</b> ${data.business_health}%</p>

<p>🏆 <b>Best Product :</b> ${data.best_product}</p>

<p>📉 <b>Worst Product :</b> ${data.worst_product}</p>

<p>💰 <b>Total Revenue :</b> ₹${Number(data.total_revenue).toLocaleString()}</p>

<p>📊 <b>Average Revenue :</b> ₹${Number(data.average_revenue).toLocaleString()}</p>

<p>⚠ <b>Inventory Risk :</b><br>${data.inventory_risk}</p>

<p>💡 <b>Recommendation :</b><br>${data.recommendation}</p>

`;

}

// ===============================
// Generate AI Report
// ===============================

async function generateReport(){

    const btn = document.getElementById("generateBtn");

    btn.disabled = true;

    btn.innerHTML = "Generating...";

    document.getElementById("status").innerHTML =
        "⏳ Generating AI Report...";

    const response = await fetch(

        "/generate-ai-report",

        {

            method:"POST"

        }

    );

    const data = await response.json();

    document.getElementById("status").innerHTML =
        "✅ " + data.message;

    document.getElementById("time").innerHTML =
        "Last Generated : " +
        new Date().toLocaleString();

    await loadDashboard();

    await loadChart();

    await loadAIReport();

    btn.disabled = false;

    btn.innerHTML = "Generate AI Report";

}

// ===============================
// Button Event
// ===============================

document
.getElementById("generateBtn")
.addEventListener(
    "click",
    generateReport
);

// ===============================
// Initial Dashboard Load
// ===============================

loadDashboard();

loadChart();

loadAIReport();