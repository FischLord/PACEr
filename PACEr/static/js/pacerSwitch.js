window.onload = function () {
  const toggleSwitch = document.getElementById("toggle-switch");
  toggleSwitch.addEventListener("change", function (event) {
    const isChecked = event.target.checked;
    setTimeout(function () {
      if (isChecked) {
        window.location.href = "/pacer";
      } else {
        window.location.href = "/pacerOld";
      }
    }, 100);
  });
};
