import pytest
from click.testing import CliRunner
from toolbox.cli import cli
from unittest.mock import patch, MagicMock

@pytest.fixture
def runner():
    return CliRunner()

def test_image_ocr_help(runner):
    result = runner.invoke(cli, ["image", "ocr", "--help"])
    assert result.exit_code == 0
    assert "--preprocess" in result.output
    assert "--scale" in result.output

@patch("toolbox.plugins.image.pytesseract.image_to_string")
@patch("toolbox.plugins.image.Image.open")
@patch("toolbox.core.engine.engine_registry.get")
def test_image_ocr_logic(mock_get_engine, mock_image_open, mock_ocr, runner):
    # Mock Tesseract engine
    mock_engine = MagicMock()
    mock_engine.is_available = True
    mock_engine.path = "/path/to/tesseract"
    mock_get_engine.return_value = mock_engine
    
    # Mock Image
    mock_img_instance = MagicMock()
    mock_image_open.return_value.__enter__.return_value = mock_img_instance
    mock_img_instance.width = 100
    mock_img_instance.height = 100
    
    mock_resized_img = MagicMock()
    mock_img_instance.resize.return_value = mock_resized_img
    
    mock_grayscale_img = MagicMock()
    mock_resized_img.convert.return_value = mock_grayscale_img
    
    # Mock OCR result
    mock_ocr.return_value = "Extracted Text"
    
    with runner.isolated_filesystem():
        with open("test.png", "w") as f:
            f.write("fake image data")
            
        result = runner.invoke(cli, ["image", "ocr", "test.png", "--preprocess", "threshold", "--scale", "2.0"])
        
        assert result.exit_code == 0
        assert "Extracted Text" in result.output
        
        # Verify scaling was called on original
        mock_img_instance.resize.assert_called()
        # Verify convert was called on the resized image
        mock_resized_img.convert.assert_called_with("L")
        # Verify point was called on the grayscale image (for threshold)
        mock_grayscale_img.point.assert_called()

@patch("toolbox.plugins.image.Image.new")
@patch("toolbox.plugins.image.Image.open")
def test_image_to_sticker(mock_image_open, mock_image_new, runner):
    # Mock Input Image
    mock_img_instance = MagicMock()
    mock_image_open.return_value.__enter__.return_value = mock_img_instance
    mock_img_instance.size = (100, 200)
    mock_img_instance.width = 100
    mock_img_instance.height = 200
    mock_img_instance.is_animated = False
    
    # Mock Canvas
    mock_canvas = MagicMock()
    mock_image_new.return_value = mock_canvas
    
    with runner.isolated_filesystem():
        with open("test.png", "w") as f:
            f.write("fake image data")
            
        result = runner.invoke(cli, ["image", "to-sticker", "test.png", "-o", "sticker.webp"])
        
        assert result.exit_code == 0
        assert "Sticker created" in result.output
        # Verify canvas was created with 512x512
        mock_image_new.assert_called_with("RGBA", (512, 512), (0, 0, 0, 0))
        # Verify save was called on the canvas
        mock_canvas.save.assert_called()
        args, kwargs = mock_canvas.save.call_args
        assert kwargs['format'] == "WEBP"
