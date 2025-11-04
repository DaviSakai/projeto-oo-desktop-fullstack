
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

# App e paths
app = FastAPI(title="Kelaryz Desk – API")
BASE_DIR = Path(__file__).resolve().parent


from api.auth import router as auth_router
app.include_router(auth_router)  # => /auth/register, /auth/login, /auth/me, /auth/logout

#  Outros routers (exemplos)
from controller.cliente_controller import router as cliente_router
from controller.produto_controller import router as produto_router
from controller.administrador_controller import router as admin_router
from controller.carrinho_controller import router as carrinho_router
from controller.pedido_controller import router as pedido_router

app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(admin_router)
app.include_router(carrinho_router)
app.include_router(pedido_router)

#  Estáticos
#    /static -> pasta "static" (login.html, css, js)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

#  Raiz mostra o login
@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse(str(BASE_DIR / "static" / "login.html"))


app.mount("/app", StaticFiles(directory=str(BASE_DIR / "view"), html=True), name="view")

