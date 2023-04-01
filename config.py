"""
Configuration Variables for Gigapixel plugin
"""
import os
from enum import Enum
from gigapixel import Gigapixel, Scale, Mode

# URL to the Stash instance
STASH_URL = 'http://localhost:9999/graphql'

# API Key from Stash (URL/settings?tab=security)
API_KEY = ""

"""
Setup custom mapped folders in Stash
About: https://github.com/stashapp/stash/pull/620)
This is needed for GraphQL mutation to upload images
"""
# Folder to Stah custom mapped folder i.e. (C:\Stash\custom\static)
CUSTOM_MAPPED_FOLDER = "B:\Stash\custom\static"
# URL to mapped folder as above i.e. (http://localhost:9999/custom)
CUSTOM_MAPPED_URL = "http://localhost:9999/custom"

# Set to yes or no when setting up tags to add images to tags
SET_TAG_IMAGE_GENERATION = 'Yes'

# [TOPAZ GIGAPIXEL] Full path to Topaz Gigapixel exe
EXE_PATH = ""

VERSION = ""

# Gigapixel Output file suffix. (e.g. pic.jpg -> pic-gigapixel.jpg)
# You should set same value inside Gigapixel (File -> Preferences -> Default filename suffix).
IMAGE_NAME = 'image_to_process'
OUTPUT_SUFFIX = '-gigapixel'

# Compatible image types for Gigapixel
IMAGE_TYPES = ['bmp', 'heic', 'heif', 'jpg', 'jpeg', 'jp2', 'j2k', 'tif',
               'tiff', 'png', 'tga', 'webp', 'ppm', 'pgm', 'pbm', 'pnm',
               '3fr', 'ari', 'arw', 'sr2', 'srf', 'bay', 'bmq', 'cap',
               'liq', 'cine', 'crw', 'cr2', 'cr3', 'cs1', 'dc2', 'dcr',
               'drf', 'dsc', 'kc2', 'k25', 'kdc', 'dng', 'erf', 'fff',
               'hdr', 'mos', 'ia', 'mef', 'mdc', 'mrw', 'nef', 'nrw',
               'orf', 'pef', 'ptx', 'pxn', 'qtk', 'raf', 'raw', 'rdc',
               'rw2', 'rwl', 'rwz', 'srw', 'sti', 'x3f']

# Gigapixel Mode enum if version => 6.3
class MODE_EqualAbove6_3(Enum):
    STANDARD = "Standard"
    Lines = "Lines"
    ART_AND_CG = "Art & CG"
    HQ = 'HQ'
    LOW_RES = "Low Res"
    VERY_COMPRESSED = "Very Compressed"

SCALE_MAPPING = {
    "0.5x": Scale.X05,
    "2x": Scale.X2,
    "4x": Scale.X4,
    "6x": Scale.X6,
}

MODE_MAPPING = {
    "Standard": Mode.STANDARD,
    "Lines": Mode.Lines,
    "Art & CG": Mode.ART_AND_CG,
    "Low Resolution": Mode.LOW_RESOLUTION,
    "Very Compressed": Mode.VERY_COMPRESSED,
}

# Gigapixel Mode Mapping if version => 6.3
MODE_MAPPING_EqualAbove6_3 = {
    "Standard": Mode.STANDARD,
    "Lines": Mode.Lines,
    "Art & CG": Mode.ART_AND_CG,
    "Low Res": MODE_EqualAbove6_3.LOW_RES,
    "Very Compressed": Mode.VERY_COMPRESSED,
}

# Gigapixel tag names
TAG_NAMES = ['Upscale Standard:0.5x', 'Upscale Standard:2x',
             'Upscale Standard:4x', 'Upscale Standard:6x',
             'Upscale Lines:0.5x', 'Upscale Lines:2x',
             'Upscale Lines:4x', 'Upscale Lines:6x',
             'Upscale Art & CG:0.5x', 'Upscale Art & CG:2x',
             'Upscale Art & CG:4x', 'Upscale Art & CG:6x',
             'Upscale Low Resolution:0.5x', 'Upscale Low Resolution:2x',
             'Upscale Low Resolution:4x', 'Upscale Low Resolution:6x',
             'Upscale Very Compressed:0.5x', 'Upscale Very Compressed:2x',
             'Upscale Very Compressed:4x', 'Upscale Very Compressed:6x',
             'Upscaled: Performer Image']

