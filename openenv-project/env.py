from models import Observation, Action, Reward

class WorkEnv:
    def __init__(self):
        self.max_steps = 20
        self.reset()

    # -------------------------
    # RESET
    # -------------------------
    def reset(self, task="email"):
        self.step_count = 0
        self.current_task = task

        # base state
        self.state_data = {}
        self.state_data["history"] = []

        # -------- EMAIL TASK --------
        if task == "email":
            self.state_data["emails"] = [
                {"id": 1, "text": "URGENT: client meeting", "priority": "high"},
                {"id": 2, "text": "Win iPhone now!!!", "priority": "low"},
                {"id": 3, "text": "Project update needed", "priority": "medium"}
            ]
            self.state_data["processed"] = []

        # -------- SUPPORT TASK --------
        elif task == "support":
            self.state_data["tickets"] = [
                {"id": 1, "issue": "Product broken, want refund immediately"}
            ]

        # -------- SCHEDULING TASK --------
        elif task == "schedule":
            self.state_data["calendar"] = [
                {"time": "9AM"},
                {"time": "10AM"},
                {"time": "2PM"}
            ]
            self.state_data["meeting_scheduled"] = False

        return self._get_obs()

    # -------------------------
    # STEP
    # -------------------------
    def step(self, action: Action):
        self.step_count += 1
        reward = 0.0
        feedback = ""

        # -------- EMAIL LOGIC --------
        if self.current_task == "email":
            email = next((e for e in self.state_data["emails"] if e["id"] == action.target_id), None)

            if email:
                if action.action_type == "mark_important" and email["priority"] == "high":
                    reward += 1.0
                    feedback = "Correct high priority email"
                elif action.action_type == "delete" and email["priority"] == "low":
                    reward += 0.8
                    feedback = "Spam email deleted"
                elif action.action_type == "archive" and email["priority"] == "medium":
                    reward += 0.6
                    feedback = "Medium email archived"
                else:
                    reward -= 0.5
                    feedback = "Wrong email action"
            else:
                reward -= 0.5
                feedback = "Invalid email id"

        # -------- SUPPORT LOGIC --------
        elif self.current_task == "support":
            if action.content:
                text = action.content.lower()
                score = 0.0

                if "sorry" in text:
                    score += 0.3
                if "refund" in text:
                    score += 0.4
                if "help" in text or "assist" in text:
                    score += 0.3

                reward += score
                feedback = f"Support response quality: {score}"
            else:
                reward -= 0.5
                feedback = "No response provided"

        # -------- SCHEDULING LOGIC --------
        elif self.current_task == "schedule":
            if action.content:
                times = [slot["time"] for slot in self.state_data["calendar"]]

                if action.content not in times:
                    reward += 1.0
                    feedback = "Meeting scheduled successfully"
                    self.state_data["meeting_scheduled"] = True
                else:
                    reward -= 0.5
                    feedback = "Time slot already occupied"
            else:
                reward -= 0.5
                feedback = "No time provided"

        # -------- EFFICIENCY PENALTY --------
        reward -= 0.05 * self.step_count

        # clamp reward between 0 and 1
        reward = max(0.0, min(1.0, reward))

        # -------- STORE HISTORY --------
        self.state_data["history"].append({
            "step": self.step_count,
            "action": action.action_type,
            "reward": reward
        })

        # -------- DONE CONDITION --------
        done = (
            self.step_count >= self.max_steps
            or reward >= 0.9
        )

        return self._get_obs(), Reward(score=reward, feedback=feedback), done, {}

    # -------------------------
    # STATE
    # -------------------------
    def state(self):
        return self.state_data

    # -------------------------
    # OBSERVATION
    # -------------------------
    def _get_obs(self):
        return Observation(
            task_type=self.current_task,
            inbox=self.state_data.get("emails", []),
            tickets=self.state_data.get("tickets", []),
            calendar=self.state_data.get("calendar", []),
            history=self.state_data.get("history", [])
        )