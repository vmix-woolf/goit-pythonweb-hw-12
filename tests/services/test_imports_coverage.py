"""
Тести для покриття імпортів.
"""
def test_config_import():
    """Тест імпорту конфігурації."""
    from app.config import Settings, settings
    assert Settings is not None
    assert settings is not None
    assert isinstance(settings, Settings)


def test_database_import():
    """Тест імпорту модуля бази даних."""
    from app.database import engine, get_session
    assert engine is not None
    assert get_session is not None


def test_main_app_import():
    """Тест імпорту головного застосунку."""
    from app.main import app
    assert app is not None
    assert app.title == "Contacts API"


def test_models_import():
    """Тест імпорту моделей."""
    from app.models.user import User
    from app.models.contact import Contact
    from app.models.base import Base

    assert User is not None
    assert Contact is not None
    assert Base is not None