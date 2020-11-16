"""
    Main file.
    Copyright (C) 2020  Vadim Vergasov

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import telebot
import random
import conf

BOT = telebot.TeleBot(conf.TG_TOKEN)


@BOT.message_handler(commands=["start", "help"])
def about(message):
    BOT.send_message(
        message.chat.id, "This bot will shuffle text. Этот бот будет мешать текст."
    )


@BOT.message_handler()
def answer(message):
    answer = ""
    text = message.text.split(" ")
    for word in text:
        vowels_pos = []
        consonants_pos = []
        symbols = []
        start, end = 0, len(word) - 1
        while start < len(word) and not word[start].isalpha():
            start += 1
        start += 1
        while end >= 0 and not word[end].isalpha():
            end -= 1
        if start >= end:
            answer += word + " "
            continue
        print(word, start, end)
        for symbol_pos in range(start, end):
            if word[symbol_pos] in conf.CONSONANTS:
                consonants_pos.append(symbol_pos)
                symbols.append("c")
            elif word[symbol_pos] in conf.VOWELS:
                vowels_pos.append(symbol_pos)
                symbols.append("v")
        random.shuffle(vowels_pos)
        random.shuffle(consonants_pos)
        for s in range(start):
            answer += word[s]
        counter1, counter2 = 0, 0
        for s in symbols:
            if s == "c":
                answer += word[consonants_pos[counter1]]
                counter1 += 1
            elif s == "v":
                answer += word[vowels_pos[counter2]]
                counter2 += 1
        if len(word) != 1:
            for s in range(end, len(word)):
                answer += word[s]
        answer += " "
    BOT.reply_to(message, answer)


BOT.polling()
