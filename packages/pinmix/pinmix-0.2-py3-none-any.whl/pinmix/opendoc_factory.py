from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H, P, Span


def sample():
    textdoc = OpenDocumentText()
    # Styles
    s = textdoc.styles
    h1style = Style(name="Heading 1", family="paragraph")
    h1style.addElement(TextProperties(attributes={'fontsize':"24pt",'fontweight':"bold" }))
    s.addElement(h1style)
    # An automatic style
    boldstyle = Style(name="Bold", family="text")
    boldprop = TextProperties(fontweight="bold")
    boldstyle.addElement(boldprop)
    textdoc.automaticstyles.addElement(boldstyle)
    # Text
    h=H(outlinelevel=1, stylename=h1style, text="My first texta")
    textdoc.text.addElement(h)
    p = P(text="Hello world. ")
    boldpart = Span(stylename=boldstyle, text="This part is bold. ")
    p.addElement(boldpart)
    p.addText("This is after bold.")

    quotStyle = Style(name="Quotations")
    marginaliaStyle = Style(name="Marginalia")

    # p2 = P(text="2nd par. ", stylename=textBodyStyle)
    p3 = P(text="3rd par. ", stylename=quotStyle)

    textdoc.text.addElement(p)
    textdoc.text.addElement(p2)
    textdoc.text.addElement(p3)
    a = textdoc.save("myfirstdocument.odt")


class DocFactory:

    def __init__(self, filename):
        self.filename = filename
        self.quotStyle = Style(name="Quotations")
        self.marginaliaStyle = Style(name="Marginalia")
        self.doc = OpenDocumentText()

    def add_p1_text(self, txt):
        self.doc.text.addElement(P(text=txt))

    def add_p2_text(self, txt):
        self.doc.text.addElement(P(text=txt, stylename=self.quotStyle))

    def add_p3_text(self, txt):
        self.doc.text.addElement(P(text=txt, stylename=self.marginaliaStyle))

    def save(self):
        self.doc.save(self.filename)