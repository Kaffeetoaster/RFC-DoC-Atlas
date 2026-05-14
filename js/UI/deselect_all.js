const deselectAllButton = document.getElementById("deselect-all");


export function initializeDeselectAllButton() {
    deselectAllButton.addEventListener("click", () => {
    const checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change')); // trigger change event to update map
        }
    });
    });
}
