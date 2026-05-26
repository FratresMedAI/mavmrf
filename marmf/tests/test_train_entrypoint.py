from unittest.mock import patch

import pytest

import train


def test_train_run_accepts_epochs_without_sys_argv():
    with patch("train.train_model") as mock_train, patch("train.validate_dataset"):
        train.run(epochs=3)
        mock_train.assert_called_once()
        _, kwargs = mock_train.call_args
        assert kwargs["epochs"] == 3


def test_train_run_raises_when_dataset_missing():
    with patch("train.validate_dataset", side_effect=FileNotFoundError("Run generate_dataset first")):
        with pytest.raises(FileNotFoundError, match="generate_dataset"):
            train.run(epochs=1)
