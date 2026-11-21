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

import { spreadOffsets } from "./json/marker_spread.js";

export const registry = [];

// Marker and layer of the same spawn carry the same value in this field of MapObjects.json (set by the python export).
export const LINK_FIELD = "id";

export const state = {
    enabled: new Set(),
    filters: new Map(),
};

let map = null;
const linkedMarkerCopies = new WeakSet();

export function initMapState(leafletMap) {
    map = leafletMap;
    // markers outside the view are removed, so the view changing can change what is shown
    map.on('moveend zoomend', render);
}

export function subcategoryKey(data) {
    return `${data.category}/${data.subcategory}`;
}

// options (all optional):
//   spread:  { spotKey } for markers that must not hide each other. All shown entries with the
//            same spotKey are moved apart, see render().
//   outline: leaflet objects that are only shown while a related marker is hovered, see setHighlight()
export function registerEntry(data, items, {
    spread = null,
    outline = [],
    getCopyOffsets = null,
    createCopy = null,
    updateCopy = null,
} = {}) {
    const entry = {
        data,
        items,
        key: subcategoryKey(data),
        spread,
        outline,
        offset: null,
        related: [],
        copies: new Map(),
        getCopyOffsets,
        createCopy,
        updateCopy,
    };
    registry.push(entry);
    return entry;
}

// Links every marker with the layers that have the same id and makes hovering the marker highlight them.
// Call once after all entries are registered.
export function linkRelatedEntries() {
    const byId = new Map();
    for (const entry of registry) {
        const id = entry.data[LINK_FIELD];
        if (id == null) continue;
        if (!byId.has(id)) byId.set(id, []);
        byId.get(id).push(entry);
    }

    for (const group of byId.values()) {
        const layers = group.filter(entry => entry.data.type === "layer");
        for (const marker of group.filter(entry => entry.data.type === "marker")) {
            marker.related = layers;
        }
    }
}

function linkMarkerCopy(markerEntry, item) {
    if (linkedMarkerCopies.has(item)) return;
    item.on("mouseover", () => setHighlight(markerEntry, true));
    item.on("mouseout", () => setHighlight(markerEntry, false));
    linkedMarkerCopies.add(item);
}

// Gold outline around the related layers of the marker, and all other area layers are dimmed (classes in style.css).
// A layer that is not on the map has no element yet and is skipped.
function setHighlight(markerEntry, on) {
    for (const layer of markerEntry.related) {
        for (const item of layer.items) {
            item.getElement()?.classList.toggle("area-highlight", on);
        }
        const layerShown = layer.items.some(item => map.hasLayer(item));
        for (const outline of layer.outline) {
            if (on && layerShown) outline.addTo(map);
            else outline.removeFrom(map);
        }
    }
    map.getContainer().classList.toggle("area-dim", on);
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

// Entries that are allowed (checkbox + filters) and share a spotKey are moved apart. This depends only on what is
// allowed, not on what is in the view, so the markers move when the filters change but not when panning.
function spreadEntries(allowedEntries) {
    const bySpot = new Map();
    for (const entry of allowedEntries) {
        if (!entry.spread) continue;
        if (!bySpot.has(entry.spread.spotKey)) bySpot.set(entry.spread.spotKey, []);
        bySpot.get(entry.spread.spotKey).push(entry);
    }
    for (const group of bySpot.values()) {
        const offsets = spreadOffsets(group.length);
        group.forEach((entry, index) => {
            const [dx, dy] = offsets[index];
            if (entry.offset && entry.offset[0] === dx && entry.offset[1] === dy) return;
            entry.offset = [dx, dy];
        });
    }
}

// the one place that touches the map: add/remove whatever changed.
// Markers are only added while they are (almost) inside the view; the padding keeps markers
// whose box reaches into the view from popping in late. Layers (image overlays) are not checked.
export function render() {
    const viewBounds = map.getBounds().pad(0.25);
    const allowedEntries = new Set(registry.filter(isAllowed));
    spreadEntries(allowedEntries);

    for (const entry of registry) {
        const allowed = allowedEntries.has(entry);

        // DYNAMIC COPY CHANGE: entries without copy factories keep their existing fixed items.
        if (!entry.getCopyOffsets || !entry.createCopy || !entry.updateCopy) {
            for (const item of entry.items) {
                const inView = !item.getLatLng || viewBounds.contains(item.getLatLng());
                const show = allowed && inView;
                if (show === map.hasLayer(item)) continue;
                if (show) item.addTo(map);
                else item.removeFrom(map);
            }
            continue;
        }

        const [dx, dy] = entry.offset ?? [0, 0];
        const neededOffsets = allowed ? new Set(entry.getCopyOffsets(viewBounds)) : new Set();

        entry.items = [];
        entry.outline = [];

        for (const [offset, copy] of entry.copies) {
            if (!neededOffsets.has(offset)) {
                for (const item of copy.items) item.removeFrom(map);
                for (const outline of copy.outlines) outline.removeFrom(map);
            }
        }

        for (const offset of neededOffsets) {
            let copy = entry.copies.get(offset);
            if (!copy) {
                copy = entry.createCopy(offset, dx, dy);
                entry.copies.set(offset, copy);
            } else {
                entry.updateCopy(copy, offset, dx, dy);
            }

            entry.items.push(...copy.items);
            entry.outline.push(...copy.outlines);

            for (const item of copy.items) {
                const inView = !item.getLatLng || viewBounds.contains(item.getLatLng());
                if (inView && !map.hasLayer(item)) item.addTo(map);
                else if (!inView && map.hasLayer(item)) item.removeFrom(map);

                if (dataTypeMarker(entry) && inView) linkMarkerCopy(entry, item);
            }
        }

        for (const [offset, copy] of entry.copies) {
            if (neededOffsets.has(offset)) continue;
            entry.copies.delete(offset);
        }
    }
}

function dataTypeMarker(entry) {
    return entry.data.type === "marker";
}
