import { addLegendToggle } from "../UI/legend.js";




function createMapLayer(layerData, category, GAME_TILE_SIZE, width, MAP_OFFSET) {
    // Create the image overlay
    const lat = GAME_TILE_SIZE * (layerData.y) + MAP_OFFSET;
    const lng = GAME_TILE_SIZE * (layerData.x);
    const bounds = [[lat, lng], [lat + layerData.h, lng + layerData.w]];
    const boundsLeft = [[lat, lng - width], [lat + layerData.h, lng + layerData.w - width]];
    const boundsRight = [[lat, lng + width], [lat + layerData.h, lng + layerData.w + width]];
    
    let imageOverlay, imageOverlayLeft, imageOverlayRight;
    if (category === "Birth") {
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

function addLayerToggle(checkbox, imageOverlay, imageOverlayLeft, imageOverlayRight) {
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

export function loadLayers(GAME_TILE_SIZE, map, width, height,MAP_OFFSET) {
    // Load layers from JSON and create categories
    console.log('Starting to fetch layers.json...');
    fetch('json/layers.json')
    .then(response => {
        console.log('Response received:', response.status);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log('JSON loaded successfully.');
        const container = document.querySelector('.options-container');
        
        for (const [category, items] of Object.entries(data)) {
        console.log("Category:", category, "with", items.length, "items");

        if (category === "Birth and Stability") {
            items.sort((a, b) => a.display_name.localeCompare(b.display_name));
        }
        const ReligionsList = []
        

        const details = document.createElement('details');
        const summary = document.createElement('summary');
        summary.textContent = category;
        details.appendChild(summary);

        for (const layerData of items) {
            const label = document.createElement('label');
            label.className = 'checkbox-container';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            
            const checkmark = document.createElement('span');
            checkmark.className = 'checkmark';
            
            const text = document.createElement('span');
            text.className = 'label-text';
            text.textContent = layerData.display_name;
            
            label.appendChild(checkbox);
            label.appendChild(checkmark);
            label.appendChild(text);
            details.appendChild(label);
            
            let imageOverlay, imageOverlayLeft, imageOverlayRight = createMapLayer(layerData,category, GAME_TILE_SIZE, width, MAP_OFFSET);
            
            // Toggle overlay on checkbox change
            addLayerToggle(checkbox, imageOverlay, imageOverlayLeft, imageOverlayRight);

            if (category === "Religion") {
                ReligionsList.push(checkbox);
            }
        };
        
        for (const checkbox of ReligionsList) {
             addLegendToggle(checkbox, ReligionsList);
        }

        container.appendChild(details);
        };
        
        console.log('All layers loaded and UI created successfully!');
    })
    .catch(error => {
        console.error('Error loading layers:', error);
        console.error('Error details:', error.message);
    });
}
