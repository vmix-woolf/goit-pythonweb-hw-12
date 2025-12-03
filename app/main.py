from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.services.limiter import limiter
from app.api.auth import router as auth_router
from app.api.contacts import router as contacts_router
from app.api.users import router as users_router


app = FastAPI(title="Contacts API")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth_router)
app.include_router(contacts_router, prefix="/contacts")
app.include_router(users_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Contacts API is running"}
