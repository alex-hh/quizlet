from googletrans import Translator

# linguee, wordref

class GoogleTranslator:

  def __init__(self, source_lang='fr', dest_lang='en'):
    self.source_lang = source_lang
    self.dest_lang = dest_lang
    self.translator = Translator()

  def translate(self, text):
    if type(text)==str:
        return self.translator.translate(text, src=self.source_lang,
                                         dest=self.dest_lang).text
    elif type(text)==list:
        return [w.text for w in self.translator.translate(text, src=self.source_lang,
                                                     dest=self.dest_lang)]