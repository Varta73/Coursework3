import os

import dotenv
import psycopg2
from dotenv import load_dotenv
# from psycopg2 import sql

from src.hh_api import HHAPI


load_dotenv()


def create_database(db_name):
    """Создание базы данных и таблиц работодатели и вакансии"""
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
    )

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name} WITH (FORCE)")
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    # conn.close()

    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE employer (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE)"""
        )

        cur.execute(
            """CREATE TABLE vacancy (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url VARCHAR(255),
            employer_id INTEGER REFERENCES employer(id) NOT NULL)"""
        )

    conn.close()



def save_data(db_name):
    """Сохранение данных в БД"""
    conn = psycopg2.connect(
        dbname=db_name,
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),

        # user="postgres",
        # password="2006",
        # host="localhost",
        # port="5432",
    )
    with conn:
        with conn.cursor() as cur:
            hh = HHAPI()
            employers = hh.get_employers()
            for employer in employers:
                employer_id = employer["id"]
                cur.execute(
                    "INSERT INTO employer VALUES (%s, %s, %s, %s)",
                    (employer_id, employer["name"], employer["alternate_url"], employer["open_vacancies"]),
                )
                vacansies = hh.get_vacancies(employer_id)
                for vacancy in vacansies:
                    salary_from = (
                        vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] is not None else 0
                    )
                    salary_to = (
                        vacancy["salary"]["to"] if vacancy["salary"] and vacancy["salary"]["to"] is not None else 0
                    )

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
