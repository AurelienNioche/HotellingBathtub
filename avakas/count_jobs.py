import os


def count_jobs():
    if os.path.exists("tasks") and os.listdir("tasks"):
        n_jobs = len(
            [f for f in os.listdir("tasks") if os.path.isfile(os.path.join("tasks", f))])
    else:
        n_jobs = 0

    return n_jobs
