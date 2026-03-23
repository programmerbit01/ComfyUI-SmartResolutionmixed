from .smart_resolution import SmartResolutionPicker
from .smart_latent import SmartLatentGenerator

NODE_CLASS_MAPPINGS = {
    "SmartResolutionPicker": SmartResolutionPicker,
    "SmartLatentGenerator": SmartLatentGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SmartResolutionPicker": "Smart Resolution Picker",
    "SmartLatentGenerator": "Smart Latent Generator",
}
