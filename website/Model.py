import os

from presentation_maker import TaskHandler

from website.config import RESULTS_WEB_DIR, clear_results_folder


class Model:
    _task_handler: TaskHandler

    def __init__(self):
        self._task_handler = TaskHandler()

    def create_presentation(self, title: str, paths: list[str]
                            , presentation_type: str = "simple"):
        generator_used = ""
        if presentation_type == "simple":
            generator_used = "bart-large-cnn"
        elif presentation_type == "detailed":
            generator_used = "bart-large-paper-2-slides-summarizer"

        clear_results_folder()
        self._task_handler.create_presentation(title, paths, RESULTS_WEB_DIR, generator_used)
        return self._get_powerpoint()

    def _get_powerpoint(self):
        result_name = self._task_handler.get_presentation_title()
        return os.path.join(RESULTS_WEB_DIR, result_name + ".pptx")

