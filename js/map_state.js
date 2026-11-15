// Global registry of all map objects + the state that decides which of them are visible.
//
// registry: one entry per map object (marker OR layer):
//     { data: <object from MapObjects.json>, items: [leaflet objects], key }
//     items = everything that has to be added to / removed from the map together
//             (marker: centre + left/right wrap copy, layer: the 3 image overlays)
//
// state.enabled: keys of the subcategories whose checkbox is ticked
// state.filters: name -> predicate(data) => boolean. Filter UIs (bonus select, year input, ...)
//                register a predicate with setFilter(); an entry is visible only if its
//                subcategory is enabled AND every predicate returns true.

export const registry = [];

export const state = {
    enabled: new Set(),
    filters: new Map(),
};

let map = null;

export function initMapState(leafletMap) {
    map = leafletMap;
    // markers outside the view are removed, so the view changing can change what is shown
    map.on('moveend zoomend', render);
}

export function subcategoryKey(data) {
    return `${data.category}/${data.subcategory}`;
}

export function registerEntry(data, items) {
    const entry = { data, items, key: subcategoryKey(data) };
    registry.push(entry);
    return entry;
}

// called by the checkbox of a subcategory
export function setSubcategoryEnabled(key, enabled) {
    if (enabled) {
        state.enabled.add(key);
    } else {
        state.enabled.delete(key);
    }
    render();
}

// called by filter UIs. predicate(data) => true keeps the object visible; null removes the filter.
// Objects a filter does not care about (e.g. no year, no bonusType) must simply return true.
export function setFilter(name, predicate) {
    if (predicate) {
        state.filters.set(name, predicate);
    } else {
        state.filters.delete(name);
    }
    render();
}

// does the subcategory checkbox + every filter allow this map object?
function isAllowed(entry) {
    if (!state.enabled.has(entry.key)) return false;
    for (const predicate of state.filters.values()) {
        if (!predicate(entry.data)) return false;
    }
    return true;
}

// the one place that touches the map: add/remove whatever changed.
// Markers are only added while they are (almost) inside the view; the padding keeps markers
// whose box reaches into the view from popping in late. Layers (image overlays) are not checked.
export function render() {
    const viewBounds = map.getBounds().pad(0.25);
    for (const entry of registry) {
        const allowed = isAllowed(entry);
        for (const item of entry.items) {
            const inView = !item.getLatLng || viewBounds.contains(item.getLatLng());
            const show = allowed && inView;
            if (show === map.hasLayer(item)) continue;
            if (show) item.addTo(map);
            else item.removeFrom(map);
        }
    }
}
