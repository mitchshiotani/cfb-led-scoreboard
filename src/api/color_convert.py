from webcolors import hex_to_rgb, rgb_to_hex
from colorsys import rgb_to_hsv, hsv_to_rgb
import math

primary = "F20017" # the background color
alternative = "f5f1e7" # the text color

def hex_to_hsv(hex):
    # input: string of hex
    if hex[0] != '#':
        hex = '#' + hex

    rgb = hex_to_rgb(hex)
    hsv = rgb_to_hsv(*rgb) 
    # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255].

    return hsv

def hsv_to_hex(hsv):
    # input: set of hsv values
    # output: string of hex (with # at beginning)
    rgb = hsv_to_rgb(*hsv)
    # hex = rgb_to_hex((int(c) for c in rgb))
    hex = rgb_to_hex((int(math.ceil(c)) for c in rgb))

    return hex


def darken_text(primary_hsv, alternative_hsv):
    # returns [primary_hsv, alternative_hsv] with new alternative_hsv
    # with darker values

    # change to list

    # print(alternative_hsv)
    alternative_hsv = list(alternative_hsv)

    # keep unchanged if alt is dark enough
    if alternative_hsv[2] <= 225 * 0.25:
        # print("color unchanged!")
        return [primary_hsv, alternative_hsv]

    # alternative_hsv[1] = 0.01
    alternative_hsv[2] = 225 * 0.14
    # print(tuple(alternative_hsv))
    return [primary_hsv, tuple(alternative_hsv)]

def brighten_text(primary_hsv, alternative_hsv):
    # returns [primary_hsv, alternative_hsv] with new alternative_hsv
    # with brighter values

    # change to list

    # print(alternative_hsv)
    alternative_hsv = list(alternative_hsv)

    # keep unchanged if alt is bright enough
    if alternative_hsv[2] >= 225 * 0.85:
        print("color unchanged!")
        return [primary_hsv, alternative_hsv]

    alternative_hsv[1] = 0.01
    alternative_hsv[2] = 225 * 0.99
    # print(tuple(alternative_hsv))
    return [primary_hsv, tuple(alternative_hsv)]

def adjust_colors(primary_hex, alternative_hex):
    # input: two strings 
    # output: ONE list with two strings

    # convert to hsv
    primary_hsv = hex_to_hsv(primary_hex)
    alternative_hsv = hex_to_hsv(alternative_hex)
    # check how bright primary color is
    primary_value = primary_hsv[2]
    # if primary color is dark, brighten alt color
    if primary_value < 225 * 0.85:
        # print("dark background; making text brighter")
        adj_cs = brighten_text(primary_hsv, alternative_hsv)
        # print([hsv_to_hex(adj_cs[0]), hsv_to_hex(adj_cs[1])])
        return [hsv_to_hex(adj_cs[0]), hsv_to_hex(adj_cs[1])]

    # elif primary color is bright, darken alt color
    elif primary_value > 225 * 0.95:
        # print("bright background; making text darker")
        adj_cs = darken_text(primary_hsv, alternative_hsv)
        # print([hsv_to_hex(adj_cs[0]), hsv_to_hex(adj_cs[1])])
        return [hsv_to_hex(adj_cs[0]), hsv_to_hex(adj_cs[1])]

    # if no changes, return original values
    return [primary_hex, alternative_hex]
