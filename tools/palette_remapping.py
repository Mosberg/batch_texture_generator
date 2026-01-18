from PIL import Image
import numpy as np
import json


def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))


def load_palette(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return [hex_to_rgb(c) for c in data["items"][0]["groups"]["base"]["colors"]]


def closest_color(pixel, palette):
    pixel = np.array(pixel[:3])
    distances = [np.linalg.norm(pixel - np.array(color)) for color in palette]
    return palette[np.argmin(distances)]


def remap_image(image_path, palette, output_path):
    img = Image.open(image_path).convert("RGBA")
    pixels = np.array(img)

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            if pixels[y, x][3] > 0:  # skip fully transparent
                pixels[y, x][:3] = closest_color(pixels[y, x], palette)

    new_img = Image.fromarray(pixels, "RGBA")
    new_img.save(output_path)


# Load palettes
iron_palette = load_palette("palettes/metal/iron.texture-palettes.json")
oak_palette = load_palette("palettes/wood/oak.texture-palettes.json")

# Remap images
remap_image(
    "remap/iron_keg_32x32.png",
    iron_palette,
    "remap/iron_keg_recolored.png",
)
remap_image(
    "remap/oak_iron_barrel_32x32.png",
    oak_palette,
    "remap/oak_iron_barrel_recolored.png",
)
