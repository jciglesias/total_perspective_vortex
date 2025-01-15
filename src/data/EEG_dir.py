experimental_runs = {
    'baseline': ['01', '02'], # eyes open and eyes closed
    'task 1': ['03', '07', '11'], # open and close left or right fist
    'task 2': ['04', '08', '12'], # imagine opening and closing left or right fist
    'task 3': ['05', '09', '13'], # open and close both fists or both feet
    'task 4': ['06', '10', '14'] # imagine opening and closing both fists or both feet
}

annotation_codes = {
    'LR': {
        'runs': ['03', '04', '07', '08', '11', '12'],
        'codes': {
            'T0': 'rest',
            'T1': 'left fist',
            'T2': 'right fist',
        },
    },
    'both': {
        'runs': ['05', '06', '09', '10', '13', '14'],
        'codes': {
            'T0': 'rest',
            'T1': 'both fists',
            'T2': 'both feet',
        },
    },
}
