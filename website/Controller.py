import os

from presentation_maker import TaskHandler
from utils import WORKING_DIR


class Controller:

    def __init__(self):
        self._handler = TaskHandler()

    def create_presentation(self, title, paths):
        # clear output file
        self._clear_output_files()

        # call TaskHandler to create the presentation

        # export file to static folder as output.pptx
        pass

    def _clear_output_files(self):
        output_files = os.listdir(WORKING_DIR)

        for item in output_files:
            if item.endswith(".pptx"):
                os.remove(os.path.join(WORKING_DIR, item))
