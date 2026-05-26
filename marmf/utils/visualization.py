import logging
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt

from config import REPORTS_DIR

LOGGER = logging.getLogger(__name__)


def plot_tracking_and_fusion(track_history: List[Dict], fused_objects: List[Dict], frame_id: int) -> Path:
    # Visualization supports monitoring support in complex marine environments.
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    for tr in track_history:
        xs = []
        ys = []
        for h in tr.get("history", []):
            bbox = h.get("bbox", [0, 0, 0, 0])
            xs.append((bbox[0] + bbox[2]) / 2)
            ys.append((bbox[1] + bbox[3]) / 2)
        if xs and ys:
            ax.plot(xs, ys, marker="o", linewidth=1.2, label=f"Track {tr['track_id']}")

    for obj in fused_objects:
        ax.scatter(obj.get("fused_x", 0.0), obj.get("fused_y", 0.0), marker="x", s=50, color="red")
        if obj.get("track_id") is not None:
            ax.text(
                obj.get("fused_x", 0.0) + 5,
                obj.get("fused_y", 0.0) + 5,
                f"T{obj['track_id']}",
                fontsize=7,
                color="white",
            )

    ax.set_title("Marine Object Tracking and Fused Positions")
    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")
    ax.grid(True, alpha=0.3)
    if len(track_history) <= 10 and track_history:
        ax.legend(loc="best", fontsize=8)

    out_path = REPORTS_DIR / f"visualization_frame_{frame_id:05d}.png"
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    LOGGER.info("Saved visualization: %s", out_path)
    return out_path
