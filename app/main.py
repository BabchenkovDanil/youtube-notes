from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from app.admin import UserAdmin, VideoAdmin, NoteAdmin
from app.database import engine
from app.routers import videos, notes
from app.auth import router

app = FastAPI()

app.include_router(router)
app.include_router(videos.router)
app.include_router(notes.router)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

admin = Admin(app, engine, base_url="/admin")

admin.add_view(UserAdmin)
admin.add_view(VideoAdmin)
admin.add_view(NoteAdmin)

@app.get('/')
def root():
    return {'message': 'Hello World'}

print("=== Registered routes ===")
for route in app.routes:
    print(route.path, getattr(route, "methods", None))