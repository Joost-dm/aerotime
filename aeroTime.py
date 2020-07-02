import time
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys


def input_data():
    """Примитивный UI"""

    employee_id = input("Введите табельный номер: ")
    exam_type = ""
    while exam_type not in ("lms", "lmseng"):
        exam_type_input = input("Выберете тип экзамена(1 - КПК, 2 - ВЛП) Введите 1 или 2: ")
        if exam_type_input == '1':
            exam_type = "lms"
        elif exam_type_input == '2':
            exam_type = "lmseng"
        else:
            print('Некорректный ввод.')
    return employee_id, exam_type


def get_urls(exam_type):
    """Ссылки на страницы получения сида, логина и дирректорию с темами для накрутки времени."""

    if exam_type == 'lms':
        sid_url = (
                'http://lms.aeroflot.ru/webcmi/lesmodule.php?router=%D0%A0%D0%B5%D0%B7%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1' +
                '%82+%D0%B8%D1%82%D0%BE%D0%B3%D0%BE%D0%B2%D1%8B%D1%85+%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2+%D0%B4%D0%B8' +
                '%D1%81%D1%86%D0%B8%D0%BF%D0%BB%D0%B8%D0%BD+%D0%B2+%D0%90%D0%9E%D0%A1&action=forward#')
        login_url = "http://lms.aeroflot.ru/"
        time_url = (
                "http://lms.aeroflot.ru/lesrouteur.php?menu=%28%D0%9A%D0%9F%D0%9A+%D0%B8%D0%BB%D0%B8+%D0%95%D0%9F+" +
                "%D0%91%D0%9F+1-5+%D1%82%D0%B8%D0%BF%D0%BE%D0%B2+%D0%92%D0%A1%29+&action=forward")
    else:
        sid_url = (
            'http://lmseng.aeroflot.ru/lesmodule.php?router=%D0%94%D0%9E%D0%91+%D0%92%D0%9B%D0%9F+2020&action=forward#')

        login_url = "http://lmseng.aeroflot.ru/"

        time_url = (
            "http://lmseng.aeroflot.ru/lesmodule.php?router=%D0%94%D0%9E%D0%91+%D0%92%D0%9B%D0%9F+2020&action=forward#")

    return sid_url, login_url, time_url


def login(employee_id, login_url):
    """Авторизация в системе."""

    driver = webdriver.Chrome()
    driver.get(login_url)
    driver.implicitly_wait(2)
    driver.find_element_by_id('Username').send_keys(employee_id)
    enter = driver.find_element_by_id('Password')
    enter.send_keys(employee_id)
    driver.implicitly_wait(2)
    enter.send_keys(Keys.ENTER)
    return driver


def get_sid(sid_url, login_url):
    """Получение сида сессии."""

    driver = login(employee_id, login_url)
    driver.get(sid_url)
    tasks = driver.find_elements_by_css_selector('li.au > a')
    tasks[0].click()
    time.sleep(1)
    windows = driver.window_handles
    driver.switch_to.window(windows[1])
    sid = driver.execute_script('return aicc_sid')
    driver.execute_script('close();')
    driver.switch_to.window(windows[0])
    driver.close()
    return sid


def get_exam_list(sid, exam_type):
    """Ссылки на экзамены в зависимости от типа проверки."""

    if exam_type == 'lms':
        # КПК / ежегодка
        exam_list = {
        '1. CRM': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008747&link=data/Q_CRM_2016/exam.html&aicc_sid" +
               "="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '2. Воздушно-правовая подготовка': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008746&link=data/vozd_zak"+
                                           "/Q02/exam.html&aicc_sid" +
               "="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '3. Организация перевозок': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008789&link=data/MVP_DOB_2016"+
                                    "/EXAM/exam.html&aicc" +
               "_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '4. Сервис': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008896&link=data/Service_30_08_18/exam_new2/exa" +
                     "m.html&aicc_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '5. B737': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008750&link=Data/DOB_Construction_2018/Constr_B737/Q" +
                "_B737/exam.html&aicc_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '6. B777': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008751&link=Data/DOB_Construction_2018/Constr_B777/Q" +
                "_B777/exam.html&aicc_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '7. RRj': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008752&link=Data/Construction_BP/Constr_RRJ/Q_RRJ/" +
               "exam.html&aicc_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '8. A320': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008753&link=Data/DOB_Construction_2018/Constr_A320/" +
                "Q_A320/exam.html&aicc_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '9. A330': "http://lms.aeroflot.ru/webcmi/show_res_redirect.php?au=A000008749&link=Data/DOB_Construction_2018/" +
                   "Constr_A330/Q_A330/exam.html&aicc_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        '10. Охрана труда': "http://lms.aeroflot.ru/show_res_redirect.php?au=A000008930&link=data/DOB_KPK_Labour_" +
                            "safety_2018/Q_Labour_" +
              "safety_01/exam/exam.html&aicc_sid="+ sid + "&aicc_url=http://lms.aeroflot.ru/webcmi/cmi.php",
        }

    else:
        # ВЛП 2020
        exam_list = {
            "1. Авиационная безопасность.": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002628&link=data/VLP_DOB_2020/q/ab/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
            "2. Безопасность полета.": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002630&link=data/VLP_DOB_2020/q/bp/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
            "3. Гражданская оборона.": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002631&link=data/VLP_DOB_2020/q/Civil_protect/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
            "4. Медицина": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002633&link=data/VLP_DOB_2020/q/Medicine/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
            "5. Организация работы КЭ.": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002635&link=data/VLP_DOB_2020/q/Work_manage/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
            "6. Охрана труда.": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002637&link=data/VLP_DOB_2020/q/Labour_protection/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
            "7. Сервис на борту.": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002639&link=data/VLP_DOB_2020/q/Service/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
            "8. Руководящие документы.": "http://lmseng.aeroflot.ru/show_res_redirect.php?au=A000002641&link=data/VLP_DOB_2020/q/ruk_doc/exam.html&aicc_sid="+ sid + "&aicc_url=http://lmseng.aeroflot.ru/webcmi/cmi.php",
        }
    return exam_list


