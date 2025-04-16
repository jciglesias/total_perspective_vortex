
subjects = [f"S{n:03}" for n in range(1, 110)]

tasks = {
    'open and close fist': ["R03", "R07", "R11"],
    'imagine opening and closing fist': ["R04", "R08", "R12"],
    'open and close fists or feets': ["R05", "R09", "R13"],
    'imagine opening and closing fists or feets': ["R06", "R10", "R14"],
}

def get_file_name(subject, task):
    """
    Get the file name based on the subject and task.
    """
    if subject not in subjects:
        raise ValueError(f"Invalid subject: {subject}")
    if task not in tasks:
        raise ValueError(f"Invalid task: {task}")
    
    files = [f'{subject}{task_}.edf' for task_ in tasks[task]]
    return files