def extract_palette(color_palette):
    if isinstance(color_palette, dict):
        return list(color_palette.values())
    elif isinstance(color_palette, list):
        return color_palette
    else:
        raise ValueError('Not a color list or a dictionary')
