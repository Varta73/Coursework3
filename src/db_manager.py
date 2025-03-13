import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """Класс, который подключается к базе данных"""

    def __init__(self, db_name):
        self.db_name = db_name
    # def __init__(self, db_name, params):
    #     """инициализация"""
    #     self.db_name = db_name
    #     self.params = params
    #     self.connection = None

    def connect_to_db(self, query):
        """Метод, который подключается в базе данных"""
        conn = psycopg2.connect(
            dbname=self.db_name,
            # user="postgres",
            # password="2006",
            # host="localhost",
            # port="5432",
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
        )
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        execute_message = """SELECT employers.company_name, COUNT(vacancies.employer_id)
        FROM employers JOIN vacancies USING (employer_id) GROUP BY employer_id"""
        return f"Компании и количество вакансий:\n{self.connect_to_db(execute_message)}"

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        execute_message = """SELECT employers.company_name, vacancies.vacancy_name, 
        ((vacancies.salary_from + vacancies.salary_to) / 2), vacancies.url
        FROM vacancies JOIN employers USING(employer_id)"""
        return f"Список всех вакансий:\n{self.connect_to_db(execute_message)[:10]} \n ..."

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        execute_message = """SELECT AVG((vacancies.salary_from + vacancies.salary_to) / 2) FROM vacancies"""
        return f"Средняя зарплата по вакансиям:\n{self.connect_to_db(execute_message)}"

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        execute_message = """SELECT * FROM vacancies WHERE ((vacancies.salary_from + vacancies.salary_to) / 2) > 
    (SELECT (AVG((vacancies.salary_from + vacancies.salary_to) / 2)) FROM vacancies)"""
        return f"Вакансии с зарплатой выше среднего:\n{self.connect_to_db(execute_message)[:10]}"

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        execute_message = f"""SELECT * FROM vacancies WHERE vacancy_name ILIKE '%{keyword}%'"""
        return f"Вакансии по ключевому слову:\n{self.connect_to_db(execute_message)[:10]}"
