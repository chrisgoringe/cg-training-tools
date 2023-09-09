from .common import TrainingBase, textdisplay, terminator, selfmodify
import os
from PIL import Image, ImageOps
import numpy as np
import torch

def load_image(filepath:str) -> torch.Tensor:
        i = Image.open(filepath)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        return torch.from_numpy(image)[None,]

@selfmodify
@terminator
@textdisplay
class IterateImages(TrainingBase):
    def __init__(self):
        self.files_left = None

    REQUIRED = { 
        "folder": ("STRING", {} ), 
        "extensions": ("STRING", {"default":".jpg,.png"}),
        "reset": (["no","yes"], {})
    }
    RETURN_TYPES = ("IMAGE","STRING",)
    RETURN_NAMES = ("image","filepath",)

    def func(self, folder, extensions:str, reset):
        if self.files_left is None or reset=="yes":
            extension_list = extensions.split(",")
            def is_image_filename(filename):
                split = os.path.splitext(filename)
                return len(split)>0 and split[1] in extension_list
            self.files_left = [file for file in os.listdir(folder) if is_image_filename(file)]

        if self.files_left==[]:
            return (None, "", [], "yes", f"No more files matching {extensions} in {folder}")
        
        filepath = os.path.join(folder, self.files_left[0])
        self.files_left = self.files_left[1:]
        message = f"{len(self.files_left)} files remaining"
        terminate = "yes" if len(self.files_left)==0 else "no"

        return (load_image(filepath), filepath, [("reset","no"),], terminate, message)
