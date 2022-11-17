from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from functools import partial
from string import ascii_lowercase
from DMS import DatabaseManagementSystem
from CustomWidgets import *
from constants import *
import urllib.request
import os
import sys

"https://disk.yandex.ru/d/QQloKLl7SO5xWg"  # Here you can download the database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.img = None
        self.read_and_create_files()
        self.init_objects()
        self.database_management = DatabaseManagementSystem()
        self.init_list_of_words()
        self.init_geometry()
        self.init_connections()
        self.init_default_values()
        self.init_text()

    def read_and_create_files(self):
        """
        Files initialization and data reading
        """
        if not os.path.exists(COLOR_FILE_NAME):
            open(COLOR_FILE_NAME, 'w').close()
        if not os.path.exists(MY_DICTIONARY_FILE_NAME):
            open(MY_DICTIONARY_FILE_NAME, 'w').close()
        if not os.path.isdir("sounds"):
            os.makedirs("sounds/us", exist_ok=True)
            os.makedirs("sounds/uk", exist_ok=True)
        if not os.path.exists("pictures"):
            os.makedirs("pictures", exist_ok=True)
        with open(COLOR_FILE_NAME, "r+", encoding="utf-8") as file:
            try:
                self.current_color_index = int(file.read().strip())
            except ValueError:
                self.current_color_index = 0
        with open(MY_DICTIONARY_FILE_NAME, "r+", encoding="utf-8") as file:
            self.my_dictionary = set(map(int, file.read().split()))

    def init_objects(self):
        self.setLayoutDirection(Qt.LeftToRight)
        self.central_widget = QWidget(self, objectName="central_widget")
        self.widget = QWidget(self.central_widget, objectName="widget")
        self.verticalLayout = QVBoxLayout(self.widget, objectName="verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout(objectName="horizontalLayout")
        self.logo_label = QLabel(self.widget, objectName="logo_label")
        self.horizontalLayout.addWidget(self.logo_label)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.search_line = QLineEdit(self.widget, objectName="search_line")
        self.horizontalLayout.addWidget(self.search_line)
        self.search_button = QPushButton(self.widget, objectName="search_button")
        self.horizontalLayout.addWidget(self.search_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.main_tab_widget = TabWidget(parent=self.widget, objectName="main_tab_widget")
        self.main_tab_widget.setTabPosition(QTabWidget.West)
        self.main_tab = QWidget(objectName="main_tab")
        self.main_tab_widget.addTab(self.main_tab, "")
        self.word_in_english_label = LabelWithId(self.main_tab, objectName="word_in_english_label")
        self.pronunciation_list = QListWidget(self.main_tab, objectName="pronunciation_list")
        self.categories_of_examples_list = QListWidget(self.main_tab, objectName="categories_of_examples_list")
        self.examples_list = QListWidget(self.main_tab, objectName="examples_list")
        self.word_page_picture_label = QLabel(self.main_tab, objectName="word_page_picture_label")
        self.add_to_dictionary_button = QPushButton(self.main_tab, objectName="add_to_dictionary_button")
        self.exercises_tab = QWidget(objectName="exercises_tab")
        self.exercises_tab_widget = TabWidget(self.exercises_tab, objectName="exercises_tab_widget")
        self.exercises_tab_widget.setTabPosition(QTabWidget.West)
        self.list_of_words_tab = QWidget(objectName="list_of_words_tab")
        self.exercises_tab_widget.addTab(self.list_of_words_tab, "")
        self.list_of_words_list_widget = QListWidget(self.list_of_words_tab, objectName="list_of_words_list_widget")
        self.page_number_spin_box = QSpinBox(self.list_of_words_tab, objectName="page_number_spin_box")
        self.page_number_spin_box.setMinimum(1)
        self.cards_tab = QWidget(objectName="cards_tab")
        self.exercises_tab_widget.addTab(self.cards_tab, "")
        self.flip_card_button = PushButtonWithId(self.cards_tab, objectName="flip_card_button")
        self.previous_card_button = QPushButton(self.cards_tab, objectName="previous_card_button")
        self.next_card_button = QPushButton(self.cards_tab, objectName="next_card_button")
        self.spelling_tab = QWidget(objectName="spelling_tab")
        self.exercises_tab_widget.addTab(self.spelling_tab, "")
        self.spelling_label = LabelWithId(self.spelling_tab, objectName="spelling_label")
        self.spelling_label.setAlignment(Qt.AlignHCenter)
        self.check_spelling_button = QPushButton(self.spelling_tab, objectName="check_spelling_button")
        self.spelling_line = QLineEdit(self.spelling_tab, objectName="spelling_line")
        self.spelling_line.setAlignment(Qt.AlignHCenter)
        self.previous_spelling_button = QPushButton(self.spelling_tab, objectName="previous_spelling_button")
        self.next_spelling_button = QPushButton(self.spelling_tab, objectName="next_spelling_button")
        self.main_tab_widget.addTab(self.exercises_tab, "")
        self.redactor = QWidget(objectName="redactor")
        self.main_tab_widget.addTab(self.redactor, "")
        self.word_to_change_line = QLineEdit(self.redactor, objectName="word_to_change_line")
        self.translation_of_word_to_change = QLineEdit(self.redactor, objectName="translation_of_word_to_change")
        self.word_to_change_label = QLabel(self.redactor, objectName="word_to_change_label")
        self.translation_of_word_to_change_label = QLabel(self.redactor,
                                                          objectName="translation_of_word_to_change_label")
        self.word_to_change_picture_label = QLabel(self.redactor, objectName="word_to_change_picture_label")
        self.add_picture_label = QPushButton(self.redactor, objectName="add_picture_label")
        self.word_to_change_save_button = QPushButton(self.redactor, objectName="word_to_change_save_button")
        self.word_to_change_save_picture_button = QPushButton(self.redactor,
                                                              objectName="word_to_change_save_picture_button")
        self.word_to_change_delete_button = QPushButton(self.redactor, objectName="word_to_change_delete_button")
        self.history_tab = QWidget(objectName="history_tab")
        self.main_tab_widget.addTab(self.history_tab, "")
        self.history_list_widget = QListWidget(self.history_tab, objectName="history_list_widget")
        self.my_dictionary_tab = QWidget(objectName="my_dictionary_tab")
        self.main_tab_widget.addTab(self.my_dictionary_tab, "")
        self.my_dictionary_list_widget = QListWidget(self.my_dictionary_tab, objectName="my_dictionary_list_widget")
        self.settings_tab = QWidget(objectName="settings_tab")
        self.choose_first_app_theme_button = QPushButton(self.settings_tab, objectName="choose_first_app_theme_button")
        self.choose_second_app_theme_button = QPushButton(self.settings_tab, objectName="choose_first_app_theme_button")
        self.main_tab_widget.addTab(self.settings_tab, "")
        self.verticalLayout.addWidget(self.main_tab_widget)
        self.setCentralWidget(self.central_widget)
        self.statusbar = QStatusBar(self, objectName="statusbar")
        self.setStatusBar(self.statusbar)
        self.media_player = QMediaPlayer()

    def init_geometry(self):
        self.setFixedSize(800, 600)
        self.widget.setMinimumSize(800, 570)
        self.logo_label.setMinimumSize(240, 60)
        self.search_line.setMinimumSize(0, 40)
        self.search_button.setMinimumSize(0, 40)
        self.word_in_english_label.setGeometry(10, 10, 251, 31)
        self.pronunciation_list.setGeometry(10, 40, 256, 192)
        self.categories_of_examples_list.setGeometry(10, 240, 160, 251)
        self.examples_list.setGeometry(180, 240, 525, 251)
        self.word_page_picture_label.setGeometry(280, 40, 401, 191)
        self.add_to_dictionary_button.setGeometry(560, 5, 120, 30)
        self.exercises_tab_widget.setGeometry(0, 0, 695, 490)
        self.list_of_words_list_widget.setGeometry(0, 40, 570, 441)
        self.page_number_spin_box.setGeometry(250, 0, 70, 30)
        self.flip_card_button.setGeometry(10, 10, 550, 251)
        self.previous_card_button.setGeometry(210, 270, 81, 23)
        self.next_card_button.setGeometry(290, 270, 81, 23)
        self.spelling_label.setGeometry(10, 60, 571, 41)
        self.check_spelling_button.setGeometry(250, 192, 75, 31)
        self.spelling_line.setGeometry(180, 130, 211, 41)
        self.previous_spelling_button.setGeometry(140, 192, 101, 31)
        self.next_spelling_button.setGeometry(330, 192, 101, 31)
        self.word_to_change_line.setGeometry(180, 30, 501, 41)
        self.translation_of_word_to_change.setGeometry(180, 80, 501, 41)
        self.word_to_change_label.setGeometry(50, 35, 121, 31)
        self.translation_of_word_to_change_label.setGeometry(50, 80, 121, 31)
        self.word_to_change_picture_label.setGeometry(50, 190, 600, 300)
        self.add_picture_label.setGeometry(40, 130, 141, 41)
        self.word_to_change_save_button.setGeometry(380, 130, 141, 41)
        self.word_to_change_save_picture_button.setGeometry(200, 130, 141, 41)
        self.word_to_change_delete_button.setGeometry(540, 130, 141, 41)
        self.history_list_widget.setGeometry(0, 0, 695, 490)
        self.my_dictionary_list_widget.setGeometry(0, 0, 695, 490)
        self.choose_first_app_theme_button.setGeometry(50, 50, 100, 40)
        self.choose_second_app_theme_button.setGeometry(160, 50, 100, 40)

    def init_connections(self):
        self.search_button.clicked.connect(self.search_word)
        self.main_tab_widget.tabBarClicked.connect(self.load_list_by_tab_index)
        self.add_to_dictionary_button.clicked.connect(self.add_to_dictionary_by_id)
        self.exercises_tab_widget.tabBarClicked.connect(self.load_words_to_list_of_words)
        self.page_number_spin_box.valueChanged.connect(self.load_words_to_list_of_words)
        self.flip_card_button.clicked.connect(self.flip_over_card)
        self.previous_card_button.clicked.connect(partial(self.change_item_id_and_text, -1, self.flip_card_button, 1))
        self.next_card_button.clicked.connect(partial(self.change_item_id_and_text, 1, self.flip_card_button, 1))
        self.check_spelling_button.clicked.connect(self.check_spelling)
        self.previous_spelling_button.clicked.connect(partial(self.change_item_id_and_text, -1, self.spelling_label, 2))
        self.next_spelling_button.clicked.connect(partial(self.change_item_id_and_text, 1, self.spelling_label, 2))
        self.choose_first_app_theme_button.clicked.connect(partial(self.change_app_theme, 0))
        self.choose_second_app_theme_button.clicked.connect(partial(self.change_app_theme, 1))
        self.list_of_words_list_widget.itemClicked.connect(self.change_my_dictionary)
        self.list_of_words_list_widget.itemDoubleClicked.connect(self.open_word_page)
        self.my_dictionary_list_widget.itemClicked.connect(self.change_my_dictionary)
        self.my_dictionary_list_widget.itemDoubleClicked.connect(self.open_word_page)
        self.categories_of_examples_list.itemDoubleClicked.connect(self.show_item_value)
        self.history_list_widget.itemDoubleClicked.connect(self.open_word_page)
        self.pronunciation_list.itemDoubleClicked.connect(self.play_sound)
        self.add_picture_label.clicked.connect(self.add_picture)
        self.word_to_change_delete_button.clicked.connect(self.delete_from_database)
        self.word_to_change_save_button.clicked.connect(self.insert_into_database)
        self.word_to_change_save_picture_button.clicked.connect(self.save_picture)

    def init_default_values(self):
        self.setWindowIcon(QIcon("AppIcon.png"))
        self.main_tab_widget.setCurrentIndex(0)
        self.exercises_tab_widget.setCurrentIndex(0)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(8)
        self.shadow.setColor(QColor(COLORS[self.current_color_index][2]))
        self.central_widget.setGraphicsEffect(self.shadow)
        self.search_line.setText("welcome")
        self.search_word()
        self.change_app_theme(self.current_color_index)

    def init_text(self):
        self.setWindowTitle("EasyWords")
        self.word_to_change_label.setText("Слово (на английском):")
        self.translation_of_word_to_change_label.setText("Перевод:")
        self.search_button.setText("Найти")
        self.previous_card_button.setText("Предыдущая")
        self.next_card_button.setText("Следующая")
        self.check_spelling_button.setText("Проверить")
        self.previous_spelling_button.setText("Предыдущее")
        self.next_spelling_button.setText("Следующее")
        self.add_to_dictionary_button.setText("Добавить в словарь")
        self.add_picture_label.setText("Добавить картинку")
        self.word_to_change_save_picture_button.setText("Сохранить картинку")
        self.word_to_change_save_button.setText("Сохранить всё")
        self.word_to_change_delete_button.setText("Удалить")
        self.choose_first_app_theme_button.setText("Тема № 1")
        self.choose_second_app_theme_button.setText("Тема № 2")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.main_tab), "Главная")
        self.exercises_tab_widget.setTabText(self.exercises_tab_widget.indexOf(self.list_of_words_tab), "Список слов")
        self.exercises_tab_widget.setTabText(self.exercises_tab_widget.indexOf(self.cards_tab), "Карточки")
        self.exercises_tab_widget.setTabText(self.exercises_tab_widget.indexOf(self.spelling_tab), "Правописание")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.exercises_tab), "Упражнения")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.redactor), "Редактор")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.history_tab), "История")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.my_dictionary_tab), "Мой словарь")
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.settings_tab), "Настройки")

    def init_list_of_words(self):
        """
        Initializing the main word list
        """
        self.list_of_words_in_english = {id_: (word, tr) for id_, word, tr in
                                         sorted(self.database_management.get_list_of_words_and_translations(),
                                                key=lambda x: x[1])}
        length = len(self.list_of_words_in_english)
        self.page_number_spin_box.setMaximum(length // 1000 + bool(length % 1000))

    def load_words_to_list_of_words(self):
        """
        Visualization of the main list of words
        """
        n = self.page_number_spin_box.value()
        self.list_of_words_list_widget.clear()
        for id_, value in list(self.list_of_words_in_english.items())[(n - 1) * 1000:n * 1000]:
            word_in_english, translation_in_russian = value
            if not translation_in_russian:
                translation_in_russian = "no translation"
            item = ListWidgetItemWithId(word_in_english + " — " + translation_in_russian, id_=id_)
            if id_ in self.my_dictionary:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list_of_words_list_widget.addItem(item)

    def change_my_dictionary(self, item: ListWidgetItemWithId):
        if item.checkState() and item.get_id() not in self.my_dictionary:
            self.my_dictionary |= {item.get_id()}
            self.load_list_by_tab_index(1)
            self.load_list_by_tab_index(4)
        elif not item.checkState() and item.get_id() in self.my_dictionary:
            self.my_dictionary -= {item.get_id()}
            self.load_list_by_tab_index(1)
            self.load_list_by_tab_index(4)
        self.save_my_dictionary()

    def add_to_dictionary_by_id(self):
        id_ = self.word_in_english_label.get_id()
        if id_:
            self.my_dictionary |= {id_}
            self.save_my_dictionary()

    def search_word(self):
        word_to_find_id = None
        word_to_find = self.search_line.text().lower().strip()
        for id_, value in self.list_of_words_in_english.items():
            word_in_english, tr = value
            if word_in_english == word_to_find:
                word_to_find_id = id_
                break
        if not word_to_find:
            word_to_find_id = self.database_management.get_random_id()
        self.open_word_page(id_=word_to_find_id)

    def open_word_page(self, item=None, id_=None):
        if item:
            id_ = item.get_id()
        if id_:
            self.load_word_to_main_page(id_)
        else:
            self.load_word_to_main_page(-1, not_found=True)
        self.main_tab_widget.setCurrentIndex(0)

    def load_word_to_main_page(self, id_, not_found=False):
        """
        Word page visualization
        """
        self.pronunciation_list.clear()
        self.categories_of_examples_list.clear()
        self.examples_list.clear()
        self.word_page_picture_label.clear()
        self.add_to_dictionary_button.setHidden(False)
        if not_found or id_ not in self.list_of_words_in_english:
            self.word_in_english_label.setText("Not found")
            self.word_in_english_label.adjustSize()
            self.add_to_dictionary_button.setHidden(True)
            return
        word_in_english, translation_in_russian = self.list_of_words_in_english[id_]
        if not translation_in_russian:
            translation_in_russian = "no translation"
        item = ListWidgetItemWithId(word_in_english + " — " + translation_in_russian, id_=id_)
        self.history_list_widget.addItem(item)
        collocations = self.database_management.get_collocations_by_id(id_)
        pronunciation = self.database_management.get_pronunciation_by_id(id_)
        transcriptions = self.database_management.get_transcriptions_by_id(id_)
        sentences = self.database_management.get_sentences_by_id(id_)
        phrasal_verbs = self.database_management.get_phrasal_verbs_by_id(id_)
        meanings = self.database_management.get_meanings_by_id(id_)
        examples_for_meanings = self.database_management.get_examples_for_meanings_by_id(id_)
        self.word_in_english_label.setText(word_in_english + "\t" * 2 + translation_in_russian)
        self.word_in_english_label.set_id(id_)
        self.word_in_english_label.adjustSize()
        path = f"pictures/{word_in_english.replace(' ', '_')}"
        for file_path in (path + ".png", path + ".jpg"):
            if os.path.exists(file_path):
                self.word_page_picture_label.setPixmap(QPixmap(file_path).scaled(400, 200))
        if transcriptions:
            for i in range(6):
                if transcriptions[i]:
                    item = ListWidgetItemWithLinkAndValue(PRONUNCIATIONS[i] + "  —  " + transcriptions[i],
                                                          link=pronunciation[i])
                    self.pronunciation_list.addItem(item)
        if collocations:
            item = ListWidgetItemWithLinkAndValue("Примеры словосочетаний\n", value=collocations)
            self.categories_of_examples_list.addItem(item)
        if sentences:
            item = ListWidgetItemWithLinkAndValue("Примеры предложений\n", value=sentences)
            self.categories_of_examples_list.addItem(item)
        if phrasal_verbs:
            item = ListWidgetItemWithLinkAndValue("Фразовые глаголы\n", value=phrasal_verbs)
            self.categories_of_examples_list.addItem(item)
        if meanings:
            item = ListWidgetItemWithLinkAndValue("Значения\n", value=meanings)
            self.categories_of_examples_list.addItem(item)
        if examples_for_meanings:
            item = ListWidgetItemWithLinkAndValue("Примеры к значениями\n", value=examples_for_meanings)
            self.categories_of_examples_list.addItem(item)

    def save_my_dictionary(self):
        with open(MY_DICTIONARY_FILE_NAME, "w", encoding="utf-8") as file:
            for id_ in sorted(self.my_dictionary):
                file.write(str(id_) + " ")

    def load_list_by_tab_index(self, tab_index):
        """
        Updating lists when clicking on the corresponding tab
        """
        if tab_index == 0:
            word = self.word_in_english_label.text()
            if word and not self.database_management.check_if_already_exists(word):
                self.search_word()
        elif tab_index == 1:
            self.load_words_to_list_of_words()
            self.change_item_id_and_text(0, self.flip_card_button, 1)
            self.change_item_id_and_text(0, self.spelling_label, 2)
        elif tab_index == 2:
            self.img = None
            self.word_to_change_picture_label.setPixmap(QPixmap(""))
        elif tab_index == 4:
            self.load_words_to_my_dictionary_list()

    def load_words_to_my_dictionary_list(self):
        """
        Visualization of words from my dictionary
        """
        self.my_dictionary_list_widget.clear()
        for id_ in sorted(self.my_dictionary):
            try:
                ex, tr = self.list_of_words_in_english[id_]
                if not tr:
                    tr = "no translation"
                item = ListWidgetItemWithId(ex + " — " + tr, id_)
                item.setCheckState(Qt.Checked)
                self.my_dictionary_list_widget.addItem(item)
            except KeyError:
                self.my_dictionary -= {id_}

    def change_item_id_and_text(self, d, item, j):
        """
        Scrolling words in exercises (cards and spelling)
        """
        if isinstance(item, PushButtonWithId):
            item.setIcon(QIcon(""))
        if isinstance(item, LabelWithId):
            self.spelling_line.clear()
        if self.my_dictionary:
            current_id = item.get_id()
            my_dict = sorted(self.my_dictionary)
            if current_id:
                for i in range(len(my_dict)):
                    if my_dict[i] == current_id:
                        index = (i + d) % len(my_dict)
                        item.set_id(my_dict[index])
                        new_text = self.list_of_words_in_english[my_dict[index]][j - 1]
                        if not new_text:
                            new_text = "No translation"
                        item.setText(new_text)
                        break
            else:
                item.set_id(my_dict[0])
                new_text = self.list_of_words_in_english[my_dict[0]][j - 1]
                if not new_text:
                    new_text = "No translation"
                item.setText(new_text)
        else:
            item.set_id(None)
            item.setText("")

    def flip_over_card(self):
        id_ = self.flip_card_button.get_id()
        if id_:
            side = self.flip_card_button.turn()
            new_text = self.list_of_words_in_english[id_][side]
            if not new_text:
                new_text = "No translation"
            self.flip_card_button.setText(new_text)
            word_in_english = self.list_of_words_in_english[id_][0]
            path = f"pictures/{word_in_english.replace(' ', '_')}"
            if side == 1:
                for file_path in (path + ".png", path + ".jpg"):
                    if os.path.exists(file_path):
                        self.flip_card_button.setIcon(QIcon(file_path))
                        self.flip_card_button.setIconSize(QSize(300, 150))
            else:
                self.flip_card_button.setIcon(QIcon(""))

    def check_spelling(self):
        current_id = self.spelling_label.get_id()
        current_input_text = self.spelling_line.text()
        if current_id:
            if self.list_of_words_in_english[current_id][0] == current_input_text:
                self.change_text_for_a_moment(self.spelling_label, "Правильно")
            else:
                self.change_text_for_a_moment(self.spelling_label, "Неправильно")

    def show_item_value(self, item):
        """
        Sample initialization
        """
        self.examples_list.clear()
        for line in item.get_value():
            if isinstance(line, str):
                item = QListWidgetItem(line)
                self.examples_list.addItem(item)
            elif isinstance(line, tuple):
                item = QListWidgetItem(line[0] + " — " + line[1])
                self.examples_list.addItem(item)

    def add_picture(self):
        try:
            img_path = QFileDialog.getOpenFileName(self, "Выбрать картинку", "", "Image (*.png *.jpg)")[0]
            self.img = Image.open(img_path)
            pixmap = QPixmap(img_path)
            self.word_to_change_picture_label.setPixmap(pixmap.scaled(600, 300))
        except Exception:
            pass

    def change_text_for_a_moment(self, widget, text, time=1000):
        text2 = widget.text()
        widget.setText(text)
        QTimer.singleShot(time, lambda: widget.setText(text2))

    def play_sound(self, item):
        try:
            link = item.get_link()
            if not os.path.exists("sounds" + link):
                urllib.request.urlretrieve(MAIN_AUDIO_URL + link, "sounds" + link)
            url = QUrl("sounds" + link)
            content = QMediaContent(url)
            self.media_player.setMedia(content)
            self.media_player.play()
        except Exception:
            pass

    def change_app_theme(self, index):
        self.current_color_index = index
        colors = COLORS[self.current_color_index]
        self.setStyleSheet(STYLE.replace("COLOR1", colors[0]).replace("COLOR2", colors[1]))
        with open(COLOR_FILE_NAME, "w", encoding="utf-8") as file:
            file.write(str(self.current_color_index))

    def delete_from_database(self):
        word = self.word_to_change_line.text().lower().strip()
        if not word or set(word) - set(ascii_lowercase + "-"):
            self.change_text_for_a_moment(self.word_to_change_line, "Введите слово на английском!")
            return
        id_ = self.database_management.get_id_by_word(word)
        if id_:
            self.database_management.delete_completely_by_id(id_)
            try:
                path = f"pictures/{word.replace(' ', '_')}"
                for file_path in (path + ".png", path + ".jpg"):
                    if os.path.exists(file_path):
                        os.remove(file_path)
            except Exception:
                pass
            self.change_text_for_a_moment(self.word_to_change_line, "Успешно удалено")
        else:
            self.change_text_for_a_moment(self.word_to_change_line, "Такого слова нет")
        self.update_lists()

    def insert_into_database(self):
        word = self.word_to_change_line.text().lower().strip()
        if not word or set(word) - set(ascii_lowercase + "-"):
            self.change_text_for_a_moment(self.word_to_change_line, "Введите слово на английском!")
            return
        translation = self.translation_of_word_to_change.text().lower().strip()
        id_ = self.database_management.get_id_by_word(word)
        if not id_:
            id_ = self.database_management.get_min_empty_id()
            self.database_management.insert_new_word_in_english(id_, word, translation)
            if self.img:
                self.img.save(f"pictures/{word.replace(' ', '_')}.png", "PNG")
            self.change_text_for_a_moment(self.word_to_change_line, "Успешно сохранено")
        else:
            self.change_text_for_a_moment(self.word_to_change_line, "Такое слово уже есть")
        self.update_lists()

    def update_lists(self):
        """
        Lists update. Fires when the main list changes.
        """
        self.init_list_of_words()
        self.load_words_to_list_of_words()
        self.load_words_to_my_dictionary_list()

    def save_picture(self):
        word = self.word_to_change_line.text().lower().strip()
        if not word or set(word) - set(ascii_lowercase + "-"):
            self.change_text_for_a_moment(self.word_to_change_line, "Введите слово на английском!")
            return
        if self.img:
            path = f"pictures/{word.replace(' ', '_')}"
            for file_path in (path + ".png", path + ".jpg"):
                if os.path.exists(file_path):
                    dialog = QMessageBox()
                    res = dialog.question(self, 'Внимание!', "Вы хотите заменить уже существующую картинку?",
                                          dialog.Yes | dialog.No)
                    if res == dialog.Yes:
                        os.remove(file_path)
                        self.img.save(path + ".png", "PNG")
                        self.change_text_for_a_moment(self.word_to_change_line, "Картинка успешно заменена")
                    break
            else:
                self.img.save(path + ".png", "PNG")
                self.change_text_for_a_moment(self.word_to_change_line, "Картинка успешно сохранена")


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
