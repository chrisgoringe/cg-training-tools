import sys, os, shutil

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .iterate_images import *
from .common import *
from .save_description import *
from .describe_image import *

NODE_CLASS_MAPPINGS = { 
    "Iterate Images" : IterateImages, 
    "Describe Image" : TextDescriptionOfImage,
    "Save Description" : SaveDescription }

__all__ = ['NODE_CLASS_MAPPINGS']

shutil.copytree(module_js_directory_training, application_web_extensions_directory, dirs_exist_ok=True)