from pandas.io.formats.format import return_docstring
from sqlalchemy import select, insert
from urllib import request
from fastapi import FastAPI, Request, status, Response, HTTPException, status, Cookie, Depends
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
import uvicorn
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from templates.models import Item
from templates.db import Session, ItemsORM, User, engine, Base
import templates.db
from authx import AuthXConfig, AuthX
from templates.db import session
from templates.models import Item, UserLogin


app = FastAPI()

templates = Jinja2Templates(directory="templates") #в переменной template засунули папку templates

app.mount("/static", StaticFiles(directory="static"), name="static")#нужен чтобы css нутри папки статик работал

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(request=request, name="main.html", context={'title': 'sport'},)


@app.get('/home')
def home(request: Request):
    return templates.TemplateResponse(
        {'request': request},
        name="main.html",
        context={'title': 'sport'},
    )

@app.post("/items", tags=["items"])
def create_item(item: Item):
    with Session() as session:
        item_orm = ItemsORM(creator=item.creator, model=item.model, price=item.price, category=item.category)
        session.add(item_orm)
        session.commit()
        return "W"

@app.get("/items/{id_item}", tags=["items"])
def get_item(id_item: int):
    with Session() as session:
        result = session.execute(select(ItemsORM).where(ItemsORM.id == id_item))
        data = result.scalars().all()
        session.commit()
        print(data[0].id)
    return "WWW.abdullik.com", data



@app.get("/kross")
def crosovka(request: Request):
    return templates.TemplateResponse(request=request, name = "kross.html", context = {"title": 'sneakers'})



@app.get("/login", tags = ['login'])
def login(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "login.html",
        context = {"title": 'Вход'},
        )

@app.post("/login", tags = ['register'])
def voiti(user_qwe: UserLogin, response: Response):
    with Session() as session:
        stmt = session.execute(select(User).where((User.username == user_qwe.username)))
        data = stmt.scalars().first()
        if data and data.password == user_qwe.password:
            token = secretic.create_access_token(uid=str(data.id))
            response.set_cookie(kiriil.JWT_ACCESS_COOKIE_NAME, token)
            return {"access": {"id": data.id, "username": data.username}}
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Неверный логин или пароль")

@app.get("/register", tags=['reg'])
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"title": "Регистрация"},
    )

@app.post("/register", tags = ['reg'])
def rega(userqwe: UserLogin, response: Response, request: Request):
    with Session() as session:
        existing = session.execute(
            select(User).where(User.username == userqwe.username)
        ).scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким логином уже существует",
            )
        new_user = User(
            username=userqwe.username,
            password=userqwe.password,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        token = secretic.create_access_token(uid=str(new_user.id))
        response.set_cookie(kiriil.JWT_ACCESS_COOKIE_NAME, token)
        # return templates.TemplateResponse(request = request, name = 'register.html', context = {'title': "Регистрация"})
        return {"ok": True, "username": userqwe.username}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")


@app.post("/logout", tags=["auth"])
def logout(response: Response):
    response.delete_cookie(kiriil.JWT_ACCESS_COOKIE_NAME)
    return {"logout": True}

def get_current_user(access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Не авторизован")
    try:
        payload = jwt.decode(
            access_token,
            kiriil.JWT_SECRET_KEY,
            algorithms=["HS256"],
        )
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    with Session() as session:
        user = session.get(User, int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return user


@app.get("/api/me", tags=["auth"])
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username}


@app.get("/profile", tags=["profile"])
def profile_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={"title": "Профиль"},
    )
@app.get("/basket", tags=["basket"])
def basket(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="basket.html",
        context={"title": "Корзина"},
    )


# @app.get('/')
# def read_index():
#         #return{'hello': 'Adam'}
#     return temlates.TemplateResponse({"request": request}, "main.html")



kiriil = AuthXConfig() #создал экземпляр класса AuthXConfig(параметры конфигурации чего-либо)
kiriil.JWT_SECRET_KEY = "a_gde_abdullo"# СОЗДал  сектреный ключ
kiriil.JWT_ACCESS_COOKIE_NAME = "access_token"# access - дал доступ(refrash - перезагрузка (старницы например)
kiriil.JWT_TOKEN_LOCATION = ["cookies"]# TOKEN_LOCATION - где мы храним весь экземпляр
secretic = AuthX(config=kiriil)# создал экземпляр класса с конфигурацией() kiriil


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)





#class Terr:
#     aret = 1345
#
# terr = Terr()
#
# terr.aret = 4376  #пример для себя
