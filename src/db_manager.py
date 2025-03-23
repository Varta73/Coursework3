import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """Класс, который подключается к базе данных"""

    def __init__(self, db_name):
        self.db_name = db_name

    def connect_to_db(self, query):
        """Метод, который подключается в базе данных"""
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
        )
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        execute_message = """SELECT employer.employer_name, COUNT(vacancy_id) AS vacancy_count
                 FROM employer
                 LEFT JOIN vacancy ON employer.employer_id = vacancy.employer_id
                 GROUP BY employer.employer_name"""
        return self.connect_to_db(execute_message)


    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        execute_message = """SELECT employer.employer_name, vacancy.vacancy_name,
        ((vacancy.salary_from + vacancy.salary_to) / 2), vacancy.vacancy_url
        FROM employer
        LEFT JOIN vacancy ON employer.employer_id = vacancy.employer_id"""
        return self.connect_to_db(execute_message)


    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        execute_message = """SELECT vacancy.vacancy_name, AVG(vacancy.salary_from) 
        FROM vacancy
        GROUP BY vacancy.vacancy_name"""
        return self.connect_to_db(execute_message)


    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        execute_message = """SELECT vacancy.vacancy_name, vacancy.vacancy_url FROM vacancy WHERE ((vacancy.salary_from + vacancy.salary_to) / 2) > 
    (SELECT (AVG((vacancy.salary_from + vacancy.salary_to) / 2)) FROM vacancy)"""
        return self.connect_to_db(execute_message)


    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        execute_message = f"""SELECT vacancy_name, vacancy_url FROM vacancy WHERE vacancy_name ILIKE '%{keyword}%'"""
        return self.connect_to_db(execute_message)
