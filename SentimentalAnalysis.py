import sys
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import pos_tag, word_tokenize, RegexpParser
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStyle, QFrame
from PyQt5.QtGui import QFont, QColor, QPainter, QIcon
from PyQt5.QtCore import Qt, QSize

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.placeholder_text = ""

    def setPlaceholderText(self, text):
        self.placeholder_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.text() and self.placeholder_text:
            painter = QPainter(self)
            placeholder_color = QColor(192, 192, 192)
            painter.setPen(placeholder_color)
            painter.drawText(self.rect(), Qt.AlignCenter, self.placeholder_text)

class SentimentAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sentiment Analysis App")
        self.setWindowIcon(QIcon('icon.ico'))
        self.setFixedSize(1280, 680)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)  

        self.setStyleSheet("background-color: #343e55;")
        
        default_font = "Catamaran"
        
        font_heading = QFont(default_font, 32)
        font_label = QFont(default_font, 14, QFont.Bold)
        font_text = QFont(default_font, 14)
        font_text.setItalic(True)

        self.heading_label = QLabel("Sentiment Analysis using AI / ML", self)
        self.heading_label.setStyleSheet("color: white;")
        self.heading_label.setFont(font_heading)
        self.heading_label.setAlignment(Qt.AlignCenter)

        self.input_text = CustomLineEdit(self)
        self.input_text.setStyleSheet("color: white; background-color: #1e2838; border: none; padding: 20px;")
        self.input_text.setFont(font_label)
        self.input_text.setPlaceholderText("Enter your text...")
        self.input_text.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("Result: ", self)
        self.result_label.setStyleSheet("color: white;")
        self.result_label.setFont(font_label)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.result_text = QLabel(self)
        self.result_text.setStyleSheet("color: white;")
        self.result_text.setFont(font_text)
        self.result_text.setAlignment(Qt.AlignCenter)

        self.aspect_label = QLabel("Aspects: ", self)
        self.aspect_label.setStyleSheet("color: white;")
        self.aspect_label.setFont(font_label)
        self.aspect_label.setAlignment(Qt.AlignCenter)

        self.aspect_words = QLabel(self)
        self.aspect_words.setStyleSheet("color: white;")
        self.aspect_words.setFont(font_text)
        self.aspect_words.setAlignment(Qt.AlignCenter)

        self.analyze_button = QPushButton(self)
        self.analyze_button.setStyleSheet("background-color: white; color: #343e55; padding: 10px;")
        self.analyze_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        size = QSize(30, 30)
        self.analyze_button.setIconSize(size)
        self.analyze_button.setFixedWidth(50)
        self.analyze_button.clicked.connect(self.analyze_text)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.analyze_button)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.heading_label)
        layout.addSpacing(60)
        layout.addLayout(input_layout)
        layout.addSpacing(30)
        layout.addWidget(self.aspect_label)
        layout.addSpacing(10)
        layout.addWidget(self.aspect_words)
        layout.addSpacing(30)
        layout.addWidget(self.result_label)
        layout.addSpacing(10)
        layout.addWidget(self.result_text)
        layout.addSpacing(30)
        self.bottom_layout = self.create_bottom_layout()
        layout.addLayout(self.bottom_layout)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_input_text_size()

    def update_input_text_size(self):
        window_width = self.width()
        desired_width = int(window_width * 0.7)
        self.input_text.setFixedWidth(desired_width)

    def analyze_text(self):
        input_text = self.input_text.text()

        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = sentiment_analyzer.polarity_scores(input_text)
        compound_score = sentiment_scores["compound"]

        if compound_score >= 0.05:
            sentiment = "Positive"
            box_index = 0
        elif compound_score > -0.05 and compound_score < 0.05:
            sentiment = "Neutral"
            box_index = 1
        else:
            sentiment = "Negative"
            box_index = 2

        self.result_text.setText(sentiment)

        for i in range(3):
            box = self.bottom_layout.itemAt(i).widget()
            if i == box_index:
                if i == 0:
                    box.setStyleSheet("background-color: #219F94; padding: 10px;")
                elif i == 1:
                    box.setStyleSheet("background-color: #7579E7; padding: 10px;")
                elif i == 2:   
                    box.setStyleSheet("background-color: #F65A83; padding: 10px;")
            else:
                box.setStyleSheet("background-color: #1e2838; padding: 10px;")  

        aspect_words = self.extract_aspect_words(input_text)

        if aspect_words:
            aspect_words_str = ", ".join(aspect_words)
        else:
            aspect_words_str = "No aspects found"

        self.aspect_words.setText(aspect_words_str)

    def extract_aspect_words(self, text):
        tokens = word_tokenize(text)
        tagged_tokens = pos_tag(tokens)

        grammar = "Aspect: {<NN><NN|NNS>}"
        parser = RegexpParser(grammar)
        tree = parser.parse(tagged_tokens)

        aspect_words = []
        for subtree in tree.subtrees():
            if subtree.label() == "Aspect":
                aspect_words.extend([word for word, _ in subtree.leaves()])

        return aspect_words

    def create_bottom_layout(self):
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        emoji_codes = ["\U0001F600", "\U0001F610", "\U0001F615"]

        for emoji_code in emoji_codes:
            box = QFrame()
            box.setFixedSize(120, 120)

            box_style_sheet = "background-color: #1e2838; padding: 10px;"
            box.setStyleSheet(box_style_sheet)

            emoji_label = QLabel(emoji_code)
            emoji_label.setAlignment(Qt.AlignCenter)
            emoji_label.setStyleSheet("color: white; font-size: 45px;")

            box_layout = QVBoxLayout()
            box_layout.addWidget(emoji_label)
            box_layout.setAlignment(Qt.AlignCenter)

            box.setLayout(box_layout)

            bottom_layout.addWidget(box)

        return bottom_layout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SentimentAnalysisApp()
    window.show()
    sys.exit(app.exec_())
