


export function loadMarkers(map, TILE_SIZE, width, height) {
    // Load markers from JSON and create tooltips
    console.log('Starting to fetch tooltips.json...');
    fetch('json/tooltips.json')
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
        
        // Store tooltips by subcategory
        const tooltipsBySubcategory = {};
        const categoryLayerGroups = {};
        // For each subcategory
        Object.keys(categories).forEach(categoryName => {

        console.log('Creating subcategory:', categoryName, 'with', categories[categoryName].length, 'spawns/despawns');
        
        tooltipsBySubcategory[categoryName] = {};
        const layerGroup = L.layerGroup();
        categoryLayerGroups[categoryName] = layerGroup;
        // Create checkbox for subcategory
        const label = document.createElement('label');
        label.className = 'checkbox-container';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.dataset.category = categoryName;
        checkbox.checked = false;
        
        const checkmark = document.createElement('span');
        checkmark.className = 'checkmark';
        
        const text = document.createElement('span');
        text.className = 'label-text';
        text.textContent = categoryName;
        
        label.appendChild(checkbox);
        label.appendChild(checkmark);
        label.appendChild(text);
        details.appendChild(label);
        
        // For each spawn in subcategory - create tooltips
        // also creat a lookuptables for each category for the tooltips by lat,lng
        categories[categoryName].forEach(spawnData => {
            const lat = TILE_SIZE * (spawnData.y) + TILE_SIZE / 2;
            const lng = TILE_SIZE * (spawnData.x) + TILE_SIZE / 2;
            const tooltipClass = spawnData.spawn ? 'tooltip-spawn' : 'tooltip-despawn';
            const direction1 = spawnData.spawn ? 'top' : 'bottom';
            const direction = spawnData.category.includes('Terrain changes') ? 'bottom' : direction1;
            // Create tooltips for center, left wrap (-7800), and right wrap (+7800)
            const positionsToCreate = [
            { lat: lat, lng: lng },
            { lat: lat, lng: lng + width },
            { lat: lat, lng: lng - width }
            ];
            
            positionsToCreate.forEach(position => {
            const tooltip = L.tooltip({
                permanent: true,
                direction: direction,
                className: 'custom-tooltip',
                offset: [0, 0]
            })
            .setLatLng([position.lat, position.lng])
            .setContent(
                `<div class="tooltip-box">
                <img src="${spawnData.source}" class="${tooltipClass}" />
                <span class="tooltip-text">${spawnData.text}</span>
                </div>`
            );
            layerGroup.addLayer(tooltip);
            tooltipsBySubcategory[categoryName][`${position.lat},${position.lng}`] = tooltip;
            });
        });
        


        // Event listener for checkbox - show/hide all tooltips in subcategory
        checkbox.addEventListener('change', function() {

            
            Object.values(tooltipsBySubcategory[categoryName]).forEach(tooltip => {
            const mapBounds = map.getBounds();
            if (this.checked && mapBounds.contains(tooltip.getLatLng())) { 
                tooltip.addTo(map);
            } else {
                tooltip.removeFrom(map);
            }
            });
        });        
        });
        
        container.appendChild(details);
        
        // Update tooltips when map moves or zooms
        map.on('moveend', () => {
        const mapBounds = map.getBounds();
        Object.keys(tooltipsBySubcategory).forEach(categoryName => {
            Object.values(tooltipsBySubcategory[categoryName]).forEach(tooltip => {
            const checkbox = document.querySelector(`input[data-category="${categoryName}"]`);
            const isEnabled = checkbox && checkbox.checked;
            const isInBounds = mapBounds.contains(tooltip.getLatLng());
            
            if (isEnabled && isInBounds) {
                tooltip.addTo(map);
                
            } else {
                tooltip.removeFrom(map);
                
            }
            });
        });
        });
        
        map.on('zoomend', () => {
        const mapBounds = map.getBounds();
        Object.keys(tooltipsBySubcategory).forEach(categoryName => {
            Object.values(tooltipsBySubcategory[categoryName]).forEach(tooltip => {
            const checkbox = document.querySelector(`input[data-category="${categoryName}"]`);
            const isEnabled = checkbox && checkbox.checked;
            const isInBounds = mapBounds.contains(tooltip.getLatLng());
            
            if (isEnabled && isInBounds) {
                tooltip.addTo(map);
                
            } else {
                tooltip.removeFrom(map);
            }
            });
        });
        });
        
        console.log('All tooltips loaded and UI created successfully!');
    })
    .catch(error => {
        console.error('Error loading tooltips:', error);
        console.error('Error details:', error.message);
    });
}