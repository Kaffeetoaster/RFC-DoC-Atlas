const tooltip = document.getElementById("tooltip-box");


function updateTooltip(latlng, Tooltip_lookup, GAME_TILE_SIZE, width, height, MAP_OFFSET) {
    let x = Math.floor(latlng.lng/GAME_TILE_SIZE);
    let y = Math.floor((latlng.lat - MAP_OFFSET) / GAME_TILE_SIZE);
    // allow wrapping:
    const width_in_tiles = width / GAME_TILE_SIZE;
    x = ((x % width_in_tiles) + width_in_tiles) % width_in_tiles;
    if (y < 0 || y >= height / GAME_TILE_SIZE) {
        return;
    }
    // Find the tooltip for this tile
    const tooltipData = Tooltip_lookup[`${x}_${y}`];
    const lines = [];

    lines.push(tooltipData.region);

    const details = [
        tooltipData.plot,
        tooltipData.feature,
        tooltipData.terrain
    ].filter(Boolean);

    if (details.length > 0) {
        lines.push(details.join(" / "));
    }

    if (tooltipData.bonus) {
        lines.push(tooltipData.bonus);
    }

    lines.push(`${x}, ${y}`);

    tooltip.innerHTML = lines.join("<br>");
}

export function loadTooltips(map, GAME_TILE_SIZE, width, height, MAP_OFFSET) {
    // Load tooltips from JSON and create tooltips

    let Tooltip_lookup = {}; // Create a lookup object for tooltips 
    console.log('Starting to fetch tooltip_info.json...');
    fetch('json/tooltip_info.json')
    .then(response => {
        console.log('Response received:', response.status);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log('JSON loaded successfully. Total number of tooltips:', data.length);
        // fill lookup object
        Tooltip_lookup = data;
    })
    // add hover event listener to map container
    map.on("mousemove", (e) => {
        updateTooltip(e.latlng, Tooltip_lookup, GAME_TILE_SIZE, width, height, MAP_OFFSET);
    });
}