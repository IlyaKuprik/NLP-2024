import unittest
from parser import extract_data_from_text, Entry

class TestDataExtraction(unittest.TestCase):
    
    def setUp(self):
        # Для каждого теста мы будем вызывать эту функцию, чтобы создать экземпляр классов и действий.
        pass
    
    def test_full_extraction(self):
        text = "Иван Иванов родился 14 января 1980 года в городе Москва."
        expected = [
            Entry(name="Иван Иванов", birth_date="14 января 1980 года", birth_place="Москва")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)
    
    def test_multiple_entries(self):
        text = ("Мария Петрова родилась 23 февраля 1995 года в селе Озерки.\n"
                "Дмитрий Васильев родился 15.08.1990 в Тольятти.")
        expected = [
            Entry(name="Мария Петрова", birth_date="23 февраля 1995 года", birth_place="Озерки"),
            Entry(name="Дмитрий Васильев", birth_date="15.08.1990", birth_place="Тольятти")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)
    
    def test_date_without_year(self):
        text = "Александр Невский родился 30 ноября в городе Санкт-Петербург."
        expected = [
            Entry(name="Александр Невский", birth_date="30 ноября", birth_place="Санкт-Петербург")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)
    
    def test_without_place(self):
        text = "Наталья Семенова родилась 10 июля 2000 года."
        expected = [
            Entry(name="Наталья Семенова", birth_date="10 июля 2000 года", birth_place=None)
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)
    
    def test_with_short_date(self):
        text = "Сергей Павлов родился 01.01.1985."
        expected = [
            Entry(name="Сергей Павлов", birth_date="01.01.1985", birth_place=None)
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_partial_name(self):
        text = "Анна родилась 5 марта 2003 в деревне Великий Край."
        expected = [
            Entry(name="Анна", birth_date="5 марта 2003", birth_place="Великий Край")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)
    
    def test_without_date(self):
        text = "Борис Борисов родился в селе Родники."
        expected = [
            Entry(name="Борис Борисов", birth_date=None, birth_place="Родники")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_no_data(self):
        text = "этот текст не содержит информации о рождении."
        expected = []
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_non_capitalized_location(self):
        text = "Фёдор Ушаков родился 25 мая 1745 в селе Буркацкая."
        expected = [
            Entry(name="Фёдор Ушаков", birth_date="25 мая 1745", birth_place="Буркацкая")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_location_with_multiple_words(self):
        text = "Лев Толстой родился 9 сентября 1828 года в Ясная Поляна."
        expected = [
            Entry(name="Лев Толстой", birth_date="9 сентября 1828 года", birth_place="Ясная Поляна")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_name_with_middle_name(self):
        text = "Анна Ивановна Антонова родилась 12 марта в селе Лесное."
        expected = [
            Entry(name="Анна Ивановна Антонова", birth_date="12 марта", birth_place="Лесное")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_missing_name(self):
        text = "Родился 21 декабря 1997 года в городе Курган."
        expected = []
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        text = "Ирина Васильева родилась 3 марта 1999, соседи говорят о хорошем урожае."
        expected = [
            Entry(name="Ирина Васильева", birth_date="3 марта 1999", birth_place=None)
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_only_name(self):
        text = "Александр Сергеевич."
        expected = []
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)

    def test_name_with_roman_numerals(self):
        text = "Иван IV Грозный родился 25 августа в Коломне."
        expected = [
            Entry(name="Иван IV Грозный", birth_date="25 августа", birth_place="Коломне")
        ]
        result = extract_data_from_text(text)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()