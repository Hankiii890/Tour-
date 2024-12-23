import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Регистрация пользователя')

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Имя')
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email')
        layout.addWidget(self.email_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText('Телефон')
        layout.addWidget(self.phone_input)

        self.register_button = QPushButton('Зарегистрироваться', self)
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        # Здесь вы можете сделать запрос к вашему FastAPI серверу для регистрации
        # Например, с использованием requests
        import requests
        response = requests.post("http://localhost:8000/register/", json={
            "name": name,
            "email": email,
            "phone": phone
        })

        if response.status_code == 200:
            print("Пользователь зарегистрирован!")
        else:
            print("Ошибка регистрации:", response.json())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = RegistrationForm()
    form.show()
    sys.exit(app.exec_())