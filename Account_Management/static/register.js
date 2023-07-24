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
handleLabel("{{ form.username.id_for_label }}", "username_label");
handleLabel("{{ form.email.id_for_label }}", "email_label");
handleLabel("{{ form.password1.id_for_label }}", "password1_label");
handleLabel("{{ form.password2.id_for_label }}", "password2_label");