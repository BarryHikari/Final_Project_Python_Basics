# Final Project Python Basics

## 1. Instalacja pakietu lokalnie
Aby zainstalować pakiet lokalnie (na przykład, aby używać go jak każdego innego zainstalowanego pakietu Pythona), otwórz terminal, przejdź do katalogu zawierającego `setup.py` i uruchom:
```
pip install .
```
To zainstaluje Twój pakiet w bieżącym środowisku Pythona.

## 2. Instalacja w trybie edytowalnym (dla rozwoju)
Jeśli planujesz dalej rozwijać swój pakiet, możesz chcieć zainstalować go w tzw. trybie `edytowalnym`. Pozwoli to na wprowadzanie zmian w kodzie pakietu i ich natychmiastowe odzwierciedlanie bez potrzeby ponownej instalacji. Aby to zrobić, użyj:
```
pip install -e .
```
Powyższa komenda powinna być również uruchomiona w katalogu z plikiem `setup.py`.

## 3. Budowanie dystrybucji
Jeśli chcesz podzielić się swoim pakietem z innymi lub opublikować go na Python Package Index (PyPI), musisz najpierw zbudować dystrybucję. W terminalu, w katalogu z `setup.py`, uruchom:
```
python setup.py sdist bdist_wheel
```
To utworzy dystrybucję źródłową (sdist) i dystrybucję koła (wheel) w katalogu `dist/`. Te pliki można następnie wgrać na PyPI.

## 4. Wgrywanie na PyPI
Aby wgrać pakiet na PyPI, musisz najpierw zainstalować `twine`, jeśli jeszcze tego nie zrobiłeś:
```
pip install twine
```
Następnie, użyj `twine` do przesłania swoich plików dystrybucyjnych na PyPI:
```
twine upload dist/*
```
Będziesz musiał wprowadzić swoją nazwę użytkownika i hasło do PyPI, aby kontynuować.

## Ważne uwagi
- Przed publikacją swojego pakietu na PyPI, upewnij się, że masz unikalną nazwę dla swojego pakietu. Możesz sprawdzić dostępność nazwy, przeszukując PyPI.
- Rozważ dodanie pliku `requirements.txt` do swojego projektu, jeśli Twój pakiet zależy od innych pakietów. Chociaż `install_requires` w `setup.py` obsługuje zależności podczas instalacji pakietu, `requirements.txt` jest przydatny dla użytkowników chcących zainstalować zależności za `pomocą pip install -r requirements.txt`.
- Pamiętaj, aby utrzymać wersjonowanie swojego projektu i aktualizować numer wersji w `setup.py` przy każdej zmianie, którą chcesz opublikować.


## Kod pliku `setup.py`
```
from setuptools import setup, find_packages

setup(
    name="final_project_python_basics",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'myassistant=final_project_python_basics.main:main',
        ],
    },
    author="Twoje Imię",
    author_email="twoj.email@example.com",
    description="A personal assistant application for managing contacts, notes, birthdays, etc.",
    keywords="Personal Assistant, Contacts, Notes, Birthdays",
    license="MIT",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        # Tutaj dodaj zależności, np. 'requests>=2.25.1',
        # Jeśli Twój projekt nie ma zależności zewnętrznych, tę sekcję można pominąć
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```
W powyższym kodzie:
- `name` to nazwa Twojego pakietu.
- `version` to aktualna wersja Twojego pakietu.
- `packages=find_packages()`, automatycznie znajduje pakiety do załączenia. Upewnij się, że Twoje moduły/pakiety są odpowiednio strukturyzowane w katalogach.
- `entry_points` definiuje punkt wejścia do aplikacji, dzięki czemu można ją uruchamiać z linii komend. Zmodyfikuj ścieżkę final_project_python_basics.main:main zgodnie z rzeczywistą lokalizacją funkcji main w Twoim projekcie.
- `author`, `author_email`, `description`, `keywords` i `license` to metadane opisujące Twój projekt.
- `long_description` może zawierać dłuższy opis, który zazwyczaj jest wczytywany z pliku README.
- `install_requires` pozwala zdefiniować zależności, które muszą być zainstalowane wraz z Twoim pakietem. Jeśli Twój projekt zależy od zewnętrznych bibliotek Pythona, wymień je tutaj.
- `python_requires` określa wersje Pythona kompatybilne z Twoim pakietem.
- `classifiers` to lista klasyfikatorów, które pomagają innym znaleźć Twój projekt na PyPI i zrozumieć jego kontekst.

## Użycie

Aplikację można uruchomić z linii poleceń po zainstalowaniu:
```
myassistant
```

## Rozwój

Projekt jest w trakcie rozwoju. Wszelkie sugestie i zgłaszanie błędów są mile widziane.

## Licencja

Projekt jest udostępniany na licencji MIT. Szczegółowe informacje znajdują się w pliku LICENCJA.

## Autor

Grupa 2
