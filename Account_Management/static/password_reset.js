const emailInput = document.getElementById("{{ form.email.id_for_label }}");
    const defaultEmailLabel = document.querySelector("label[for=id_email]");

    emailInput.addEventListener("input", function() {
        if (emailInput.value.trim() !== "") {
            defaultEmailLabel.style.display = "none";
        } else {
            defaultEmailLabel.style.display = "inline-block";
        }
    });