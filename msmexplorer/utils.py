from .palettes import all_rgb


def extract_palette(color_palette):
    if isinstance(color_palette, dict):
        return list(color_palette.values())
    elif isinstance(color_palette, list):
        return color_palette
    elif isinstance(color_palette, str):
        return all_rgb[color_palette]
    else:
        raise ValueError('Not a color list or a dictionary')
