import { setFilter } from "../map_state.js";

const filterBox = document.getElementById("bonus-filter");
const toggleButton = document.getElementById("bonus-filter-toggle");
const panel = document.getElementById("bonus-filter-panel");
const searchInput = document.getElementById("bonus-filter-search");
const list = document.getElementById("bonus-filter-list");
const selectedList = document.getElementById("bonus-filter-selected");   // ticked options are pinned here

const header = document.getElementById("bonus-filter-header");     // only visible in portrait mode
const isPortrait = window.matchMedia("(orientation: portrait)");

const selected = new Set();     // ticked bonus types / categories
let optionCheckboxes = [];

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1);
}

// hides the options in the list that do not contain the search text (pinned, ticked options stay visible)
function filterOptions() {
    const query = searchInput.value.trim().toLowerCase();
    for (const label of list.children) {
        label.hidden = !label.textContent.toLowerCase().includes(query);
    }
}

// moves an unticked option back to its original place in the sorted list
function putBackInList(label) {
    const position = Number(label.dataset.position);
    const next = [...list.children].find(other => Number(other.dataset.position) > position);
    list.insertBefore(label, next ?? null);
}

function setPanelOpen(open) {
    panel.classList.toggle("hidden", !open);
    toggleButton.setAttribute("aria-expanded", String(open));
}

// nothing ticked = no filter. Otherwise show every object that matches one of the ticked entries.
// Objects without a bonus (other categories) are not affected by this filter.
function applyFilter() {
    setFilter("bonus", selected.size === 0 ? null : data =>
        (!data.bonusType && !data.bonusCategory) ||
        selected.has(data.bonusType) ||
        selected.has(data.bonusCategory)
    );
}

function resetFilter() {
    optionCheckboxes.forEach(checkbox => { checkbox.checked = false; });
    [...selectedList.children].forEach(putBackInList);
    selected.clear();
    applyFilter();
}

// the filter button is only shown while at least one of the given checkboxes is ticked;
// when it gets hidden all filters are reset
function updateVisibility(checkboxes) {
    const anyChecked = checkboxes.some(checkbox => checkbox.checked);
    const wasHidden = filterBox.classList.contains("hidden");
    filterBox.classList.toggle("hidden", !anyChecked);

    // first bonus checkbox ticked: show the options. Not in portrait mode, where the panel covers the
    // whole screen and the user is still picking checkboxes in the (also full screen) sidebar.
    if (anyChecked && wasHidden) {
        if (!isPortrait.matches) setPanelOpen(true);
    } else if (!anyChecked) {
        setPanelOpen(false);
        searchInput.value = "";
        filterOptions();
        if (selected.size > 0) resetFilter();
    }
}

export function addBonusFilter(checkbox, checkboxes) {
    checkbox.addEventListener("change", () => updateVisibility(checkboxes));
}

// builds one checkbox per bonus type / category
export function initializeBonusFilter(bonusTypes) {
    // order: health, happiness, general, then everything else alphabetically
    const pinned = ["health", "happiness", "general"].filter(value => bonusTypes.has(value));
    const others = [...bonusTypes]
        .filter(value => !pinned.includes(value))
        .sort((a, b) => a.localeCompare(b));

    list.innerHTML = "";
    selectedList.innerHTML = "";
    optionCheckboxes = [];
    for (const value of [...pinned, ...others]) {
        const label = document.createElement("label");
        label.className = "checkbox-container";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";

        const checkmark = document.createElement("span");
        checkmark.className = "checkmark";

        const text = document.createElement("span");
        text.className = "label-text";
        text.textContent = capitalize(value);

        label.append(checkbox, checkmark, text);
        list.appendChild(label);
        optionCheckboxes.push(checkbox);

        const position = optionCheckboxes.length - 1;   // original place in the sorted list
        label.dataset.position = position;

        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                selected.add(value);
                selectedList.appendChild(label);        // pin under the search bar
            } else {
                selected.delete(value);
                putBackInList(label);
            }
            filterOptions();
            applyFilter();
        });
    }

    searchInput.addEventListener("input", filterOptions);

    // portrait mode: the title of the full screen panel closes it
    header.addEventListener("click", () => setPanelOpen(false));

    // open/close only with the funnel button
    toggleButton.addEventListener("click", () => setPanelOpen(panel.classList.contains("hidden")));
}
