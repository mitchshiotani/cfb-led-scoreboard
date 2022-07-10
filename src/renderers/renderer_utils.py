from rgbmatrix import graphics

class RendererUtils:
  def convert_hex_to_rgb(self, hex_str):
    # convert hex to rgb, to put into graphics.Color()
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return {'r': r, 'g': g, 'b': b}
