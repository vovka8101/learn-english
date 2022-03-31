from xmlrpc.client import ResponseError
import requests
from bs4 import BeautifulSoup
from datetime import datetime

today = datetime.now().strftime('%d-%m-%y')
fname = "./daily_words/new_words" + today + ".txt"
fname_all = "all_words.txt"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def num_row(explain, rows):
    indexes = [int(i) for i in explain[6:].split()]
    explain = ''
    for i in indexes:
        explain += rows[i - 1] + ' / '
    return explain[:-4]


def findWord():
    global fname
    while True:
        rows = []
        word = input("Enter a word ('--q' for exit): ").lower()
        if word == '--q':
            break
        url = "https://dictionary.cambridge.org/dictionary/english/" + word.replace(' ', '+')
        url2 = "https://wordsinasentence.com/" + word.replace(' ', '-') + "-in-a-sentence/"
        try:
            print("\nProccess ...\n")
            response = requests.get(url, headers=headers)
            response2 = requests.get(url2, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            soup2 = BeautifulSoup(response2.text, 'lxml')
            examples = soup2.find('div', class_='thecontent clearfix')
            sentences = soup.find_all('div', class_='def ddef_d db')
            i = 1
            if examples:
                print('wordsinasentence.com:')
                for example in examples:
                    example = example.text.rstrip()
                    if not example:
                        continue
                    if example.find('PREV WORD') != -1:
                        break
                    elif example.find('\n') != -1:
                        example = example[:example.find('\n')]
                    rows.append(example)
                    print(f'{i}. {example}')
                    i += 1
                print()
            if sentences:
                print('dictionary.cambridge.org:')
                j = 1
                for sentence in sentences:
                    if j == 4:
                        break
                    print(f'{i}. {sentence.text}')
                    rows.append(sentence.text)
                    i += 1
                    j += 1
                print()

            if i == 0:
                print("Not found ;(\n")
        except (ConnectionError, ResponseError):
            print("Connection failed ;(\n")

        translate = input("Enter Ukrainian translate ('--n' - don't save): ").lower()
        if translate.find("--n") == -1:
            explain = input(f"Enter explain for '{word}' (--num): ")
            if explain.find('--num') != -1:
                explain = num_row(explain, rows)
            exmple = input("Enter some sentences (' / ' - delimeter): ")
            if exmple.find('--num') != -1:
                exmple = num_row(exmple, rows)
            with open(fname, 'a', encoding='utf-8') as f, open(fname_all, 'a', encoding='utf-8') as f2:
                f.write(f"{word} = {translate} = {explain} = {exmple}\n")
                f2.write(f"{word} = {translate} = {explain} = {exmple}\n")


if __name__ == "__main__":
    findWord()
