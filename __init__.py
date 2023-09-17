import sys, os, git
import folder_paths
try:
    import custom_nodes.cg_custom_core
except:
    print("Installing cg_custom_nodes")
    repo_path = os.path.join(os.path.dirname(folder_paths.__file__), 'custom_nodes', 'cg_custom_core')  
    repo = git.Repo.clone_from('https://github.com/chrisgoringe/cg-custom-core.git/', repo_path)
    repo.git.clear_cache()
    repo.close()

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .iterate_images import *
from .save_description import *
from .describe_image import *
from .vae_training import *

NODE_CLASS_MAPPINGS = { 
    "Iterate Images" : IterateImages, 
    "Describe Image" : TextDescriptionOfImage,
    "Save Description" : SaveDescription,
    "Prepare Vae": PrepareVae,
    "Optimizer Step" : OptimizerStep,
 }

__all__ = ['NODE_CLASS_MAPPINGS']

