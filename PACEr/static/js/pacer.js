// Client-seitige Validierung der maximalen Streckenlänge
const MAX_LENGTH = 100000; // 100 km in Metern

// === pacer.js ===
// Validierung des Formulars inklusive Max Length
document
    .getElementById("form_calculator")
    .addEventListener("submit", function (event) {
        var laengeInput = document.getElementById("laenge");
        var kmhInput = document.getElementById("kmh");
        var laengeError = document.getElementById("laenge-error");
        var bestzeitError = document.getElementById("bestzeit-error");

        var laengeValue = parseInt(laengeInput.value, 10);
        var kmhValue = parseInt(kmhInput.value, 10);

        // Überprüfung der Streckenlänge
        if (isNaN(laengeValue) || laengeValue <= 0 || laengeValue > MAX_LENGTH) {
            event.preventDefault();
            laengeError.textContent = laengeValue > MAX_LENGTH
                ? `Maximale Streckenlänge ${MAX_LENGTH} m überschritten.`
                : "Es sollte eine positive ganze Zahl größer als 0 m sein.";
            laengeError.classList.remove("hidden");
        } else {
            laengeError.classList.add("hidden");
        }

        // Überprüfung des Tempos
        if (isNaN(kmhValue) || kmhValue < 0) {
            event.preventDefault();
            bestzeitError.classList.remove("hidden");
        } else {
            bestzeitError.classList.add("hidden");
        }
    });

// Dynamische Auswahl der km/h Optionen bleibt unverändert
function updateKmhOptions(selectedValue) {
    var tempoInputField = document.getElementById("tempoInputField");
    var kmhSelect = document.getElementById("kmh");
    kmhSelect.innerHTML = "";

    if (selectedValue === "hindernisstrecke") {
        addKmhOptions(8, 14);
    } else if (selectedValue === "wegstrecke") {
        addKmhOptions(8, 15);
    } else if (selectedValue === "schrittstrecke") {
        addKmhOptions(3, 7);
    }

    tempoInputField.style.display = (selectedValue ? "block" : "none");
}

function addKmhOptions(start, end) {
    var kmhSelect = document.getElementById("kmh");
    for (var i = start; i <= end; i++) {
        var option = document.createElement("option");
        option.value = i;
        option.textContent = i + " km/h";
        kmhSelect.appendChild(option);
    }
}