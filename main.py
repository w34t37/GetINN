from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time

link = "https://service.nalog.ru/inn.do"    # сервис Узнать ИНН

try:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # получаем путь к директории текущего исполняемого файла
    file_input_path = os.path.join(current_dir, 'list.csv')
    # список в формате csv -- разделитель ;  -- ФИО;Дата рождения;Серия паспорта;Номер паспорта;ID в вашей базе (если необходим)
    file_result_path = os.path.join(current_dir, 'inn.txt')
    # в этот файл сохранится список с найденными ИНН
    file_errors_path = os.path.join(current_dir, 'err.txt')
    # в этот файл сохранится список с ошибками в данных
    file_res = open(file_result_path, "w")
    file_err = open(file_errors_path, "w")
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get(link)
    input3 = browser.find_element_by_id("unichk_0")
    input3.click()
    button = browser.find_element_by_id("btnContinue")
    # Соглашаемся на обработку персональных данных
    button.click()
    with open(file_input_path) as file:
        for item in file:
            time.sleep(0.3)
            error = ''
            resultInn = ''
            read_str = item.split(';')
            print(read_str[0])
            fio = read_str[0].split()
            if len(fio) == 3:
                surname = fio[0]
                name = fio[1]
                patronymic = fio[2]
            elif len(fio) == 4:
                surname = fio[0]
                name = fio[1]
                patronymic = fio[2]+' '+fio[3]
            # Проверка на наличие знаков ( и *   Такие во множестве присутствовали в исходных данных
            if surname.find("*") != -1 or name.find("*") != -1 or patronymic.find("*") != -1 or surname.find(
                    "(") != -1 or name.find("(") != -1 or patronymic.find("(") != -1:
                error = 'fio error * or ()'
                file_err.write(
                    read_str[0] + ';' + read_str[1] + ';' + read_str[2] + ';' + read_str[3] + ';' + read_str[
                        4] + ';' + error + '\n')
            else:
                id = read_str[4]
                birthdate = read_str[1]
                sss = read_str[2]
                nnn = read_str[3]

                if len(str(read_str[3])) == 6 and len(str(read_str[2])) == 4 and str(read_str[2]).isdigit() and str(read_str[3]).isdigit():
                    docnumber =read_str[2] +' '+ read_str[3]
                    docdate = ""
                    input_fam = browser.find_element_by_id("fam")
                    input_fam.clear()
                    for s in surname:
                        input_fam.send_keys(s)
                        time.sleep(0.01)
                    input_nam = browser.find_element_by_id("nam")
                    input_nam.clear()
                    for s in name:
                        input_nam.send_keys(s)
                        time.sleep(0.01)
                    input_otch = browser.find_element_by_id("otch")
                    input_otch.clear()
                    for s in patronymic:
                        input_otch.send_keys(s)
                        time.sleep(0.01)
                    input_birthdate = browser.find_element_by_id("bdate")
                    input_birthdate.clear()
                    for s in birthdate:
                        input_birthdate.send_keys(s)
                    # скрипт пока только для паспортов граждан РФ
                    input_docno = browser.find_element_by_id("docno")
                    input_docno.clear()
                    for s in docnumber:
                        input_docno.send_keys(s)
                    btn_send = browser.find_element_by_id("btn_send")
                    print(surname + ';' + name + ';' + patronymic + ';' + birthdate + ';' + "21" + ';' + docnumber + ';')
                    btn_send.click()
                    time.sleep(2)
                    resultInn = browser.find_element_by_id("resultInn").text
                    if resultInn !='':
                        file_res.write(surname + ';' + name + ';' + patronymic + ';' + birthdate + ';' + "21" + ';' + docnumber + ';' +
                        resultInn + ';' + id + '; \n')
                        print(resultInn)
                else:
                    error = 'passport error'
                    file_err.write(
                        read_str[0] + ';' + read_str[1] + ';' + read_str[2] + ';' + read_str[3] + ';' +
                        read_str[4] + ';' + error + '\n')
except Exception as error:
    print(f'Произошла ошибка, вот её трэйсбэк: {error}')
finally:
    time.sleep(3)
    # закрываем браузер после всех манипуляций
    browser.quit()
