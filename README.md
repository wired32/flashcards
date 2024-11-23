# Flashcards Learning System

This project is a Python-based flashcard learning system focused on mastering hiragana characters. It uses a spaced repetition algorithm to adjust the frequency and difficulty of each flashcard based on the user's performance, ensuring efficient learning over time.

## Features
- **Hiragana Learning:** The system starts by teaching basic hiragana (Gojuuon) characters and progresses to include more advanced ones (Dakuon and Youon).
- **Spaced Repetition:** Characters are presented based on their difficulty and the user's previous performance. Correct answers decrease the weight of the character, while incorrect answers increase it.
- **Dynamic Learning:** The system adapts by adjusting character weights depending on the user's response accuracy and speed, reinforcing learning over time.
- **Streak Tracking:** It tracks consecutive correct answers, resetting the streak when a mistake is made.

## Requirements
- Python 3.7+
- `requests` library (for fetching hiragana data from a remote source)

You can install the required dependencies with:
```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/wired32/flashcards.git
   cd flashcards
   cd src
   ```

2. Make sure the `data/` directory exists. If it doesn't, the program will automatically create it.

3. On the first run, the program will fetch the hiragana data from a remote source and save it locally to `data/hiragana.json`. 

## Usage

1. Run the program:

   ```bash
   python flashcards.py
   ```

2. The program will present a random hiragana character and prompt you to enter its Romaji (Romanized form). If your answer is correct, the system will adjust the character's weight and show you the next card. If incorrect, the character's weight will increase, and you'll be prompted to try again.

3. To skip a card, type `skip`. The character's Romaji will be shown, and the card will be marked as a mistake.

4. The system keeps track of your streak of consecutive correct answers and adjusts character weights based on response time and accuracy.

## Functions

### `Flashcards.__init__()`
Initializes the system by loading hiragana data and user data from local files or fetching them from a remote source.

### `Flashcards._load_data(file_path, fallback_method)`
Attempts to load data from a local file. If it fails, it calls a fallback method to fetch or initialize the data.

### `Flashcards._fetch_hiragana_data()`
Fetches hiragana data from a remote source and saves it locally.

### `Flashcards._initialize_userdata()`
Initializes user data with default values, including tracking correct answers, mistakes, and character weights.

### `Flashcards.cardInfo(id)`
Returns the hiragana character data for a given ID.

### `Flashcards._selection(identifiers, weights)`
Selects a random identifier based on weighted probabilities.

### `Flashcards.save()`
Saves user data to the `userdata.json` file.

### `Flashcards.writecard(learning_rate=0.1, learning_limit=5, save=True, difficulty=1, secondWeight=0.01)`
Presents a random character based on the selected difficulty and adjusts its weight according to the user's performance. It also calculates the effect of response time on the character's mastery.

### `main()`
Main function that runs the flashcard learning process continuously until interrupted.

## Data Structure
The hiragana data (`hiragana.json`) consists of a list of hiragana characters, each containing:
- `kana`: The hiragana character.
- `roumaji`: The Romanized pronunciation.
- `type`: The type of hiragana (Gojuuon, Dakuon, Youon).

The user data (`userdata.json`) tracks:
- `weight`: The learning weight of the character.
- `type`: The type of hiragana.
- `lastPractice`: The timestamp of the last practice session.
- `timesPracticed`: The total number of times the character has been practiced.
- `mistakes`: A count of total mistakes.
- `corrects`: A count of correct answers.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [mdzhang](https://gist.githubusercontent.com/mdzhang/899a427eb3d0181cd762/raw/0d0f60f08ae58a927b7ac5e0a872acdce88ec441/hiragana.json) for the original hiragana data.

---

Feel free to contribute or create issues for further improvements.