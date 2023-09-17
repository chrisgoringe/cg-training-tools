from custom_nodes.cg_custom_core.base import BaseNode
from custom_nodes.cg_custom_core.ui_decorator import ui_signal
import comfy.sd
import torch.optim as optim
import torch.nn as nn

class PrepareVae(BaseNode):
    REQUIRED = {
        "vae": ("VAE", {})
    }
    CATEGORY = "utilities/training"
    RETURN_TYPES = ("VAE","OPTIMIZER",)
    RETURN_NAMES = ("vae","optimizer",)

    def func(self, vae:comfy.sd.VAE):
        vae.first_stage_model.decoder.requires_grad_()
        params = vae.first_stage_model.decoder.mid.attn_1.parameters()
        optimizer = optim.AdamW(params)
        return (vae,optimizer)

@ui_signal(['display_text'])
class OptimizerStep(BaseNode):
    REQUIRED = {
        "true_image": ("IMAGE", {}),
        "pred_image": ("IMAGE", {}),
        "vae": ("VAE", {}),
        "optimizer": ("OPTIMIZER", {}),
    }
    CATEGORY = "utilities/training"
    RETURN_TYPES = ("FLOAT","VAE","OPTIMIZER",)
    RETURN_NAMES = ("loss","vae", "optimizer",)

    loss_fn = nn.MSELoss()

    def func(self, true_image, pred_image, vae, optimizer):
        loss = self.loss_fn(true_image, pred_image)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        return (loss, vae, optimizer, f"loss = {loss}")