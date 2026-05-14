import { initializeAboutPage, loadAboutInformation } from './UI/about.js';
import {initializeBurgerMenu} from './UI/burger.js';
import {initializeDeselectAllButton} from './UI/deselect_all.js';

import { loadLayers } from './json/load_layers.js';
import { loadMarkers} from './json/load_markers.js';

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
  minZoom: -3,
  maxZoom: 1,
  zoomControl: false,
  scrollWheelZoom: true,   // zoom only
  dragging: true,           // drag to pan
  //noWrap: false // allow horizontal wrapping for cylindrical map
});

 // number of tiles horizontally in the world
// const tileLayer = L.tileLayer("maps/tiles/{z}/{x}/{y}.png", {
//         tileSize: 104, //
//         minZoom: 0,
//         maxZoom: 0,
//         //noWrap: false, // ensure tiles wrap horizontally
//         bounds: [[0, -width], [height, width+ width]], // set bounds to prevent vertical wrapping
//         //errorTileUrl: "maps/tiles/0/0/0.png"
        

//     })
// tileLayer.getTileUrl = function(coords) {
//           const worldTiles_horizontal = Math.ceil(width / (104 * Math.pow(2, -coords.z)));
//           const x = ((coords.x % worldTiles_horizontal) + worldTiles_horizontal) % worldTiles_horizontal;
//           const y = coords.y;
//           console.log(`Requesting tile at z=${coords.z}, x=${coords.x}, y=${coords.y} (wrapped x=${x})`);
//           return `maps/tiles/${coords.z}/${x}/${y}.png`;
//         }
// tileLayer.addTo(map);

map.createPane("OutlinePane");
map.getPane("OutlinePane").style.zIndex = 500; // above overlays but below tooltips



// Define bounds using image dimensions
const bounds = [[0, 0], [height, width]];

map.setMaxBounds([[-height/10, -width], [height+height/10, width*2]]);
//left copy
L.imageOverlay('maps/World_cropped.jpg', [[0,-width],[height,0]]).addTo(map);
//center copy
L.imageOverlay('maps/World_cropped.jpg', bounds).addTo(map);
//right copy
L.imageOverlay('maps/World_cropped.jpg', [[0,width],[height,2*width]]).addTo(map);


// Fit map to image
map.fitBounds(bounds, { padding: [0, 0] });
map.setZoom(0); // set zoom to 0 to show the whole image at once

map.setView([height / 2, width / 2], 0);

// for better cylindrcal map performance, disable inertia and fade animation
// i dont know this cylindriacl map stuff is weird.
map.options.inertia = false;
map.options.fadeAnimation = false;



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

// load Layers, create checkboxes, and add event listeners for checkboxes to toggle layers
loadLayers(TILE_SIZE, map, width, height);

// load markers and create checkboxes to toggle them
loadMarkers(map, TILE_SIZE, width, height);