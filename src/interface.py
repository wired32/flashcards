from algorithm import Flashcards
import os

def main():
    hira = Flashcards()

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    while True: 
        hira.writecard()

        print(f"{"─" * round(os.get_terminal_size().columns / 2)}  ", end='\n\n')
        print(f"Streak: " + str(hira.streak))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)