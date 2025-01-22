import os
import flask

def test_example():
    assert True

def test_app_config():
    """Test basic application configuration"""
    try:
        from app import app
        assert app.config['DEBUG'] is not None
        
        # Flask'ın template_folder'ı göreceli yol olarak tutuyor
        assert app.template_folder == 'templates'
        
        # static_folder için tam yol kontrolü
        expected_static_folder = os.path.join(os.getcwd(), 'static')
        assert os.path.normpath(os.path.abspath(app.static_folder)) == os.path.normpath(expected_static_folder)
        
        # Template dizininin varlığını kontrol et
        template_path = os.path.join(os.getcwd(), app.template_folder)
        assert os.path.isdir(template_path), f"Template directory not found at {template_path}"
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
