# """Authentication service."""

# from datetime import datetime, timedelta, timezone

# from jose import JWTError, jwt
# from passlib.context import CryptContext

# from app.config import settings
# from app.services.mongodb_service import users_collection


# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# def hash_password(password: str) -> str:
#     """Hash a plain-text password."""

#     return pwd_context.hash(password)


# def verify_password(
#     plain_password: str,
#     hashed_password: str
# ) -> bool:
#     """Verify a password against its hash."""

#     return pwd_context.verify(
#         plain_password,
#         hashed_password
#     )


# def create_access_token(
#     user_id: str,
#     email: str
# ) -> str:
#     """Create JWT access token."""

#     expire = datetime.now(timezone.utc) + timedelta(
#         minutes=settings.jwt_access_token_expire_minutes
#     )

#     payload = {
#         "sub": user_id,
#         "email": email,
#         "exp": expire
#     }

#     return jwt.encode(
#         payload,
#         settings.jwt_secret_key,
#         algorithm=settings.jwt_algorithm
#     )


# def decode_access_token(token: str) -> dict:
#     """Decode and validate JWT token."""

#     try:
#         payload = jwt.decode(
#             token,
#             settings.jwt_secret_key,
#             algorithms=[settings.jwt_algorithm]
#         )

#         return payload

#     except JWTError:
#         raise ValueError("Invalid or expired token")


# def create_user(
#     name: str,
#     email: str,
#     password: str
# ) -> dict:

#     normalized_email = email.lower().strip()

#     existing_user = users_collection.find_one(
#         {"email": normalized_email}
#     )

#     if existing_user:
#         raise ValueError("A user with this email already exists")

#     now = datetime.now(timezone.utc)

#     user_document = {
#         "name": name.strip(),
#         "email": normalized_email,
#         "password_hash": hash_password(password),
#         "created_at": now,
#         "updated_at": now
#     }

#     result = users_collection.insert_one(user_document)

#     user_document["user_id"] = str(result.inserted_id)

#     return user_document


# def authenticate_user(
#     email: str,
#     password: str
# ) -> dict | None:

#     normalized_email = email.lower().strip()

#     user = users_collection.find_one(
#         {"email": normalized_email}
#     )

#     if not user:
#         return None

#     if not verify_password(
#         password,
#         user["password_hash"]
#     ):
#         return None

#     user["user_id"] = str(user["_id"])

#     return user

"""Authentication service."""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.services.mongodb_service import users_collection


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ---------------------------------------------------------------------------
# Password handling
# ---------------------------------------------------------------------------

def validate_password(password: str) -> None:
    """
    Validate password before passing it to bcrypt.

    bcrypt supports a maximum input length of 72 bytes.
    We validate UTF-8 byte length rather than character count.
    """

    if not password:
        raise ValueError("Password cannot be empty")

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "Password is too long. Please use a password "
            "of 72 UTF-8 bytes or fewer."
        )


def hash_password(password: str) -> str:
    """Hash a plain-text password."""

    validate_password(password)

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Verify a password against its hash."""

    validate_password(plain_password)

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------

def create_access_token(
    user_id: str,
    email: str
) -> str:
    """Create JWT access token."""

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict:
    """Decode and validate JWT token."""

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        return payload

    except JWTError:
        raise ValueError("Invalid or expired token")


# ---------------------------------------------------------------------------
# User creation
# ---------------------------------------------------------------------------

def create_user(
    name: str,
    email: str,
    password: str
) -> dict:
    """Create a new user."""

    # Validate password before interacting with bcrypt.
    validate_password(password)

    normalized_email = email.lower().strip()

    existing_user = users_collection.find_one(
        {"email": normalized_email}
    )

    if existing_user:
        raise ValueError(
            "A user with this email already exists"
        )

    now = datetime.now(timezone.utc)

    user_document = {
        "name": name.strip(),
        "email": normalized_email,
        "password_hash": hash_password(password),
        "created_at": now,
        "updated_at": now
    }

    result = users_collection.insert_one(
        user_document
    )

    user_document["user_id"] = str(
        result.inserted_id
    )

    return user_document


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def authenticate_user(
    email: str,
    password: str
) -> dict | None:
    """Authenticate a user using email and password."""

    normalized_email = email.lower().strip()

    user = users_collection.find_one(
        {"email": normalized_email}
    )

    if not user:
        return None

    try:
        password_valid = verify_password(
            password,
            user["password_hash"]
        )

    except ValueError:
        return None

    if not password_valid:
        return None

    user["user_id"] = str(
        user["_id"]
    )

    return user
