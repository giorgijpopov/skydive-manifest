function updateNextFlightPage() {
    fetch('/next_flight_data')
        .then(response => response.json(), () => {
            showNoFlights();
        })
        .then(data => {
            console.log('second then success' + data);
            if (data.flight) {
                clearAll()

                var time = document.getElementById("header");
                if (data.remaining_time <= 10) {
                    time.innerHTML = `Flight №${data.flight.flight_number}: <span class="remaining-time">${data.remaining_time} min left</span>`;
                } else {
                    time.innerHTML = `Flight №${data.flight.flight_number}: ${data.remaining_time} min left`;
                }

                skydivers = data.flight.parachutists.split(';')
                fillTable(document.getElementById("parachutists-table"), skydivers)
            } else {
                showNoFlights();
            }
        });
}

function fillTable(table, skydivers) {
    table.innerHTML = '';
    createRow(table, "№", "Skydiver", "№", "Skydiver")

    numRows = Math.max(10, Math.ceil(skydivers.length / 2));
    for (let i = 0; i < numRows; i++) {
        leftIndex = i
        rightIndex = numRows + i
        createRow(table, leftIndex + 1, skydivers[leftIndex] || '', rightIndex + 1, skydivers[rightIndex] || '');
    }
}

function createRow(table, cell1, cell2, cell3, cell4) {
    const newRow = table.insertRow();
    const c1 = newRow.insertCell();
    const c2 = newRow.insertCell();
    const c3 = newRow.insertCell();
    const c4 = newRow.insertCell();
    c1.textContent = cell1;
    c1.classList.add("number-column");

    c2.textContent = cell2;
    c2.classList.add("skydiver-column");

    c3.textContent = cell3;
    c3.classList.add("number-column");

    c4.textContent = cell4;
    c4.classList.add("skydiver-column");
}

function clearAll() {
    ['header', 'parachutists-table', 'no-flights'].forEach(s=>{
        var time = document.getElementById(s);
        time.innerHTML = ``;
    })
}

function showNoFlights() {
    clearAll()
    var noFlights = document.getElementById("no-flights");
    noFlights.textContent = `No flights yet`;
}

updateNextFlightPage();
setInterval(updateNextFlightPage, 10000);