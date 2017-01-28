#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numToWords import NumToWordsConverter
from collections import Counter
import re
import itertools

class TrueSentenceGenerator:
    """
        Generate self-described russian sentence by pattern:
            [user-prefix][self-descibed-part][user-postfix]
    """

    def __init__(self, prefix, postfix):
        self.symbols = '",.)(;!? '
        self.symbol_he = set('!? ')
        self.symbol_she = set('",.)(;')
        self.tknzr = re.compile('([^'+self.symbols+']+)')
        self.letter = set("абвгдеёжзийклмнопрстуфхцчшщьыъэюя")
        self.en_letter = set("abcdefghijklmnopqrstuvwxyz")
        self.wrd = ["слов", "слово", "слова"]
        self.ltr = ["букв", "буква", "буквы"]
        self.ltren = ["латинских букв", "латинская буква", "латинских буквы"]
        self.symbname = {'"':["кавычек", "кавычка", "кавычки"],',':["запятых", "запятая", "запятых"],'.':["точек", "точка", "точки"],'(':["левых скобок", "левая скобка", "левых скобки"],')':["правых скобок", "правая скобка", "правых скобки"],';':["точек с запятой", "точка с запятой", "точки с запятой"],'!':["восклицательных знаков", "восклицательный знак", "восклицательных знака"],'?':["знаков вопроса", "знак вопроса", "знака вопроса"]," ":["пробелов", "пробел", "пробела"]}
        self.word_to_one = dict()

        for words_line in itertools.chain([self.wrd, self.ltr, self.ltren], self.symbname.values(), NumToWordsConverter.WORD_TO_ONE):
            for word in words_line:
                word_slice = word.split(" ")
                core_slice = words_line[1].split(" ")
                for token,core_token in zip(word_slice, core_slice):
                    self.word_to_one[token] = core_token


        self.prefix = prefix
        self.postfix = postfix
        self.infix = ""
        self.stat = {"words":Counter(),"symbols":Counter()}
        self.prev_stat = None

    def __isStabilised__(self):
        return self.prev_stat == self.stat
        
    def __count_stat__(self, sentence):
        s = sentence.lower()
        return {"words":Counter(map(lambda w:self.word_to_one[w] if w in self.word_to_one else w, self.tknzr.findall(s))),"symbols":Counter(s)}

    def __check__(self, sentence = None):
        if not sentence:
            sentence = self.prefix + self.infix + self.postfix

        self.prev_stat = self.stat
        self.stat = self.__count_stat__(sentence)

if __name__ == "__main__":
    tg = TrueSentenceGenerator("","")
    tg.__check__('Привет, Picabu! Не хочешь немного рекурсии? В этом посте (не считая заголовка и тегов) сорок две буквы, двенадцать латинских букв, один восклицательный знак, сто семьдесят два пробела, восемьдесят две кавычки, одна левая скобка, пятьдесят одна запятая, один знак вопроса, одна точка, одна правая скобка, два слова "Picabu", два слова "В", два слова "Не", два слова "Привет", три слова "буква", два слова "вопроса", два слова "восемьдесят", два слова "восклицательный", тридцать шесть слов "два", два слова "двенадцать", два слова "заголовка", два слова "запятая", три слова "знак", три слова "и", два слова "кавычка", два слова "латинская", два слова "левая", два слова "не", два слова "немного", два слова "никакого", семь слов "один", два слова "посте", два слова "правая", два слова "пробел", два слова "пятьдесят", два слова "рекурсии", три слова "семь", два слова "семьдесят", три слова "скобка", сорок два слова "слово", два слова "смысла", три слова "сорок", два слова "сто", два слова "считая", два слова "тегов", два слова "точка", семь слов "три", два слова "тридцать", два слова "хочешь", два слова "шесть", два слова "этом" и никакого смысла.')
    print(tg.stat)