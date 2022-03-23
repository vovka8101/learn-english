import requests
import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import shutil
from datetime import datetime

today = datetime.now().strftime('%d-%m-%y')
fname = "./daily_words/new_words" + today + ".txt"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def findWord():
    global fname
    while True:
        word = input("Enter a word ('--q' for exit): ").lower()
        if word == '--q':
            break
        url = "https://dictionary.cambridge.org/dictionary/english/" + word.replace(' ', '+')
        try:
            print("\nProccess ...\n")
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            quotes = soup.find('div', class_='dimg')

            sentences = soup.find_all('div', class_='def ddef_d db')
            i = 0
            for sentence in sentences:
                i += 1
                print(f"{i}. {sentence.text}")

            if i == 0:
                print("Sentences not found ;(\n")
                continue
            else:
                print("Success :)")

            print("\nTry to find an image ...")
            images = quotes.find('amp-img')
            img_link = "https://dictionary.cambridge.org/" + images.attrs['src']
            r = requests.get(img_link, headers=headers, stream=True)
            if r.status_code == 200:
                with open(f"{word}.jpg", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            ok = True
        except (ConnectionError, AttributeError):
            print("Image not found ;(\n")
            ok = False

        if ok:
            print("Success :)\n")
            img = mpim.imread(f"{word}.jpg")
            plt.imshow(img)
            plt.show()
            os.remove(f"{word}.jpg")

        translate = input("Add Ukrainian translate ('--n' - don't save): ").lower()
        if translate.find("--n") == -1:
            with open(fname, 'a', encoding='utf-8') as f:
                f.write(f"{word} = {translate}\n")


if __name__ == "__main__":
    findWord()
