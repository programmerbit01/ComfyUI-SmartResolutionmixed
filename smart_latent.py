import torch
from .latent_utils import (
    MODES,
    IMAGE_PRESET_KEYS,
    VIDEO_PRESET_KEYS,
    MULTIPLE_PROFILE_KEYS,
    ASPECT_RATIOS,
    snap_to_multiple,
    resolve_multiple,
    normalize_aspect_ratio,
    parse_mode_presets,
    get_long_side,
)

class SmartLatentGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (MODES, {"default": "Video"}),
                "image_preset": (IMAGE_PRESET_KEYS, {"default": "SD (512)"}),
                "video_preset": (VIDEO_PRESET_KEYS, {"default": "480p"}),
                "multiple_profile": (MULTIPLE_PROFILE_KEYS, {"default": "Auto (Image=64, Video=32)"}),
                "aspect_ratio": (list(ASPECT_RATIOS.keys()), {"default": "9:16-TikTokReel"}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 16}),
            },
            "optional": {
                "resolution_preset": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("LATENT",)
    FUNCTION = "generate"
    CATEGORY = "latent/generator"

    def generate(self, mode, image_preset, video_preset, multiple_profile, aspect_ratio, batch_size, resolution_preset=""):
        mode, image_preset, video_preset, multiple_profile = parse_mode_presets(
            mode, image_preset, video_preset, multiple_profile, resolution_preset
        )
        aspect_ratio = normalize_aspect_ratio(aspect_ratio)
        long_side = get_long_side(mode, image_preset, video_preset)
        multiple = resolve_multiple(mode, multiple_profile)
        ar_w, ar_h = ASPECT_RATIOS[aspect_ratio]

        scale = long_side / float(max(ar_w, ar_h))
        width = snap_to_multiple(ar_w * scale, multiple)
        height = snap_to_multiple(ar_h * scale, multiple)

        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        return ({"samples": latent},)
