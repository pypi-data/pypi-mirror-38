import logging
import subprocess

from prvsnlib.utils.run import Run


class FiletypeHandlerType:
    DUTI = 'duti'


class FiletypeHandlerTask:

    _file_handler_tool = None

    @property
    def file_handler_tool(self):
        if not self.__class__._file_handler_tool:
            try:
                if subprocess.check_output(['which', 'duti']):
                    self.__class__._file_handler_tool = FiletypeHandlerType.DUTI
            except Exception:
                pass
        return self.__class__._file_handler_tool

    def run(self, extension, handler):
        logging.header('File ' + extension + ' handled by ' + handler)

        if self.__class__._file_handler_tool == FiletypeHandlerType.DUTI:
            Run(['duti', '-s', handler, extension, 'all']).run()
        raise Exception('No tool available for handling file types.')


def file_handler(extension, handler):
    FiletypeHandlerTask().run(extension, handler)
