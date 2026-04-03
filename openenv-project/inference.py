print("[START]")

from env import WorkEnv
from models import Action

env = WorkEnv()
tasks = ["email", "support", "schedule"]

def parse_action(text):
    text = text.lower()

    if "important" in text or "urgent" in text:
        return Action(action_type="mark_important", target_id=1)

    if "delete" in text or "spam" in text:
        return Action(action_type="delete", target_id=2)

    if "archive" in text:
        return Action(action_type="archive", target_id=3)

    if "schedule" in text:
        return Action(action_type="schedule", content="4PM")

    return Action(action_type="respond", content=text)


for task in tasks:
    print(f"[STEP] TASK_START: {task}")

    obs = env.reset(task)
    done = False

    while not done:

        # 🔥 NO API (hardcoded logic)
        if task == "email":
            text = "mark important urgent email"
        elif task == "support":
            text = "sorry refund help"
        else:
            text = "schedule meeting at 4PM"

        action = parse_action(text)

        obs, reward, done, _ = env.step(action)

        print(f"[STEP] ACTION: {action.action_type}")
        print(f"[STEP] REWARD: {reward.score}")
        print(f"[STEP] FEEDBACK: {reward.feedback}")

print("[END]")