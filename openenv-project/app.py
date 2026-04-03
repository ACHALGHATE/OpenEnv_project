from fastapi import FastAPI
from env import WorkEnv
from models import Action

app = FastAPI()

env = WorkEnv()


@app.get("/")
def root():
    return {"status": "running", "message": "OpenEnv is live"}


@app.post("/reset")
def reset(task: str = "email"):
    obs = env.reset(task)
    return obs.dict()
@app.post("/step")
def step(action: dict):
    act = Action(**action)
    obs, reward, done, info = env.step(act)

    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }
@app.get("/state")
def state():
    return env.state()
