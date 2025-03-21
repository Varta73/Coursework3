import os

import psycopg2
from dotenv import load_dotenv

from src.hh_api import HHApi, companies

load_dotenv()


def create_database(db_name):
    """Создание базы данных"""
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name} WITH (FORCE)")
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()


def create_tables(db_name):
    """Создание таблиц employer(работодатели) и vacancy(вакансии)"""

    conn = psycopg2.connect(
        dbname=db_name,
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE employer (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL UNIQUE,
                employer_url TEXT)"""
            )

            cur.execute(
                """CREATE TABLE IF NOT EXISTS vacancy (
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                vacancy_url VARCHAR(255),
                employer_id INTEGER REFERENCES employer(employer_id) NOT NULL)"""
            )

    conn.close()


def save_data(db_name):
    """Сохранение данных в БД"""
    conn = psycopg2.connect(
        dbname=db_name,
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
    )
    with conn:
        with conn.cursor() as cur:
            hh = HHApi()
            employers = hh.get_employers(companies)
            for employer in employers:
                cur.execute(
                    "INSERT INTO employer VALUES (%s, %s, %s)",
                    (employer["company_id"], employer["company_name"], employer["company_url"]),
                )
            vacansies = hh.get_vacancies(employers)
            for vacancy in vacansies:
                employer_id = vacancy["employer"]["id"]
                salary_from = (
                    vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] is not None else 0
                )
                salary_to = vacancy["salary"]["to"] if vacancy["salary"] and vacancy["salary"]["to"] is not None else 0

                cur.execute(
                    "INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        vacancy["id"],
                        vacancy["name"],
                        salary_from,
                        salary_to,
                        vacancy["alternate_url"],
                        employer_id,
                    ),
                )
    conn.close()
