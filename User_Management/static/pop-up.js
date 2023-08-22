
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('popup-modal');
    const closeModalBtn = document.getElementById("close-modal-btn");
    // Check your conditions here
    const shouldShowPopup = true; // Replace with your actual conditions


    if (shouldShowPopup) {
        modal.style.display = 'block';
    }

    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });
});
