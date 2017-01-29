#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numToWords import NumToWordsConverter
from collections import Counter
from sortedcontainers import SortedDict
from operator import itemgetter
import re
import itertools
import hashlib
import random
import argparse

class TrueSentenceGenerator:
    """
        Generate self-described russian sentence by pattern:
            [user-prefix][self-descibed-part][user-postfix]
    """

    def __init__(self, prefix, postfix, letter_count_type):
        self.symbols = '",.)(;!? '
        self.symbols_set = set(self.symbols)
        self.symbol_he = set('!? ')
        self.symbol_she = set('",.)(;')
        self.tknzr = re.compile('([^'+self.symbols+']+)')
        self.cv = NumToWordsConverter()
        self.ru_letter = set("абвгдеёжзийклмнопрстуфхцчшщьыъэюя")
        self.en_letter = set("abcdefghijklmnopqrstuvwxyz")
        self.wrd = ["слов", "слово", "слова"]
        self.ltrru = ["букв", "буква", "буквы"]
        self.ltren = ["латинских букв", "латинская буква", "латинских буквы"]
        self.symbname = {'"':["кавычек", "кавычка", "кавычки"],',':["запятых", "запятая", "запятых"],'.':["точек", "точка", "точки"],'(':["левых скобок", "левая скобка", "левых скобки"],')':["правых скобок", "правая скобка", "правых скобки"],';':["точек с запятой", "точка с запятой", "точки с запятой"],'!':["восклицательных знаков", "восклицательный знак", "восклицательных знака"],'?':["знаков вопроса", "знак вопроса", "знака вопроса"]," ":["пробелов", "пробел", "пробела"]}
        self.word_to_one = dict()
        self.letter_count_type = letter_count_type
        for words_line in itertools.chain([self.wrd, self.ltrru, self.ltren], self.symbname.values(), NumToWordsConverter.WORD_TO_ONE):
            for word in words_line:
                word_slice = word.split(" ")
                core_slice = words_line[1].split(" ")
                for token,core_token in zip(word_slice, core_slice):
                    if core_token != token:
                        self.word_to_one[token] = core_token


        self.prefix = prefix
        self.postfix = postfix
        self.infix = ""
        prefix_stat = self.__count_stat__(self.prefix)
        postfix_stat = self.__count_stat__(self.postfix)
        self.const_stat = {"words":prefix_stat["words"]+postfix_stat["words"],"symbols":prefix_stat["symbols"]+postfix_stat["symbols"]}
        self.stat = self.const_stat
        self.prev_stat = None

    def __isStabilised__(self):
        return self.prev_stat == self.stat

    def __count_stat__(self, sentence):
        s = sentence.lower()
        return {"words":Counter(map(lambda w:self.word_to_one[w] if w in self.word_to_one else w, self.tknzr.findall(s))),"symbols":Counter(s)}

    def __check_current__(self):
        self.prev_stat = self.stat
        self.stat = self.__count_stat__(self.infix)

    def __make_next__(self):
        next_infix = ""
        symbols = self.const_stat["symbols"]+self.stat["symbols"]
        ru_sym_count = 0
        en_sym_count = 0

        for sym in SortedDict(symbols):
            count = symbols[sym]
            if sym in self.ru_letter:
                ru_sym_count += count
                if self.letter_count_type == 'all':
                    next_infix += self.cv.convert(count,NumToWordsConverter.SHE) +' '+self.ltrru[self.cv.wordNumberDiscriminator(count)]+' "'+sym+'", '
            elif sym in self.en_letter:
                en_sym_count += count
                if self.letter_count_type == 'all':
                    next_infix += self.cv.convert(count,NumToWordsConverter.SHE) +' '+self.ltren[self.cv.wordNumberDiscriminator(count)]+' "'+sym+'", '
            elif sym in self.symbols_set:
                next_infix += self.cv.convert(count,NumToWordsConverter.HE if sym in self.symbol_he else NumToWordsConverter.SHE) +' '+self.symbname[sym][self.cv.wordNumberDiscriminator(count)]+', '

        if self.letter_count_type == 'summ':
            if ru_sym_count > 0:
                next_infix += self.cv.convert(ru_sym_count,NumToWordsConverter.SHE) +' '+self.ltrru[self.cv.wordNumberDiscriminator(ru_sym_count)]+', '
            if en_sym_count > 0:
                next_infix += self.cv.convert(en_sym_count,NumToWordsConverter.SHE) +' '+self.ltren[self.cv.wordNumberDiscriminator(en_sym_count)]+', '

        pre = ''
        words = self.const_stat["words"]+self.stat["words"]
        for word in SortedDict(words):
            count = words[word]
            next_infix += pre + self.cv.convert(count,NumToWordsConverter.IT) +' '+self.wrd[self.cv.wordNumberDiscriminator(count)]+' "'+word
            pre = '", '
        next_infix = next_infix + '"'
        self.infix = next_infix

    def generateFromSeed(self, seed):
        self.infix = seed
        self.__check_current__()
        finded = set()
        current_try = 0
        try:
            while(not self.__isStabilised__()):
                current_try += 1
                self.__make_next__()
                self.__check_current__()
                self.__clean_selflinked__()
                cur_infix_hash = hashlib.sha224(self.infix.encode()).hexdigest()
                if cur_infix_hash in finded:
                    raise Exception("cycled!")
                finded.add(cur_infix_hash)
        except Exception as e:
            pass

        return current_try,self.infix

    def __clean_selflinked__(self):
        words = self.const_stat["words"]+self.stat["words"]
        for word in words:
            if words[word] <= 1:
                del self.stat["words"][word]

    def generate(self):
        self.__make_next__()
        while not self.__isStabilised__():
            seed = " ".join(random.sample(self.tknzr.findall(self.prefix+self.infix+self.postfix)*100, 100))
            self.generateFromSeed(seed)

    def getResult(self):
        return self.prefix+self.infix+self.postfix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Генерируем истинное самоописываюшее предложение')
    parser.add_argument('--prefix', help="Неизменяемое начало предложения", default="В этом предложении ")
    parser.add_argument('--postfix', help="Неизменяемое окончание предложения", default=" и полное единство формы и содержания.")
    parser.add_argument('--letters', help="Способ перечисления букв - [all-отдельно по каждой букве|summ - количество латинских/русских букв|none - не учитывать] больше информации - дольше ждать", default="summ")

    args = parser.parse_args()

    generator = TrueSentenceGenerator(args.prefix, args.postfix, args.letters)
    generator.generate()
    print(generator.getResult())

