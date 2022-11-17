import sqlite3
from typing import Union
from random import choice
from queries import *


class DatabaseManagementSystem:
    """
    This class allows querying the database
    """

    def __init__(self, database_name="dictionary.db3"):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def get_max_id(self) -> int:
        return self.cursor.execute(GET_MAX_ID).fetchone()[0]

    def get_list_of_words_and_translations(self) -> list:
        return self.cursor.execute(GET_LIST_OF_WORDS_AND_TRANSLATIONS).fetchall()

    def get_list_of_parts_of_speech(self) -> list:
        return self.cursor.execute(GET_LIST_OF_PARTS_OF_SPEECH).fetchall()

    def get_min_empty_id(self) -> int:
        ids = set(map(lambda x: x[0], self.get_list_of_words_and_translations()))
        for word_in_english_id in range(1, self.get_max_id() + 2):
            if word_in_english_id not in ids:
                return word_in_english_id

    def get_collocations_by_id(self, word_in_english_id: int) -> list:
        return self.cursor.execute(GET_COLLOCATIONS_BY_ID, (word_in_english_id,)).fetchall()

    def get_pronunciation_by_id(self, word_in_english_id: int) -> list:
        return self.cursor.execute(GET_PRONUNCIATION_BY_ID, (word_in_english_id,)).fetchone()

    def get_transcriptions_by_id(self, word_in_english_id: int) -> list:
        return self.cursor.execute(GET_TRANSCRIPTIONS_BY_ID, (word_in_english_id,)).fetchone()

    def get_meanings_by_id(self, word_in_english_id: int) -> list:
        return list(map(lambda x: x[0], self.cursor.execute(GET_MEANINGS_BY_ID, (word_in_english_id,)).fetchall()))

    def get_sentences_by_id(self, word_in_english_id: int) -> list:
        return self.cursor.execute(GET_SENTENCES_BY_ID, (word_in_english_id,)).fetchall()

    def get_phrasal_verbs_by_id(self, word_in_english_id: int) -> list:
        return self.cursor.execute(GET_PHRASAL_VERBS_BY_ID, (word_in_english_id,)).fetchall()

    def get_examples_for_meanings_by_id(self, word_in_english_id: int) -> list:
        return self.cursor.execute(GET_EXAMPLES_FOR_MEANINGS_BY_ID, (word_in_english_id,)).fetchall()

    def check_if_already_exists(self, word_in_english: str) -> bool:
        return bool(self.cursor.execute(CHECK_IF_ALREADY_EXISTS, (word_in_english,)).fetchone())

    def get_id_by_word(self, word_in_english: str) -> Union[int, None]:
        for word_in_english_id, word, trans in self.get_list_of_words_and_translations():
            if word == word_in_english:
                return word_in_english_id
        return None

    def delete_completely_by_id(self, word_in_english_id: int) -> None:
        self.cursor.execute(DELETE_FROM_WORDS_IN_ENGLISH_BY_ID, (word_in_english_id,))
        self.cursor.execute(DELETE_FROM_TRANSCRIPTIONS_BY_ID, (word_in_english_id,))
        self.cursor.execute(DELETE_FROM_PRONUNCIATION_BY_ID, (word_in_english_id,))
        self.cursor.execute(DELETE_FROM_PHRASAL_VERBS_BY_ID, (word_in_english_id,))
        self.cursor.execute(DELETE_FROM_MEANINGS_BY_ID, (word_in_english_id,))
        self.cursor.execute(DELETE_FROM_EXAMPLES_FOR_MEANINGS_BY_ID, (word_in_english_id,))
        self.cursor.execute(DELETE_FROM_EXAMPLES_OF_SENTENCES_BY_ID, (word_in_english_id,))
        self.cursor.execute(DELETE_FROM_COLLOCATIONS_BY_ID, (word_in_english_id,))
        self.connection.commit()

    def insert_new_word_in_english(self, word_in_english_id: int, word: str, translation: str) -> None:
        self.cursor.execute(INSERT_INTO_WORDS_IN_ENGLISH, (word_in_english_id, word, translation,))
        self.connection.commit()

    def get_random_id(self):
        return choice(self.get_list_of_words_and_translations())[0]
