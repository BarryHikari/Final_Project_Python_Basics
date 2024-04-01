from setuptools import setup, find_packages

setup(
    name="Final-Project-Python-Basics",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Final-Project-Python-Basics=Final-Project-Python-Basics.main:main',
        ],
    },
    author="Twoje Imię",
    author_email="twoj.email@example.com",
    description="Personal Assistant",
    keywords="Personal Assistant for contacts, notes, birthdays",
)