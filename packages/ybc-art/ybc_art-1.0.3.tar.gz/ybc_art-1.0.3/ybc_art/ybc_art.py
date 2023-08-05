# -*- coding: utf-8 -*-

from .font_map import *


DEFAULT_FONT = "standard"


def font_list():
    """
    This Function Print All Of Fonts
    :return: None
    """
    for item in sorted(list(font_map.keys())):
        print(str(item) + " : ")
        tprint("test", str(item))


def tprint(text, font=DEFAULT_FONT, chr_ignore=True):
    """
    This function split function by \n then call text2art function
    :param text: input text
    :type text:str
    :param font: input font
    :type font:str
    :param chr_ignore: ignore not supported character
    :type chr_ignore:bool
    :return: None
    """
    try:
        split_list = text.split("\n")
        result = ""
        for item in split_list:
            if len(item) != 0:
                result = result+text2art(item, font=font, chr_ignore=chr_ignore)
        print(result)
    except Exception:
        pass


def text2art(text, font=DEFAULT_FONT, chr_ignore=True):
    """
    This function print art text
    :param text: input text
    :type text:str
    :param font: input font
    :type font:str
    :param chr_ignore: ignore not supported character
    :type chr_ignore:bool
    :return: artText as str
    """
    try:
        split_list = []
        result_list = []
        letters = standard_dic
        text_temp = text
        if font.lower() in font_map.keys():
            letters = font_map[font.lower()][0]
            if font_map[font.lower()][1] == True:
                text_temp = text.lower()
        for i in text_temp:
            if (ord(i) == 9) or (ord(i) == 32 and font == "block"):
                continue
            if (i not in letters.keys()) and (chr_ignore == True):
                continue
            if len(letters[i]) == 0:
                continue
            split_list.append(letters[i].split("\n"))
        if len(split_list) == 0:
            return ""
        for i in range(len(split_list[0])):
            temp = ""
            for j in range(len(split_list)):
                if j > 0 and (i == 1 or i == len(split_list[0])-2) and font == "block":
                    temp = temp+" "
                temp = temp + split_list[j][i]
            result_list.append(temp)
        return(("\n").join(result_list))

    except KeyError:
        print("[Error] Invalid Char!")
    except Exception:
        print("[Error] Print Faild!")


def main():
    print(text2art('nihao 1234'))


if __name__ == "__main__":
    main()
