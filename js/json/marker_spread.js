// Markers that are shown on exactly the same spot (same x and y) would hide each other.
// spreadOffsets(count) tells where each of `count` such markers goes, as [dx, dy] in game tiles
// (dx > 0 = right, dy > 0 = up):
//   1 marker:  stays where it is
//   2 markers: left, right
//   3 markers: left, right, up
//   4 markers: left, right, up, down
//   more:      a centred grid
// The offsets are in tiles (map units), so a moved marker keeps pointing at a fixed spot of the map at every zoom level.

const SPREAD_TILES = 2;     // how far a marker is moved away from the real position

export function spreadOffsets(count) {
    if (count <= 1) return [[0, 0]].slice(0, count);
    if (count <= 4) {
        return [[-1, 0], [1, 0], [0, 1], [0, -1]]
            .slice(0, count)
            .map(([dx, dy]) => [dx * SPREAD_TILES, dy * SPREAD_TILES]);
    }
    const columns = Math.ceil(Math.sqrt(count));
    const rows = Math.ceil(count / columns);
    return Array.from({ length: count }, (_, index) => [
        (index % columns - (columns - 1) / 2) * SPREAD_TILES,
        -(Math.floor(index / columns) - (rows - 1) / 2) * SPREAD_TILES,
    ]);
}
