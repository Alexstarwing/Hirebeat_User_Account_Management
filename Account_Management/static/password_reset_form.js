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
    
handleLabel("{{ form.new_password1.id_for_label }}", "password1_label");
handleLabel("{{ form.new_password2.id_for_label }}", "password2_label");