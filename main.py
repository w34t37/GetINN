from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time

from enum import Enum

class DocumentType(Enum):
    # Паспорт гражданина СССР
    passport_ussr = "01"
    # Свидетельство о рождении
    birth_certificate = "03"
    # Паспорт иностранного гражданина
    passport_foreign = "10"
    # Вид на жительство в России
    residence_permit = "12"
    # Разрешение на временное проживание в России
    residence_permit_temp = "15"
    # Свидетельство о предоставлении временного убежища на территории России
    asylum_certificate_temp = "19"
    # Паспорт гражданина России
    passport_russia = "21"
    # Свидетельство о рождении, выданное уполномоченным органом иностранного государства
    birth_certificate_foreign = "23"
    # Вид на жительство иностранного гражданина
    residence_permit_foreign = "62"

link = "https://service.nalog.ru/inn.do"    # сервис Узнать ИНН

try:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # получаем путь к директории текущего исполняемого файла
    file_input_path = os.path.join(current_dir, 'list.csv')
    # список в формате csv -- разделитель ;  -- ФИО;Дата рождения;Серия паспорта;Номер паспорта;ID в вашей базе (если необходим)
    file_result_path = os.path.join(current_dir, 'inn.txt')
    # в этот файл сохранится список с найденными ИНН
    file_errors_path = os.path.join(current_dir, 'err.txt')
    # в этот файл сохранися список с ошибками в данных
    file_res = open(file_result_path, "w")
    file_err = open(file_errors_path, "w")
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get(link)
    input3 = browser.find_element_by_id("unichk_0")
    input3.click()
    button = browser.find_element_by_id("btnContinue")
    button.click()
    with open(file_input_path) as file:
        for item in file:
            time.sleep(0.3)
            input_pass = browser.find_element_by_id("uni_select_3")
            input_pass.send_keys('33')
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
            if True:
                if surname.find("*") != -1 or name.find("*") != -1 or patronymic.find("*") != -1 or surname.find(
                        "(") != -1 or name.find("(") != -1 or patronymic.find("(") != -1:
                    error = 'fio error 8 or ()'
                    file_err.write(
                        read_str[0] + ';' + read_str[1] + ';' + read_str[2] + ';' + read_str[3] + ';' + read_str[
                            4] + ';' + error + '\n')
                else:
                    id = read_str[4]

                    birthdate = read_str[1]
                    doctype = DocumentType.passport_ussr.value
                    sss = read_str[2]
                    nnn = read_str[3]
                    if len(str(read_str[3])) == 6:
                    #if len(str(read_str[3])) == 6 and len(str(read_str[2])) == 4 and str(
                    #        read_str[2]).isdigit() and str(read_str[3]).isdigit():
                        docnumber =read_str[2] +' '+ read_str[3] #str(read_str[2])[0:2] + ' ' + str(read_str[2])[2:4] + ' ' + str(read_str[3])
                        #print(docnumber)
                        docdate = ""  # row['д   ата'].strftime("%d")+'.'+row['дата'].strftime("%m") + '.'+row['дата'].strftime("%Y")
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
                        input_pass.clear()
                        if str(read_str[2]).isdigit():
                            print(input_pass.text )
                            if input_pass.text != '21 - Паспорт гражданина Российской Федерации':
                                for q in '21 ':
                                    input_pass.send_keys(q)
                        else:
                            if input_pass.text != '01 - Паспорт гражданина СССР':
                                for q in '01 ':
                                    input_pass.send_keys(q)
                        input_docno = browser.find_element_by_id("docno")
                        input_docno.clear()
                        for s in docnumber:
                            input_docno.send_keys(s)
                        btn_send = browser.find_element_by_id("btn_send")
                        print(surname + ';' + name + ';' + patronymic + ';' + birthdate + ';' + doctype + ';' + docnumber + ';')
                        btn_send.click()
                        time.sleep(2)
                        #resultInn = browser.find_element_by_id("resultInn").text
                        #inn_elem = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, "resultInn")))
                        #print(inn_elem.text)
                        resultInn = browser.find_element_by_id("resultInn").text
                        if resultInn !='':
                            file_res.write(surname + ';' + name + ';' + patronymic + ';' + birthdate + ';' + doctype + ';' + docnumber + ';' +
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
    # успеваем скопировать код за 30 секунд
    time.sleep(3)
    # закрываем браузер после всех манипуляций
    #browser.quit()

# не забываем оставить пустую строку в конце файла