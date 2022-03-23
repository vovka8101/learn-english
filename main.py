import os
import random

lines = []
size_lines = 0
fname = ""
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def openFile():
    global fname, size_lines
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

    lines = []
    with open(fname, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            lines.append(line.lower())

    size_lines = len(lines)


def en_ua(line):
    en, ua = "", ""
    indx = line.find(" = ")
    en = line[:indx]
    ua = line[indx + 3:]
    return en, ua


def ua_to_en():
    print("\nTranslate to English ...")
    global size_lines
    incorrect = []
    count, k = 0, 0
    for i in lines:
        k += 1
        answ = ""
        en, ua = en_ua(i)
        print(f"\n{k}/{size_lines}: Sentence: {ua}")

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
    global size_lines
    count, k = 0, 0
    for i in lines:
        k += 1
        answ = ""
        ua_list = []
        en, ua = en_ua(i)
        if ua.find(' / ') != -1:
            ua_list = ua.split(' / ')
        print(f"\n{k}/{size_lines}: Sentence: {en}")

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


def menu():
    while True:
        openFile()
        random.shuffle(lines)
        md = int(input("""
Select the checking mode ...
1 - Translate UA --> EN
2 - Test (a b c...) UA --> EN
3 - Translate EN --> UA
0 - Quite\n"""))
        if md == 1:
            ua_to_en()
        elif md == 2:
            selectCorrect()
        elif md == 3:
            en_to_ua()
        elif md == 0:
            return
        else:
            print("Incorrect mode!")


if __name__ == "__main__":
    menu()
    input('Press Enter to close ...')
