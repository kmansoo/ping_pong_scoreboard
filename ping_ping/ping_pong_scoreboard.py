import sys
import datetime
from threading import Lock

from PyQt5.QtWidgets import QWidget, QApplication

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QPoint, QRect, QTimer

from device.ping_pong_input_device import InputDeviceEventListener, InputDeviceEvent
from device.mqtt_key_event_device import MQTTKeyEventDevice

from ping_ping.player_info import PlayerInfo

class PingPongScoreBoardApp(QWidget, InputDeviceEventListener):
    def __init__(self):
        super().__init__()
        self.init_app()

    def init_app(self):
        self.MAX_SCORE_NUM = 11
        self.BLINK_TIMER_INTERVAL = 300
        self.MAX_BLINK_SHOW_COUT = 10

        self.start_match_time   = datetime.datetime.now()
        self.last_check_match_time = datetime.datetime.now()

        self.left_player_info = PlayerInfo()
        self.right_player_info = PlayerInfo()

        self.show_blink = False
        self.blink_count = 0
        self.enable_drawing_match_time = True

        self.do_reset_scores()

        self.setGeometry(0, 0, 1920, 1080)

        self.center_pos = QPoint(int(self.geometry().width() / 2), int(self.geometry().height() / 2)) 
        self.center_info_rect = QRect(self.center_pos.x() - 50, self.center_pos.y() - 400, 100, 800)

        self.gap_width = 10
        
        self.game_match_time_rect = QRect(0, 0, 450, 130)

        self.left_team_rect = QRect(0, 0, 600, 100)
        self.right_team_rect = QRect(0, 0, 600, 100)

        self.left_inning_rect = QRect(0, 0, 200, 200)
        self.left_score_rect = QRect(0, 0, 440, 400)
        self.right_inning_rect = QRect(0, 0, 200, 200)
        self.right_score_rect = QRect(0, 0, 440, 400)

        self.left_side_brush = QBrush(QColor(157, 194, 156))
        self.right_side_brush = QBrush(QColor(187, 143, 142))

        # game time
        self.game_match_time_rect.moveTo(self.center_pos.x() - int(self.game_match_time_rect.width() / 2), 80);

        # left score rect
        self.left_inning_rect.moveTo(self.center_pos.x() - self.left_score_rect.width() - self.left_inning_rect.width() - self.gap_width - int(self.gap_width / 2), 350);
        self.left_score_rect.moveTo(self.center_pos.x() - self.left_score_rect.width() - int(self.gap_width / 2), 350);

        # right score rect
        self.right_inning_rect.moveTo(self.center_pos.x() + self.right_score_rect.width() + self.gap_width + int(self.gap_width / 2), 350);
        self.right_score_rect.moveTo(self.center_pos.x() + int(self.gap_width / 2), 350);

        # name rect
        self.left_team_rect.moveTo(self.center_pos.x() - self.gap_width * 4 - self.left_team_rect.width(), self.left_score_rect.top() - self.left_team_rect.height() - int(self.gap_width / 2))
        self.right_team_rect.moveTo(self.center_pos.x() + self.gap_width * 4, self.left_team_rect.top())

        self.setWindowTitle("아푸지만 탁구 점수판")
        self.setStyleSheet("background-color:black;")
        self.showFullScreen()

        # Start check timer for device Input
        self.input_device_event_list_mutex = Lock()
        self.input_device_event_list = []
        self.input_device_event_check_timer = QTimer()
        self.input_device_event_check_timer.setInterval(1)
        self.input_device_event_check_timer.start()
        self.input_device_event_check_timer.timeout.connect(self.do_check_device_input_event)

        if self.enable_drawing_match_time:
            self.match_time_check_timer = QTimer()
            self.match_time_check_timer.setInterval(1)
            self.match_time_check_timer.start()
            self.match_time_check_timer.timeout.connect(self.do_check_match_time)

        self.do_start_input_devices()

        # self.show()
    def draw_scoreboard(self, qp):
        red_brush = QBrush(Qt.red)
        black_brush = QBrush(Qt.black)
        white_brush = QBrush(Qt.white)

        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        # Draw left side
        qp.setBrush(self.left_side_brush)
        qp.drawRoundedRect(self.left_inning_rect, 15, 15)
        qp.drawRoundedRect(self.left_score_rect, 15, 15)

        qp.setBrush(self.right_side_brush)
        qp.drawRoundedRect(self.right_inning_rect, 15, 15)
        qp.drawRoundedRect(self.right_score_rect, 15, 15)

        if self.show_blink == True and (self.blink_count % 2) == 1:
            qp.setBrush(white_brush)

            if self.left_player_info.score > self.right_player_info.score:
                qp.drawRoundedRect(self.left_score_rect, 15, 15)
            else:
                qp.drawRoundedRect(self.right_score_rect, 15, 15)

        qp.setBrush(black_brush)
        qp.setPen(QPen(Qt.black, 1))

        if self.left_player_info.service == True:
            qp.drawEllipse(
                self.left_score_rect.right() - 50, self.left_score_rect.bottom() - 50,
                40, 40)
        else:
            qp.drawEllipse(
                self.right_score_rect.right() - 50, self.right_score_rect.bottom() - 50,
                40, 40)

    def draw_game_time(self, qp):
        # Draw game time
        qp.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        qp.drawRoundedRect(self.game_match_time_rect, 15, 15)

        minutes = int(self.last_check_match_time.total_seconds() / 60)
        seconds = self.last_check_match_time.total_seconds() % 60
        last_check_match_time = str("%02d:%02d" % (minutes, seconds))
        
        qp.setPen(QPen(Qt.white, 1))
        qp.setFont(QFont("Courier New", 120))

        qp.drawText(self.game_match_time_rect, Qt.AlignHCenter|Qt.AlignVCenter|Qt.TextSingleLine, last_check_match_time)

    def draw_score(self, qp):
        # draw score
        qp.setPen(QPen(Qt.white, 1))
        qp.setFont(QFont("Sans Bold", 80))

        qp.drawText(self.left_team_rect, Qt.AlignRight|Qt.AlignVCenter|Qt.TextSingleLine, self.left_player_info.name)
        qp.drawText(self.right_team_rect, Qt.AlignLeft|Qt.AlignVCenter|Qt.TextSingleLine, self.right_player_info.name)

        flags = Qt.AlignHCenter|Qt.AlignVCenter|Qt.TextSingleLine
        qp.setPen(QPen(Qt.black, 1))

        qp.setFont(QFont("Sans Bold", 150))
        qp.drawText(self.left_inning_rect, flags, str(self.left_player_info.inning_score))
        qp.drawText(self.right_inning_rect, flags, str(self.right_player_info.inning_score))

        qp.setFont(QFont("Sans Bold", 300))
        qp.drawText(self.left_score_rect, flags, str(self.left_player_info.score))
        qp.drawText(self.right_score_rect, flags, str(self.right_player_info.score))

        # Show who is a active server

    # Input Device Service
    def do_start_input_devices(self):
        # Create Input Device
        self._mqtt_key_event_device = MQTTKeyEventDevice()
        self._mqtt_key_event_device.set_event_listener(self)
        self._mqtt_key_event_device.start_service()

        # Please add devices if the system has more key event devices
        # self._ir_device = IRRemoteDevice()
        # self._ir_device.set_event_listener(self)
        # self._ir_device.start_service()

    def do_stop_input_devices(self):
        self._mqtt_key_event_device.stop_service()

        # Please call stop_service() for more devices
        # self._ir_device.stop_service()

    # Input Device Event
    def do_check_match_time(self):
        self.do_cal_match_time()

    def do_check_device_input_event(self):
        if len(self.input_device_event_list) == 0:
            return

        self.input_device_event_list_mutex.acquire(True)

        new_key_event = self.input_device_event_list[0]
        self.input_device_event_list.pop(0)
        self.input_device_event_list_mutex.release()

        if new_key_event == InputDeviceEvent.INCREASE_HOME_SCORE:
            self.do_increase_home_score()
        elif new_key_event == InputDeviceEvent.DECREASE_HOME_SCORE:
            self.do_decrease_home_score()
        elif new_key_event == InputDeviceEvent.INCREASE_VISITOR_SCORE:
            self.do_increase_visitor_score()
        elif new_key_event == InputDeviceEvent.DECREASE_VISITOR_SCORE:
            self.do_decrease_visitor_score()
        elif new_key_event == InputDeviceEvent.SWITCH_PLAYER_SIDE:
            self.do_switch_player_side()
        elif new_key_event == InputDeviceEvent.SWITCH_SERVER:
            self.do_switch_server()
        elif new_key_event == InputDeviceEvent.RESET_SCORE:
            self.do_reset_scores()
    
    def do_inning_over(self):
        self.blink_count = 0
        self.show_blink = True

        self.inning_over_timer = QTimer()
        self.inning_over_timer.setInterval(self.BLINK_TIMER_INTERVAL)
        self.inning_over_timer.start()
        self.inning_over_timer.timeout.connect(self.do_blink_score)

    def do_blink_score(self):
        self.blink_count = self.blink_count + 1

        if self.blink_count == self.MAX_BLINK_SHOW_COUT:
            self.show_blink = False
            self.blink_count = 0

            self.inning_over_timer.stop()
            self.left_player_info.score = 0
            self.right_player_info.score = 0
            self.update()
        else:
            if self.left_player_info.score > self.right_player_info.score:
                self.repaint(self.left_score_rect)
            else:
                self.repaint(self.right_score_rect)

    def do_check_whether_server_is_switched(self):
        if self.left_player_info.score >= self.MAX_SCORE_NUM - 1 and self.right_player_info.score >= self.MAX_SCORE_NUM - 1:
            self.do_switch_server()
            return True

        if (self.left_player_info.score + self.right_player_info.score) % 2 == 0:
            self.do_switch_server()
            return True

        return False

    # 
    def do_cal_match_time(self):
        cur_match_time = datetime.datetime.now() - self.start_match_time

        if cur_match_time.total_seconds() > self.last_check_match_time.total_seconds():
            self.last_check_match_time = cur_match_time

            self.repaint(self.game_match_time_rect)

    # 
    def do_increase_home_score(self):
        if self.show_blink == True:
            return

        self.left_player_info.increase_score()

        if self.do_check_whether_server_is_switched() == False:
            self.repaint(self.left_score_rect)

        if self.left_player_info.score >= self.MAX_SCORE_NUM:
            if abs(self.left_player_info.score - self.right_player_info.score) <= 1:
                return

            self.left_player_info.increase_inning_score()
            self.do_inning_over()

    def do_decrease_home_score(self):
        if self.show_blink == True:
            return

        self.left_player_info.decrease_score()

        if self.do_check_whether_server_is_switched() == False:
            self.repaint(self.left_score_rect)

    def do_increase_visitor_score(self):
        if self.show_blink == True:
            return

        self.right_player_info.increase_score()

        if self.do_check_whether_server_is_switched() == False:
            self.repaint(self.right_score_rect)

        if self.right_player_info.score >= self.MAX_SCORE_NUM:
            if abs(self.left_player_info.score - self.right_player_info.score) <= 1:
                return

            self.right_player_info.increase_inning_score()
            self.do_inning_over()

    def do_decrease_visitor_score(self):
        if self.show_blink == True:
            return

        self.right_player_info.decrease_score()

        if self.do_check_whether_server_is_switched() == False:
            self.repaint(self.right_score_rect)

    def do_switch_player_side(self):
        if self.show_blink == True:
            return

        temp_info = PlayerInfo()

        temp_info.copy_from(self.left_player_info)
        self.left_player_info.copy_from(self.right_player_info)
        self.right_player_info.copy_from(temp_info)
        self.update()

    def do_switch_server(self):
        if self.show_blink == True:
            return

        if self.left_player_info.service == True:
            self.left_player_info.set_service(False)
            self.right_player_info.set_service(True)
        else:
            self.left_player_info.set_service(True)
            self.right_player_info.set_service(False)

        self.update()

    def do_reset_scores(self):
        if self.show_blink == True:
            return

        self.start_match_time = datetime.datetime.now()
        self.last_check_match_time = datetime.datetime.now() - self.start_match_time

        self.left_player_info.reset()
        self.right_player_info.reset()

        self.left_player_info.set_name("home")
        self.right_player_info.set_name("visitor")

        self.left_player_info.set_service(True)
        self.update()

    def end_app(self):
        self.do_stop_input_devices()

        self.input_device_event_check_timer.stop()

        self.close()

    # Implement InputDeviceEventListener interface
    def on_device_new_event(self, new_event : InputDeviceEvent):
        self.input_device_event_list_mutex.acquire(True)
        self.input_device_event_list.append(new_event)
        self.input_device_event_list_mutex.release()

    # QT Events
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_scoreboard(qp)

        if self.enable_drawing_match_time:
            self.draw_game_time(qp)

        self.draw_score(qp)
        qp.end()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.end_app()
            return

        # Increase a left player score: '1'
        if e.key() == Qt.Key_1:
            self.on_device_new_event(InputDeviceEvent.INCREASE_HOME_SCORE)
        # Decrease a left player score: '2'
        elif e.key() == Qt.Key_2:
            self.on_device_new_event(InputDeviceEvent.DECREASE_HOME_SCORE)
        # Increase a right player score: '3'
        elif e.key() == Qt.Key_3:
            self.on_device_new_event(InputDeviceEvent.INCREASE_VISITOR_SCORE)
        # Decrease a right player score: '4'
        elif e.key() == Qt.Key_4: 
            self.on_device_new_event(InputDeviceEvent.DECREASE_VISITOR_SCORE)
        # Switch a display score position for a players
        elif e.key() == Qt.Key_5:
            self.on_device_new_event(InputDeviceEvent.SWITCH_PLAYER_SIDE)
        # Switch a server
        elif e.key() == Qt.Key_9:
            self.on_device_new_event(InputDeviceEvent.SWITCH_SERVER)
        # Reset scores
        elif e.key() == Qt.Key_0:
            self.on_device_new_event(InputDeviceEvent.RESET_SCORE)


def start_game(argv):
    app = QApplication(argv)
    ping_pong_board = PingPongScoreBoardApp()

    app.exec_()

    # sys.exit(0)
