import mne
import matplotlib.pyplot as plt
from mne.io import BaseRaw

subjects = [f"S{n:03}" for n in range(1, 110)]

tasks = {
    'open and close fist': ["R03", "R07", "R11"],
    'imagine opening and closing fist': ["R04", "R08", "R12"],
    'open and close fists or feets': ["R05", "R09", "R13"],
    'imagine opening and closing fists or feets': ["R06", "R10", "R14"],
}

channels = [
    # 'Cp5.',
    # 'Af3.',
    # 'Fc2.',
    # 'Ft8.',
    # 'Po4.',
    'Cp3.',
    # 'F6..',
    # 'Tp8.',
    # 'P3..',
    # 'P2..',
    # 'Po7.',
    # 'T7..',
    # 'C1..',
    # 'Cp1.',
    # 'C2..',
    # 'Cp2.',
    # 'Af7.',
    # 'F4..',
    'C3..',
    'Fc4.',
    # 'Fc1.',
    # 'P6..',
    # 'F1..',
    'Cpz.',
    # 'Fpz.',
    # 'F2..',
    # 'P8..',
    # 'O2..',
    # 'Iz..',
    # 'Af4.',
    # 'P5..',
    # 'Af8.',
    # 'T10.',
    'Cp4.',
    # 'P1..',
    # 'Fc5.',
    # 'Fp1.',
    # 'Tp7.',
    # 'F8..',
    'Fc3.',
    # 'Po8.',
    # 'Oz..',
    # 'Fp2.',
    # 'Poz.',
    # 'O1..',
    # 'Ft7.',
    # 'P4..',
    # 'Afz.',
    # 'Fc6.',
    # 'Fz..',
    # 'Pz..',
    'Fcz.',
    # 'P7..',
    # 'F7..',
    'Cz..',
    # 'Cp6.',
    # 'F5..',
    # 'C5..',
    # 'F3..',
    'C4..',
    # 'T9..',
    # 'Po3.',
    # 'T8..',
    # 'C6..'
    ]

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

def read_raw_data(filename: str):
    """
    Read raw data from a file and return the raw object.
    """
    try:
        raw = mne.io.read_raw_edf(filename, preload=True)
        return raw
    except Exception as e:
        print(f"Error reading raw data: {e}")
        return None

def create_image(raw: BaseRaw, filename: str):
    fig = raw.plot()
    file_address = f"./images/{filename}"
    fig.savefig(file_address, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    return file_address
