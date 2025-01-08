from yargy import Parser, rule, or_
from yargy.predicates import eq, type, is_capitalized, dictionary, caseless, normalized
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from dataclasses import dataclass
from typing import Optional
import pandas as pd
from tqdm import tqdm

Person = fact('Person', ['name', 'birth_date', 'birth_place'])

NAME = rule(
    is_capitalized().repeatable().interpretation(
        Person.name
    )
)

MONTH_NAME = morph_pipeline([
    'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
])

# Формат даты: "14 января 2001 года"
LONG_DATE = rule(
    type('INT'),
    MONTH_NAME,
    type('INT').optional(),
    eq('года').optional()
)

# Формат даты: "14.01.2001"
SHORT_DATE = rule(
    type('INT'),
    eq('.'),
    type('INT'),
    eq('.'),
    type('INT')
)

# Объединенная грамматика для даты
DATE = or_(
    LONG_DATE,
    SHORT_DATE
).optional().interpretation(Person.birth_date)

LOCATION = rule(
    caseless('в').optional(),
    dictionary({
        'городе', 'селе', 'посёлке', 'поселке', 'поселке городского типа', 'деревне'
    }).optional(),
    rule(
        is_capitalized(),
        eq('-').optional()
    ).repeatable().interpretation(Person.birth_place)
).optional()

PERSON = rule(
    NAME,
    normalized('родиться').optional(),
    DATE,
    LOCATION
).interpretation(Person)

@dataclass
class Entry:
    name: Optional[str]
    birth_date: Optional[str]
    birth_place: Optional[str]

def extract_data_from_text(text):
    person_parser = Parser(PERSON)

    entries = []
    for match in person_parser.findall(text):
        entries.append(
            Entry(
                name=match.fact.name,
                birth_date = match.fact.birth_date,
                birth_place = match.fact.birth_place
                )
            )
    
    return entries

def read_news_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n')
        for line in content:
            parts = line.split('\t')
            if len(parts) == 3:
                category, title, article = parts
                yield category, title, article

if __name__ == '__main__':

    filepath = 'data/news.txt'
    all_entries = []

    for category, title, article in tqdm(read_news_file(filepath), desc='Парсинг новостей', total=10000):
        # print(f'Текст: {article}')
        entries = extract_data_from_text(article)
        # print(f'Извлеченные данные: {entries}')
        all_entries.extend(entries)

    data = pd.DataFrame(all_entries)
    data.to_csv('data/output.csv', index=False)