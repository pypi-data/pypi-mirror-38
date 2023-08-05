import ctypes
import subprocess
import math
from os.path import join, basename, dirname
from wand.image import Image
from wand.api import library
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
from datetime import datetime

library.MagickAutoGammaImage.argtypes = (ctypes.c_void_p,)  # MagickWand *


class SelfDevPhoto(object):
    def __init__(self, filepath, logo=None, border_color='white', label=''):
        self.filepath = filepath
        filename = basename(filepath)
        root_path = dirname(filepath)
        self.working_path = join(root_path, "polaroid", filename)
        img = Image(filename=filepath)
        print("largeur:{}  hauteur:{}".format(img.width, img.height))
        if img.width > img.height:
            size = img.height
            coord_x, coord_y = (img.width//2 - size//2, 0)
            rotate = 0
        else:
            size = img.width
            coord_x, coord_y = (0, img.height//2 - size//2)
            rotate = 1
        coord = (coord_x, coord_y, coord_x + size, coord_y + size)
        img.crop(*coord)
        self.save(img)
#        self.colortone('#222b6d', 50, 0)
#        self.colortone('#f7daae', 120, 1)
        self.polaroid()
        self.vignette()
        img = Image(filename=self.working_path)
        img.resize(width=930, height=930)
        if rotate:
            img = img.rotate(90)
        with Color('gray') as border:
            img.border(border, 6, 6)
        with Color('White') as bg:
            new_img = Image(height=60+930+268, width=60+930+60,
                            background=bg, resolution=300)
        new_img.composite(img, 60-6, 60-6)
        if logo:
            with Image(filename=logo) as logo:
                logo.resize(height=250, width=792)
                new_img.composite(logo, 129, 1002)
        if label:
            with Drawing() as draw:
                draw.font = 'JMH_Typewriter.otf'
                draw.font_size = 12
                draw.text(185, 365, "{}, le {}".format(
                            label, datetime.now().strftime("%d/%m/%Y")))
                draw(new_img)
        with Color('black') as border:
            new_img.border(border, 1, 1)
        self.save(new_img)

    def save(self, img):
        self.image = img
        img.save(filename=self.working_path)

    def autogamma(self, wand):
        if not isinstance(wand, Image):
            raise TypeError('wand must be instance of Image, not '
                            + repr(wand))
        library.MagickAutoGammaImage(wand.wand)

    def execute(self, command, **kwargs):
        default = {'filename': self.working_path,
                   'width': self.image.width,
                   'height': self.image.height}
        cformat = {**default, **kwargs}
        command = command.format(**cformat)
        error = subprocess.check_output(command, shell=True,
                                        stderr=subprocess.STDOUT)
        return error

    def colortone(self, color, level, type=0):
        arg0 = level
        arg1 = 100 - level
        if type == 0:
            negate = '-negate'
        else:
            negate = ''

        self.execute((
            "convert {filename} \( -clone 0 -fill '{color}' -colorize 100% \)"
            " \( -clone 0 -colorspace gray {negate} \) -compose blend "
            "-define compose:args={arg0},{arg1} -composite {filename}"),
            color=color,
            negate=negate,
            arg0=arg0,
            arg1=arg1
        )

    def polaroid(self):
        self.execute((
            "convert {filename} -color-matrix '6x3: "
            "1.438 -0.122 -0.016 0 0 -0.03 "
            "-0.062 1.378 -0.016 0 0 0.05 "
            "-0.062 -0.122 1.483 0 0 -0.02' {filename}"))

    def vignette(self, color_1='none', color_2='black', crop_factor=2.5):
        crop_x = math.floor(self.image.width * crop_factor)
        crop_y = math.floor(self.image.height * crop_factor)

        self.execute((
            "convert \( {filename} \) \( -size {crop_x}x{crop_y} "
            "radial-gradient:{color_1}-{color_2} -gravity center "
            "-crop {width}x{height}+0+0 +repage \) -compose multiply "
            "-flatten {filename}"),
            crop_x=crop_x,
            crop_y=crop_y,
            color_1=color_1,
            color_2=color_2,
        )
