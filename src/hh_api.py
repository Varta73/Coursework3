import requests

companies = {
    "Сбербанк": 3529,
    "Яндекс.Такси": 9439962,
    "МАГНИТ, Розничная сеть": 49357,
    "Озон": 2180,
    "Пятёрочка": 1942330,
    "Ростелеком": 2748,
    "Додо Пицца Россия": 10317521,
    "Газпром нефть": 39305,
    "ЛУКОЙЛ": 907345,
    "Skyeng": 1122462,
}


class HHApi:
    """Класс для получения вакансий с hh.ru"""

    def __init__(self):
        self.__url = "https://api.hh.ru"
        # self._headers = {"User-Agent": "HH-User-Agent"}
        # self._params = {"per_page": 100, "page": 0, "only_with_salary": True}

    def get_employers(self, companies):
        """Получение работодателей"""
        list_employers = []
        for company_name, company_id in companies.items():
            company_url = f"https://api.hh.ru/employers{company_id}"
            company_info = {"company_id": company_id, "company_name": company_name, "company_url": company_url}
            list_employers.append(company_info)
        return list_employers


    def get_vacancies(self, list_employers):
        """Получение вакансий"""
        list_vacancies = []
        for employer in list_employers:
            company_id = employer["company_id"]
            vacancy_url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
            response = requests.get(vacancy_url)
            list_vacancies.extend(response.json()["items"])
        return list_vacancies
