from typing import Optional

from fastapi import APIRouter, Body, Header, HTTPException
from starlette import status
from starlette.responses import JSONResponse, Response

from database.database import check_exists_user
from service import createResponce, get_pass_score, get_pwned, regex_login, regex_password

router = APIRouter()


@router.get('/api/passwordStrength/{password}')
async def password_strength(password: Optional[str]):
    if password:
        score = get_pass_score(password)
        pwned = await get_pwned(password)
        print(pwned)
        print(score)
        return createResponce(JSONResponse, status.HTTP_200_OK, {'password': password, 'score': score, 'pwned': pwned})


@router.post('/api/validate')
async def post_validate(action: str = Header(...), data: dict = Body(None)):
    match action:
        case 'CheckPassword':
            if regex_password(data['obj']):
                return createResponce(Response, status.HTTP_200_OK)
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)
        case 'CheckLogin':
            login = data['obj']
            if check_exists_user(login):
                if regex_login(login):
                    return createResponce(Response, status.HTTP_200_OK)
                else:
                    return createResponce(JSONResponse, status.HTTP_401_UNAUTHORIZED, {'message': 'Неправильное имя пользователя!'})
            else:
                return createResponce(JSONResponse, status.HTTP_401_UNAUTHORIZED,
                                      {'message': 'Пользователь с таким именем уже существует!'})
