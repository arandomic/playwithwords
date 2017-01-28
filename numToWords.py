#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NumToWordsConverter:
    """
        Сonverts numbers (from 0 to 999999) to russian words according Grammatical Gender
    """
    #to convert all grammatical forms to one
    WORD_TO_ONE = [['одна','один','одно'],['две','два','два'],['тысяч','тысяча','тысячи']]

    #Grammatical gender
    HE='he'
    SHE='she'
    IT='it'

    def __init__(self):
        self.genderSigned = {1:{NumToWordsConverter.HE:'один',NumToWordsConverter.SHE:'одна',NumToWordsConverter.IT:'одно'},2:{NumToWordsConverter.HE:'два',NumToWordsConverter.SHE:'две',NumToWordsConverter.IT:'два'}}
        self.thousandWordNumber = ['тысяч','тысяча','тысячи']
        self.hundreds = ['-not-use-','сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']
        self.first = ['-not-use-','-not-use-','-not-use-','три','четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать']
        self.dozens = ['-not-use-','-not-use-', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']

    def wordNumberDiscriminator(self, n):
        """
            return one of three word form for numerable object
            0 - ноль [десять, тысяча, пять] вещей
            1 - одна вещь
            2 - две [три, четыре] вещи
        """
        n = n % 100
        
        #exceptional case for 11-19
        if (n < 20) and (n > 10):
            return 0
            
        nd = n % 10
        return [0,1,2,2,2,0,0,0,0,0][nd]

    def __convert_first_ten__(self, n, gg):
        ret = ""
        #first three numbers has a grammatical gender
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
        n2 = (n % 1000) // 100
        n1 = (n % 100) // 10
        n0 = n % 10
        
        if(n3 > 0):
            ret = self.convert(n3, NumToWordsConverter.SHE) + " " +self.thousandWordNumber[self.wordNumberDiscriminator(n3)] + " "

        if(n2 > 0):
            ret = ret + self.hundreds[n2] + " "


        if n1 > 1:
            ret = ret + self.dozens[n1] + " "
            
        n10 = n1*10+n0            
        if(n10 < 20):
            ret = ret + self.__convert_first_ten__(n10,gg)
        else:            
            ret = ret + self.__convert_first_ten__(n0,gg)

        return ret.strip()

if __name__ == "__main__":
    cv = NumToWordsConverter()
    print(cv.convert(195321, NumToWordsConverter.SHE))
    print(cv.convert(999999, NumToWordsConverter.SHE))
    print(cv.convert(0, NumToWordsConverter.SHE))
    print(cv.convert(1, NumToWordsConverter.SHE))
    print(cv.convert(1, NumToWordsConverter.HE))
    print(cv.convert(3221, NumToWordsConverter.IT))
