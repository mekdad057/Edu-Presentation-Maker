import os.path
from enum import Enum

from utils import MAIN_DIR

TEMPLATES_DIR = os.path.join(MAIN_DIR, "templates" + os.sep)


class TEMPLATE(Enum):
    TEMPLATE_1 = TEMPLATES_DIR + "template_1.pptx"
