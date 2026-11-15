const legend = document.getElementById("legend");



export function addLegendToggle(checkbox, ReligionsList) {
    checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
            legend.classList.remove("hidden");
        } else {
            if (ReligionsList.every(checkbox => !checkbox.checked)) {
                legend.classList.add("hidden");
            }
        }
    });
}   