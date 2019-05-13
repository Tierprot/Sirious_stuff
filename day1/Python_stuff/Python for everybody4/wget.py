__author__ = 'Admin'

import urllib.request as urllib

def search_for_localization(splitted_text):
    localization = ''
    for line in range(len(splitted_text)):
        if '-!- SUBCELLULAR LOCATION' in splitted_text[line]:
            localization += splitted_text[line][9:]
            line+=1
            if '-!-' in splitted_text[line] \
                    or '-------------------------------------' in splitted_text[line]:
                break
            else:
                while splitted_text[line]:
                    localization += ' ' + splitted_text[line][9:]
                    line += 1
                    if '-!-' in splitted_text[line] \
                            or '-------------------------------------' in splitted_text[line]:
                        break
    return localization


#это идентификатор APP для человека, ишем все взаимодействующие с APP белки через API String
code = "http://string-db.org/api/tsv" \
       "/interactors?identifier=APP&required_score=400&limit=2000&species=9606"

try:
    conn = urllib.urlopen(code)
    data = conn.read().decode("utf-8")
except:
    print("ooops, something went wrong!")
else:
    print("data received")

list_dump = open("list_dump.txt","w")
list_dump.write(data)
list_dump.close()

#делаем список списком
data = data.split('\n')

#выделяем участок значимой информации
data = data[1:len(data)-1]

#открываем файл для последующей записи всяких интересностей
file = open("interactors.txt", "w")

for i in range(len(data)):
    #выпечатывающийся счетчик что бы было не скучно ждать :)
    if i == 0 or i > 1:
        print("{0} out of {1} are ready".format(i, len(data)))
    else:
        print("{0} out of {1} is ready".format(i, len(data)))

    entry = data[i]
    #находим первый подходящий Uniprot ID

    adress = 'http://www.uniprot.org/uniprot/?query=' + entry + '&format=list'
    request = urllib.urlopen(adress)
    result = request.read().decode("utf-8")

    #может статься, что Uniprot ничего не найдет
    if not result:
        file.write("string_id {0}, Uniprot record is missing\n".format(entry))
        print("string_id {0}, Uniprot record is missing\n".format(entry))
        continue

    result = result.split('\n')
    entry = result[0]
    #что бы не грузить сервер, пауза 2 секунды
    #time.sleep(2)

    #открываем по ID запись в Uniprot и вытаскиваем ништяки
    adress = 'http://www.uniprot.org/uniprot/?query=' + entry + '&format=txt'
    request = urllib.urlopen(adress)
    fullaccess = request.read().decode("utf-8")
    fullaccess = fullaccess.split('\n')
    id = fullaccess[0].split()

    #отдельно описание локализации в/вне клетки
    #в каких-то записях оно отсутвует так что перестраховываемся
    localisation = search_for_localization(fullaccess)

    if localisation == '':
        localisation = "SUBCELLULAR LOCATION: no record"

    #пишем результат в файл
    file.write("string_id {0}, Uniprot_id {1},  Name {2}, Status {3}, Lenght {4}, {5}\n".format(
                        data[i],    result[0],    id[1], id[2][:len(id[2])-1], id[3], localisation))
    print("string_id {0}, Uniprot_id {1},  Name {2}, Status {3}, Lenght {4}, {5}\n".format(
                    data[i],    result[0],    id[1], id[2][:len(id[2])-1], id[3], localisation))

print("request completed!\n")
file.close()

