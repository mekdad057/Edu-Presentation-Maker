import re

from data_objects import Document
from data_preparation_stage.preprocessing.DocumentProcessor\
    import DocumentProcessor


class NonEnglishMathSafeRemover(DocumentProcessor):
    """
    removes any strange characters to English Language.

    keeps main characters like English letters, some Math operations,
     parenthesis, brackets, punctuation, $ % &
    """
    LATIN_LETTERS: str
    def __init__(self):
        super().__init__()

    def process_document(self, doc: Document):
        for i in range(len(self._texts)):
            self._texts[i] = re.sub(r"[^&%\$0-9a-zA-Z.,:;?!`>()<"
                                    r"{}\[\]\-\\\'\"\s"
                                    # math symbols
                                    r"+÷×−*∗=√∞≈≠≤≥^/πe∑∆∫∂∏∪∩∈∀∃¬∧∨→↔" 
                                    r"±∞=≠~×÷!∝<≪>≫≤≥∓≅≈≡∀∁∂∛∪∜∩√∅%°℉℃∆"
                                    r"∇∃∄∈∋←↑→↓↔∴±¬*∙⋮⋯⋰⋱ℵℶαβγδεϵζηθϑικλμν"
                                    r"ξοπϖρϱσςτυφϕχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧ"
                                    r"ΨΩ∀∁∂CðℇϜgHHhℏ℩ıIjϰLlN℘QRZ℧ÅB℮E∃∄FMo"
                                    r"ℵℶℷℸ∫∬∭∮∯∰⋀⋁⨂⨀⨁∧∨⊔≮≰≯≱≡≃≈≅≢≄≉≇∝⊂⊃⊆"
                                    r"⊇≺≻≼≽∥⊥⊢⊣⋈≍⋋⋉⋊†‡⋆⋄⋙⋘≦∵∴⨁⨂△≀≧≲≳⋍⊨≗"
                                    r"≜∝⋈⇐⇒⇑⇓⇔⇕⟵⟶⟷⟸⟹⟺↗↖↘↙↚↛↮⇍⇏⇎⇠⇢↤↦⟻"
                                    r"⟼↼↽⇀⇁↿↾⇃⇂⇜⇝∟∠∡∢⊾⊿⋕⊥∤∥∦∶∷]"
                                    , "", self._texts[i])
            doc.paragraphs[i].processed_data = self._texts[i]
