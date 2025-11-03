# main.py (na raiz)
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

# 1) App e paths
app = FastAPI(title="Kelaryz Desk – API")
BASE_DIR = Path(__file__).resolve().parent

# 2) IMPORTA E INCLUI O ROUTER DE AUTENTICAÇÃO
#    (se não existir, vamos querer que isso quebre mesmo, pra ver o erro)
from api.auth import router as auth_router
app.include_router(auth_router)  # => /auth/register, /auth/login, /auth/me, /auth/logout

# 3) Seus outros routers (exemplos)
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

# 4) Estáticos
#    /static -> pasta "static" (login.html, css, js)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# 5) Raiz mostra o login
@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse(str(BASE_DIR / "static" / "login.html"))

# 6) SUA VIEW não pode ficar montada em "/" (senão mascara a API).
#    Se quiser servir a pasta "view", use /app (ou troque pelo que quiser).
app.mount("/app", StaticFiles(directory=str(BASE_DIR / "view"), html=True), name="view")

# 7) OPCIONAL: /docs para checar rotas
#    Abra http://127.0.0.1:8000/docs e confirme que /auth/register aparece lá.
