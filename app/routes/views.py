from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../templates'))

@router.get('/register', response_class=HTMLResponse)
def render_register(request: Request):
    return templates.TemplateResponse('register.html', {"request": request})

@router.get('/login', response_class=HTMLResponse)
def render_login(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})

@router.get('/profile', response_class=HTMLResponse)
def render_profile(request: Request):
    return templates.TemplateResponse('profile.html', {"request": request}) 