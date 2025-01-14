experimental_runs = {
    'baseline': ['R01', 'R02'], # eyes open and eyes closed
    'task 1': ['R03', 'R07', 'R11'], # open and close left or right fist
    'task 2': ['R04', 'R08', 'R12'], # imagine opening and closing left or right fist
    'task 3': ['R05', 'R09', 'R13'], # open and close both fists or both feet
    'task 4': ['R06', 'R10', 'R14'] # imagine opening and closing both fists or both feet
}

annotation_codes = {
    'LR': {
        'runs': ['R03', 'R04', 'R07', 'R08', 'R11', 'R12'],
        'codes': {
            'T0': 'rest',
            'T1': 'left fist',
            'T2': 'right fist',
        },
    },
    'both': {
        'runs': ['R05', 'R06', 'R09', 'R10', 'R13', 'R14'],
        'codes': {
            'T0': 'rest',
            'T1': 'both fists',
            'T2': 'both feet',
        },
    },
}