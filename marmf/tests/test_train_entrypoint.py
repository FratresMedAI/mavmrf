from unittest.mock import patch

import train


def test_train_run_accepts_epochs_without_sys_argv():
    with patch("train.train_model") as mock_train:
        train.run(epochs=3)
        mock_train.assert_called_once()
        _, kwargs = mock_train.call_args
        assert kwargs["epochs"] == 3
