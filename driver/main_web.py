from website import create_app
from website import model
app = create_app()

if __name__ == '__main__':
    # app.run(debug=True)
    model.create_presentation("Artificail Intelligence"
                              , ["https://en.wikibooks.org/wiki/Artificial_Intelligence_for_Computational_Sustainability%3A_A_Lab_Companion%2FMachine_Learning_for_Prediction"])
