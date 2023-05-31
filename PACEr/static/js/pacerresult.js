// Großschreibung der Art der Strecke
const artElement = document.getElementById("capitalized-art");
const artValue = artElement.textContent;
const capitalizedArt = artValue.charAt(0).toUpperCase() + artValue.slice(1);
artElement.textContent = capitalizedArt;
