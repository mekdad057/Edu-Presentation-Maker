from presentation_maker import TaskHandler


def main():
    handler = TaskHandler()
    link = "https://en.wikibooks.org/wiki/Artificial_Intelligence_for_Computational_Sustainability%3A_A_Lab_Companion%2FMachine_Learning_for_Prediction"
    handler.create_presentation("Artificail Intelligence and Computational Complexity"
                                , [link]
                                , r"C:\Users\VISION\Desktop 2\PROJECT_FORTH_YEAR\Edu-Presentation-Maker\driver"
                                )


if __name__ == '__main__':
    main()