# Gigapixel tag names if version => 6.3
TAG_NAMES_EqualAbove6_3 = [
             'Upscale Standard:0.5x', 'Upscale Standard:2x',
             'Upscale Standard:4x', 'Upscale Standard:6x',
             'Upscale Lines:0.5x', 'Upscale Lines:2x',
             'Upscale Lines:4x', 'Upscale Lines:6x',
             'Upscale Art & CG:0.5x', 'Upscale Art & CG:2x',
             'Upscale Art & CG:4x', 'Upscale Art & CG:6x',
             'Upscale HQ:0.5x', 'Upscale HQ:2x',
             'Upscale HQ:4x', 'Upscale HQ:6x',
             'Upscale Low Res:0.5x', 'Upscale Low Res:2x',
             'Upscale Low Res:4x', 'Upscale Low Res:6x',
             'Upscale Very Compressed:0.5x', 'Upscale Very Compressed:2x',
             'Upscale Very Compressed:4x', 'Upscale Very Compressed:6x',
             'Upscaled: Performer Image']

# Mapping of asset images to tag names
TAG_MAPPING = {
    "art&cg-0.5x.svg": "Upscale Art & CG:0.5x",
    "art&cg-2x.svg": "Upscale Art & CG:2x",
    "art&cg-4x.svg": "Upscale Art & CG:4x",
    "art&cg-6x.svg": "Upscale Art & CG:6x",
    "lines-0.5x.svg": "Upscale Lines:0.5x",
    "lines-2x.svg": "Upscale Lines:2x",
    "lines-4x.svg": "Upscale Lines:4x",
    "lines-6x.svg": "Upscale Lines:6x",
    "low-resolution-0.5x.svg": "Upscale Low Resolution:0.5x",
    "low-resolution-2x.svg": "Upscale Low Resolution:2x",
    "low-resolution-4x.svg": "Upscale Low Resolution:4x",
    "low-resolution-6x.svg": "Upscale Low Resolution:6x",
    "standard-0.5x.svg": "Upscale Standard:0.5x",
    "standard-2x.svg": "Upscale Standard:2x",
    "standard-4x.svg": "Upscale Standard:4x",
    "standard-6x.svg": "Upscale Standard:6x",
    "very-compressed-0.5x.svg": "Upscale Very Compressed:0.5x",
    "very-compressed-2x.svg": "Upscale Very Compressed:2x",
    "very-compressed-4x.svg": "Upscale Very Compressed:4x",
    "very-compressed-6x.svg": "Upscale Very Compressed:6x",
    "upscaled-performer-image.svg": "Upscaled: Performer Image"
}

# GigaPixel tag mapping if version => 6.3
TAG_MAPPING_EqualAbove6_3 = {
    "art&cg-0.5x.svg": "Upscale Art & CG:0.5x",
    "art&cg-2x.svg": "Upscale Art & CG:2x",
    "art&cg-4x.svg": "Upscale Art & CG:4x",
    "art&cg-6x.svg": "Upscale Art & CG:6x",
    "hq-0.5x.svg": "Upscale HQ:0.5x",
    "hq-2x.svg": "Upscale HQ:2x",
    "hq-4x.svg": "Upscale HQ:4x",
    "hq-6x.svg": "Upscale HQ:6x",
    "lines-0.5x.svg": "Upscale Lines:0.5x",
    "lines-2x.svg": "Upscale Lines:2x",
    "lines-4x.svg": "Upscale Lines:4x",
    "lines-6x.svg": "Upscale Lines:6x",
    "low-resolution-0.5x.svg": "Upscale Low Res:0.5x",
    "low-resolution-2x.svg": "Upscale Low Res:2x",
    "low-resolution-4x.svg": "Upscale Low Res:4x",
    "low-resolution-6x.svg": "Upscale Low Res:6x",
    "standard-0.5x.svg": "Upscale Standard:0.5x",
    "standard-2x.svg": "Upscale Standard:2x",
    "standard-4x.svg": "Upscale Standard:4x",
    "standard-6x.svg": "Upscale Standard:6x",
    "very-compressed-0.5x.svg": "Upscale Very Compressed:0.5x",
    "very-compressed-2x.svg": "Upscale Very Compressed:2x",
    "very-compressed-4x.svg": "Upscale Very Compressed:4x",
    "very-compressed-6x.svg": "Upscale Very Compressed:6x",
    "upscaled-performer-image.svg": "Upscaled: Performer Image",
}

# Descriptions for each tag
MODE_DESCRIPTIONS = {"Art": "Best for any image that is not a pphotograph, inclues computer graphics, art, drawings or scans.",
                    "HQ": "Best for high quality images from modern cameras. Works Well for images with many details and few compression artifiacts, or as the final set after denoising or sharpening.",
                    "Lines": "Previously called 'Architectural'. Good for architecture, cityscapes, typography and any image with thick lines.",
                    "Low Res": "Previously called 'Compressed. Best for images with blocky compression artifacts. Keeps more detail than the Very Compressed model.",
                    "Standard": "Best choice across a variety of images. Works well for all photography, but can cause artifacts with fur and feathers.",
                    "Compressed": "Best for images with a lot of compression artifacts. For example images that were saved at a small size, scanned images, and old digital images.",
                    "Performer": "Performer Images has been upscaled."
}