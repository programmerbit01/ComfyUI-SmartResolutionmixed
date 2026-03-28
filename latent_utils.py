MODES = ["Image", "Video"]

IMAGE_PRESETS = {
    "SD (512)": 512,
    "HD (768)": 768,
    "1K (1024)": 1024,
    "2K (2048)": 2048,
    "3K (3072)": 3072,
    "4K (4096)": 4096,
}

VIDEO_PRESETS = {
    "360p (640x360)": 640,
    "480p (854x480)": 854,
    "520p (960x520)": 960,
    "720p (1280x720)": 1280,
    "1080p (1920x1080) - Premium": 1920,
}

MULTIPLE_PROFILES = {
    "Auto (Image=64, Video=32)": "auto",
    "Flux / SDXL (64)": 64,
    "LTX (32)": 32,
    "Wan (16)": 16,
    "SD1.5 (8)": 8,
}

IMAGE_PRESET_KEYS = list(IMAGE_PRESETS.keys())
VIDEO_PRESET_KEYS = list(VIDEO_PRESETS.keys())
MULTIPLE_PROFILE_KEYS = list(MULTIPLE_PROFILES.keys())

LEGACY_PRESETS = {
    "SD-512px": 512,
    "HD-1280px": 1280,
    "FullHD-1920px": 1920,
    "2K-2048px": 2048,
    "QHD-2560px": 2560,
    "4K-3840px": 3840,
    "8K-7680px": 7680,
    "FullHD_1920x1080": 1920,
}

ASPECT_RATIOS = {
    # Square
    "1:1-AlbumArt": (1, 1),

    # Portrait Formats
    "4:5-InstagramPortrait": (4, 5),
    "2:3-ClassicPortrait": (2, 3),
    "3:4-EditorialPortrait": (3, 4),

    # Vertical Video
    "9:16-TikTokReel": (9, 16),

    # Landscape / Video
    "4:3-ClassicVideo": (4, 3),
    "16:9-Widescreen (YouTube)": (16, 9),

    # Cinematic Aspect
    "21:9-CinemaScope": (21, 9),

    # Ultra Wide
    "32:9-UltraWideBanner": (32, 9),
}

def snap_to_multiple(x, multiple):
    return max(multiple, int(round(x / float(multiple))) * multiple)


def resolve_multiple(mode, multiple_profile):
    value = MULTIPLE_PROFILES.get(multiple_profile, "auto")
    if value == "auto":
        return 32 if mode == "Video" else 64
    return int(value)


def normalize_aspect_ratio(aspect_ratio):
    # Allow old broken saved values too
    if aspect_ratio == "16:9_Widescreen":
        return "16:9-Widescreen (YouTube)"
    if aspect_ratio == "16:9-Widescreen":
        return "16:9-Widescreen (YouTube)"
    if aspect_ratio in ASPECT_RATIOS:
        return aspect_ratio
    return "16:9-Widescreen (YouTube)"


def nearest_image_preset(long_side):
    return min(IMAGE_PRESETS, key=lambda k: abs(IMAGE_PRESETS[k] - long_side))


def nearest_video_preset(long_side):
    return min(VIDEO_PRESETS, key=lambda k: abs(VIDEO_PRESETS[k] - long_side))


def parse_mode_presets(mode, image_preset, video_preset, multiple_profile, resolution_preset=""):
    if mode not in MODES:
        mode = "Image"

    # Migrate old workflows carrying resolution_preset only
    if resolution_preset in LEGACY_PRESETS:
        legacy_long = LEGACY_PRESETS[resolution_preset]
        if mode == "Video":
            video_preset = nearest_video_preset(legacy_long)
        else:
            image_preset = nearest_image_preset(legacy_long)

    if image_preset not in IMAGE_PRESETS:
        image_preset = "1K (1024)"
    if video_preset not in VIDEO_PRESETS:
        video_preset = "720p (1280x720)"
    if multiple_profile not in MULTIPLE_PROFILES:
        multiple_profile = "Auto (Image=64, Video=32)"

    return mode, image_preset, video_preset, multiple_profile


def get_long_side(mode, image_preset, video_preset):
    if mode == "Video":
        return VIDEO_PRESETS[video_preset]
    return IMAGE_PRESETS[image_preset]
