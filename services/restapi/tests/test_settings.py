from api.settings import Settings


def test_settings_loading(monkeypatch):
    """
    Test if settings load correctly from environment variables.
    """
    # Set environment variables
    monkeypatch.setenv('guestready__api__auth__user', 'admin')
    monkeypatch.setenv('guestready__api__auth__password', 'test123')
    monkeypatch.setenv('guestready__api__port', '8001')
    monkeypatch.setenv('guestready__logger__level', 'DEBUG')
    monkeypatch.setenv('guestready__logger__enable_log_color', 'True')
    monkeypatch.setenv('guestready__db__username', 'api_postgres_user')
    monkeypatch.setenv('guestready__db__password', 'api_guestready123')
    monkeypatch.setenv('guestready__db__port', '5432')
    monkeypatch.setenv('guestready__db__database', 'api_db')
    monkeypatch.setenv('guestready__db__host', 'localhost')

    # Load settings
    settings = Settings()  # type:ignore

    # Assertions
    assert settings.api.auth.user == 'admin'
    assert settings.api.auth.password == 'test123'
    assert settings.api.port == 8001
    assert settings.logger.level == 'DEBUG'
    assert settings.logger.enable_log_color is True
    assert settings.db.username == 'api_postgres_user'
    assert settings.db.password.get_secret_value() == 'api_guestready123'
    assert settings.db.port == 5432
    assert settings.db.database == 'api_db'
    assert settings.db.host == 'localhost'
