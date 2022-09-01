import sys

from src.ping_pong_scoreboard import PingPongScoreBoardApp

from PyQt5.QtWidgets import QWidget, QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PingPongScoreBoardApp()

    sys.exit(app.exec_())
