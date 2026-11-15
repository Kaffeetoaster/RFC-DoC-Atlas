import { setFilter } from "../map_state.js";

// The bar is not linear: early years are squeezed together (big steps), late years are stretched
// (small steps), because most map objects are in the later years.
// handle position (0..1) = ((year - min) / (max - min)) ^ CURVE      1 = linear, bigger = more stretched at the end
// CURVE 2 puts the middle of the bar at around year 550 for a range of -3000 to 2025.
const CURVE = 2;
const SLIDER_MAX = 1000;        // the range inputs go from 0 to SLIDER_MAX

const filterBox = document.getElementById("year-filter");
const startNumber = document.getElementById("year-start");
const endNumber = document.getElementById("year-end");
const startRange = document.getElementById("year-range-start");
const endRange = document.getElementById("year-range-end");
const fill = document.getElementById("year-fill");

let minYear = 0;
let maxYear = 0;
let startYear = 0;
let endYear = 0;

function clamp(value, low, high) {
    return Math.min(Math.max(value, low), high);
}

function yearToPosition(year) {
    const share = (year - minYear) / (maxYear - minYear || 1);
    return Math.round(share ** CURVE * SLIDER_MAX);
}

function positionToYear(position) {
    const share = (position / SLIDER_MAX) ** (1 / CURVE);
    return Math.round(minYear + share * (maxYear - minYear));
}

// writes the current range into all controls and (un)sets the map filter
function applyRange() {
    const startPosition = yearToPosition(startYear);
    const endPosition = yearToPosition(endYear);

    startNumber.value = startYear;
    endNumber.value = endYear;
    // do not touch a handle that is being dragged (would make it jitter by rounding)
    if (startRange.valueAsNumber !== startPosition) startRange.value = startPosition;
    if (endRange.valueAsNumber !== endPosition) endRange.value = endPosition;

    fill.style.left = `${startPosition / SLIDER_MAX * 100}%`;
    fill.style.width = `${(endPosition - startPosition) / SLIDER_MAX * 100}%`;

    // when both handles are in the right half, the start handle must be on top or it could not be moved
    startRange.style.zIndex = startPosition > SLIDER_MAX / 2 ? 3 : 1;

    if (startYear === minYear && endYear === maxYear) {
        setFilter("year", null);    // whole range = no filter
        return;
    }
    setFilter("year", data => {
        if (!data.time_frame) return true;
        const objectStart = data.time_frame[0] ?? -Infinity;
        const objectEnd = data.time_frame[1] ?? Infinity;
        return objectStart <= endYear && objectEnd >= startYear;
    });
}

function setStart(year) {
    startYear = clamp(Math.round(year), minYear, endYear);
    applyRange();
}

function setEnd(year) {
    endYear = clamp(Math.round(year), startYear, maxYear);
    applyRange();
}

// number inputs: apply when the user is done typing; invalid input is replaced by the current value
function numberInputHandler(setter) {
    return event => {
        const value = parseInt(event.target.value, 10);
        if (Number.isNaN(value)) applyRange();
        else setter(value);
    };
}

// the bar is only shown while at least one of the given checkboxes is ticked;
// when it gets hidden the range is reset to everything
function updateVisibility(checkboxes) {
    const anyChecked = checkboxes.some(checkbox => checkbox.checked);
    filterBox.classList.toggle("hidden", !anyChecked);
    if (!anyChecked) {
        startYear = minYear;
        endYear = maxYear;
        applyRange();
    }
}

export function addYearFilter(checkbox, checkboxes) {
    checkbox.addEventListener("change", () => updateVisibility(checkboxes));
}

// minimum and maximum year of all map objects
export function initializeYearFilter(min, max) {
    minYear = startYear = min;
    maxYear = endYear = max;

    for (const input of [startNumber, endNumber]) {
        input.min = min;
        input.max = max;
    }
    for (const input of [startRange, endRange]) {
        input.min = 0;
        input.max = SLIDER_MAX;
    }

    startRange.addEventListener("input", () => setStart(positionToYear(startRange.valueAsNumber)));
    endRange.addEventListener("input", () => setEnd(positionToYear(endRange.valueAsNumber)));
    startNumber.addEventListener("change", numberInputHandler(setStart));
    endNumber.addEventListener("change", numberInputHandler(setEnd));
    applyRange();
}
