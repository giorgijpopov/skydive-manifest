function addParachutist() {
    var table = document.getElementById("parachutists-table");
    var tr = document.createElement("tr");
    console.log(table.rows.length)
    tr.innerHTML = `
        <td>${table.rows.length + 1}</td>
        <td><input type="text" name="parachutist" required></td>
        <td><button type="button" onclick="deleteSkydiver(this)">Delete</button></td>`;
    table.appendChild(tr);
}

function deleteSkydiver(button) {
    var closestTr = button.closest('tr')
    if (closestTr) {
        closestTr.remove()
    }
}