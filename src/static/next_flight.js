function updateNextFlightPage() {
    fetch('/next_flight_data')
        .then(response => response.json(), () => {
            showNoFlights();
        })
        .then(data => {
            console.log('second then success' + data);
            if (data.flight) {
                var time = document.getElementById("time");
                if (data.remaining_time <= 10) {
                    time.innerHTML = `Time Left: <span class="remaining-time">${data.remaining_time} min</span>`;
                } else {
                    time.innerHTML = `Time Left: ${data.remaining_time} min`;
                }

                var flightNumber = document.getElementById("flight-number");
                flightNumber.textContent = `Flight Number: ${data.flight.flight_number}`

                var aircraft = document.getElementById("aircraft");
                aircraft.textContent = `Aircraft: ${data.flight.aircraft_model}`

                var table = document.getElementById("parachutists-table");
                if (!table) return;

                table.innerHTML = '';
                const newRow = table.insertRow();
                const num = newRow.insertCell();
                const name = newRow.insertCell();
                num.textContent = "№";
                name.textContent = "Skydiver";

                data.flight.parachutists.split(';').forEach((sk, i)=>{
                    const newRow = table.insertRow();
                    const num = newRow.insertCell();
                    const name = newRow.insertCell();

                    num.textContent = i + 1;
                    name.textContent = sk;
                })

                var noFlights = document.getElementById("no-flights");
                noFlights.textContent = ``;
            } else {
                showNoFlights();
            }
        });
}

function showNoFlights() {
    var time = document.getElementById("time");
    time.innerHTML = ``;

    var flightNumber = document.getElementById("flight-number");
    flightNumber.innerHTML = ``;

    var aircraft = document.getElementById("aircraft");
    aircraft.innerHTML = ``;

    var table = document.getElementById("parachutists-table");
    table.innerHTML = '';

    var noFlights = document.getElementById("no-flights");
    noFlights.textContent = `No flights yet`;
}

updateNextFlightPage();
setInterval(updateNextFlightPage, 30000);