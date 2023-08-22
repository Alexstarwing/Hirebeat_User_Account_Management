
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('popup-modal');
    const closeModalBtn = document.getElementById("submit-button");
    const updateCompanyForm = document.getElementById("update-company-form");
    // Check your conditions here
    const shouldShowPopup = true; // Replace with your actual conditions


    if (shouldShowPopup) {
        modal.style.display = 'block';
    }

    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
        updateCompanyForm.submit();
    });
});
