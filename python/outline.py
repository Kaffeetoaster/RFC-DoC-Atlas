from PIL import Image, ImageDraw

def create_tile_outline(image_width, image_height, tiles_x, tiles_y, output_path):
    # Create transparent image
    img = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate tile size from counts
    tile_width = image_width / tiles_x
    tile_height = (image_height-23-27) / tiles_y
    print(f"tilewidth in pixels: {tile_width}")
    print(f"tileheigth in pixels: {tile_height}")
    

    # Draw vertical lines
    for i in range(tiles_x + 1):
        x = int(round(i * tile_width))
        draw.line([(x, 0), (x, image_height)], fill=(0, 0, 0, 255), width=1)

    # Draw horizontal lines
    offset_y = 23
    for i in range(tiles_y + 1):
        y = int(round(i * tile_height)) + offset_y
        draw.line([(0, y), (image_width, y)], fill=(0, 0, 0, 255), width=1)

    # Save image
    img.save(output_path)

# Example: 150 tiles wide, 80 tiles high
create_tile_outline(
    image_width=8112,
    image_height=4170,
    tiles_x=156,
    tiles_y=80,
    output_path="./maps/tile_outline.png"
)