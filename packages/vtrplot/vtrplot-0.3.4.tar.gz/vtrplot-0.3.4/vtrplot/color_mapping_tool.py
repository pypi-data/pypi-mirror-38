from __future__ import print_function

from defusedxml.ElementTree import parse
import os
import json


def cl2xml_to_swatch(input_cl2_filepath, output_filepath=None):
    # Converts cl2 internal format to our internal swatch

    colors = _get_colors_from_cl2xml(input_cl2_filepath)
    colors_rgb = map(_hexcolor_to_rgb256_tuple, colors)

    if output_filepath:
        with open(output_filepath, "w") as f:
            json.dump(colors_rgb, f)
    else:
        print("# JSON representation:")
        print(json.dumps(colors_rgb))


def cl2xml_to_matlab(input_cl2_filepath, name, output_path="."):
    # Converts cl2 internal format to a matlab colormap file

    colors = _get_colors_from_cl2xml(input_cl2_filepath)
    colors_rgb = map(_hexcolor_to_rgb1_tuple, colors)

    output_filename = name + ".m"
    output_filepath = os.path.join(output_path, output_filename)

    with open(output_filepath, "w") as f:
        f.write(matlab_doc_template_start.format(palette_name=name))
        for color in colors_rgb:
            f.write("{:.5f}, {:.5f}, {:.5f};\n".format(*color))
        f.write("];\n")


def _get_colors_from_cl2xml(input_cl2_filepath):
    if not os.path.isfile(input_cl2_filepath):
        raise ValueError('Input does not seem to be a valid file')

    palette = parse(input_cl2_filepath).getroot()
    colors = map(lambda x: x.attrib["color"], palette.findall("paint"))
    if len(colors) != 256:
        print("Warning: expected palette to contain 256 colors, but got %d" % len(colors))

    return colors


def _hexcolor_to_rgb256_tuple(hexcolor):
    # "#ffffff" -> (255, 255, 255)
    hexcolor = hexcolor.lstrip('#')
    return tuple(int(hexcolor[i:i + 2], base=16) for i in (0, 2, 4))


def _hexcolor_to_rgb1_tuple(hexcolor):
    # "#ffffff" -> (1.00000, 1.00000, 1.00000)
    rgb256 = _hexcolor_to_rgb256_tuple(hexcolor)
    return tuple(round(color / 255.0, 5) for color in rgb256)


matlab_doc_template_start = """function c = {palette_name}()

% converted from cl2 xml file

c = [
"""
