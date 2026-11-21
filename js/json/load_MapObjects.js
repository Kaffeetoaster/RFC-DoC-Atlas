import { addLegendToggle } from "../UI/legend.js";
import { addBonusFilter, initializeBonusFilter } from "../UI/bonus_filter.js";
import { addYearFilter, initializeYearFilter } from "../UI/year_filter.js";
import { initMapState, registerEntry, setSubcategoryEnabled, subcategoryKey, linkRelatedEntries, LINK_FIELD } from "../map_state.js";




// Only the markers of this category are spread out when several of them are shown on exactly the same spot,
// see spreadOffsets() in marker_spread.js and render() in map_state.js
const SPREAD_CATEGORY = "Barbarian spawns and City spawns";

function createDivIcon(spawnData) {
    const direction = (spawnData.spawn === false || spawnData.category === "Terrain changes") ? 'arrow-top' : 'arrow-bottom';
    const markerClass = spawnData.spawn ? 'marker-spawn' : 'marker-despawn';
    const onlyText = spawnData.source=="" ? true : false;

    const imghtml = onlyText ? "" : `<img src="${spawnData.source}" class="${markerClass}" />`;

    if (direction === 'arrow-top') {
         return L.divIcon({
                className: 'custom-marker marker-anchor-top',
                html: `<div class="marker-box">
                <div class="marker-arrow-top"></div>
                ${imghtml}
                <span class="marker-text">${spawnData.text.replace(' - ', '\n')}</span>
                </div>`,
                iconSize: [0, 0],
                iconAnchor: [0, 0]
            });
    } else {
        return L.divIcon({
                    className: 'custom-marker marker-anchor-bottom',
                    html: `<div class="marker-box">
                    ${imghtml}
                    <span class="marker-text">${spawnData.text.replace(' - ', '\n')}</span>
                    <div class="marker-arrow-bottom"></div>
                    </div>`,
                    iconSize: [0, 0],
                    iconAnchor: [0, 0]
                });
    }
}

function createMapLayer(layerData, GAME_TILE_SIZE, width, MAP_OFFSET) {
    // Create the image overlay
    const lat = GAME_TILE_SIZE * (layerData.y) + MAP_OFFSET;
    const lng = GAME_TILE_SIZE * (layerData.x);
    
    // Layers that belong to a marker (they have an id) get the class "area-layer": the hovered marker highlights
    // its area and dims all other area layers, see style.css
    const options = {};
    if (layerData.subcategory === "Birth") options.pane = "OutlinePane";
    if (layerData[LINK_FIELD] != null) options.className = "area-layer";

    // DYNAMIC COPY CHANGE: calculate only the world offsets whose overlay could intersect the view.
    const getCopyOffsets = viewBounds => {
        const west = viewBounds.getWest();
        const east = viewBounds.getEast();
        const kMin = Math.floor((west - lng - layerData.w) / width);
        const kMax = Math.ceil((east - lng) / width);
        const offsets = [];
        for (let k = kMin; k <= kMax; k++) offsets.push(k);
        return offsets;
    };

    const makeBounds = k => [
        [lat, lng + k * width],
        [lat + layerData.h, lng + layerData.w + k * width],
    ];

    const createCopy = k => {
        const copyBounds = makeBounds(k);
        const imageOverlay = L.imageOverlay(layerData.source, copyBounds, options);
        const outlines = layerData[LINK_FIELD] != null
            ? [L.rectangle(copyBounds, {
                pane: "OutlinePane",
                className: "area-outline",
                color: "#ffcc66",
                weight: 3,
                fill: false,
                interactive: false,
            })]
            : [];
        return { items: [imageOverlay], outlines };
    };

    const updateCopy = (copy, k) => {
        const copyBounds = makeBounds(k);
        copy.items[0].setBounds(copyBounds);
        for (const outline of copy.outlines) outline.setBounds(copyBounds);
    };

    return { getCopyOffsets, createCopy, updateCopy };
}

// Dynamic marker copies are added to the registry by world offset.
// Spread offsets move all visible copies by dx/dy game tiles.
function createMarkerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET) {
    const lat = GAME_TILE_SIZE * mapObject.y + GAME_TILE_SIZE / 2 + MAP_OFFSET;
    const lng = GAME_TILE_SIZE * mapObject.x + GAME_TILE_SIZE / 2;
    // DYNAMIC COPY CHANGE: marker offsets are calculated from the current view.
    const getCopyOffsets = viewBounds => {
        const west = viewBounds.getWest();
        const east = viewBounds.getEast();
        const kMin = Math.floor((west - lng) / width) - 1;
        const kMax = Math.ceil((east - lng) / width) + 1;
        const offsets = [];
        for (let k = kMin; k <= kMax; k++) offsets.push(k);
        return offsets;
    };

    const createCopy = (k, dx = 0, dy = 0) => {
        const item = L.marker([
            lat + dy * GAME_TILE_SIZE,
            lng + k * width + dx * GAME_TILE_SIZE,
        ], { icon: createDivIcon(mapObject) });
        return { items: [item], outlines: [] };
    };

    const updateCopy = (copy, k, dx = 0, dy = 0) => {
        copy.items[0].setLatLng([
            lat + dy * GAME_TILE_SIZE,
            lng + k * width + dx * GAME_TILE_SIZE,
        ]);
    };

    return { getCopyOffsets, createCopy, updateCopy };
}

function createLayerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET) {
    return createMapLayer(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET);
}

// category -> subcategory -> [mapObjects]  (keeps the order of the json)
function groupByCategory(data) {
    const categories = {};
    for (const mapObject of data) {
        categories[mapObject.category] ??= {};
        categories[mapObject.category][mapObject.subcategory] ??= [];
        categories[mapObject.category][mapObject.subcategory].push(mapObject);
    }
    return categories;
}

// one checkbox per subcategory; it only tells the state to enable/disable that subcategory
function createSubcategoryCheckbox(subcategory, key) {
    const label = document.createElement('label');
    label.className = 'checkbox-container';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = false;

    const checkmark = document.createElement('span');
    checkmark.className = 'checkmark';

    const text = document.createElement('span');
    text.className = 'label-text';
    text.textContent = subcategory;

    label.append(checkbox, checkmark, text);

    checkbox.addEventListener('change', () => setSubcategoryEnabled(key, checkbox.checked));
    return { label, checkbox };
}

export function loadMapObjects(map, GAME_TILE_SIZE, width, height, MAP_OFFSET) {
    initMapState(map);

    fetch('json/MapObjects.json')
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log('MapObjects loaded:', data.length);
        const container = document.querySelector('.options-container');
        const checkboxesByCategory = {};

        // all bonus types / categories that can be selected in the bonus filter
        const bonusTypes = new Set();
        for (const mapObject of data) {
            if (mapObject.bonusType) bonusTypes.add(mapObject.bonusType);
            if (mapObject.bonusCategory) bonusTypes.add(mapObject.bonusCategory);
        }
        initializeBonusFilter(bonusTypes);

        // year range that can be selected in the year filter
        const years = data.flatMap(mapObject => mapObject.time_frame ?? []).filter(year => year != null);
        const hasYears = years.length > 0;
        if (hasYears) initializeYearFilter(Math.min(...years), Math.max(...years));

        // A filter belongs to every subcategory checkbox that contains objects the filter works on.
        // The filter UI is shown while one of these checkboxes is ticked.
        const bonusCheckboxes = [];
        const yearCheckboxes = [];

        for (const [category, subcategories] of Object.entries(groupByCategory(data))) {
            const details = document.createElement('details');
            const summary = document.createElement('summary');
            summary.textContent = category;
            details.appendChild(summary);
            checkboxesByCategory[category] = [];

            for (const [subcategory, mapObjects] of Object.entries(subcategories)) {
                // build the map objects of this subcategory and put them into the registry
                for (const mapObject of mapObjects) {
                    if (mapObject.type === "marker") {
                        const { getCopyOffsets, createCopy, updateCopy } =
                            createMarkerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET);
                        const spread = mapObject.category === SPREAD_CATEGORY
                            ? { spotKey: `${mapObject.x},${mapObject.y}` }
                            : null;
                        // DYNAMIC COPY CHANGE: register copy factories instead of fixed marker objects.
                        registerEntry(mapObject, [], { spread, getCopyOffsets, createCopy, updateCopy });
                    } else if (mapObject.type === "layer") {
                        const { getCopyOffsets, createCopy, updateCopy } =
                            createLayerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET);
                        // DYNAMIC COPY CHANGE: register copy factories instead of fixed image overlays.
                        registerEntry(mapObject, [], { getCopyOffsets, createCopy, updateCopy });
                    }
                }

                const { label, checkbox } = createSubcategoryCheckbox(subcategory, subcategoryKey(mapObjects[0]));
                details.appendChild(label);
                checkboxesByCategory[category].push(checkbox);

                if (mapObjects.some(mapObject => mapObject.bonusType || mapObject.bonusCategory)) {
                    bonusCheckboxes.push(checkbox);
                }
                if (mapObjects.some(mapObject => mapObject.time_frame)) {
                    yearCheckboxes.push(checkbox);
                }
            }

            // category specific UI that only needs to know about the checkboxes
            if (category === "Religions") {
                for (const checkbox of checkboxesByCategory[category]) {
                    addLegendToggle(checkbox, checkboxesByCategory[category]);
                }
            }


            container.appendChild(details);
        }

        // markers and layers with the same id belong together (hovering the marker highlights the layer)
        linkRelatedEntries();

        for (const checkbox of bonusCheckboxes) addBonusFilter(checkbox, bonusCheckboxes);
        if (hasYears) {
            for (const checkbox of yearCheckboxes) addYearFilter(checkbox, yearCheckboxes);
        }
    });
}
