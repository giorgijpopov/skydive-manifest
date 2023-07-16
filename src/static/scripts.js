function addParachutist() {
    var table = document.getElementById("parachutists-table");
    var tr = document.createElement("tr");
    tr.innerHTML = `
        <td>${table.rows.length + 1}</td>
        <td><input type="text" name="parachutist" required></td>
        <td><button type="button" onclick="deleteSkydiver(this)">Delete</button></td>`;
    table.appendChild(tr);
}

function deleteSkydiver(button) {
    var closestTr = button.closest('tr');
    if (closestTr) {
        closestTr.remove();
    }
    var table = document.getElementById("parachutists-table");
    if (!table) return;
    for (let i = 0; i < table.rows.length; i++) {
        table.rows[i].cells[0].textContent = i + 1;
    }
    rowCount = table.rows.length - 1;
}