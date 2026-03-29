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
// for better cylindrcal map performance, disable inertia and fade animation
// i dont know this cylindriacl map stuff is weird.
map.options.inertia = false;
map.options.fadeAnimation = false;


// Define bounds using image dimensions
const bounds = [[0, 0], [height, width]];

map.setMaxBounds([[-height/10, -width], [height+height/10, width*2]]);
// left copy
L.imageOverlay('maps/World_cropped.jpg', [[0,-width],[height,0]]).addTo(map);
// center copy
L.imageOverlay('maps/World_cropped.jpg', bounds).addTo(map);
// right copy
L.imageOverlay('maps/World_cropped.jpg', [[0,width],[height,2*width]]).addTo(map);


// Fit map to image
map.fitBounds(bounds, { padding: [0, 0] });
map.setView([height / 2, width / 2], -2);

// set up cylindrical map by wrapping when user scrolls past edges
let isWrapping = false; // prevent recursive wrapping

map.on('moveend', () => {
  if (isWrapping) return;
  
  const center = map.getCenter();
  const currentZoom = map.getZoom();
  
  if (center.lng < width * 0.20) {
    // user scrolled past left edge → wrap to the right
    isWrapping = true;
    map.setView([center.lat, center.lng + width], currentZoom, {animate: false});
    setTimeout(() => { isWrapping = false; }, 100);
  } else if (center.lng > width * 0.8) {
    // user scrolled past right edge → wrap to the left
    isWrapping = true;
    map.setView([center.lat, center.lng - width], currentZoom, {animate: false});
    setTimeout(() => { isWrapping = false; }, 100);
  }
});




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
        label.className = 'checkbox-container';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.dataset.layerId = layerData.id;
        
        const checkmark = document.createElement('span');
        checkmark.className = 'checkmark';
        
        const text = document.createElement('span');
        text.className = 'label-text';
        text.textContent = layerData.displayName;
        
        label.appendChild(checkbox);
        label.appendChild(checkmark);
        label.appendChild(text);
        details.appendChild(label);
        
        // Create the image overlay
        const bounds = [[layerData.y, layerData.x], [layerData.y + layerData.h, layerData.x + layerData.w]];
        const imageOverlay = L.imageOverlay(layerData.source, bounds);
        const imageOverlayLeft = L.imageOverlay(layerData.source, [[layerData.y, layerData.x - width], [layerData.y + layerData.h, layerData.x + layerData.w - width]]);
        const imageOverlayRight = L.imageOverlay(layerData.source, [[layerData.y, layerData.x + width], [layerData.y + layerData.h, layerData.x + layerData.w + width]]);
        
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
      });
      
      container.appendChild(details);
    });
    
    console.log('All layers loaded and UI created successfully!');
  })
  .catch(error => {
    console.error('Error loading layers:', error);
    console.error('Error details:', error.message);
  });