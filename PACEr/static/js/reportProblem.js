const emailInput = document.getElementById('email');
const emailError = document.getElementById('email-error');
const botField = document.getElementById('bot-field');

emailInput.addEventListener('input', function () {
    if (!isValidEmail(emailInput.value)) {
        emailError.textContent = 'Ungültige Email-Adresse';
    } else {
        emailError.textContent = '';
    }
});

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Überprüfung des versteckten Feldes beim Absenden des Formulars
document.querySelector('form').addEventListener('submit', function (event) {
    if (botField.value !== '') {
        // Wenn das versteckte Feld ausgefüllt ist, handelt es sich wahrscheinlich um einen Bot
        event.preventDefault(); // Verhindere das Absenden des Formulars
        // Füge hier ggf. eine Fehlermeldung oder andere Aktionen hinzu
    }
});
