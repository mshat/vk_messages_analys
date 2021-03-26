import json
from my_file import MyFile


class Analyzer:
    def __init__(self, data=None, in_file_name=None):
        if not data and not in_file_name:
            raise Exception("No argument passed")
        if in_file_name:
            in_file = MyFile(in_file_name, encoding='utf-8')
            f_h = in_file.open("r")
            self.data = json.load(f_h)
            f_h.close()
        if data:
            self.data = data

        self._user_word_frequency_dicts = None

    def _sort_data(self, sort_by_arg=1, reverse=False):
        sorted_data = {}
        for user, messages in self._user_word_frequency_dicts.items():
            sorted_data[user] = list(sorted(messages.items(), key=lambda item: item[sort_by_arg], reverse=reverse))
        return sorted_data

    def sort_data_by_message(self, reverse=False):
        return self._sort_data(sort_by_arg=0, reverse=reverse)

    def sort_data_by_message_frequency(self, reverse=False):
        return self._sort_data(reverse=reverse)

    def calculate_most_popular_words(self, min_word_len=None, exclude_list=None, keep_list=None):
        counters = {}
        if exclude_list:
            exclude_list = list(map(str.lower, exclude_list))
        if keep_list:
            keep_list = list(map(str.lower, keep_list))

        for item in self.data:
            person, phrase = list(item.items())[0][0], list(item.items())[0][1]
            if person not in counters.keys():
                counters.update({person: {}})
            for word in phrase.split():
                if not self.check_need_exclude_word(word, min_word_len, exclude_list, keep_list):
                    if word in counters[person].keys():
                        counters[person][word] += 1
                    else:
                        counters[person][word] = 1
        self._user_word_frequency_dicts = counters
        return counters

    @staticmethod
    def check_need_exclude_word(word, min_word_len=None, exclude_list=None, keep_list=None):
        if not min_word_len and not exclude_list:
            return False
        else:
            if keep_list and word in keep_list:
                return False
            if exclude_list and word in exclude_list:
                return True
            if min_word_len and len(word) < min_word_len:
                return True

    @property
    def user_word_frequency_dicts(self):
        if not self._user_word_frequency_dicts:
            raise Exception("Analyze first (call method calculate_most_popular_words)")
        else:
            return self._user_word_frequency_dicts


def save_statistics(data, name_tag="", save=True, print_=False):
    for user, messages in data.items():
        out_str = ""
        for word in messages:
            out_str += f"{word[0]} {word[1]} \n"
        if save:
            out_file = MyFile(f"analysed/{user}_word_frequency_{name_tag}.txt", encoding="utf-8")
            out_file.write_file_with_codecs(out_str)
        if print_:
            print(out_str)


def analyze(
        data=None,
        in_file_name=None,
        name_tag="",
        save=True,
        print_=False,
        min_word_len=None,
        exclude_list=None,
        keep_list=None
):
    analyzer = Analyzer(data=data, in_file_name=in_file_name)
    user_word_frequency_dicts = analyzer.calculate_most_popular_words(min_word_len, exclude_list, keep_list)
    save_statistics(analyzer.sort_data_by_message_frequency(reverse=True), name_tag=name_tag, save=save, print_=print_)
