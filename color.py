import colorsys

# Tune this in [0, 1] if you don't want the light to reach max brightness.
MAX_BRIGHTNESS = 1

# Takes a color and a brightness target in [0, 1].
def adjust_brightness(color, target):
    return (color[0], color[1], color[2] * target * MAX_BRIGHTNESS, color[3])

# Interpolates between hsbk1 and hsbk2, where alpha is a number in
# [0, 1] indicating how close we are to hsbk2.
def interpolate(hsbk1, hsbk2, alpha):
    # Normalize the values in the range [0, 1] based on LIFX ranges.
    hsbk1 = tuple([x / 65535 for x in hsbk1])
    hsbk2 = tuple([x / 65535 for x in hsbk2])

    rgb1 = colorsys.hsv_to_rgb(hsbk1[0], hsbk1[1], hsbk1[2])
    rgb2 = colorsys.hsv_to_rgb(hsbk2[0], hsbk2[1], hsbk2[2])
    interpolated_rbg = [(rgb2[i] - rgb1[i]) * alpha + rgb1[i] for i in range(3)]

    interpolated_hsv = colorsys.rgb_to_hsv(interpolated_rbg[0], interpolated_rbg[1], interpolated_rbg[2])

    return tuple([interpolated_hsv[0] * 65535, interpolated_hsv[1] * 65535, interpolated_hsv[2] * 65535, hsbk1[3]])