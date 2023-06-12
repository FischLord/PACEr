// Validierung des Formulars
document
    .getElementById("form_calculator")
    .addEventListener("submit", function (event) {
        var laengeInput = document.getElementById("laenge");
        var kmhInput = document.getElementById("kmh");
        var laengeError = document.getElementById("laenge-error");
        var bestzeitError = document.getElementById("bestzeit-error");

        var laengeValue = parseInt(laengeInput.value);
        var kmhValue = parseInt(kmhInput.value);

        // Überprüfung der Streckenlänge
        if (isNaN(laengeValue) || laengeValue <= 0) {
            event.preventDefault(); // Verhindert das Absenden des Formulars
            laengeError.classList.remove("hidden"); // Zeigt den Fehler an
        } else {
            laengeError.classList.add("hidden"); // Versteckt den Fehler
        }

        // Überprüfung des Tempos
        if (isNaN(kmhValue) || kmhValue < 0) {
            event.preventDefault(); // Verhindert das Absenden des Formulars
            bestzeitError.classList.remove("hidden"); // Zeigt den Fehler an
        } else {
            bestzeitError.classList.add("hidden"); // Versteckt den Fehler
        }
    });

// Dynamische Auswahl der km/h Optionen
function updateKmhOptions(selectedValue) {
    var tempoInputField = document.getElementById("tempoInputField");
    var kmhSelect = document.getElementById("kmh");
    kmhSelect.innerHTML = ""; // Clear existing options

    if (selectedValue === "hindernisstrecke") {
        addKmhOptions(8, 14);
    } else if (selectedValue === "wegstrecke") {
        addKmhOptions(8, 15);
    } else if (selectedValue === "schrittstrecke") {
        addKmhOptions(3, 7);
    }

    if (
        selectedValue === "hindernisstrecke" ||
        selectedValue === "wegstrecke" ||
        selectedValue === "schrittstrecke"
    ) {
        tempoInputField.style.display = "block";
    } else {
        tempoInputField.style.display = "none";
    }
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
