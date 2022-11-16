from main import ensure_langs, find_fuzzy_value, read_lang
import os
import multiprocessing

SOURCE_LANG = 'en'
LANGS = ['ja', 'zh', 'zh_tw']

if __name__ == '__main__':
    ensure_langs()
    source_lang = read_lang(SOURCE_LANG)
    if source_lang is None:
        print('source lang is missing')
        exit(1)

    # read all LANGS
    target_langs = [read_lang(lang) for lang in LANGS]
    if None in target_langs:
        print('missing lang file')
        exit(1)

    # merge languages with their name
    langs = list(zip(target_langs, LANGS))

    # find all xliff files
    xliff_files = [f for f in os.listdir('./') if f.endswith('.xliff')]
    for xliff_file in xliff_files:
        print(f'processing {xliff_file}')
        all_entries = []
        # read xliff file
        with open(xliff_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if '<source>' in line:
                    # get value between <source> and </source>
                    value = line.split('<source>')[1].split('</source>')[0]
                    all_entries.append(value)
        print(f'found {len(all_entries)} entries')
        # find the number of threads this machine can handle
        num_threads = int(multiprocessing.cpu_count() / 2)
        print(f'using {num_threads} threads')
        # split all_entries into num_threads parts
        entries = [all_entries[i::num_threads] for i in range(num_threads)]
        # create a pool of threads
        pool = multiprocessing.Pool(num_threads)
        # find fuzzy values for each thread
        entries = [(source_lang, entry) for entry in entries]
        results = pool.starmap(find_fuzzy_value, entries)
        print(results)
        # flatten the results
        results = [item for sublist in results for item in sublist]
        print(f'found {len(results)} results')
        for result in results:
            print(result)
            for lang, lang_name in langs:
                print(f'{lang_name}: {lang[result.key]}')
            print()
