from .common import TrainingBase
import os

class SaveDescription(TrainingBase):
    REQUIRED = {"description": ("STRING", {"defaultInput":True}), "image_filepath": ("STRING", {"defaultInput":True})}
    OUTPUT_NODE = True
    def func(self, description, image_filepath):
        text_filepath = os.path.splitext(image_filepath)[0] + ".txt"
        print(description, file=open(file=text_filepath,mode="w"))
        return ()
