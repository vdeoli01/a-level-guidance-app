from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import users, quizzes, meetings

# Initialise App
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also specify particular origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(quizzes.router)
app.include_router(meetings.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
