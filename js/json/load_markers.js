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

function refreshBonusMarkers(categoryCheckboxes, markersByCategory, markersByCategoryAndBonusType, map) {
    const selectedBonusType = bonusSelect.value;
    const mapBounds = map.getBounds();

    Object.entries(markersByCategory).forEach(([categoryName, markers]) => {
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

        const markersByBonusType = markersByCategoryAndBonusType[categoryName] || {};
        const allowedMarkers = new Set(markersByBonusType[selectedBonusType] || []);

        markers.forEach(marker => {
            updateMarkerVisibility(marker, allowedMarkers.has(marker), map, mapBounds);
        });
    });

    setBonusSelectVisibility(categoryCheckboxes);
}


function setIconSize(spawnData) {
    if (spawnData.text.includes(' - ')) {
        return [170, 126]; // create two lines
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

export function loadMarkers(map, GAME_TILE_SIZE, width, height, MAP_OFFSET) {
    // Load markers from JSON and create tooltips
    console.log('Starting to fetch markers.json...');
    fetch('json/markers.json')
    .then(response => {
        console.log('Response received:', response.status);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log('JSON loaded successfully. Total number of markers:', data.length);
        const container = document.querySelector('.options-container');
        
        if (!container) {
        console.error('ERROR: .options-container not found in HTML!');
        return;
        }
        
        const categories = {};
        
        // Group by category from ALL lists in the JSON
        
        data.spawns_and_despawns.forEach(spawn => {
        if (!categories[spawn.category]) {
            categories[spawn.category] = [];
        }
        categories[spawn.category].push(spawn);
        });
        
        
        
        console.log('Categories created:', Object.keys(categories));
        
        // Create main category details
        const details = document.createElement('details');
        const summary = document.createElement('summary');
        summary.textContent = 'Map markers';
        details.appendChild(summary);
        
        // Store markers by category and bonus type, plus their checkboxes.
        const markersByCategory = {};
        const categoryCheckboxes = {};
        const markersByCategoryAndBonusType = {};
        // For each subcategory
        Object.keys(categories).forEach(categoryName => {

        console.log('Creating subcategory:', categoryName, 'with', categories[categoryName].length, 'spawns/despawns');
        
        markersByCategory[categoryName] = [];
        markersByCategoryAndBonusType[categoryName] = {};
        // Create checkbox for subcategory
        const label = document.createElement('label');
        label.className = 'checkbox-container';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.dataset.category = categoryName;
        checkbox.checked = false;
        categoryCheckboxes[categoryName] = checkbox;
        
        const checkmark = document.createElement('span');
        checkmark.className = 'checkmark';
        
        const text = document.createElement('span');
        text.className = 'label-text';
        text.textContent = categoryName;
        
        label.appendChild(checkbox);
        label.appendChild(checkmark);
        label.appendChild(text);
        details.appendChild(label);
        
        // For each spawn in subcategory - create markers with divIcon
        // also create lookup tables for each category for the markers by lat,lng
        categories[categoryName].forEach(spawnData => {
            const lat = GAME_TILE_SIZE * (spawnData.y) + GAME_TILE_SIZE / 2 + MAP_OFFSET;
            const lng = GAME_TILE_SIZE * (spawnData.x) + GAME_TILE_SIZE / 2;
            // Create markers for center, left wrap (-7800), and right wrap (+7800)
            const positionsToCreate = [
            { lat: lat, lng: lng },
            { lat: lat, lng: lng + width },
            { lat: lat, lng: lng - width }
            ];

            positionsToCreate.forEach(position => {
            const divIcon = createDivIcon(spawnData);

            const marker = L.marker([position.lat, position.lng], { icon: divIcon });
            markersByCategory[categoryName].push(marker);

            if (spawnData.bonusType) { 
                markersByCategoryAndBonusType[categoryName][spawnData.bonusType] = markersByCategoryAndBonusType[categoryName][spawnData.bonusType] || [];
                markersByCategoryAndBonusType[categoryName][spawnData.bonusType].push(marker);
            }

            });
        });
        
        checkbox.addEventListener('change', function() {
            refreshBonusMarkers(categoryCheckboxes, markersByCategory, markersByCategoryAndBonusType, map);
        });
        });

        container.appendChild(details);

        bonusSelect.addEventListener("change", () => refreshBonusMarkers(categoryCheckboxes, markersByCategory, markersByCategoryAndBonusType, map));
        

        map.on('moveend zoomend', () => {
            refreshBonusMarkers(categoryCheckboxes, markersByCategory, markersByCategoryAndBonusType, map);
        });

        refreshBonusMarkers(categoryCheckboxes, markersByCategory, markersByCategoryAndBonusType, map);
        
    
        
        console.log('All markers loaded and UI created successfully!');
    })
    .catch(error => {
        console.error('Error loading tooltips:', error);
        console.error('Error details:', error.message);
    });
}