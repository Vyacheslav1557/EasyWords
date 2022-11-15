import sqlite3
from typing import Union
from random import choice

GET_LIST_OF_WORDS_AND_TRANSLATIONS = """
SELECT *
  FROM words_in_english;
"""
GET_LIST_OF_PARTS_OF_SPEECH = """
SELECT part_of_speech_id,
       part_of_speech_in_russian
  FROM parts_of_speech;
"""
GET_COLLOCATIONS_BY_ID = """
SELECT collocation,
       translation_of_collocation
  FROM collocations
 WHERE word_in_english_id = ?;
"""
GET_PRONUNCIATION_BY_ID = """
SELECT audio_us,
       audio_us_s,
       audio_us_w,
       audio_uk,
       audio_uk_s,
       audio_uk_w
  FROM pronunciation_of_english_words
 WHERE word_in_english_id = ?;
"""
GET_TRANSCRIPTIONS_BY_ID = """
SELECT transcription_us,
       transcription_us_s,
       transcription_us_w,
       transcription_uk,
       transcription_uk_s,
       transcription_uk_w
  FROM transcriptions_of_english_words
 WHERE word_in_english_id = ?;
"""
GET_MEANINGS_BY_ID = """
SELECT meaning
  FROM meanings
 WHERE word_in_english_id = ?;
"""
GET_SENTENCES_BY_ID = """
SELECT example_for_sentence,
       translation_of_example_for_sentence
  FROM examples_of_sentences
 WHERE word_in_english_id = ?;
"""
GET_PHRASAL_VERBS_BY_ID = """
SELECT phrasal_verb,
       translation_of_phrasal_verb
  FROM phrasal_verbs
 WHERE word_in_english_id = ?;
"""
GET_EXAMPLES_FOR_MEANINGS_BY_ID = """
SELECT example_for_meaning,
       translation_of_example_for_meaning
  FROM examples_for_meanings
 WHERE meaning_id IN (
           SELECT meaning_id
             FROM meanings
            WHERE word_in_english_id = ?
       );
"""
GET_MAX_ID = """
SELECT MAX(word_in_english_id) 
  FROM words_in_english;
"""
CHECK_IF_ALREADY_EXISTS = """
SELECT *
  FROM words_in_english
 WHERE word_in_english = ?;
"""
DELETE_FROM_WORDS_IN_ENGLISH_BY_ID = """
DELETE 
  FROM words_in_english
 WHERE word_in_english_id = ?;
"""
DELETE_FROM_TRANSCRIPTIONS_BY_ID = """
DELETE 
  FROM transcriptions_of_english_words
 WHERE word_in_english_id = ?;
"""
DELETE_FROM_PRONUNCIATION_BY_ID = """
DELETE 
  FROM pronunciation_of_english_words
 WHERE word_in_english_id = ?;
"""
DELETE_FROM_PHRASAL_VERBS_BY_ID = """
DELETE 
  FROM phrasal_verbs
 WHERE word_in_english_id = ?;
"""
DELETE_FROM_MEANINGS_BY_ID = """
DELETE 
  FROM meanings 
 WHERE word_in_english_id = ?;
"""
DELETE_FROM_EXAMPLES_FOR_MEANINGS_BY_ID = """
DELETE
  FROM examples_for_meanings
 WHERE meaning_id IN (
           SELECT meaning_id
             FROM meanings
            WHERE word_in_english_id = ?
       );
"""
DELETE_FROM_EXAMPLES_OF_SENTENCES_BY_ID = """
DELETE 
  FROM examples_of_sentences
 WHERE word_in_english_id = ?;
"""
DELETE_FROM_COLLOCATIONS_BY_ID = """
DELETE
  FROM collocations
 WHERE word_in_english_id = ?;
"""
INSERT_INTO_WORDS_IN_ENGLISH = """
INSERT INTO words_in_english VALUES(?, ?, ?);
"""


class DatabaseManagementSystem:
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


if __name__ == "__main__":
    pass
