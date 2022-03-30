import os
import requests
from bs4 import BeautifulSoup

lines = []
size_lines = 0
fname = ""
new_fname = "reamked_words.txt"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def openFile():
    global fname, size_lines, lines
    lines = []
    os_root = '/' if os.name != 'nt' else '\\'
    fn_list = []
    path = '.' + os_root
    for root, dirs, files in os.walk('.'):
        i = 0
        if fname and path + fname != root:
            continue
        if len(dirs) > 0:
            print("\nDirectories list:")
            for dir in dirs:
                i += 1
                print(f"{i}. {dir}")
                fn_list.append(dir)

        print("\nFiles list:")
        for fn in files:
            if fn.find('.txt') != -1:
                i += 1
                print(f"{i}. {fn}")
                fn_list.append(fn)

        i = int(input("\nSelect the filename or directory number: ")) - 1
        fname = fn_list[i]
        if fname.find('.txt') != -1:
            fname = root + os_root + fname if root != '.' else fname
            break
        else:
            if root != '.':
                path = root + os_root
            fn_list = []

    with open(fname, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            lines.append(line.lower())

    size_lines = len(lines)


def findWord():
    global new_fname
    count, size = 1, len(lines)
    for i in lines:
        rows = []
        explain = ""
        en, ua = i.split(' = ')
        url = "https://dictionary.cambridge.org/dictionary/english/" + en.replace(' ', '+')
        url2 = "https://wordsinasentence.com/" + en.replace(' ', '-') + "-in-a-sentence/"
        try:
            print(f"\n{count}/{size}| {i}\nProccess ...\n")
            response = requests.get(url, headers=headers)
            response2 = requests.get(url2, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            soup2 = BeautifulSoup(response2.text, 'lxml')
            examples = soup2.find('div', class_='thecontent clearfix')
            sentences = soup.find_all('div', class_='def ddef_d db')
            i = 0
            flag = False
            if examples:
                flag = True
                print('Check the: ~wordsinasentence.com~:')
                for example in examples:
                    example = example.text.rstrip()
                    if not example:
                        continue
                    if example.find('PREV WORD') != -1:
                        break
                    elif example.find('\n') != -1:
                        example = example[:example.find('\n')]
                    print(f"{i + 1}. {example}")
                    rows.append(example)
                    i += 1
                print()
            if sentences:
                flag = True
                print('Check the: ~dictionary.cambridge.org~:')
                for sentence in sentences:
                    if i == 4:
                        break
                    print(f"{i + 1}. {sentence.text}")
                    rows.append(sentence.text)
                    i += 1
                print()

            if not flag:
                print("Not found. Enter your sentences ...")
                explain = input().lower()
        except ConnectionError:
            print("Connection Error ;(\n")

        if not explain and flag:
            indxes = map(int, input("Enter the number of sentences ('@' - delimeter): ").split())
            for i in indxes:
                explain += rows[i - 1] + ' / '
            explain = explain[:-3]
        with open(new_fname, 'a', encoding='utf-8') as f:
            f.write(f"{en} = {ua} = {explain}\n")
        count += 1


if __name__ == "__main__":
    openFile()
    findWord()
    input('Press Enter to close ...')
