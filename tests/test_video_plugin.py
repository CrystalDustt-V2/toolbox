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
        mock_ffmpeg.run_with_progress.assert_called()
        args = mock_ffmpeg.run_with_progress.call_args[0][0]
        assert "-i" in args
        assert "test.mp4" in args
        assert "sticker.webp" in args
        assert "libwebp" in args
        # Check for the complex filter string
        filter_arg = args[args.index("-vf") + 1]
        assert "scale=512:512" in filter_arg
        assert "pad=512:512" in filter_arg

@patch("toolbox.core.engine.engine_registry.get")
def test_video_watermark(mock_get_engine, runner):
    mock_ffmpeg = MagicMock()
    mock_get_engine.return_value = mock_ffmpeg
    
    with runner.isolated_filesystem():
        with open("test.mp4", "w") as f:
            f.write("fake video data")
            
        result = runner.invoke(cli, ["video", "watermark", "test.mp4", "--text", "MyBrand", "-o", "watermarked.mp4"])
        
        assert result.exit_code == 0
        assert "Watermark added" in result.output
        mock_ffmpeg.run_with_progress.assert_called()
        args = mock_ffmpeg.run_with_progress.call_args[0][0]
        assert "drawtext" in str(args)

@patch("toolbox.core.engine.engine_registry.get")
def test_video_remove_watermark(mock_get_engine, runner):
    mock_ffmpeg = MagicMock()
    mock_get_engine.return_value = mock_ffmpeg
    
    with runner.isolated_filesystem():
        with open("test.mp4", "w") as f:
            f.write("fake video data")
            
        result = runner.invoke(cli, ["video", "remove-watermark", "test.mp4", "-x", "0", "-y", "0", "-w", "100", "-h", "50"])
        
        assert result.exit_code == 0
        assert "Watermark removed" in result.output
        mock_ffmpeg.run_with_progress.assert_called()
        args = mock_ffmpeg.run_with_progress.call_args[0][0]
        assert "delogo" in str(args)
