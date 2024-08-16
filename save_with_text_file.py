from nodes import SaveImage
import folder_paths as comfy_paths
import os

class SaveWithText(SaveImage):
    FUNCTION = "func"

    @classmethod   
    def INPUT_TYPES(s):
        it = SaveImage.INPUT_TYPES()
        it['required']['text'] = ("STRING", {"default": ""})
        return it
    
    def func(self, images, filename_prefix, text, prompt=None, extra_pnginfo=None):
        returnable = self.save_images(images, filename_prefix, prompt, extra_pnginfo)
        for result in returnable['ui']['images']:
            path = os.path.join(comfy_paths.output_directory, result['subfolder'], result['filename'])
            txt_path = os.path.splitext(path)[0] + ".txt"
            with open(txt_path, 'w') as f:
                print(text, file=f)
        return returnable
    

