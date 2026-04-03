# AI Work Assistant (Top 1% OpenEnv Submission)
correct_actions = 0
total_emails = 1

# TODO: set these values based on actual data before computing score
response = ""  # Define response as a string (update with actual response data)
no_conflict = False  # Placeholder: set to True if no conflict detected
correct_time = False  # Placeholder: set to True if time is correct
score = correct_actions / total_emails
if "refund" in response and "sorry" in response:
    score = 1.0
else:
    score = 0.5 or 0
    if no_conflict and correct_time:
        score = 1.0
    else:
        score = 0.0