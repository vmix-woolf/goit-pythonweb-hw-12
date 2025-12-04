from slowapi.util import get_remote_address
from app.services.limiter import limiter


def test_limiter_is_configured():
    """
    Перевіряємо, що лімітер створено і використовує _key_func (внутрішнє поле SlowAPI).
    """
    assert limiter is not None
    # SlowAPI зберігає key_func у приватному полі _key_func
    assert callable(limiter._key_func)
    assert limiter._key_func == get_remote_address

