import os
import unittest
from unittest.mock import patch
import sys

# Ensure the root directory is in the path so we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_default_config():
    """Test that default configuration values are correctly set."""
    # We import inside the test to ensure environment variables are controlled
    import config
    
    # Assertions check if the actual value matches the expected value
    assert config.DEFAULT_LANGUAGE == "English"
    assert config.OUTPUT_DIR == "outputs"
    assert "reference_audio" in config.REFERENCE_AUDIO_DIR

def test_env_override():
    """Test that environment variables correctly override defaults."""
    # Mocking the environment variable
    with patch.dict(os.environ, {"MODEL_ID": "custom-model-abc"}):
        # Reloading the module to pick up the new environment variable
        import importlib
        import config
        importlib.reload(config)
        
        assert config.MODEL_ID == "custom-model-abc"

def test_supported_languages():
    """Test that the supported languages list is present and contains expected values."""
    import config
    assert isinstance(config.SUPPORTED_LANGUAGES, list)
    assert "English" in config.SUPPORTED_LANGUAGES
    assert "Chinese" in config.SUPPORTED_LANGUAGES
    assert len(config.SUPPORTED_LANGUAGES) >= 10
