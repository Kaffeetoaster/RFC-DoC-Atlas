const width = 7800;   // image width in pixels
const height = 4160;  // image height in pixels

const map = L.map('map', {
  crs: L.CRS.Simple,
  minZoom: -3,
  maxZoom: 1,
  zoomControl: false,
  scrollWheelZoom: true,   // zoom only
  dragging: true           // drag to pan
});

// Define bounds using image dimensions
const bounds = [[0, 0], [height, width]];

map.setMaxBounds([[-height/3, 0], [height+height/3, width]]);
// Add your image
L.imageOverlay('maps/World_cropped.jpg', bounds).addTo(map);

// Fit map to image
map.fitBounds(bounds, { padding: [0, 0] });
map.setView([height / 2, width / 2], -2);





// Load layers from JSON and create categories
console.log('Starting to fetch layers.json...');
fetch('json/layers.json')
  .then(response => {
    console.log('Response received:', response.status);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  })
  .then(data => {
    console.log('JSON loaded successfully. Total layers:', data.layers.length);
    const container = document.querySelector('.options-container');
    console.log('Container found:', container);
    
    if (!container) {
      console.error('ERROR: .options-container not found in HTML!');
      return;
    }
    
    const categories = {};
    
    // Group layers by category
    data.layers.forEach(layer => {
      if (!categories[layer.category]) {
        categories[layer.category] = [];
      }
      categories[layer.category].push(layer);
    });
    
    console.log('Categories created:', Object.keys(categories));
    
    // Create detail tags for each category
    Object.keys(categories).forEach(categoryName => {
      console.log('Creating category:', categoryName, 'with', categories[categoryName].length, 'layers');
      const details = document.createElement('details');
      
      const summary = document.createElement('summary');
      summary.textContent = categoryName;
      details.appendChild(summary);
      
      // Add checkboxes for each layer in this category
      categories[categoryName].forEach(layerData => {
        const label = document.createElement('label');
        label.className = 'option';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.dataset.layerId = layerData.id;
        
        const text = document.createElement('span');
        text.textContent = layerData.displayName;
        
        label.appendChild(checkbox);
        label.appendChild(text);
        details.appendChild(label);
        
        // Create the image overlay
        const bounds = [[layerData.y, layerData.x], [layerData.y + layerData.h, layerData.x + layerData.w]];
        const imageOverlay = L.imageOverlay(layerData.source, bounds);
        
        // Toggle overlay on checkbox change
        checkbox.addEventListener('change', function() {
          if (this.checked) {
            imageOverlay.addTo(map);
          } else {
            imageOverlay.removeFrom(map);
          }
        });
      });
      
      container.appendChild(details);
    });
    
    console.log('All layers loaded and UI created successfully!');
  })
  .catch(error => {
    console.error('Error loading layers:', error);
    console.error('Error details:', error.message);
  });