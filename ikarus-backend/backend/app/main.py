from .routers import analytics
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import recommend, analytics

app = FastAPI(title='Ikarus Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5176','http://127.0.0.1:5176',
        'http://localhost:5175','http://127.0.0.1:5175',
        'http://localhost:5173','http://127.0.0.1:5173'
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
def health(): return {'ok': True}

app.include_router(recommend.router)
app.include_router(analytics.router)
