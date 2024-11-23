from algorithm import Flashcards
import os, sys
from rich.panel import Panel
import rich

def main() -> None:
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    clear()

    while True:
        print("Select your difficulty:")
        print("1 - Gojuuon (basic hiragana characters)")
        print("2 - Dakuon (voiced hiragana characters, includes Gojuuon)")
        print("3 - Youon (hiragana characters with a \"y\" sound, includes Gojuuon and Dakuon)")
        selection = input("> ").strip()

        if selection.split()[0] not in ["1", "2", "3"]:
            print("Invalid selection. Please try again.\n")
            continue

        difficulty = int(selection.split()[0])
        break
    
    clear()

    hira = Flashcards()

    while True: 
        max_size = os.get_terminal_size().columns

        rows = [[], []]

        table = {
            hira.cardInfo(id)['kana']: str(hira.userdata['data'][str(id)]['timesPracticed'])
            for id in hira.difficulty[difficulty]
        }

        table = dict(sorted(table.items(), key=lambda item: item[1], reverse=True))

        base = 0
        c_column = 0
        last = 1

        for index, (k, v) in enumerate(table.items()):
            if len(k) == 2 and last == 1:
                rows += [[], [], []]
                base += 3
                c_column = 0

            rows[base] += list(f"{k} ")

            if len(k) < 2:
                rows[base + 1] += list(f"{v}  ")
                c_column += 4
            else:
                rows[base + 1] += list(f"{v}    ")
                c_column += 8

            if index == round(len(table) / 2) or c_column >= max_size:
                rows += [[], [], []]
                base += 3
                c_column = 0

            last = len(k)

        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

        print(f"Streak: " + str(hira.streak))

        print("Your table:")

        renderable = "\n".join(["".join(row) if isinstance(row, list) else str(row) for row in rows])
        rich.print(Panel(renderable))

        print()

        hira.writecard(
            difficulty=difficulty, 
            learning_rate=0.1,
            learning_limit=5, 
            save=True, 
            secondWeight=0.01
        )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)