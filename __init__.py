import sys, os

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .iterate_images import *
from .save_description import *
from .describe_image import *
from .save_with_text_file import *

NODE_CLASS_MAPPINGS = { 
    "Iterate Images" : IterateImages, 
    "Save With Text File" : SaveWithText,

    "Describe Image" : TextDescriptionOfImage,
    "Save Description" : SaveDescription,
 }

WEB_DIRECTORY = "./js" 
__all__ = ['NODE_CLASS_MAPPINGS', 'WEB_DIRECTORY']

