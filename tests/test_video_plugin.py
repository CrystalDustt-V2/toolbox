import pytest
from click.testing import CliRunner
from toolbox.cli import cli
from unittest.mock import patch, MagicMock

@pytest.fixture
def runner():
    return CliRunner()

@patch("toolbox.core.engine.engine_registry.get")
def test_video_to_sticker(mock_get_engine, runner):
    # Mock FFmpeg engine
    mock_ffmpeg = MagicMock()
    mock_get_engine.return_value = mock_ffmpeg
    
    with runner.isolated_filesystem():
        with open("test.mp4", "w") as f:
            f.write("fake video data")
            
        result = runner.invoke(cli, ["video", "to-sticker", "test.mp4", "-o", "sticker.webp"])
        
        assert result.exit_code == 0
        assert "Video converted to sticker" in result.output
        
        # Verify FFmpeg was called with correct arguments
        mock_ffmpeg.run.assert_called()
        args = mock_ffmpeg.run.call_args[0][0]
        assert "-i" in args
        assert "test.mp4" in args
        assert "sticker.webp" in args
        assert "libwebp" in args
        # Check for the complex filter string
        filter_arg = args[args.index("-vf") + 1]
        assert "scale=512:512" in filter_arg
        assert "pad=512:512" in filter_arg
