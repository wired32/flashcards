import json
import time
import os
import requests
import logging
import random
from pathlib import Path

logging.basicConfig(level=logging.INFO)

class Flashcards:
    def __init__(self):
        self.hiragana = self._load_data('data/hiragana.json', self._fetch_hiragana_data)
        self.userdata = self._load_data('data/userdata.json', self._initialize_userdata)

        self.last = None
        self.streak = 0
        self.difficulty = {         
            1: [
                i for i, h in enumerate(self.hiragana)
                if h['type'] == 'gojuuon' and i != self.last
            ],
            2: [
                i for i, h in enumerate(self.hiragana)
                if h['type'] in ['gojuuon', 'dakuon'] and i != self.last
            ],
            3: [
                i for i in range(len(self.hiragana))
                if i != self.last
            ]
        }
        
    def _load_data(self, file_path, fallback_method):
        """
        Tries to load data from a local file. If it fails, falls back to a provided method to fetch or initialize data.
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data or data is not None:
                        return data
                    fallback_method()
            except json.JSONDecodeError:
                logging.warning(f"File {file_path} is corrupted. Attempting to recover...")
                return fallback_method()
        else:
            return fallback_method()
        
    def download(self, path: Path):
        logging.info("Fetching hiragana data from remote source...")

        response = requests.get(
                'https://raw.githubusercontent.com/wired32/flashcards/refs/heads/main/data/hiragana.json'
            )
        response.encoding = 'utf-8'
        response.raise_for_status()

        hiragana_data = response.json()

        with open(path / 'hiragana.json', 'w', encoding='utf-8') as f:
                json.dump(hiragana_data, f, indent=4)

        logging.info("Successfully fetched and saved hiragana data.")

        return response.json()
    
    def _fetch_hiragana_data(self):
        """
        Fetches hiragana data from a remote source if the local data is missing.
        """
        # ensure data directory exists
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        try:
            hiragana_data = self.download(Path(data_dir))
            
            return hiragana_data
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch hiragana data: {e}")
            raise Exception(f"Failed to fetch hiragana data: {e}")
    
    def _initialize_userdata(self):
        """
        Initializes user data with default values.
        """
        if not self.hiragana:
            raise Exception("Cannot initialize userdata without hiragana data.")

        userdata = {'data': {}}
        for id, hira in enumerate(self.hiragana):
            userdata['data'][str(id)] = {
                "weight": 1,
                "type": hira['type'],
                "lastPractice": time.time(),
                "timesPracticed": 0,
                "mistakes": {"alltime": 0},
                "corrects": {"alltime": 0}
            }
        
        # save user data
        with open('data/userdata.json', 'w', encoding='utf-8') as f:
            json.dump(userdata, f, indent=4)
        
        logging.info("Initialized userdata with default values.")
        return userdata

    def cardInfo(self, id: int):
        """
        Retrieves a hiragana character by its id.

        :param id: Id of the character to retrieve.
        :type id: int
        :return: The requested character.
        :rtype: dict
        """
        return self.hiragana[id]
    
    def _selection(self, identifiers, weights):
        """
        Selects a random identifier based on the given weights.

        :param identifiers: A list of identifiers to select from.
        :type identifiers: list
        :param weights: A list of weights corresponding to the identifiers. The weights should add up to 1.0.
        :type weights: list
        :return: A randomly selected identifier.
        :rtype: str
        """
        return random.choices(identifiers, weights=weights, k=1)
    
    def save(self):
        """
        Saves user data to file.

        :return: None
        :rtype: None
        """
        if not os.path.exists('data'):
            os.makedirs('data')

        with open('data/userdata.json', 'w', encoding='utf-8') as f:
            json.dump(self.userdata, f, indent=4)
    
    def writecard(
            self,
            learning_rate: float = 0.1,
            learning_limit: int = 5,
            save: bool = True,
            difficulty: int = 1,
            secondWeight: float = 0.01
        ) -> tuple[int, bool]:
        """
        Presents a random character based on the specified difficulty level and adjusts its weight
        according to the user's performance, simulating a spaced repetition process.

        :param learning_rate: A float representing the adjustment to the character's weight, indicating
            the rate of learning based on the user's performance.
        :type learning_rate: float
        :param learning_limit: An integer defining the maximum weight of the character.
        :type learning_limit: int
        :param save: A boolean indicating whether the updated user data should be saved to a file 
            after presenting the character and evaluating the response.
        :type save: bool
        :param difficulty: An integer that defines the difficulty level of the character to present:
            1 - Gojuuon (basic hiragana characters)
            2 - Dakuon (voiced hiragana characters, includes Gojuuon)
            3 - Youon (hiragana characters with a "y" sound, includes Gojuuon and Dakuon)
        :type difficulty: int
        :param secondWeight: A float representing the weight given to the response time when 
            calculating character mastery, with a higher value indicating more influence from response time.
        :type secondWeight: float
        :return: A tuple containing the character's ID and a boolean indicating whether the character 
            was answered correctly.
        :rtype: tuple[int, bool]
        """

        if difficulty > 3 or difficulty < 1:
            raise Exception("Difficulty must be between 1 and 3.")

        ids = self.difficulty[difficulty]


        weights = [i['weight'] for n, i in self.userdata['data'].items()
                   if int(n) in ids
        ]

        id = self._selection(ids, weights)[0]
        card = self.cardInfo(id)

        id = str(id)

        start = time.time()

        while True:
            answer = input("Character: " + card['kana'] + "\nRoumaji: ")
            if answer.lower().strip() == card['roumaji']:
                print("Correct! Press Enter to continue...\n")

                self.userdata['data'][id]['timesPracticed'] += 1
                self.userdata['data'][id]['corrects']['alltime'] += 1

                if self.userdata['data'][id]['weight'] > 0.5:
                    self.userdata['data'][id]['weight'] -= learning_rate # subtract weight

                r2 = True # signalize success

                self.streak += 1

                break
            if answer.lower().split()[0] == 'skip':
                input(f"Skipped! The character was {card['roumaji']}! Press Enter to continue...")
                print()

                self.userdata['data'][id]['mistakes']['alltime'] += 1

                if self.userdata['data'][id]['weight'] < learning_limit:
                    self.userdata['data'][id]['weight'] += learning_rate # add weight

                r2 = False # signalize fail

                if self.streak > 0:
                    print(f"Streak reset! {self.streak} consecutive correct answers.\n")
                    self.streak = 0

                break
            
            print("Incorrect, try again!\n")
            self.userdata['data'][id]['mistakes']['alltime'] += 1

            self.userdata['data'][id]['weight'] += learning_rate # add weight

            if self.streak > 0:
                print(f"Streak reset! {self.streak} consecutive correct answers.\n")
                self.streak = 0

        self.userdata['data'][id]['lastPractice'] = time.time() # register last character practice

        duration = time.time() - start

        penal = (secondWeight * duration)
        w = self.userdata['data'][id]['weight']

        if w < learning_limit and (w + penal) < learning_limit:
            self.userdata['data'][id]['weight'] += penal # add weight based on time taken

        if save: 
            self.save()

        self.last = int(id)

        return id, r2 
