from translate import Translator

string = input('My string: ')

translator = Translator(to_lang='en', from_lang='zh')

print(translator.translate(string))
