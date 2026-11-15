import { setFilter } from "../map_state.js";

const bonusSelect = document.getElementById("bonus-select");

// the select is only shown while at least one of the given checkboxes is ticked;
// when it gets hidden it is reset to "all" (the change event removes the filter)
function updateBonusSelectVisibility(checkboxes) {
    const anyChecked = checkboxes.some(checkbox => checkbox.checked);
    bonusSelect.classList.toggle("hidden", !anyChecked);

    if (!anyChecked && bonusSelect.value !== "all") {
        bonusSelect.value = "all";
        bonusSelect.dispatchEvent(new Event("change"));
    }
}

export function addBonusFilter(checkbox, checkboxes) {
    checkbox.addEventListener("change", () => updateBonusSelectVisibility(checkboxes));
}

// fills the select with the given bonus types and filters the map objects with it
export function initializeBonusSelect(bonusTypes) {
    // order: all, health, happiness, then everything else alphabetically
    const pinned = ["all", "health", "happiness"].filter(value => value === "all" || bonusTypes.has(value));
    const others = [...bonusTypes]
        .filter(value => !pinned.includes(value))
        .sort((a, b) => a.localeCompare(b));

    bonusSelect.innerHTML = "";
    for (const value of [...pinned, ...others]) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value.charAt(0).toUpperCase() + value.slice(1);
        bonusSelect.appendChild(option);
    }

    bonusSelect.addEventListener("change", () => {
        const selected = bonusSelect.value;
        // objects without a bonus (other categories) are not affected by this filter
        setFilter("bonus", selected === "all" ? null : data =>
            (!data.bonusType && !data.bonusCategory) ||
            data.bonusType === selected ||
            data.bonusCategory === selected
        );
    });
}