def exam_choice(employee_id, sid, exam_type, login_url):
    """Выбор экзаменов для прохождения."""

    exam_list = get_exam_list(sid, exam_type)
    choice_list = []
    print('\n------------------------------- ')
    for key in exam_list:
        choice_list.append(key)
        print(key)
    print('------------------------------- \n')
    print('Выберете экзамены для прохождения: [Пример: "2, 3, 4", что бы выбрать все, введите *]')
    exam_choice = input('Ввод: ')
    try:
        if exam_choice:
            driver = login(employee_id, login_url)
            if exam_choice == "*":
                for key in exam_list:
                    driver.get(exam_list[key])
                    get_exam(driver, started=False)
            else:
                exam_choice = exam_choice.replace(" ", "").split(",")
                for choice in exam_choice:
                    choice_url = exam_list[choice_list[int(choice) - 1]]
                    driver.get(choice_url)
                    get_exam(driver, started=False)
    except ValueError:
        print('Некорректный или пустой ввод.')


def get_time_start(driver, target_time, time_url):
    """Инициация накрутки времени."""

    driver.get(time_url)
    parser(driver, target_time)


def parser(driver, target_time):
    """Парсирование списка тем."""

    driver.implicitly_wait(1)
    links = []
    topics = driver.find_elements_by_class_name('rtr')
    for topic in topics:
        links.append(topic.get_attribute('href'))
    if links:
        for link in links:
            driver.get(link)
            driver.implicitly_wait(1)
            parser(driver, target_time)
    else:
        tasks = driver.find_elements_by_css_selector('li.au > a')
        for task in tasks:
            print('Открытие: ' + task.get_attribute('text') + '...')
            task.click()
            get_time(driver, target_time)


def get_time(driver, target_time):
    """Накрутка времени в тему."""

    try:
        time.sleep(1.5)  # время затрачиваемое на страницу
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        if len(str(target_time)) == 1:
            target_time = '0' + str(target_time)

        # Установка разброса времени в пределах +- 10 минут при установке желаемого времени больше 20 минут
        if int(target_time) >= 20:
            target_time = random.randint(int(target_time) - 10, int(target_time) + 10)
        print('начисленно: ' + str(target_time) + 'мин.')

        # Подмена заменов таймера, отправка данных и закрытие темы
        driver.execute_script('closetimer();')
        driver.execute_script('elapsed_time = 0 + ":" + ' + str(target_time) + ' + ":" + ' + str(random.randint(0, 5)) +
                              str(random.randint(0, 9)))
        driver.execute_script('Putparam();')
        driver.execute_script('ExitAU();')
        driver.execute_script('close();')
        time.sleep(0.5)
        driver.switch_to.window(windows[0])
    except IndexError:
        pass


def get_exam(driver, started):
    """Деактивация режима экзамена и парсинг ответов с последующим прохождением."""

    try:
        if started == False:
            driver.implicitly_wait(2)
            start_button = driver.find_element_by_class_name('StartButton')

            # Деактивация режима экзамена с активацией проверочной кнопки
            driver.execute_script("lesson.isItExam_ = false")

            start_button.click()
            get_exam(driver, started=True)

        else:
            raise ValueError
    except:
        try:
            #  Вызов подсветки правильных ответов
            driver.implicitly_wait(2)
            check_button = driver.find_element_by_class_name('NavButton')
            time.sleep(1)
            check_button.click()

            #  Фиксация правильных ответов
            right_answers = driver.find_elements_by_css_selector('[style="color:green"]')
            answers = set()
            for x in right_answers:
                answers.add(x.get_attribute('for'))

            # Активация заблокированных инпутов
            driver.execute_script("$('input').removeAttr('disabled')")

            # Выбор правильных вариантов, переход к следующему вопросу
            for answer in answers:
                choice = driver.find_element_by_id(answer)
                choice.click()
            next_button = driver.find_element_by_class_name('NavNextButton')
            time.sleep(0.5)
            next_button.click()
            get_exam(driver, started)

        # Действия при окончании вопросов.
        except NoSuchElementException:
            print('Done')


#Подопытный табельный: 21077

if __name__ == '__main__':
    employee_id, exam_type = input_data()
    sid_url, login_url, time_url = get_urls(exam_type)
    print('Получение сида сессии...\n')
    sid = get_sid(sid_url, login_url)
    print('Сид получен: ' + sid + '\n')
    target_time = input('Сколько минут начислить к темам? [0 - 59]: ')
    exam_choice(employee_id, sid, exam_type, login_url)
    driver = login(employee_id, login_url)
    if target_time != '' or '0':
        get_time_start(driver, target_time, time_url)
    time.sleep(2)
    driver.close()




