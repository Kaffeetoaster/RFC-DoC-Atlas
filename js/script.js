import { initializeAboutPage, loadAboutInformation } from './UI/about.js';
import {initializeBurgerMenu} from './UI/burger.js';
import {initializeDeselectAllButton} from './UI/deselect_all.js';


// loading about information and adding event listeners for about page
initializeAboutPage();
loadAboutInformation();


// Event listener for Burger menu
initializeBurgerMenu();

// Event listener for "Deselect All" button
initializeDeselectAllButton();



// Initialize Leaflet map
const width = 7800;   // image width in pixels
const height = 4160;  // image height in pixels
const TILE_SIZE = 52; // size of each game tile in pixels 

const map = L.map('map', {
  crs: L.CRS.Simple,
  minZoom: 0,
  maxZoom: 0,
  zoomControl: false,
  scrollWheelZoom: true,   // zoom only
  dragging: true,           // drag to pan
  //noWrap: false // allow horizontal wrapping for cylindrical map
});

 // number of tiles horizontally in the world
const tileLayer = L.tileLayer("maps/tiles/{z}/{x}/{y}.png", {
        tileSize: 104, //
        minZoom: 0,
        maxZoom: 0,
        //noWrap: false, // ensure tiles wrap horizontally
        bounds: [[0, -width], [height, width+ width]], // set bounds to prevent vertical wrapping
        //errorTileUrl: "maps/tiles/0/0/0.png"
        

    })
tileLayer.getTileUrl = function(coords) {
          const worldTiles_horizontal = Math.ceil(width / (104 * Math.pow(2, -coords.z)));
          const x = ((coords.x % worldTiles_horizontal) + worldTiles_horizontal) % worldTiles_horizontal;
          const y = coords.y;
          console.log(`Requesting tile at z=${coords.z}, x=${coords.x}, y=${coords.y} (wrapped x=${x})`);
          return `maps/tiles/${coords.z}/${x}/${y}.png`;
        }
tileLayer.addTo(map);

map.createPane("OutlinePane");
map.getPane("OutlinePane").style.zIndex = 500; // above overlays but below tooltips

// for better cylindrcal map performance, disable inertia and fade animation
// i dont know this cylindriacl map stuff is weird.
map.options.inertia = false;
map.options.fadeAnimation = false;


// Define bounds using image dimensions
const bounds = [[0, 0], [height, width]];

map.setMaxBounds([[-height/10, -width], [height+height/10, width*2]]);
// left copy
//L.imageOverlay('maps/World_cropped.jpg', [[0,-width],[height,0]]).addTo(map);
// center copy
//L.imageOverlay('maps/World_cropped.jpg', bounds).addTo(map);
// right copy
//L.imageOverlay('maps/World_cropped.jpg', [[0,width],[height,2*width]]).addTo(map);




// Fit map to image
map.fitBounds(bounds, { padding: [0, 0] });
map.setZoom(0); // set zoom to 0 to show the whole image at once
//map.setView([-height / 4, width / 4], 0);

map.setView([height / 2, width / 2], 0);

// set up cylindrical map by wrapping when user scrolls past edges
// let isWrapping = false; // prevent recursive wrapping

// map.on('moveend', () => {
//   if (isWrapping) return;
  
//   const center = map.getCenter();
//   const currentZoom = map.getZoom();
  
//   if (center.lng < width * 0.20) {
//     // user scrolled past left edge → wrap to the right
//     isWrapping = true;
//     map.setView([center.lat, center.lng + width], currentZoom, {animate: false});
//     setTimeout(() => { isWrapping = false; }, 100);
//   } else if (center.lng > width * 0.8) {
//     // user scrolled past right edge → wrap to the left
//     isWrapping = true;
//     map.setView([center.lat, center.lng - width], currentZoom, {animate: false});
//     setTimeout(() => { isWrapping = false; }, 100);
//   }
// });






// Load tooltips from JSON and create tooltips
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