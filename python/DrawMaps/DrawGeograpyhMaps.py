from python.consts import *
from python.helper.helper import *
from python.helper.DrawHelper import *
import config
import colorsys

from pathlib import Path
from PIL import Image, ImageDraw

def generate_color_scheme(num_colors):
    # generates a HSL color scheme with num_colors distinct colors
    # goal is to have strong contrast
    if num_colors <= 0:
        return [], []

    hsl_colors = []
    rgba_colors = []

    # Golden-ratio spacing gives good perceptual separation, even for larger palettes.
    golden_ratio_conjugate = 0.618033988749895
    hue = 0.0

    for i in range(num_colors):
        hue = (hue + golden_ratio_conjugate) % 1.0
        saturation = 0.4 + 0.15 * ((i % 3) / 2.0)  
        lightness = 0.4 + 0.12 * ((i % 2))         

        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)

        hsl = (int(round(hue * 360)) % 360, int(round(saturation * 100)), int(round(lightness * 100)))
        rgba = (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)

        hsl_colors.append(hsl)
        rgba_colors.append(rgba)

    return hsl_colors, rgba_colors

def filter_regions(dRegionOutlines, dRegionTiles, dRegionNeigbours, min_size=2):
    # removes regions that are smaller than min_size
    dRegionTiles = {region: tiles for region, tiles in dRegionTiles.items() if len(tiles) >= min_size}
    dRegionOutlines = {region: outlines for region, outlines in dRegionOutlines.items() if region in dRegionTiles}
    dRegionNeigbours = {region: neighbours for region, neighbours in dRegionNeigbours.items() if region in dRegionTiles}
    return dRegionOutlines, dRegionTiles, dRegionNeigbours
    
    
    
### TODO: needs a refactor, splitting up into smaller functions.
def DrawRegionMap(json_config, region_type, tile_size, line_strength):
    dRegionOutlines = {}
    dRegionNeigbours = {}
    dRegionColors = {}
    dRegionTiles = {}

    

    ## 1. get Region outline and Region neighbours
    for (x, y), tile_info in dTileMap.items():
        region = tile_info.get(region_type)
        if region not in dRegionTiles:
            dRegionTiles[region] = []
        dRegionTiles[region].append((x, y))
        
        lines = []
        inset = (line_strength-1) // 2  # Inset to avoid overlap with neighbouring tiles
        p_left = x * tile_size 
        p_top = y * tile_size
        p_right = (x + 1) * tile_size - 1
        p_bottom = (y + 1) * tile_size - 1

        if region is not None:
            # Check neighbors
            check_configs = [
            # Neighbour, (x1, y1, x2, y2), Side
                ((x - 1, y), (p_left + inset, p_top, p_left + inset, p_bottom), "L"),
                ((x + 1, y), (p_right - inset, p_top, p_right - inset, p_bottom), "R"),
                ((x, y - 1), (p_left, p_top + inset, p_right, p_top + inset), "T"),
                ((x, y + 1), (p_left, p_bottom - inset, p_right, p_bottom - inset), "B"),
                ((x-1, y-1), (p_left, p_top + inset, p_left + (line_strength-1), p_top + inset), "TL"),
                ((x+1, y-1), (p_right - (line_strength-1), p_top + inset, p_right, p_top + inset), "TR"),
                ((x-1, y+1), (p_left, p_bottom - inset, p_left + (line_strength-1), p_bottom - inset), "BL"),
                ((x+1, y+1), (p_right - (line_strength-1), p_bottom - inset, p_right, p_bottom - inset), "BR"),
            ]
            for (nx, ny), (lx1, ly1, lx2, ly2), side in check_configs:
                
                neighbor_region = dTileMap.get((nx % iWorldX, ny), {}).get(region_type)
                is_other_region = neighbor_region != region

                if is_other_region:
                    # This tile is part of the outline for its region
                    if region not in dRegionOutlines:
                        dRegionOutlines[region] = []
                    # Add line segment based on which neighbor is different
                    dRegionOutlines[region].append(((lx1, ly1), (lx2, ly2)))
                    # Add neighbor region to the list of neighbors for this region
                    if region not in dRegionNeigbours:
                        dRegionNeigbours[region] = set()
                    if neighbor_region is not None:
                        dRegionNeigbours[region].add(neighbor_region)

    
    dRegionOutlines, dRegionTiles, dRegionNeigbours = filter_regions(dRegionOutlines, dRegionTiles, dRegionNeigbours, min_size=5)
    print(f"Region type: {region_type}, Number of regions: {len(dRegionTiles)}, Average size: {sum(len(tiles) for tiles in dRegionTiles.values())/len(dRegionTiles) if dRegionTiles else 0}")
    # 2. Draw Region outlines in differnt colors
    # set colors for regions, ensuring neighboring regions have different colors
    COLORSCHEME = generate_color_scheme(len(dRegionTiles))[1]  # Generate a color scheme 
    
    for i, region in enumerate(dRegionTiles):
        dRegionColors[region] = COLORSCHEME[i]
    

    
        
    # create image and draw
    img = Image.new("RGBA", (int(iWorldX * tile_size), int(iWorldY * tile_size)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # fill tiles with respective region color
    for region, tiles in dRegionTiles.items():
        for tile in tiles:
                x, y = tile
                r,g,b,_ = dRegionColors[region]
                color = (r, g, b, 130)  # Use RGB from color scheme and set alpha to 130 for transparency
                fill_in_tile(x, y, color, img, Hatching=False) 
            


    # draw region outline
    for region, lines in dRegionOutlines.items():
        line_color = dRegionColors[region]
        for start, end in lines:
            draw.line([start, end], fill=line_color, width=line_strength)

    img_path = config.OUTPUT_PATH / f"maps/layers/Geography/{region_type}.webp"
    img.save(img_path, "WEBP", quality=80, method=6)  # Save as WebP with good compression

    
    # save img
    # and add entry to layers config
    add_layer_config_entry(
                            config = json_config,
                            text = f"{region_type.capitalize()} map",
                            category="Geography",
                            image_path = Path(img_path).relative_to(config.OUTPUT_PATH),
                            image_size = img.size
                            )





def DrawGeographyMaps(json_config):
    DrawRegionMap(json_config, region_type="region", tile_size=TILE_SIZE, line_strength=3)
    DrawRegionMap(json_config, region_type="landmass", tile_size=TILE_SIZE, line_strength=3)
    DrawRegionMap(json_config, region_type="continent", tile_size=TILE_SIZE, line_strength=5)
    