import os

from presentation_maker import TaskHandler

from website.config import RESULTS_WEB_DIR, clear_results_folder


class Model:
    _task_handler: TaskHandler

    def __init__(self):
        self._task_handler = TaskHandler()

    def create_presentation(self, title: str, paths: list[str]):
        clear_results_folder()
        self._task_handler.create_presentation(title, paths, RESULTS_WEB_DIR)
        return self._get_powerpoint()

    def _get_powerpoint(self):
        result_path = self._task_handler.get_presentation_title()
        return os.path.join(RESULTS_WEB_DIR, result_path + ".pptx")

