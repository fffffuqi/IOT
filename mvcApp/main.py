from PyQt5.QtWidgets import QApplication
from views import LoginRegisterUI
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_ui = LoginRegisterUI()
    login_ui.show()
    sys.exit(app.exec_())
