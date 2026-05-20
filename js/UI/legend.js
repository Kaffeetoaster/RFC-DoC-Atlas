
const legend = document.getElementById("legend");


export function addLegendToggle(checkbox) {
    checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
            legend.classList.remove("hidden");
        } else {
            legend.classList.add("hidden");
        }
    });
}   