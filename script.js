const sidebar = document.getElementById("sidebar");
const burger = document.getElementById("burger");
const header = document.getElementById("sidebar-header");
const aboutToggle = document.getElementById("about-toggle");
const aboutPage = document.getElementById("about-page");
const aboutClose = document.getElementById("about-close");
const aboutTitle = document.getElementById("about-title");
const aboutContent = document.getElementById("about-content");
const headerMeta = document.getElementById("header-meta");
const deselectAllButton = document.getElementById("deselect-all");


// About page rendering functions
function isAboutLinkObject(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  if (value.type !== 'link') return false;
  return typeof value.url === 'string' && value.url.trim() !== '';
}

function createAboutLink(linkData) {
  const link = document.createElement('a');
  link.href = linkData.url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.textContent = linkData.label || linkData.text || linkData.url;
  return link;
}

function renderAboutValue(value) {
  if (isAboutLinkObject(value)) {
    const paragraph = document.createElement('p');
    paragraph.appendChild(createAboutLink(value));
    return paragraph;
  }

  if (Array.isArray(value)) {
    const list = document.createElement('ul');
    value.forEach(item => {
      const listItem = document.createElement('li');
      if (item && typeof item === 'object') {
        listItem.appendChild(renderAboutValue(item));
      } else {
        listItem.textContent = item;
      }
      list.appendChild(listItem);
    });
    return list;
  }

  if (value && typeof value === 'object') {
    const container = document.createElement('div');
    Object.entries(value).forEach(([key, item]) => {
      const block = document.createElement('div');
      block.className = 'about-entry';

      const title = document.createElement('h4');
      title.textContent = key;
      block.appendChild(title);
      block.appendChild(renderAboutValue(item));
      container.appendChild(block);
    });
    return container;
  }

  const paragraph = document.createElement('p');
  paragraph.textContent = value;
  return paragraph;
}

function setAboutOpen(isOpen) {
  if (!aboutPage) return;
  aboutPage.classList.toggle('open', isOpen);
  aboutPage.setAttribute('aria-hidden', String(!isOpen));
}

if (aboutToggle && aboutPage) {
  aboutToggle.addEventListener('click', () => {
    setAboutOpen(!aboutPage.classList.contains('open'));
  });
}

if (aboutClose) {
  aboutClose.addEventListener('click', () => setAboutOpen(false));
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    setAboutOpen(false);
  }
});

if (aboutPage) {
  document.addEventListener('click', (event) => {
    if (!aboutPage.classList.contains('open')) return;
    if (aboutPage.contains(event.target)) return;
    if (aboutToggle && aboutToggle.contains(event.target)) return;
    setAboutOpen(false);
  });
}

// Load about information from JSON and populate the about page
fetch('about/about.json')
  .then(response => {
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  })
  .then(data => {
    const aboutData = data.about ?? data.entries ?? {};
    const version = data.version ?? '';
    const lastUpdate = data.last_update ?? data.lastUpdate ?? '';

    if (aboutTitle && data.title) {
      aboutTitle.textContent = data.title;
    }

    if (headerMeta) {
      headerMeta.textContent = [version, lastUpdate].filter(Boolean).join(' | ');
    }

    if (aboutContent) {
      aboutContent.innerHTML = '';

      if (aboutData && typeof aboutData === 'object') {
        Object.entries(aboutData).forEach(([key, value]) => {
          const section = document.createElement('section');
          section.className = 'about-section';

          const title = document.createElement('h4');
          title.textContent = key;
          section.appendChild(title);
          section.appendChild(renderAboutValue(value));
          aboutContent.appendChild(section);
        });
      } else {
        aboutContent.appendChild(renderAboutValue(aboutData));
      }
    }
  })
  .catch(error => {
    console.error('Error loading about.json:', error);
    if (headerMeta) {
      headerMeta.textContent = '';
    }
    if (aboutContent) {
      aboutContent.textContent = 'About information is unavailable.';
    }
  });


// open on burger click
burger.addEventListener("click", () => {
  sidebar.classList.remove("hidden");
  burger.classList.add("hidden");
});

// close on header click
header.addEventListener("click", () => {
  sidebar.classList.add("hidden");
  burger.classList.remove("hidden");
});

deselectAllButton.addEventListener("click", () => {
  const checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]');
  checkboxes.forEach(checkbox => {
    if (checkbox.checked) {
      checkbox.checked = false;
      checkbox.dispatchEvent(new Event('change')); // trigger change event to update map
    }
  });
});



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
  dragging: true           // drag to pan
});

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
          { lat: lat, lng: lng + 7800 },
          { lat: lat, lng: lng - 7800 }
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