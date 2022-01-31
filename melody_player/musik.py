import winsound
import time

tones: dict[str, int] = {
            'c1': 321, 'd1': 367, 'e1': 412, 'f1': 436, 'g1': 490, 'a1': 550, 'b1': 617, 
            'c2': 654, 'd2': 734, 'e2': 824, 'f2': 873, 'g2': 980, 'a2': 110, 'b2': 1235
        }

durations: dict[str, int] = {  
                'whole': 1000, 
                'half': 500, 
                'quarter': 250, 
                'eight': 125, 
                'sixteenth': 62
            }

melody: dict[dict] = [
                    {'note': ['f1', 'eight']}, 
                    {'note': ['c1', 'quarter']},
                    {'note': ['c1', 'quarter']},
                    {'note': ['c1', 'quarter']},
                    {'pause': 'quarter'}, 
                    {'note': ['c1', 'quarter']},
                    {'note': ['d1', 'quarter']}, 
                    {'note': ['a1', 'quarter']}, 
                    {'note': ['a1', 'quarter']}, 
                ]

def play_note(tone: str, duration: str) -> None:
    winsound.Beep(tones[tone], durations[duration])

def pause(duration: str) -> None:
    time.sleep(durations[duration]/1000)

def main() -> None:
    for sign in melody:                             # ---> {'note': ['f1', 'eight']}
        for key, values in sign.items():            # ---> key = 'note'  values = ['f1', 'eight']
            if key == 'note':
                play_note(values[0], values[1])     # ---> play_note('f1', 'eight')
            elif key == 'pause':                    
                pause(values)                       # ---> pause('quarter')

    # play_note('f1', 'eight')
    # play_note('c1', 'quarter')
    # play_note('c1', 'quarter')
    # play_note('c1', 'quarter')
    # add_pause('quarter')
    # play_note('c1', 'quarter')
    # play_note('d1', 'quarter')
    # play_note('a1', 'quarter')
    # play_note('a1', 'quarter')

if __name__ == '__main__':
    main()