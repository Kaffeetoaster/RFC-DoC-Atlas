
const legend = document.getElementById("legend");


function checkReligionMaps(ReligionsList) {
    const AllUnchecked = ReligionsList.every(checkbox => !checkbox.checked);
    return AllUnchecked;
}    


export function addLegendToggle(checkbox, ReligionsList) {
    checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
            legend.classList.remove("hidden");
        } else {
            if (checkReligionMaps(ReligionsList)) {
                legend.classList.add("hidden");
            }
        }
    });
}   