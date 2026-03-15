from fastapi import Depends, HTTPException
from fastapi import status

username_already_in_use = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Usuário já cadastrado"
)

invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciais inválidas",
    headers={"WWW-Authenticate": "Bearer"}
)

unknown_product_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Produto não cadastrado"
)

product_already_created_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Produto já cadastrado"
)

not_enought_instock = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Estoque insuficiente para esta venda"
)

