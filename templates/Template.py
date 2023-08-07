import os.path
from enum import Enum

from utils import MAIN_DIR

TEMPLATES_DIR = os.path.join(MAIN_DIR, "templates" + os.sep)


class TEMPLATE(Enum):
    TEMPLATE_1 = TEMPLATES_DIR + "template_1.pptx"
    TEMPLATE_1_DARK = TEMPLATES_DIR + "template_1_dark.pptx"  # fixme: create it
    TEMPLATE_2 = TEMPLATES_DIR + "template_2.pptx"  # fixme : create it
    TEMPLATE_3 = TEMPLATES_DIR + "template_3.pptx"  # fixme : create it
