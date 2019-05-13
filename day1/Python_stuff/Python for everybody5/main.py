__author__ = 'Bones'

from mutation_list import MutGen
from single_seq import single_query
from multiprocessing import Pool
import time

def routine(tuple):
    name, seq = tuple
    query = single_query()
    query.paste_query(seq)
    query.open_advanced_options()
    query.check_PDB()
    query.provide_job_title(name[1:])
    query.submit()

    while (1):
        time.sleep(3)
        if query.download_results():
            break
    return name

if __name__ == '__main__':

    # TODO: Должна быть функция которая перехватит ошибку и снова запустит драйвер
    # TODO: нужен класс для работы с gzip у которого будет метод для возвращения имен файлов, нужно для
    # TODO: цикла с вебдрайвером, что бы точно крутился пока все не посчитает

    mut = MutGen('input.txt', positions=[14, 18, 20, 117])
    mut.gen_mut()
    mut.save_fasta()

    main_title = mut.main_name
    main_seq = mut.get_sequnce(main_title)

    a = mut.sequences

    # upload/download routine
    with Pool(processes=5) as p:
        names = p.map(routine, zip(mut.sequences.keys(), mut.sequences.values()))
