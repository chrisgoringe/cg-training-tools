from .base import BaseNode
from .ui_decorator import ui_signal
import os, json
from PIL import Image, ImageOps
import numpy as np
import torch

def load_image(filepath:str) -> torch.Tensor:
        i = Image.open(filepath)
        text = i.text if hasattr(i,'text') else {}
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        return torch.from_numpy(image)[None,], json.dumps(text, indent=1)

@ui_signal(['modify_self','terminate','display_text'])
class IterateImages(BaseNode):
    REQUIRED = { 
        "folder": ("STRING", {} ), 
        "extensions": ("STRING", {"default":".jpg,.png"}),
        "reset": (["no","yes","always"], {}),
        "delete_images": (["no","yes"], {}),
    }
    RETURN_TYPES = ("IMAGE","STRING","STRING","STRING",)
    RETURN_NAMES = ("image","filepath","metadata",".txt")
    CATEGORY = "utilities/training"

    def func(self, folder, extensions:str, reset, delete_images):
        if not hasattr(self,'files_left') or reset!="no":
            extension_list = extensions.split(",")
            def is_image_filename(filename):
                split = os.path.splitext(filename)
                return len(split)>0 and split[1] in extension_list
            self.files_left = [file for file in os.listdir(folder) if is_image_filename(file)]

        if self.files_left==[]:
            return (None, "", [], "terminate", f"No more files matching {extensions} in {folder}")
        
        filename = self.files_left[0]
        filepath = os.path.join(folder, filename)
        self.files_left = self.files_left[1:]
        message = f"{filename}\n{len(self.files_left)} files remaining"

        image, metadata = load_image(filepath)

        textpath = os.path.splitext(filepath)[0] + ".txt"
        try:
            with open(textpath,'r') as f:
                text = "\n".join(f.readlines())
        except:
            text = ""

        if delete_images=="yes": os.remove(filepath)

        return (image, filepath, metadata, text, [("reset","no"),] if reset!="always" else [], "no" if len(self.files_left) else "autoqueueoff", message)
