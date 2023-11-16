import random
import time

from PyQt6 import uic
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTextEdit, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('million_dice_roll.ui', self)

        self.input_field: QLineEdit = self.findChild(QLineEdit, 'InputField')

        self.start_btn: QPushButton = self.findChild(QPushButton, 'StartButton')

        self.text_view: QTextEdit = self.findChild(QTextEdit, 'textEdit')

        self.set_btns_events()

    def set_btns_events(self):
        self.start_btn.clicked.connect(self.start_simulate)

    def check_fields(self) -> bool:
        txt = self.input_field.text().strip()

        if txt == '':
            self.show_error('Поле не может быть пустым')
            return False

        elif len(txt.split()) > 1:
            self.show_error('Только одно число')
            return False

        elif not txt.isdigit():
            self.show_error('Введите число, букв быть не должно')
            return False

        return True

    def show_error(self, error_msg: str):
        self.text_view.setStyleSheet('color: red;')
        self.text_view.setText(error_msg)
        self.input_field.setStyleSheet('border-color: red;')

    def start_simulate(self):
        if not self.check_fields():
            return

        self.text_view.setStyleSheet('color: #fff;')

        number_of_dice = int(self.input_field.text())

        results = {}
        for i in range(number_of_dice, (number_of_dice * 6) + 1):
            results[i] = 0

        # Simulate dice rolls:
        last_print_time = time.time()
        for i in range(1000000):
            if time.time() > last_print_time + 1:
                last_print_time = time.time()

            total = 0
            for j in range(number_of_dice):
                total = total + random.randint(1, 6)
            results[total] = results[total] + 1

        # Display results:
        # self.text_view.setText('Результат:\n TOTAL - ROLLS - PERCENTAGE')

        html_tr_tag = ''
        for i in range(number_of_dice, (number_of_dice * 6) + 1):
            roll = results[i]
            percentage = round(results[i] / 10000, 1)
            html_tr_tag += f'<tr><td style="border: 1px solid #fff; padding: 5px;">{i}</td><td style="border: 1px solid #fff; padding: 5px;">{roll}</td><td style="border: 1px solid #fff; padding: 5px;">{percentage}%</td></tr>'
            # self.text_view.setText(f'{self.text_view.toPlainText()}\n{i} - {roll} - {percentage}')

        html = f"""
                <html>
                <body>
                    <table>
                        <tr>
                            <th style="border: 1px solid #fff; padding: 5px;">TOTAL</th>
                            <th style="border: 1px solid #fff; padding: 5px;">ROLLS</th>
                            <th style="border: 1px solid #fff; padding: 5px;">PERCENTAGE</th>
                        </tr>
                       {html_tr_tag}
                    </table>
                </body>
                </html>
                """

        self.text_view.setHtml(html)
