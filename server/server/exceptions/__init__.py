from fastapi import Depends, HTTPException
from fastapi import status

username_already_in_use = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already exists"
)

invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

unknown_product_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Unknown product"
)

product_already_created_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Product already created"
)