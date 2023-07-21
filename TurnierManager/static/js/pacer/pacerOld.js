function validateInput(input, errorDiv) {
    if (!Number.isInteger(Number(input.value)) || Number(input.value) <= 0) {
        errorDiv.innerHTML =
            "Es sollte eine positive ganze Zahl die größer als 0m ist angegeben werden.";
        errorDiv.classList.remove("hidden");
        errorDiv.classList.add("block");
        input.classList.add("border-red-600");
        document.getElementById("submit-button").disabled = true; // disable submit button
        return false;
    } else {
        errorDiv.classList.remove("block");
        errorDiv.classList.add("hidden");
        input.classList.remove("border-red-600");
        document.getElementById("submit-button").disabled = false; // enable submit button
        return true;
    }
}

var laengeInput = document.getElementById("laenge");
var laengeError = document.getElementById("laenge-error");
laengeInput.addEventListener("input", function () {
    validateInput(laengeInput, laengeError);
});

var bestzeitMinInput = document.getElementById("bestzeit_min");
var bestzeitSecInput = document.getElementById("bestzeit_sec");
var bestzeitError = document.getElementById("bestzeit-error");
bestzeitMinInput.addEventListener("input", function () {
    validateTimeInput(bestzeitMinInput, bestzeitSecInput, bestzeitError);
});
bestzeitSecInput.addEventListener("input", function () {
    validateTimeInput(bestzeitMinInput, bestzeitSecInput, bestzeitError);
});

var erlaubtezeitMinInput = document.getElementById("erlaubtezeit_min");
var erlaubtezeitSecInput = document.getElementById("erlaubtezeit_sec");
var erlaubtezeitError = document.getElementById("erlaubtezeit-error");
erlaubtezeitMinInput.addEventListener("input", function () {
    validateTimeInput(
        erlaubtezeitMinInput,
        erlaubtezeitSecInput,
        erlaubtezeitError
    );
});
erlaubtezeitSecInput.addEventListener("input", function () {
    validateTimeInput(
        erlaubtezeitMinInput,
        erlaubtezeitSecInput,
        erlaubtezeitError
    );
});

var hoechstzeitMinInput = document.getElementById("hoechstzeit_min");
var hoechstzeitSecInput = document.getElementById("hoechstzeit_sec");
var hoechstzeitError = document.getElementById("hoechstzeit-error");
hoechstzeitMinInput.addEventListener("input", function () {
    validateTimeInput(hoechstzeitMinInput, hoechstzeitSecInput, hoechstzeitError);
});
hoechstzeitSecInput.addEventListener("input", function () {
    validateTimeInput(hoechstzeitMinInput, hoechstzeitSecInput, hoechstzeitError);
});

function validateTimeInput(minInput, secInput, errorDiv) {
    var min = Number(minInput.value);
    var sec = Number(secInput.value);
    if (min < 0 || sec < 0 || sec > 60) {
        errorDiv.innerHTML =
            "Es dürfen keine negativen Minuten oder Sekunden eingegeben werden und die Sekunden dürfen nicht mehr als 60 betragen.";
        errorDiv.classList.remove("hidden");
        errorDiv.classList.add("block");
        minInput.classList.add("border-red-600");
        secInput.classList.add("border-red-600");
        document.getElementById("submit-button").disabled = true; // disable submit button
        return false;
    } else {
        errorDiv.classList.remove("block");
        errorDiv.classList.add("hidden");
        minInput.classList.remove("border-red-600");
        secInput.classList.remove("border-red-600");
        document.getElementById("submit-button").disabled = false; // enable submit button
        return true;
    }
}

document
    .getElementById("form_calculator")
    .addEventListener("submit", function (event) {
        var valid = true;
        valid = validateInput(laengeInput, laengeError) && valid;
        valid =
            validateTimeInput(bestzeitMinInput, bestzeitSecInput, bestzeitError) &&
            valid;
        valid =
            validateTimeInput(
                erlaubtezeitMinInput,
                erlaubtezeitSecInput,
                erlaubtezeitError
            ) && valid;
        valid =
            validateTimeInput(
                hoechstzeitMinInput,
                hoechstzeitSecInput,
                hoechstzeitError
            ) && valid;
        if (!valid) {
            event.preventDefault();
        }
    });
