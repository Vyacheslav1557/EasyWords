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
