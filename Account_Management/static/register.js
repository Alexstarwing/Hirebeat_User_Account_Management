function handleLabel(field, labelId) {
    const inputField = document.getElementById(field);
    const label = document.getElementById(labelId);

    inputField.addEventListener("input", function() {
        if (inputField.value.trim() !== "") {
            label.style.display = "none";
        } else {
            label.style.display = "inline-block";
        }
    });
}
    