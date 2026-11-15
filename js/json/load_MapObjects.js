import { addLegendToggle } from "../UI/legend.js";
import { addBonusFilter, initializeBonusFilter } from "../UI/bonus_filter.js";
import { initMapState, registerEntry, setSubcategoryEnabled, subcategoryKey } from "../map_state.js";




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
    const bounds = [[lat, lng], [lat + layerData.h, lng + layerData.w]];
    const boundsLeft = [[lat, lng - width], [lat + layerData.h, lng + layerData.w - width]];
    const boundsRight = [[lat, lng + width], [lat + layerData.h, lng + layerData.w + width]];
    
    let imageOverlay, imageOverlayLeft, imageOverlayRight;
    if (layerData.subcategory === "Birth") {
    imageOverlay = L.imageOverlay(layerData.source, bounds, {pane: "OutlinePane"});
    imageOverlayLeft = L.imageOverlay(layerData.source, boundsLeft, {pane: "OutlinePane"});
    imageOverlayRight = L.imageOverlay(layerData.source, boundsRight, {pane: "OutlinePane"});
    
    } else {
    imageOverlay = L.imageOverlay(layerData.source, bounds);
    imageOverlayLeft = L.imageOverlay(layerData.source, boundsLeft);
    imageOverlayRight = L.imageOverlay(layerData.source, boundsRight);
    }
    return { imageOverlay, imageOverlayLeft, imageOverlayRight };

}

// Leaflet objects of one map object. Everything in the array is added/removed together.
function createMarkerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET) {
    const lat = GAME_TILE_SIZE * mapObject.y + GAME_TILE_SIZE / 2 + MAP_OFFSET;
    const lng = GAME_TILE_SIZE * mapObject.x + GAME_TILE_SIZE / 2;
    // centre, left wrap and right wrap copy
    return [lng, lng + width, lng - width].map(
        wrappedLng => L.marker([lat, wrappedLng], { icon: createDivIcon(mapObject) })
    );
}

function createLayerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET) {
    const { imageOverlay, imageOverlayLeft, imageOverlayRight } =
        createMapLayer(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET);
    return [imageOverlay, imageOverlayLeft, imageOverlayRight];
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
                        registerEntry(mapObject, createMarkerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET));
                    } else if (mapObject.type === "layer") {
                        registerEntry(mapObject, createLayerItems(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET));
                    }
                }

                const { label, checkbox } = createSubcategoryCheckbox(subcategory, subcategoryKey(mapObjects[0]));
                details.appendChild(label);
                checkboxesByCategory[category].push(checkbox);
            }

            // category specific UI that only needs to know about the checkboxes
            if (category === "Religion") {
                for (const checkbox of checkboxesByCategory[category]) {
                    addLegendToggle(checkbox, checkboxesByCategory[category]);
                }
            }
            if (category === "Resource spawns and despawns") {
                for (const checkbox of checkboxesByCategory[category]) {
                    addBonusFilter(checkbox, checkboxesByCategory[category]);
                }
            }
            if (category === "Barbarian spawns") {
                for (const checkbox of checkboxesByCategory[category]) {
                    addYearFilter(checkbox, checkboxesByCategory[category]);
                }
            }


            container.appendChild(details);
        }
    });
}
