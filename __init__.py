import sys, os, git
import folder_paths
try:
    from custom_nodes.cg_custom_core import CC_VERSION
    if CC_VERSION < 2.3: raise Exception()
except:
    print("Installing cg_custom_nodes - you may need to restart comfy")
    repo_path = os.path.join(os.path.dirname(folder_paths.__file__), 'custom_nodes', 'cg_custom_core')  
    repo = git.Repo.clone_from('https://github.com/chrisgoringe/cg-custom-core.git/', repo_path)
    repo.git.clear_cache()
    repo.close()

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .iterate_images import *
from .save_description import *
from .describe_image import *
from save_with_text_file import *

NODE_CLASS_MAPPINGS = { 
    "Iterate Images" : IterateImages, 
    "Save With Text File" : SaveWithText,
    "Describe Image" : TextDescriptionOfImage,
    "Save Description" : SaveDescription,
 }

__all__ = ['NODE_CLASS_MAPPINGS']

