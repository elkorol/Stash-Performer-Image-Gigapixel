"""Log messages to stderr with a prefix that,
 can be used by the host application to filter them out. """
import sys

class Logger:
    """Log messages to stderr with a prefix that,
     can be used by the host application to filter them out. """
    def __prefix(self, levelchar):
        startlevelchar = b'\x01'
        endlevelchar = b'\x02'

        ret = startlevelchar + levelchar + endlevelchar
        return ret.decode()

    def __log(self, levelchar, error_code):
        if levelchar == "":
            return
        if error_code == "":
            return

        print(self.__prefix(levelchar) + error_code +
                "\n", file=sys.stderr, flush=True)

    def trace(self, error_code):
        self.__log(b't', error_code)

    def debug(self, error_code):
        self.__log(b'd', error_code)

    def info(self, error_code):
        self.__log(b'i', error_code)

    def warning(self, error_code):
        self.__log(b'w', error_code)

    def error(self, error_code):
        self.__log(b'e', error_code)

    def progress(self, p):
        progress = min(max(0, p), 1)
        self.__log(b'p', str(progress))
