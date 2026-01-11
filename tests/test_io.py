import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from toolbox.core.io import get_input_path

def test_get_input_path_local_exists(tmp_path):
    # Create a dummy local file
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")
    
    with get_input_path(str(test_file)) as path:
        assert path == str(test_file)
        assert os.path.exists(path)

def test_get_input_path_local_not_exists():
    with pytest.raises(FileNotFoundError):
        with get_input_path("non_existent_file.txt") as path:
            pass

@patch("urllib.request.urlretrieve")
@patch("os.remove")
@patch("os.close")
def test_get_input_path_url(mock_close, mock_remove, mock_urlretrieve):
    url = "https://example.com/image.png"
    
    # We need to mock tempfile.mkstemp to control the path
    with patch("tempfile.mkstemp") as mock_mkstemp:
        mock_mkstemp.return_value = (99, "/tmp/fake_temp_file.png")
        
        with get_input_path(url) as path:
            assert path == "/tmp/fake_temp_file.png"
            mock_urlretrieve.assert_called_once_with(url, "/tmp/fake_temp_file.png")
            mock_close.assert_called_once_with(99)
        
        # Verify cleanup
        # We also need to mock os.path.exists for the cleanup logic
        with patch("os.path.exists", return_value=True):
            # The cleanup logic happens in finally, which has already run
            pass

@patch("urllib.request.urlretrieve")
@patch("os.path.exists")
@patch("os.remove")
@patch("os.close")
def test_get_input_path_url_cleanup(mock_close, mock_remove, mock_exists, mock_urlretrieve):
    url = "https://example.com/video.mp4"
    fake_path = "/tmp/fake_video.mp4"
    
    with patch("tempfile.mkstemp") as mock_mkstemp:
        mock_mkstemp.return_value = (99, fake_path)
        mock_exists.return_value = True # For the cleanup check
        
        with get_input_path(url) as path:
            assert path == fake_path
            
        # After the context manager, remove should have been called
        mock_remove.assert_called_once_with(fake_path)
        mock_close.assert_called_once_with(99)

@patch("os.close")
def test_get_input_path_url_with_query_params(mock_close):
    # Test that suffix is correctly extracted even with query parameters
    url = "https://example.com/doc.pdf?version=1&auth=abc"
    
    with patch("tempfile.mkstemp") as mock_mkstemp:
        mock_mkstemp.return_value = (99, "/tmp/fake.pdf")
        with patch("urllib.request.urlretrieve"):
            with get_input_path(url) as path:
                # Check that mkstemp was called with .pdf suffix
                args, kwargs = mock_mkstemp.call_args
                assert kwargs.get("suffix") == ".pdf"
                mock_close.assert_called_once_with(99)
