from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header(...)):
    if x_token != 'my_secret_token':
        raise HTTPException(status_code=403, detail='Invalid token')


async def get_query_token(token: str):
    if token != 'vector':
        raise HTTPException(status_code=403, detail='Invalid token')
