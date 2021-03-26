import sys, traceback
import codecs


class MyFileError(Exception): pass
class ReadError(Exception): pass
class SetterError(Exception): pass


class MyFile:
    def __init__(self, filename, encoding=None):
        self.filename = filename
        self.encoding = encoding
        self._file = None

    def read_file(self):
        try:
            with open(self.filename, encoding=self.encoding) as file:
                return file.read()
        except FileNotFoundError:
            raise ReadError("Read file error")
        except:
            raise MyFileError(f"Unknown error: \n\n {traceback.format_exc()}")

    def read_line(self, n):
        try:
            s = ''
            with open(self.filename, encoding=self.encoding) as file:
                for i in range(n):
                    s += file.readline()
            return s
        except FileNotFoundError:
            raise ReadError()
        except:
            raise MyFileError(f"Unknown error: \n\n {traceback.format_exc()}")

    @staticmethod
    def redirect_stdout(file):
        original = sys.stdout
        sys.stdout = file
        return original

    def print_to_file(self, data, mode='w'):
        file = open(self.filename, mode, encoding=self.encoding)
        temp = sys.stdout
        MyFile.redirect_stdout(file)
        print(data)
        MyFile.redirect_stdout(temp)
        file.close()

    def write_file_with_codecs(self, data, mode="w"):
        with codecs.open(self.filename, mode, self.encoding) as temp:
            temp.write(data)

    def write_file(self, data):
        with open(self.filename, "w") as file:
            file.write(data)

    def open(self, mode, encoding='utf-8'):
        self._file = open(self.filename, mode, encoding=encoding)
        return self._file

    def close(self):
        self._file.close()

    @staticmethod
    def debug_print(data, encoding, mode="w"):
        file = open("debug_print.txt", mode, encoding=encoding)
        original_out = MyFile.redirect_stdout(file)
        print(data)
        MyFile.redirect_stdout(original_out)
        file.close()

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, new_file):
        if not hasattr(new_file, "read"):  # is file like check
            raise SetterError("Argument is not a file like type")
        else:
            self._file = new_file
