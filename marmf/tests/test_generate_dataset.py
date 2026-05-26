from pathlib import Path

from scripts.generate_dataset import generate_dataset


def test_generate_dataset_writes_images_and_labels(tmp_path: Path):
    generate_dataset(
        output_dir=tmp_path,
        train_frames=2,
        val_frames=1,
        num_objects=2,
        clean=True,
    )

    assert (tmp_path / "images" / "train").exists()
    assert (tmp_path / "labels" / "train").exists()
    assert len(list((tmp_path / "images" / "train").glob("*.jpg"))) == 2
    assert len(list((tmp_path / "labels" / "train").glob("*.txt"))) == 2
    assert len(list((tmp_path / "images" / "val").glob("*.jpg"))) == 1
