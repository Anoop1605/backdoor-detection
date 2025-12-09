/* ===== CONTROL BUTTONS ===== */

function startSystem() {
    fetch("/start")
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error starting system: " + data.error);
                return;
            }
            setStatus("suricata_status", true);
            setStatus("ann_status", true);
            setStatus("hybrid_status", true);
        })
        .catch(err => alert("Network error: " + err));
}

function stopSystem() {
    fetch("/stop")
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error stopping system: " + data.error);
                return;
            }
            setStatus("suricata_status", false);
            setStatus("ann_status", false);
            setStatus("hybrid_status", false);
        })
        .catch(err => alert("Network error: " + err));
}

/* ===== STATUS LIGHT ===== */

function setStatus(id, state) {
    const el = document.getElementById(id);
    el.className = "light " + (state ? "green" : "red");
}

/* ===== LIVE LOG FETCHING ===== */

function fetchLogs() {

    // ANN logs
    fetch("/stream_ann")
        .then(res => res.json())
        .then(lines => {
            const box = document.getElementById("logBox");
            box.innerHTML =
                "<h3>🔍 ANN Predictions</h3>" +
                lines.map(l => `<div>${l}</div>`).join("");
        });

    // Hybrid logs
    fetch("/stream_hybrid")
        .then(res => res.json())
        .then(lines => {
            const box = document.getElementById("hybridBox");
            box.innerHTML =
                "<h3>🛡 Hybrid Engine</h3>" +
                lines.map(l => `<div>${l}</div>`).join("");
        });

    // Suricata logs
    fetch("/stream_suricata")
        .then(res => res.json())
        .then(lines => {
            const box = document.getElementById("suricataBox");
            box.innerHTML =
                "<h3>📡 Suricata IDS</h3>" +
                lines.map(l => `<div>${l}</div>`).join("");
        });
}

/* Update every 1 second */
setInterval(fetchLogs, 1000);
