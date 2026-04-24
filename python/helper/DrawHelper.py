
from python.consts import *
from python.helper.helper import *

from PIL import Image, ImageDraw


def get_area_outline(rect_coords, exceptions, tile_size, line_strength):
    """
    rect_coords: ((x1, y1), (x2, y2)) defining the bounding box of tiles.
    exceptions: list of (x, y) tuples within bounds to exclude.
    Returns: List of line segments [((x1, y1), (x2, y2)), ...]
    """
    (x_min, y_min), (x_max, y_max) = rect_coords
    active_tiles = set()

    # 1. Map out active tiles within the rectangle that aren't excepted
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max +1):
            if (x, y) not in exceptions:
                active_tiles.add((x, y))

    lines = []
    inset = (line_strength-1) // 2  # Inset to avoid overlap with neighbouring tiles
    
    for (x, y) in active_tiles:
        # Pixel boundaries of the current tile, but inset to draw inside the tile
        
        p_left = x * tile_size 
        p_top = y * tile_size
        p_right = (x + 1) * tile_size - 1
        p_bottom = (y + 1) * tile_size - 1

        # Define neighbours and the corresponding edge lines
        # Check: Is neighbour (nx, ny) outside rect OR in exceptions list?
        check_configs = [
            # neighbour, (x1, y1, x2, y2), Side
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
            # If neighbour is outside the rect bounds OR is an explicit exception
            is_outside_bounds = not (x_min <= nx <= x_max and y_min <= ny <= y_max)
            is_exception = (nx, ny) in exceptions
            
            if is_outside_bounds or is_exception:
                # Add the line segment for the exposed edge
                lines.append(((lx1, ly1), (lx2, ly2)))

    return lines

def draw_outlines(lines, color, line_strength, img):
    # Create a transparent or solid background image
    # 'RGBA' is useful if you want to overlay this on another image
    
    draw = ImageDraw.Draw(img)

    for start_point, end_point in lines:
        # start_point and end_point are (x, y) tuples
        
        draw.line([start_point, end_point], fill=color, width=line_strength)

    return img

def draw_outlines_for_area( tArea, LExceptions, color, line_strength, img):
    (x_min, y_min), (x_max, y_max) = tArea
    width_px = (x_max - x_min + 1) * TILE_SIZE
    height_px = (y_max - y_min + 1) * TILE_SIZE
    offset = (-x_min * TILE_SIZE, -y_min * TILE_SIZE)
    lines = get_area_outline(tArea, LExceptions, tile_size=TILE_SIZE, line_strength=line_strength)
    #for start, end in lines:
        # start = transform_coordinates(start, new_width=width_px, new_height=height_px, offset=offset)
        # end = transform_coordinates(end, new_width=width_px, new_height=height_px, offset=offset)
        # lines_transformed.append((start, end))
    draw_outlines(lines, color=color, line_strength=line_strength, img=img)

def create_HatchMask(hatching_width, hatching_line_width,tile_size):
    # Build a reusable diagonal hatch mask once; 255 = painted pixel, 0 = transparent pixel.
    scale_factor = 1  # Adjust this to make the hatching denser or sparser
    hatching_width = 3  # Distance between hatch lines
    hatching_line_width = 1  # Thickness of hatch lines

    HATCH_MASK = Image.new("L", (tile_size * scale_factor, tile_size * scale_factor), 0)
    _hatch_draw = ImageDraw.Draw(HATCH_MASK)
    for offset in range(0 + hatching_width*scale_factor, tile_size * scale_factor * 2, hatching_width*scale_factor +1):
        _hatch_draw.line(
            [(offset, 0), (offset - tile_size * scale_factor, tile_size * scale_factor)],
            fill=255, 
            width=hatching_line_width*scale_factor
            )
    # scale back down to tile size
    HATCH_MASK = HATCH_MASK.resize((TILE_SIZE, TILE_SIZE), resample=Image.LANCZOS)
    return HATCH_MASK

def fill_in_tile(x, y, color, img, Hatching = False):
    tile_left = x * TILE_SIZE
    tile_top = y * TILE_SIZE
    tile_color = color if len(color) == 4 else (*color, 255)
    tile = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), tile_color)
    if Hatching:
        HATCH_MASK = create_HatchMask(11,2,TILE_SIZE)
        
        img.paste(tile, (tile_left, tile_top), HATCH_MASK)
    else:
        img.paste(tile, (tile_left, tile_top))

def draw_fill_in_area(area, exceptions, color, img, Hatching = False):
    (x_min, y_min), (x_max, y_max) = area
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            if (x, y) not in exceptions:
                fill_in_tile(x, y, color, img, Hatching= Hatching)
    


    





