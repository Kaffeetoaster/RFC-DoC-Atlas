import { addLegendToggle } from "../UI/legend.js";

const bonusSelect = document.getElementById("bonus-select");


function setBonusSelectVisibility(categoryCheckboxes) {
    const anyCategoryEnabled = Object.values(categoryCheckboxes).some(checkbox => checkbox.checked);
    bonusSelect.classList.toggle("hidden", !anyCategoryEnabled);
}

function updateMarkerVisibility(marker, shouldShow, map, mapBounds) {
    const isInBounds = mapBounds.contains(marker.getLatLng());

    if (shouldShow && isInBounds) {
        marker.addTo(map);
    } else {
        marker.removeFrom(map);
    }
}

function refreshBonusMarkers(categoryCheckboxes, markersBySubcategory, markersBySubcategoryAndBonusType, map) {
    const selectedBonusType = bonusSelect.value;
    const mapBounds = map.getBounds();

    Object.entries(markersBySubcategory).forEach(([categoryName, markers]) => {
        const categoryCheckbox = categoryCheckboxes[categoryName];
        const categoryEnabled = Boolean(categoryCheckbox && categoryCheckbox.checked);

        if (!categoryEnabled) {
            markers.forEach(marker => marker.removeFrom(map));
            return;
        }

        if (selectedBonusType === "all") {
            markers.forEach(marker => updateMarkerVisibility(marker, true, map, mapBounds));
            return;
        }

        const markersByBonusType = markersBySubcategoryAndBonusType[categoryName] || {};
        const allowedMarkers = new Set(markersByBonusType[selectedBonusType] || []);

        markers.forEach(marker => {
            updateMarkerVisibility(marker, allowedMarkers.has(marker), map, mapBounds);
        });
    });

    setBonusSelectVisibility(categoryCheckboxes);
}

function setIconSize(spawnData) {
    let countlinebreaks = (spawnData.text.match(/\n/g) || []).length;
    if (spawnData.text.includes('\n')) {
        return [170, 108 + (countlinebreaks * 18)]; // create multiple lines
    } else if (spawnData.text =='') {
        return [170, 90]; // no text
    } else {
        return [170, 108]; // default size for all markers
    }
}
function setIconAnchor(iconSize, direction) {
    if (direction === 'arrow-top') {
        return [iconSize[0]/2, -7]; // anchor at top center of the icon
    }
    return [iconSize[0]/2, iconSize[1]-7]; // anchor at bottom center of the icon
}

