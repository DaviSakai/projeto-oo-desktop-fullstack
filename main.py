from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# importa todos os routers
from controller.cliente_controller import router as cliente_router
from controller.produto_controller import router as produto_router
from controller.administrador_controller import router as admin_router
from controller.carrinho_controller import router as carrinho_router
from controller.pedido_controller import router as pedido_router  # 👈 ADICIONE ESTA LINHA

app = FastAPI(title="MVC — Model / View / Controller")

# registra todos os routers
app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(admin_router)
app.include_router(carrinho_router)
app.include_router(pedido_router)  # 👈 E ESTA LINHA TAMBÉM

# serve os arquivos estáticos (frontend)
app.mount("/", StaticFiles(directory="view", html=True), name="view")
