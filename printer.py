import time
import sys
import threading
import os

start_b = "\033[1m"
end_b = "\033[0;0m"

touches = {
  0: 'hold',
  1: 'rub',
  2: 'pat',
  3: 'pick',
  4: 'poke',
  5: 'press',
  6: 'scratch',
  7: 'slap',
  8: 'stroke',
  9: 'tap',
  10: 'tickle'
}

rel_emotions = {
  'hold': ['enjoyment', 'suprise'],
  'rub': ['enjoyment'],
  'pat': ['enjoyment'],
  'pick': ['surprise', 'anger'],
  'poke': ['anger', 'surprise'],
  'press': ['anger', 'fear', 'surprise'],
  'scratch': ['enjoyment', 'surprise'],
  'slap': ['anger', 'surprise', 'fear', 'sadness', 'disgust'],
  'stroke': ['enjoyment'],
  'tap': ['surprise'],
  'tickle': ['enjoyment']
}

rel_emotions_w_strength = {
  'hold': ['0.61 enjoyment', '0.58 surprise'],
  'rub': ['0.63 enjoyment'],
  'pat': ['0.40 enjoyment'],
  'pick': ['0.65 surprise', '0.46 anger'],
  'poke': ['0.59 anger', '0.45 surprise'],
  'press': ['0.56 anger', '0.47 fear', '0.43 surprise'],
  'scratch': ['0.67 enjoyment', '0.46 surprise'],
  'slap': ['0.89 anger', '0.63 surprise', '0.60 fear', '0.45 sadness', '0.41 disgust'],
  'stroke': ['0.73 enjoyment'],
  'tap': ['0.61 surprise'],
  'tickle': ['0.54 enjoyment']
}

def print_epi(f):
    if (f == -1): # NEUTRAL
        print(
            '\n  ┌──────────────────┐\n  │                  │\n  │                  │\n┌─│  ┌────┐  ┌────┐  │─┐\n│ │  │ ▄▄ │  │ ▄▄ │  │ │\n│ │  │ ▀▀ │  │ ▀▀ │  │ │\n└─│  └────┘  └────┘  │─┘\n  │                  │\n  │      ::::::      │\n  │                  │\n  └──────────────────┘'
        )
    if (f == 0): # SURPRISE
        print(
            '\n  ┌──────────────────┐\n  │   ───      ───   │\n  │                  │\n┌─│  ┌────┐  ┌────┐  │─┐\n│ │  │ ▄▄ │  │ ▄▄ │  │ │\n│ │  │ ▀▀ │  │ ▀▀ │  │ │\n└─│  └────┘  └────┘  │─┘\n  │                  │\n  │        ::        │\n  │                  │\n  └──────────────────┘'
        )
    if (f == 1): # ANGER
        print(
            '\n  ┌──────────────────┐\n  │                  │\n  │                  │\n┌─│   ─┐__    __┌─   │─┐\n│ │  ┌─▄▄─┐  ┌─▄▄─┐  │ │\n│ │  └─▀▀─┘  └─▀▀─┘  │ │\n└─│                  │─┘\n  │                  │\n  │      ::::::      │\n  │                  │\n  └──────────────────┘'
        )
    if (f == 2): # EXCITEMENT
        print(
            '\n  ┌──────────────────┐\n  │                  │\n  │  /───      ───\  │\n┌─│  ┌────┐  ┌────┐  │─┐\n│ │  │ ▄▄ │  │ ▄▄ │  │ │\n│ │  │ ▀▀ │  │ ▀▀ │  │ │\n└─│  └────┘  └────┘  │─┘\n  │  * ─┌▄▄▄▄▄▄┐─ *  │\n  │      \____/      │\n  │                  │\n  └──────────────────┘'
        )
    if (f == 3): # FEAR
        print(
            '\n  ┌──────────────────┐\n  │   /──      ──\   │\n  │                  │\n┌─│  ┌────┐  ┌────┐  │─┐\n│ │  │ ▄▄ │  │ ▄▄ │  │ │\n│ │  │ ▀▀ │  │ ▀▀ │  │ │\n└─│  └────┘  └────┘  │─┘\n  │     ┌──────┐     │\n  │     │      │     │\n  │     └──────┘     │\n  └──────────────────┘'
        )
    if (f == 4): # SADNESS
        print(
            '\n  ┌──────────────────┐\n  │   /──      ──\   │\n  │                  │\n┌─│  ┌────┐  ┌────┐  │─┐\n│ │  │    │  │    │  │ │\n│ │  │    │  │    │  │ │\n└─│ o└─▀▀─┘  └─▀▀─┘o │─┘\n  │ O              O │\n  │      ┌────┐      │\n  │                  │\n  └──────────────────┘'
        )
    if (f == 5): # DISGUST
        print(
            '\n  ┌──────────────────┐\n  │                  │\n  │                  │\n┌─│   ────┘||└────   │─┐\n│ │  ┌─▄▄─┐  ┌─▄▄─┐  │ │\n│ │  └─▀▀─┘  └─▀▀─┘  │ │\n└─│                  │─┘\n  │      ┌────┐      │\n  │     ┼┘────└┼     │\n  │                  │\n  └──────────────────┘'
        )

def print_loading():
    print('\nStarting Epi...')
    loadbarwidth = 23

    for i in range(1, loadbarwidth + 1):
        time.sleep(0.1) 

        strbarwidth = '[{}{}] - {}\r'.format(
            (i * '█'),
            ((loadbarwidth - i) * ' '),
            (('{:0.2f}'.format(((i) * (100/loadbarwidth))) + '%'))
        )

        print(strbarwidth ,end = '')
    print()

def clear():
    os.system('clear')

def print_response(predictions, probabilities):
    first_touch = touches[predictions[0]]
    first_prob = probabilities[0] * 100 # in percent
    second_touch = touches[predictions[1]]
    second_prob = probabilities[1] * 100 # in percent
    if (rel_emotions.get(first_touch)[0] == 'sadness'):
        print_epi(-1)
    if (rel_emotions.get(first_touch)[0] == 'anger'):
        print_epi(1)
    if (rel_emotions.get(first_touch)[0] == 'enjoyment'):
        print_epi(2)
    if (rel_emotions.get(first_touch)[0] == 'disgust'):
        print_epi(1)
    if (rel_emotions.get(first_touch)[0] == 'surprise'):
        print_epi(0)
    if (rel_emotions.get(first_touch)[0] == 'fear'):
        print_epi(1)
    print(f'\n– I felt a {first_touch}, and therefore feel {rel_emotions.get(first_touch)[0]}.')
    print(f'\n_____________________________________________________________')
    print("\nClassified as " + start_b + first_touch + end_b + " with the probability of " + start_b + '{:0.2f}'.format(first_prob) + "%" + end_b + ".")
    print("Second guess was " + second_touch + " with the probability of " + '{:0.2f}'.format(second_prob) + "%.")
    print(f'\n_____________________________________________________________\n')

    for i in range(11):
        strongest_emotion = rel_emotions_w_strength.get(touches[predictions[i]])[0]
        formatted_emotions = ", ".join(rel_emotions_w_strength.get(touches[predictions[i]])[1:])
        print("\nTouch: " + start_b + touches[predictions[i]] + end_b + "\t" 
        + "Probability: " + start_b + '{:0.2f}'.format(probabilities[i] * 100) + "%" + end_b + "\t" 
        + "Related emotions: " + start_b + strongest_emotion + ", " + end_b + formatted_emotions)

    print(f'\n_____________________________________________________________')

if __name__ == '__main__':
    print_epi(-1)