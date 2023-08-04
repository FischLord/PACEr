document.addEventListener("DOMContentLoaded", function() {
  const answersContainer = document.getElementById("answersContainer");
  const addAnswerButton = document.getElementById("addAnswer");
  
  let answerCount = 1;
  
  addAnswerButton.addEventListener("click", function() {
    const newInput = document.createElement("input");
    newInput.className = "w-full p-2 border rounded mb-2 mr-2";
    newInput.type = "text";
    newInput.name = "answers[]";
    newInput.required = true;
    
    const newCheckbox = document.createElement("input");
    newCheckbox.className = "mr-2";
    newCheckbox.type = "checkbox";
    newCheckbox.name = "correct_answers[]";
    // Setze den Wert der Checkbox auf die Nummer der Antwort
    newCheckbox.value = answerCount;
    
    const answerWrapper = document.createElement("div");
    answerWrapper.className = "flex items-center mb-2";
    answerWrapper.appendChild(newInput);
    
    // Die Checkbox und das Label direkt nach dem Input platzieren
    answerWrapper.appendChild(newCheckbox);
    answerWrapper.appendChild(document.createTextNode("Richtig"));
    
    answersContainer.appendChild(answerWrapper);
    
    // Erhöhe die Variable answerCount um eins
    answerCount++;
  });
});



  // Get the file input element
var imageInput = document.getElementById("image");

// Get the div element to show the file info
var imageInfo = document.getElementById("image-info");

// Add an event listener for when the user selects a file
imageInput.addEventListener("change", function() {
  // Check if a file is selected
  if (this.files && this.files[0]) {
    // Get the file name and size
    var fileName = this.files[0].name;
    var fileSize = this.files[0].size;

    // Format the file size to KB or MB
    var fileSizeFormatted = "";
    if (fileSize < 1024) {
      fileSizeFormatted = fileSize + " B";
    } else if (fileSize < 1048576) {
      fileSizeFormatted = (fileSize / 1024).toFixed(2) + " KB";
    } else {
      fileSizeFormatted = (fileSize / 1048576).toFixed(2) + " MB";
    }

    // Show the file name and size in the div element
    imageInfo.textContent = fileName + " (" + fileSizeFormatted + ")";
  } else {
    // No file is selected, show a default message
    imageInfo.textContent = "Keine Datei ausgewählt";
  }
});
