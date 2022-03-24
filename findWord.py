import requests
from bs4 import BeautifulSoup
from datetime import datetime

today = datetime.now().strftime('%d-%m-%y')
fname = "./daily_words/new_words" + today + ".txt"
fname_all = "./daily_words/all_words.txt"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def findWord():
    global fname
    while True:
        explain = ""
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
            i = 0
            if examples:
                for example in examples:
                    i += 1
                    example = example.text.rstrip()
                    if not example:
                        continue
                    if example.find('PREV WORD') != -1:
                        break
                    elif example.find('\n') != -1:
                        example = example[:example.find('\n')]
                    print(example)
                    explain += example + '@'
            elif sentences:
                for sentence in sentences:
                    i += 1
                    print(f"{i}. {sentence.text}")
                    explain += f"{i}. {sentence.text}@"

            if i == 0:
                print("Not found ;(\n")
                continue
            else:
                print("Success :)")
        except ConnectionError:
            print("Connection Error ;(\n")

        translate = input("Add Ukrainian translate ('--n' - don't save): ").lower()
        if translate.find("--n") == -1:
            with open(fname, 'a', encoding='utf-8') as f, open(fname_all, 'a', encoding='utf-8') as f2:
                f.write(f"{word} = {translate} = {explain}\n")
                f2.write(f"{word} = {translate} = {explain}\n")


if __name__ == "__main__":
    findWord()
