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
