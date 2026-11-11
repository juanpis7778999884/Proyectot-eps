from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from datetime import timedelta


def test_password_hash_y_verify():
    hashed = get_password_hash("Secreta123!")
    assert verify_password("Secreta123!", hashed) is True
    assert verify_password("Incorrecta", hashed) is False


def test_access_token_expiracion():
    token = create_access_token(subject="1", expires_delta=timedelta(seconds=-1))
    from app.core.security import JWTError
    try:
        decode_token(token)
        assert False, "Debería haber expirado"
    except JWTError:
        pass


def test_access_token_valido():
    token = create_access_token(subject="42")
    payload = decode_token(token)
    assert payload["sub"] == "42"
    assert payload["type"] == "access"
