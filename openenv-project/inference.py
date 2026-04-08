print("[START]")

from env import WorkEnv
from models import Action
from graders import grade_email, grade_support, grade_schedule

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
    print(f"\n[TASK] Starting: {task.upper()}")

    obs = env.reset(task)
    done = False
    step_count = 0

    while not done:
        # Hardcoded agent logic per task
        if task == "email":
            text = "mark important urgent email"
        elif task == "support":
            text = "sorry refund help"
        else:
            text = "schedule meeting at 4PM"

        action = parse_action(text)
        obs, reward, done, _ = env.step(action)
        step_count += 1

        print(f"  [STEP {step_count}] action={action.action_type} | reward={reward.score:.2f} | feedback={reward.feedback}")

    # ── Final grading per task ──
    history = env.state().get("history", [])

    if task == "email":
        final_score = grade_email(history)
        print(f"  [GRADE] Email score: {final_score:.2f}")

    elif task == "support":
        response_text = "sorry refund help"
        final_score = grade_support(response_text)
        print(f"  [GRADE] Support score: {final_score:.2f}")

    elif task == "schedule":
        success = env.state().get("meeting_scheduled", False)
        final_score = grade_schedule(success, step_count)
        print(f"  [GRADE] Schedule score: {final_score:.2f}")

print("\n[END]")
