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



// Initialize Leaflet map Coordinates space is here important!!
const width = 4800;   // image width in pixels
const height = 2880;  // image height in pixels
const GAME_TILE_SIZE = 32; // size of each game tile in pixels 
const MAP_OFFSET = 160; // offset to align map with game world, determined empirically
const MAP_TILE_SIZE = 240; // size of each tile in the map in pixels, determined empirically to align with game tiles

const map = L.map('map', {
  crs: L.CRS.Simple,
  minZoom: -2,
  maxZoom: 2,
  zoomControl: false,
  scrollWheelZoom: true,   // zoom only
  dragging: true,           // drag to pan
  //noWrap: false // allow horizontal wrapping for cylindrical map
});

 // number of tiles horizontally in the world
const tileLayer = L.tileLayer("maps/tiles/{z}/{x}/{y}.webp", {
        tileSize: MAP_TILE_SIZE, //
        minZoom: -2,
        maxZoom: 2,
        //noWrap: false, // ensure tiles wrap horizontally
        //worldCopyJump: true, // enable seamless horizontal wrapping
        bounds: [[0, -width], [height, width+ width]], // set bounds to prevent vertical wrapping
        //errorTileUrl: "maps/tiles/0/0/0.png"
        

    })
tileLayer.getTileUrl = function(coords) {
          const worldTiles_horizontal = Math.ceil((width * Math.pow(2, coords.z))/MAP_TILE_SIZE);
          const x = ((coords.x % worldTiles_horizontal) + worldTiles_horizontal) % worldTiles_horizontal;
          const y = coords.y;
          console.log(`Requesting tile at z=${coords.z}, x=${coords.x}, y=${coords.y} (wrapped x=${x})`);
          return `maps/tiles/${coords.z}/${x}/${y}.webp`;
        }
tileLayer.addTo(map);

map.createPane("OutlinePane");
map.getPane("OutlinePane").style.zIndex = 500; // above overlays but below tooltips



// Define bounds using image dimensions
const bounds = [[0, 0], [height, width]];

map.setMaxBounds([[-height/10, -width], [height+ height/10, width*2]]);
// //left copy
// L.imageOverlay('maps/World_cropped.jpg', [[0,-width],[height,0]]).addTo(map);
// //center copy
// L.imageOverlay('maps/World_cropped.jpg', bounds).addTo(map);
// //right copy
// L.imageOverlay('maps/World_cropped.jpg', [[0,width],[height,2*width]]).addTo(map);


// Fit map to image
map.fitBounds(bounds, { padding: [0, 0] });
map.setZoom(-2); // set zoom to -2 to show the whole image at once

map.setView([height/2, width/2], -2);

// for better cylindrcal map performance, disable inertia and fade animation
// i dont know this cylindriacl map stuff is weird.
map.options.inertia = false;
map.options.fadeAnimation = false;



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

// load Layers, create checkboxes, and add event listeners for checkboxes to toggle layers
loadLayers(GAME_TILE_SIZE, map, width, height, MAP_OFFSET);

// load markers, create checkboxes to toggle them and create a cache canvas for the markers
loadMarkers(map, GAME_TILE_SIZE, width, height, MAP_OFFSET);

