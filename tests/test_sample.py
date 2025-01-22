import os
import flask

def test_example():
    assert True

def test_app_config():
    """Test basic application configuration"""
    try:
        from app import app
        assert app.config['DEBUG'] is not None

        # Normalize both paths before comparison
        expected_static_folder = os.path.join(os.getcwd(), 'static')
        expected_template_folder = os.path.join(os.getcwd(), 'templates')

        assert os.path.normpath(app.static_folder) == os.path.normpath(expected_static_folder)
        assert os.path.normpath(app.template_folder) == os.path.normpath(expected_template_folder)
    except ImportError:
        assert False, "Failed to import app module"

def test_environment():
    """Test Python environment and basic imports"""
    import sys
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 10

def test_dependencies():
    """Test if critical dependencies can be imported"""
    try:
        import flask
        import requests
        import dotenv
        assert True
    except ImportError as e:
        assert False, f"Failed to import dependencies: {str(e)}"
