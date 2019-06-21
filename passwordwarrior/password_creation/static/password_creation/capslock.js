var input = document.getElementById("fieldCaps");
var text = document.getElementById("warningText");
input.addEventListener("keyup", function (event) {
    if (event.getModifierState("CapsLock")) {
        text.style.display = "block";
    } else {
        text.style.display = "none"
    }
});