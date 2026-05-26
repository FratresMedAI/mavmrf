from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
INCOMING_DATA_DIR = PROJECT_ROOT / "incoming_data"
INCOMING_SAMPLES_DIR = INCOMING_DATA_DIR / "samples"
REPORTS_DIR = PROJECT_ROOT / "reports"
DATA_YAML = PROJECT_ROOT / "data.yaml"
TRAINED_WEIGHTS = PROJECT_ROOT / "runs" / "mavmrf_yolo_training" / "weights" / "best.pt"

CLASS_NAMES = [
    "large_uuv",
    "small_rov",
    "semi_submersible",
    "research_glider",
    "commercial_drone",
    "unidentified_object",
    "surface_buoy",
    "debris_cluster",
]

SIMULATION = {
    "world_width": 1000.0,
    "world_height": 1000.0,
    "depth_min": 5.0,
    "depth_max": 120.0,
    "default_duration_sec": 10,
    "fps": 5,
    "default_num_objects": 8,
    "max_speed_mps": 4.0,
    "min_speed_mps": 0.5,
    "object_spawn_padding": 50,
    "sonar_noise_std": 2.5,
    "acoustic_noise_std": 0.1,
    "magnetic_noise_std": 0.05,
    "optical_noise_std": 3.0,
    "change_detection_threshold": 4.0,
    "default_filter_sensitivity": "medium",
    "filter_sensitivity_scale": {
        "low": 1.4,
        "medium": 1.0,
        "high": 0.65,
    },
    "sensor_weights": {
        "sonar": 0.35,
        "acoustic": 0.2,
        "optical": 0.3,
        "magnetic": 0.15,
    },
}

# Default monitor mode uses simulation detections unless trained weights exist or flags override.
DETECTION = {
    "model_name": "yolov8n.pt",
    "img_size": 640,
    "conf_threshold": 0.35,
    "iou_threshold": 0.45,
    "train_epochs": 10,
    "batch_size": 8,
}

TRACKING = {
    "iou_match_threshold": 0.2,
    "max_age": 8,
    "min_hits": 1,
}

RESPONSE = {
    "proximity_alert_distance": 100.0,
    "high_confidence": 0.7,
    "notification_cooldown_sec": 10,
}

LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
}
