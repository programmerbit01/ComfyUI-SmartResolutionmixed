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

class SmartResolutionPicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (MODES, {"default": "Image"}),
                "image_preset": (IMAGE_PRESET_KEYS, {"default": "1K (1024)"}),
                "video_preset": (VIDEO_PRESET_KEYS, {"default": "720p (1280x720)"}),
                "multiple_profile": (MULTIPLE_PROFILE_KEYS, {"default": "Auto (Image=64, Video=32)"}),
                "aspect_ratio": (list(ASPECT_RATIOS.keys()), {"default": "16:9-Widescreen"}),
            },
            "optional": {
                # Backward compatibility with older saved workflows
                "resolution_preset": ("STRING", {"default": "HD-1280px"}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution_info")
    FUNCTION = "calculate"
    CATEGORY = "utils/latent"

    def calculate(self, mode, image_preset, video_preset, multiple_profile, aspect_ratio, resolution_preset=""):
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

        info = f"{width}x{height} | {mode} | {aspect_ratio} | mul={multiple}"
        return {
            "ui": {"text": [info]},
            "result": (width, height, info),
        }
