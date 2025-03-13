from src.utils import create_database, save_data
from src.db_manager import DBManager


def user_interaction() -> None:
    """Основная функция по взаимодействию с пользователем"""
    db_name = "DB_HH"
    create_database(db_name)
    save_data(db_name)

    db_manager = DBManager(db_name)

    print("Здравствуйте!\nЭта программа по поиску и сравнению вакансий на сайте hh.ru \n")
    while True:
        answer = main_menu()
        if answer == 1:
            employer_list = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компании:")
            for i in employer_list:
                print(i)
        elif answer == 2:
            vacancy_list = db_manager.get_all_vacancies()
            print("Список всех вакансий с указанием  компании, вакансии и зарплаты и ссылки на вакансию:")
            for i in vacancy_list:
                print(i)
        elif answer == 3:
            vacancy_list_avg_salary = db_manager.get_avg_salary()
            print("Список всех вакансий co средней зарплатой по вакансиям:")
            for i in vacancy_list_avg_salary:
                print(i)
        elif answer == 4:
            vacancy_list_with_higher = db_manager.get_vacancies_with_higher_salary()
            print("Список всех вакансий с зарплатой выше средней:")
            for i in vacancy_list_with_higher:
                print(i)
        elif answer == 5:
            keyword = input("Введите слово, по которому хотите отфильтровать вакансии: \n").lower()
            vacancy_list_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print("Список всех вакансий в названии которых содержатся переданные в метод слова:")
            for i in vacancy_list_keyword:
                print(i)
        elif answer == 6:
            print("Благодарим за использование программы.\n До свидания.")
            break


def main_menu() -> int:
    """Главное меню"""

    print(
        "1 - Вывести список всех компаний и количество вакансий у каждой компании.\n"
        "2 - Вывести список всех вакансий с указанием  компании, вакансии и зарплаты и ссылки на вакансию.\n"
        "3 - Вывести среднюю зарплату по вакансиям.\n"
        "4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
        "5 - Вывести список всех вакансий, в названии которых содержатся переданные в метод слова.\n"
        "6 - Выход.\n"
    )

    while True:
        answer = input("Выберите действие: ").strip()
        if answer.isdigit():
            answer: int = int(answer)
            if 1 <= answer <= 6:
                break
            else:
                print("Можно ввести только число от 1 до 6!")
        else:
            print("Можно ввести только целое число")
    # print("*" * 50)
    return answer


def valid_input(message: str) -> int | None:
    """Если возможно, переводит str в int, иначе предлагает ввести число."""
    while True:
        count = input(message).strip()
        if count.isdigit():
            return int(count)
        else:
            print("Можно ввести только целое число")


if __name__ == "__main__":
    user_interaction()
