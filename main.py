import os
import random
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import shutil

lines = []
fname = ""
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def openFile():
    global fname
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


def findImage():
    word = input("Enter a word: ")
    url = "https://dictionary.cambridge.org/dictionary/english/" + word
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find('div', class_='dimg')
        images = quotes.find('amp-img')
        img_link = "https://dictionary.cambridge.org/" + images.attrs['src']

        r = requests.get(img_link, headers=headers, stream=True)
        if r.status_code == 200:
            with open(f"{word}.jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        ok = True
    except (ConnectionError, AttributeError):
        print("Image not found")
        ok = False

    if ok:
        img = mpim.imread(f"{word}.jpg")
        plt.imshow(img)
        plt.show()
        os.remove(f"{word}.jpg")


def parseWords(word):
    if word.startswith("a "):
        word = word[2:]
    elif word.startswith("an ") or word.startswith("to "):
        word = word[3:]

    url = "https://dictionary.cambridge.org/dictionary/english/" + word
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div', class_='def ddef_d db')
        quote = quotes[0].text
        # i = 0
        # for quote in quotes:
        #     print(quote.text)
        #     i += 1
        #     if i == 3:
        #         break
    except ConnectionError:
        print("Connection Error")

    return quote
    # if i == 0:
    #     print("The hint doesn't find")


def find_word_description():
    pass


def en_ua(line):
    en, ua = "", ""
    indx = line.find(" = ")
    en = line[:indx]
    ua = line[indx + 3:]
    return en, ua


def ua_to_en():
    print("\nTranslate to English ...")
    incorrect = []
    count = 0
    for i in lines:
        answ = ""
        en, ua = en_ua(i)
        print(f"\nSentence: {ua}")

        answ = input("Your answer: ").lower()

        if answ == en:
            count += 1
            print("+ True +")
        else:
            print(f"- False - | Right answer: {en}")
            incorrect.append(i)

    print(f"\nResult: {count}/{len(lines)}\n", *incorrect, sep="\n")


def en_to_ua():
    print("\nTranslate to Ukrainian ...")
    incorrect = []
    count = 0
    for i in lines:
        answ = ""
        ua_list = []
        en, ua = en_ua(i)
        if ua.find(' / ') != -1:
            ua_list = ua.split(' / ')
        print(f"\nSentence: {en}")

        answ = input("Your answer: ").lower()
        flag = False
        if len(ua_list) > 0:
            for i in ua_list:
                if i == answ:
                    flag = True
                    break
        if answ == ua or flag:
            count += 1
            print("+ True +")
        else:
            print(f"- False - | Right answer: {ua}")
            incorrect.append(i)

    print(f"\nResult: {count}/{len(lines)}\n", *incorrect, sep="\n")


def selectCorrect():
    max_n = len(lines) - 1
    n = int(input(f"Enter variants amount (3 - {max_n}): "))
    if n < 3 and n >= max_n:
        print("Argument is wrong")
        return
    print("\nSelect the correct answer ...")
    incorrect = []
    count = 0
    for line in lines:
        variants = []
        en, ua = en_ua(line)
        print(f"\nWord: {ua}")
        variants.append(en)
        i = 0
        while i < n - 1:
            var, _ = en_ua(random.choice(lines))
            if var not in variants:
                variants.append(var)
                i += 1
        random.shuffle(variants)
        for j in range(n):
            print(f"{j + 1}. {variants[j]}")
        answ = int(input("Your answer: "))
        if answ > 0 and answ <= n and variants[answ - 1] == en:
            count += 1
            print("+ True +")
        else:
            print(f"- False - | Right answer: {en} - {ua}")
            incorrect.append(line)

    print(f"\nResult: {count}/{len(lines)}\n", *incorrect, sep="\n")


if __name__ == "__main__":
    openFile()
    random.shuffle(lines)
    md = int(input("""\nSelect the checking mode ...
1 - Translate UA --> EN
2 - Test (a b c...) UA --> EN
3 - Translate EN --> UA
4 - Find word image\n"""))
    if md == 1:
        ua_to_en()
    elif md == 2:
        selectCorrect()
    elif md == 3:
        en_to_ua()
    elif md == 4:
        findImage()
    else:
        print("Incorrect mode!")
    input()
