function passwordunhide() {
    var x = document.getElementById("AppPasswordInput");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
};