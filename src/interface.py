import os
import sys
from rich.panel import Panel
from rich import print as rprint
from algorithm import Flashcards

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_difficulty():
    """Prompts the user to select a difficulty level."""
    while True:
        print("Select your difficulty:")
        print("1 - Gojuuon (basic hiragana characters)")
        print("2 - Dakuon (voiced hiragana characters, includes Gojuuon)")
        print("3 - Youon (hiragana characters with a 'y' sound, includes Gojuuon and Dakuon)")
        selection = input("> ").strip()

        if selection in ["1", "2", "3"]:
            return int(selection)
        else:
            print("Invalid selection. Please try again.\n")

def display_flashcards_table(hira, difficulty, last: int = None):
    """Displays the flashcards table with kana and their frequencies."""
    max_size = os.get_terminal_size().columns
    rows = [[], []]

    table = {
        hira.cardInfo(id)['kana']: [str(hira.userdata['data'][str(id)]['timesPracticed']), str(id)]
        for id in hira.difficulty[difficulty]
    }

    table = dict(sorted(table.items(), key=lambda item: item[1][0], reverse=True))

    base, c_column = 0, 0
    for index, (k, v) in enumerate(table.items()):
        identifier = v[1]

        if len(k) == 2 and c_column == 0:
            rows += ([], [], [])
            base += 3
            c_column = 0

        if identifier == last:
            rows[base].append(f"[bold green]{k}[/] ")
        else:
            rows[base].append(f"{k} ")
            
        rows[base + 1].append(f"{v[0]}    " if len(k) >= 2 else f"{v[0]}  ")
        c_column += 8 if len(k) >= 2 else 4

        if index == round(len(table) / 2) or c_column >= max_size:
            rows += ([], [], [])
            base += 3
            c_column = 0

    renderable = "\n".join("".join(row) for row in rows)
    rprint(Panel(renderable))

def main():
    clear_terminal()

    difficulty = get_difficulty()
    clear_terminal()

    hira = Flashcards()
    last = None

    while True:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

        print(f"\033[1mStreak: {hira.streak}\033[0m")
        print("Your table:")
        display_flashcards_table(hira, difficulty, last=last)

        print()
        last, state = hira.writecard(
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
