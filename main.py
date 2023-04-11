"""
DocumentCloud Add-On that translates documents using Google Translate services.
"""
from google.cloud import translate_v2 as translate
from util.constants import ENCODING_STANDARD
from documentcloud.addon import AddOn
import os

class Translate(AddOn):
    """DocumentCloud premium Add-On that translates documents"""
    def translate_text(text, target_lan, source_lan:
        translate_client = translate.Client()
        result = translate.client.translate(text=text, target_language=target_lan, source_language=source_lan)
        return result['translatedText']
                       
    def main(self):
        # Retrieve input and out language charactor codes
        source_lang = self.data.get("input_lang")
        target_lang = self.data.get("output_lang")
        # Checks that input and output language codes are valid. 
        if len(input_lang) != 2:
            self.set_message(
                "You submitted an improper ISO language code as an input. "
                "It is supposed to be two characters in length."
            )
            sys.exit(1)
        if len(output_lang) != 2:
            self.set_message(
                "You submitted an improper ISO language code for the output language. "
                "It is supposed to be two characters in length."
            )
            sys.exit(1)                         
        # Creates temporary directory out to store translations in before upload
        os.makedirs(os.path.dirname("./out/"), exist_ok=True)    
        os.chdir("./out/")
        # For each document, translate the text and create a text file with the translation 
        for document in self.get_documents():
            translated_text=str(translate_text(document.full_text, source_lang, target_lang))
            with open(f"{document.title}-translation_{target_lang}", "wb") as file:
                       file.write(translated_text)
                       self.client.documents.upload(f"{document.title}-translation_{target_lang}", original_extension="txt", title=f"{document.title}-translation_{target_lang}")
                       

if __name__ == "__main__":
    Translate().main()
