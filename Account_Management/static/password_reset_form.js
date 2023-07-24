document.addEventListener("DOMContentLoaded", function() {

    function handleLabel(field, labelId) {
        const inputField = document.getElementById(field);
        const label = document.getElementById(labelId);
        console.log(inputField);
        inputField.addEventListener("input", function() {
            if (inputField.value.trim() !== "") {
                label.style.display = "none";
            } else {
                label.style.display = "inline-block";
            }
        });
    }
    handleLabel("id_new_password1", "password1_label");
    handleLabel("id_new_password2", "password2_label");

});
