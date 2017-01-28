#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NumToWordsConverter:
    """
        Сonverts numbers (from 0 to 999999) to russian words according Grammatical Gender
    """
    NUMBERS0m=["ноль","один", "два", "три", "четыре"]
    NUMBERS0w=["ноль","одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
    NUMBERS0d=["ноль","одно", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
    
    #to convert all grammatical forms to one
    WORD_TO_ONE = [['одна','один','одно'],['две','два','два'],['тысяч','тысяча','тысячи']]
    
    #Grammatical gender
    HE='he'
    SHE='she'
    IT='it'

    def __init__(self):
        self.genderSigned = {1:{NumToWordsConverter.HE:'один',NumToWordsConverter.SHE:'одна',NumToWordsConverter.IT:'одно'},2:{NumToWordsConverter.HE:'два',NumToWordsConverter.SHE:'две',NumToWordsConverter.IT:'два'}}
        self.thousandWordNumber = ['тысяч','тысяча','тысячи']
        self.hundreds = [':(','сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']
        self.first = ['','1','2','три','четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать']
        self.dozens = ['0','10', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']

    def wordNumberDiscriminator(self, n):
        n = n % 100
        if (n < 20) and (n > 4):
            return 0
        nd = n % 10
        return [0,1,2,2,2,0,0,0,0,0][nd]

    def __convert_first__(self, n, gg):
        ret = ""
        if(n < 3):
            if(n in self.genderSigned):
                ret = ret + self.genderSigned[n][gg]
        else:
            ret = ret + self.first[n]
        return ret

    def convert(self, n, gg):
        """
            convert n to words with Grammatical Gender == gg
        """

        ret = ""

        if n == 0:
            return "ноль"


        n3 = (n // 1000) % 1000
        n3d = self.wordNumberDiscriminator(n3)
        n2 = (n % 1000) // 100
        n1 = (n % 100) // 10
        n0 = n % 10

        if(n3 > 0):
            ret = self.convert(n3, NumToWordsConverter.SHE) + " " +self.thousandWordNumber[n3d] + " "

        if(n2 > 0):
            ret = ret + self.hundreds[n2] + " "

        n10 = n1*10+n0

        if(n10 < 20):
            ret = ret + self.__convert_first__(n10,gg)
        else:
            ret = ret + self.dozens[n1] + " "
            ret = ret + self.__convert_first__(n0,gg)

        return ret.strip()




if __name__ == "__main__":
    cv = NumToWordsConverter()
    print(cv.convert(195321, NumToWordsConverter.SHE))
    # for n in range(0,99):
        # print(cv.convert(n, NumToWordsConverter.HE))