function createDivIcon(spawnData) {
    const direction = (spawnData.spawn === false || spawnData.category === "Terrain changes") ? 'arrow-top' : 'arrow-bottom';
    const iconSize = setIconSize(spawnData);
    const anchor = setIconAnchor(iconSize, direction);
    const markerClass = spawnData.spawn ? 'marker-spawn' : 'marker-despawn';

    if (direction === 'arrow-top') {
         return L.divIcon({
                className: 'custom-marker',
                html: `<div class="marker-box">
                <div class="marker-arrow-top"></div>
                <img src="${spawnData.source}" class="${markerClass}" />
                <span class="marker-text">${spawnData.text.replace(' - ', '\n')}</span>
                </div>`,
                iconSize: iconSize,
                iconAnchor: anchor
            });
    } else {
        return L.divIcon({
                    className: 'custom-marker',
                    html: `<div class="marker-box">
                    <img src="${spawnData.source}" class="${markerClass}" />
                    <span class="marker-text">${spawnData.text.replace(' - ', '\n')}</span>
                    <div class="marker-arrow-bottom"></div>
                    </div>`,
                    iconSize: iconSize,
                    iconAnchor: anchor
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

function addLayerToggle(checkbox, imageOverlay, imageOverlayLeft, imageOverlayRight, map) {
    checkbox.addEventListener('change', function() {
            if (this.checked) {
                imageOverlay.addTo(map);
                imageOverlayLeft.addTo(map);
                imageOverlayRight.addTo(map);
            } else {
                imageOverlay.removeFrom(map);
                imageOverlayLeft.removeFrom(map);
                imageOverlayRight.removeFrom(map);
            }
            });
}







export function loadMapObjects(map, GAME_TILE_SIZE, width, height, MAP_OFFSET) {
    // Load markers from JSON and create tooltips
    console.log('Starting to fetch MapObjects.json...');
    fetch('json/MapObjects.json')
    .then(response => {
        console.log('Response received:', response.status);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log('JSON loaded successfully. Total number of MapObjects:', data.length);
        const container = document.querySelector('.options-container');

        // create a nested structure of categories and subcategories
        const categories = {};
        for (const mapObject of data) {
            if (!categories[mapObject.category]) {
                categories[mapObject.category] = {};
            }
            if (!categories[mapObject.category][mapObject.subcategory]) {
                categories[mapObject.category][mapObject.subcategory] = [];
            }
            categories[mapObject.category][mapObject.subcategory].push(mapObject);
        }
        console.log('Categories created:', Object.keys(categories));
        // sort the categories and subcategories alphabetically
        const sortedCategories = {};
        for (const category of Object.keys(categories).sort()) {
            sortedCategories[category] = {};

            for (const subcategory of Object.keys(categories[category]).sort()) {
                sortedCategories[category][subcategory] =
                    categories[category][subcategory];
            }
        }

        // Store markers by category and bonus type, plus their checkboxes for use in filtering and toggling visibility
        const markersBySubcategory = {};
        const subcategoryCheckboxes = {};
        const markersBySubcategoryAndBonusType = {};
        const possibleBonusTypes = new Set();

        // create the HTML structure for the categories and subcategories
        for (const [category, subcategories] of Object.entries(sortedCategories)) {
            const details = document.createElement('details');
            const summary = document.createElement('summary');
            summary.textContent = category;
            details.appendChild(summary);

            // Religions get a Legend
            let ReligionsList = [];
            if (category === "Religion") {
                ReligionsList.push(checkbox);
            }

            for (const [subcategory, mapObjects] of Object.entries(subcategories)) {
                //create checkbox for subcategory
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

                label.appendChild(checkbox);
                label.appendChild(checkmark);
                label.appendChild(text);
                details.appendChild(label);

                // Store the checkbox for later use in filtering and toggling visibility
                subcategoryCheckboxes[subcategory] = checkbox;
                markersBySubcategory[subcategory] = [];
                markersBySubcategoryAndBonusType[subcategory] = {};

                for (const mapObject of mapObjects) {
                    if (mapObject.type == "marker") {
                        // create marker
                        const lat = GAME_TILE_SIZE * (mapObject.y) + GAME_TILE_SIZE / 2 + MAP_OFFSET;
                        const lng = GAME_TILE_SIZE * (mapObject.x) + GAME_TILE_SIZE / 2;
                        // Create markers for center, left wrap (-7800), and right wrap (+7800)
                        const positionsToCreate = [
                            { lat: lat, lng: lng },
                            { lat: lat, lng: lng + width },
                            { lat: lat, lng: lng - width }
                        ];

                        positionsToCreate.forEach(position => {
                            const divIcon = createDivIcon(mapObject);

                            const marker = L.marker([position.lat, position.lng], { icon: divIcon });
                            markersBySubcategory[subcategory].push(marker);
                            if (mapObject.bonusType) {
                                possibleBonusTypes.add(mapObject.bonusType);
                                if (!markersBySubcategoryAndBonusType[subcategory][mapObject.bonusType]) {
                                    markersBySubcategoryAndBonusType[subcategory][mapObject.bonusType] = [];
                                }
                                markersBySubcategoryAndBonusType[subcategory][mapObject.bonusType].push(marker);
                            }

                        });

                    }
                    else if (mapObject.type == "layer") {
                        // create layer
                        const {
                            imageOverlay,
                            imageOverlayLeft,
                            imageOverlayRight
                        } = createMapLayer(mapObject, GAME_TILE_SIZE, width, MAP_OFFSET);
                        // Toggle overlay on checkbox change
                        addLayerToggle(checkbox, imageOverlay, imageOverlayLeft, imageOverlayRight, map);
                    }
                }
                // Add event listener to checkbox to toggle visibility of markers
                checkbox.addEventListener('change', function() {
                    refreshBonusMarkers(subcategoryCheckboxes, markersBySubcategory, markersBySubcategoryAndBonusType, map);
                });
            }

            for (const checkbox of ReligionsList) {
                addLegendToggle(checkbox, ReligionsList);
            }
            bonusSelect.addEventListener("change", () => refreshBonusMarkers(subcategoryCheckboxes, markersBySubcategory, markersBySubcategoryAndBonusType, map));
            map.on('moveend zoomend', () => {
                refreshBonusMarkers(subcategoryCheckboxes, markersBySubcategory, markersBySubcategoryAndBonusType, map);
            });
            
            container.appendChild(details);
        }
    });
    
}