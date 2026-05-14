


export function loadLayers(TILE_SIZE, map, width, height) {
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
        console.log('Container found:', container);
        
        if (!container) {
        console.error('ERROR: .options-container not found in HTML!');
        return;
        }
        for (const [category, items] of Object.entries(data)) {
        console.log("Category:", category, "with", items.length, "items");
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
            
            // Create the image overlay
            // this should be its own function maybe.
            const lat = TILE_SIZE * (layerData.y);
            const lng = TILE_SIZE * (layerData.x);
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




            // Toggle overlay on checkbox change
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
        };
        
        container.appendChild(details);
        };
        
        console.log('All layers loaded and UI created successfully!');
    })
    .catch(error => {
        console.error('Error loading layers:', error);
        console.error('Error details:', error.message);
    });
}
