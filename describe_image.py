from custom_nodes.cg_custom_core.base import BaseNode
from custom_nodes.cg_custom_core.ui_decorator import ui_signal
from .models.blip import blip_decoder
import os
import sys
import numpy as np
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from PIL import Image
from folder_paths import models_dir

BLIP_NODE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BLIP_NODE_ROOT)

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(
        np.clip(255.0 * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
    )

def transformImage(input_image, image_size, device):
    raw_image = input_image.convert("RGB")
    raw_image = raw_image.resize((image_size, image_size))
    transform = transforms.Compose(
        [
            transforms.Resize(raw_image.size, interpolation=InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.48145466, 0.4578275, 0.40821073),
                (0.26862954, 0.26130258, 0.27577711),
            ),
        ]
    )
    image = transform(raw_image).unsqueeze(0).to(device)
    return image.view(
        1, -1, image_size, image_size
    )  # Change the shape of the output tensor

@ui_signal('display_text')
class TextDescriptionOfImage(BaseNode):
    REQUIRED = { "image": ("IMAGE",),
                 "min_length": ("INT", {"default":5, "min":0, "max":100}), 
                 "max_length": ("INT", {"default":20, "min":0, "max":100}) }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    CATEGORY = "utilities/training"
    
    def func(self, image, min_length, max_length):
# Change the current working directory to BLIP_NODE_ROOT
        cwd = os.getcwd()
        os.chdir(BLIP_NODE_ROOT)

        # Add BLIP_NODE_ROOT to the Python path
        #sys.path.insert(0, BLIP_NODE_ROOT)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        image = tensor2pil(image)
        size = 384

        tensor = transformImage(image, size, device)

        blip_dir = os.path.join(models_dir, "blip")
        if not os.path.exists(blip_dir):
            os.mkdir(blip_dir)

        torch.hub.set_dir(blip_dir)

        model_url = "https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth"

        model = blip_decoder(pretrained=model_url, image_size=size, vit="base")
        model.eval()
        model = model.to(device)

        with torch.no_grad():
            caption = model.generate(
                tensor,
                sample=False,
                num_beams=1,
                min_length=min_length,
                max_length=max_length,
            )

        os.chdir(cwd)
        return (caption[0],caption[0],)
    