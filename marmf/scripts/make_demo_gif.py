"""Build an animated GIF from monitor visualization frames for the README."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORTS = PROJECT_ROOT / "reports"
DEFAULT_OUT = PROJECT_ROOT.parent / "docs" / "screenshots" / "monitor_demo.gif"


def collect_frames(reports_dir: Path, max_frames: int) -> list[Path]:
    frames = sorted(reports_dir.glob("visualization_frame_*.png"))
    if not frames:
        raise FileNotFoundError(
            f"No visualization_frame_*.png in {reports_dir}. "
            "Run: python main.py --mode monitor --no-trained --duration 3 --num-objects 4"
        )
    return frames[:max_frames]


def build_gif(frame_paths: list[Path], out_path: Path, duration_ms: int, max_width: int) -> None:
    images: list[Image.Image] = []
    for path in frame_paths:
        img = Image.open(path).convert("RGB")
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.Resampling.LANCZOS)
        images.append(img)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        out_path,
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {out_path} ({len(images)} frames)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create README demo GIF from monitor visualizations")
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-frames", type=int, default=12)
    parser.add_argument("--duration-ms", type=int, default=350)
    parser.add_argument("--max-width", type=int, default=720)
    args = parser.parse_args()

    frames = collect_frames(args.reports_dir, args.max_frames)
    build_gif(frames, args.out, args.duration_ms, args.max_width)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
