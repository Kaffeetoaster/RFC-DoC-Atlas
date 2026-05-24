const city_planner_button = document.getElementById("city-planner-toggle");
const city_planner_clear_button = document.getElementById("city-planner-clear");
const city_planner_show_button = document.getElementById("city-planner-show");

export function initCityPlanner(map, GAME_TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, MAP_OFFSET) {
	// some helper functions.
	function wrapLngToWorld(lng) {
		return ((lng % WORLD_WIDTH) + WORLD_WIDTH) % WORLD_WIDTH;
	}

	function getTileFromLatLng(latlng) {
		const tileX = Math.floor(wrapLngToWorld(latlng.lng) / GAME_TILE_SIZE);
		const tileY = Math.floor((latlng.lat - MAP_OFFSET) / GAME_TILE_SIZE);
		return { x: tileX, y: tileY };
	}

	function getBoundsForTile(tile) {
		return [
			[(tile.y-2) * GAME_TILE_SIZE + MAP_OFFSET, (tile.x-2) * GAME_TILE_SIZE],
			[(tile.y + 3) * GAME_TILE_SIZE + MAP_OFFSET, (tile.x + 3) * GAME_TILE_SIZE]
		];
	}

	const city_planner_source = "Assets/Art/Interface/Buttons/city_radius.svg";
	map.createPane("CityPlannerPane");
	map.getPane("CityPlannerPane").style.zIndex = 560;

	const previewOverlay = L.imageOverlay(city_planner_source, [0, 0], {pane: "CityPlannerPane"});
	const previewOverlayLeft = L.imageOverlay(city_planner_source, [0, 0], {pane: "CityPlannerPane"});
	const previewOverlayRight = L.imageOverlay(city_planner_source, [0, 0], {pane: "CityPlannerPane"});
	
	const placedOverlaysByTile = new Map();

	let showPlane = true;
	let plannerActive = false;
	let currentPreviewTileKey = null;

	function checkTile(latlng) {
		const tile = getTileFromLatLng(latlng);
		const tileKey = `${tile.x}_${tile.y}`;
		return placedOverlaysByTile.has(tileKey);
	}
	function createOverlayForTile(tile) {
		const bounds = getBoundsForTile(tile);
		return L.imageOverlay(city_planner_source, bounds, {pane: "CityPlannerPane"});
	}
	function clearPreview() {
		previewOverlay.removeFrom(map);
		previewOverlayLeft.removeFrom(map);
		previewOverlayRight.removeFrom(map);
		currentPreviewTileKey = null;
	}
	function refreshPreview(latlng) {
		const tile = getTileFromLatLng(latlng);
		const tileKey = `${tile.x}_${tile.y}`;

		if (tileKey === currentPreviewTileKey) {
			return;
		}
		currentPreviewTileKey = tileKey;
		let bounds = getBoundsForTile(tile);
		previewOverlay.setBounds(bounds);
		previewOverlay.addTo(map);
		previewOverlayLeft.setBounds([[bounds[0][0], bounds[0][1] - WORLD_WIDTH], [bounds[1][0], bounds[1][1] - WORLD_WIDTH]]);
		previewOverlayLeft.addTo(map);
		previewOverlayRight.setBounds([[bounds[0][0], bounds[0][1] + WORLD_WIDTH], [bounds[1][0], bounds[1][1] + WORLD_WIDTH]]);
		previewOverlayRight.addTo(map);
	}

	function placeOverlayAtCurrentTile(latlng) {
		const tile = getTileFromLatLng(latlng);
		const tileKey = `${tile.x}_${tile.y}`;
		
		const tileLeft = { x: tile.x - WORLD_WIDTH / GAME_TILE_SIZE, y: tile.y };
		const tileKeyLeft = `${tileLeft.x}_${tileLeft.y}`;
			
		const tileRight = { x: tile.x + WORLD_WIDTH / GAME_TILE_SIZE, y: tile.y };
		const tileKeyRight = `${tileRight.x}_${tileRight.y}`;

		const overlay = placedOverlaysByTile.get(tileKey);
		if (overlay) {
			return;
		}
		
		const newOverlay = createOverlayForTile(tile);
		newOverlay.addTo(map);
		placedOverlaysByTile.set(tileKey, newOverlay);

		const newOverlayLeft = createOverlayForTile(tileLeft);
		newOverlayLeft.addTo(map);
		placedOverlaysByTile.set(tileKeyLeft, newOverlayLeft);

		const newOverlayRight = createOverlayForTile(tileRight);
		newOverlayRight.addTo(map);
		placedOverlaysByTile.set(tileKeyRight, newOverlayRight);
		
		
	}

	function removeOverlayAtCurrentTile(latlng) {
		const tile = getTileFromLatLng(latlng);
		const tileKey = `${tile.x}_${tile.y}`;
		const overlay = placedOverlaysByTile.get(tileKey);

		const tileLeft = { x: tile.x - WORLD_WIDTH / GAME_TILE_SIZE, y: tile.y };
		const tileKeyLeft = `${tileLeft.x}_${tileLeft.y}`;
		const overlayLeft = placedOverlaysByTile.get(tileKeyLeft);

		const tileRight = { x: tile.x + WORLD_WIDTH / GAME_TILE_SIZE, y: tile.y };
		const tileKeyRight = `${tileRight.x}_${tileRight.y}`;
		const overlayRight = placedOverlaysByTile.get(tileKeyRight);
	
		if (overlay) {
			overlay.removeFrom(map);
			placedOverlaysByTile.delete(tileKey);
		}
		if (overlayLeft) {
			overlayLeft.removeFrom(map);
			placedOverlaysByTile.delete(tileKeyLeft);
		}
		if (overlayRight) {
			overlayRight.removeFrom(map);
			placedOverlaysByTile.delete(tileKeyRight);
		}
	}

	city_planner_button.addEventListener("click", () => {
		plannerActive = !plannerActive;
		city_planner_button.classList.toggle("active", plannerActive);

		if (!plannerActive) {
			clearPreview();
		}
	});
	city_planner_clear_button.addEventListener("click", () => {
		placedOverlaysByTile.forEach(overlay => overlay.removeFrom(map));
		placedOverlaysByTile.clear();
	});
	city_planner_show_button.addEventListener("click", () => {
		
		city_planner_show_button.classList.toggle("active", showPlane);
		showPlane = !showPlane;
		map.getPane("CityPlannerPane").style.display = showPlane ? "" : "none";
	});

	map.on("mousemove", (event) => {
		if (plannerActive) {
			refreshPreview(event.latlng);
		}
	});

	map.on("click", (event) => {
		if (plannerActive) {
			const is_used = checkTile(event.latlng);
			if (!is_used) {
				placeOverlayAtCurrentTile(event.latlng);
			} else {
				removeOverlayAtCurrentTile(event.latlng);
			}
		}
	});

}
