import os
if os.getenv('LED_ENV') == 'production':
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
else:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics

# class RGBMatrixWrapper:
#   # def __init__(self):
#   #   self.json = layout_json

#   @classmethod
#   def RGBMatrix(cls):
#     return RGBMatrix

#   @classmethod
#   def RGBMatrixOptions(cls):
#     return RGBMatrixOptions

#   @classmethod
#   def graphics(cls):
#     return graphics
