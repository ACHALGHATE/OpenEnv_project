def grade_email(log):
    correct = sum(1 for x in log if x["reward"] > 0)
    return min(1.0, correct / 3)


def grade_support(response):
    text = response.lower()
    score = 0
    if "sorry" in text: score += 0.3
    if "refund" in text: score += 0.4
    if "help" in text: score += 0.3
    return score


def grade_schedule(success, steps):
    return 1.0 if success and steps <= 3 else 0.7 if success else 0.0