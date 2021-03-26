import json
import html2text
from my_file import MyFile


class HTMLParser:
    def __init__(self, html_str, persons):
        self.html_str = html_str
        self.prepare_html_str()
        self.html_text = self.get_html_text()
        self.persons = persons
        self.messages = []

    def remove_block(self, start_substr, stop_substr):
        self.html_str = self.html_str.replace(
            self.html_str[self.html_str.find(start_substr): self.html_str.find(stop_substr) + 5], '')

    def remove_string_block(self, start_substr, number):
        start_index = self.html_str.find(start_substr)
        index = start_index
        for i in range(number):
            index = self.html_str.find('\n', index + 1)
        self.html_str = self.html_str.replace(self.html_str[start_index:index], '')

    def prepare_html_str(self):
        self.remove_block('<h2 class="page_block_h2">', '</h2>')
        self.remove_string_block('<div class="pagination clear_fix">', 6)

    def get_html_text(self):
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        return converter.handle(self.html_str)

    def find_person(self, text):
        for person in self.persons:
            p_ind = text.find(person)
            if p_ind != -1:
                return person
        return None

    def replace_extra_characters(self, phrase):
        replace_dict = {
            ",": "",
            "(": " ",
            ")": " ",
            ".": "",
            "!": "",
            "?": "",
            "🤷‍♂": "",
            "🤷‍♀": "",
            "✊": "",
            "👍": "",
            "🙃": ""
        }

        for char, new in replace_dict.items():
            phrase = phrase.replace(char, new)

        phrase = ' '.join(phrase.split())
        return phrase

    def concatenate_not_word(self, phrase):
        ind = phrase.find(' не ')
        while ind != -1:
            phrase = phrase[:ind + 3] + '_' + phrase[ind + 4:]
            ind = phrase.find(' не ', ind)
        return phrase

    def prepare_data(self, phrase):
        phrase = self.concatenate_not_word(phrase)
        phrase = self.replace_extra_characters(phrase)
        return phrase

    def parse(self):
        new_sep = "\n\n\n"
        self.html_text = self.html_text.replace("\n\n", new_sep)
        split_text = self.html_text.split(sep=new_sep)

        i = 0
        while i < len(split_text):
            person = self.find_person(split_text[i])
            if person:
                phrase = split_text[i + 1]
                if phrase.find('Вы,') != -1 or phrase.find('Света Курилова,') != -1:
                    # print('Bug string')
                    pass
                else:
                    phrase = self.prepare_data(phrase)
                    self.messages.append({person: phrase.lower()})
            i += 1
        return self.messages


def generate_filenames_by_file_numbers(from_file_number, to_file_number, messages_in_file=50):
    if from_file_number >= to_file_number:
        raise Exception("From_file_number >= to_file_number")
    filenames = []
    num = 0
    if from_file_number:
        num = from_file_number * messages_in_file
    for i in range(from_file_number, to_file_number):
        filename = f"messages{num}.html"
        filenames.append(filename)
        num += messages_in_file

    return filenames


def generate_filenames_by_file_postfixes(from_file_postfix, to_file_postfix, messages_in_file=50):
    if from_file_postfix >= to_file_postfix:
        raise Exception("From_file_postfix >= to_file_postfix")
    filenames = []
    num = from_file_postfix
    while num <= to_file_postfix:
        filename = f"messages{num}.html"
        filenames.append(filename)
        num += 50

    return filenames


def parse(
        users,
        from_file_number=None,
        to_file_number=None,
        from_file_postfix=None,
        to_file_postfix=None,
        out_file_name=None,
        save=False
):
    encoding = "windows-1251"
    messages = []

    # if (from_file_number or from_file_number >= 0) and to_file_number:
    #     filenames = generate_filenames_by_file_numbers(from_file_number, to_file_number) # TODO TypeError: '>=' not supported between instances of 'NoneType' and 'int'
    if (from_file_postfix or from_file_postfix >= 0) and to_file_postfix:
        filenames = generate_filenames_by_file_postfixes(from_file_postfix, to_file_postfix)
    else:
        raise Exception("No file searching argument passed")

    print(f"Parsing files: {filenames[0]} - {filenames[-1]}")
    for in_filename in filenames:
        in_file = MyFile("data/" + in_filename, encoding=encoding)

        html_string = in_file.read_file()
        parser = HTMLParser(html_string, users)
        messages += parser.parse()

    if save and out_file_name:
        out_final_file = MyFile("parsed/" + out_file_name, encoding="utf-8")
        file_handler = out_final_file.open("w")
        json.dump(messages, file_handler, ensure_ascii=False, indent=2)
        file_handler.close()

    return messages


if __name__ == '__main__':
    print(generate_filenames_by_file_postfixes(191400,176000))
