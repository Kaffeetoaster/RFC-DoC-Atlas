from PIL import Image, ImageDraw




from python.consts import *
from python.helper.helper import *



def get_tile_outline(rect_coords, exceptions, tile_size, line_strength):
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
    inset = (line_strength-1) // 2  # Inset to avoid overlap with neighboring tiles
    
    for (x, y) in active_tiles:
        # Pixel boundaries of the current tile, but inset to draw inside the tile
        
        p_left = x * tile_size 
        p_top = y * tile_size
        p_right = (x + 1) * tile_size - 1
        p_bottom = (y + 1) * tile_size - 1

        # Define neighbors and the corresponding edge lines
        # Check: Is neighbor (nx, ny) outside rect OR in exceptions list?
        check_configs = [
            # Neighbor, (x1, y1, x2, y2), Side
            ((x - 1, y), (p_left + inset, p_top, p_left + inset, p_bottom), "L"),
            ((x + 1, y), (p_right - inset, p_top, p_right - inset, p_bottom), "R"),
            ((x, y - 1), (p_left, p_top + inset, p_right, p_top + inset), "T"),
            ((x, y + 1), (p_left, p_bottom - inset, p_right, p_bottom - inset), "B")
        ]

        for (nx, ny), (lx1, ly1, lx2, ly2), side in check_configs:
            # If neighbor is outside the rect bounds OR is an explicit exception
            is_outside_bounds = not (x_min <= nx <= x_max and y_min <= ny <= y_max)
            is_exception = (nx, ny) in exceptions
            
            if is_outside_bounds or is_exception:
                # Add the line segment for the exposed edge
                lines.append(((lx1, ly1), (lx2, ly2)))

    return lines

def draw_outlines(lines, width_px, height_px, color, line_strength):
    # Create a transparent or solid background image
    # 'RGBA' is useful if you want to overlay this on another image
    img = Image.new('RGBA', (width_px, height_px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for start_point, end_point in lines:
        # start_point and end_point are (x, y) tuples
        
        draw.line([start_point, end_point], fill=color, width=line_strength)

    return img

def draw_outlines_for_area( tArea, LExceptions, color, line_strength):
    (x_min, y_min), (x_max, y_max) = tArea
    width_px = (x_max - x_min + 1) * TILE_SIZE
    height_px = (y_max - y_min + 1) * TILE_SIZE
    offset = (-x_min * TILE_SIZE, -y_min * TILE_SIZE)
    lines = get_tile_outline(tArea, LExceptions, tile_size=TILE_SIZE, line_strength=line_strength)
    lines_transformed = []
    for start, end in lines:
        start = transform_coordinates(start, new_width=width_px, new_height=height_px, offset=offset)
        end = transform_coordinates(end, new_width=width_px, new_height=height_px, offset=offset)
        lines_transformed.append((start, end))
    img = draw_outlines(lines_transformed, width_px, height_px, color=color, line_strength=line_strength)
    return img





