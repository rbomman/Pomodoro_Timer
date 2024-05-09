from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QLineEdit
from PyQt5.QtCore import QTimer, QTime
from plyer import notification

class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pomodoro Timer')
        self.setGeometry(100, 100, 400, 300)
        
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Task")
        self.tabs.addTab(self.tab2, "Short Break")
        self.tabs.addTab(self.tab3, "Long Break")
        
        self.setupTab(self.tab1, "25:00", "Start Timer")
        self.setupTab(self.tab2, "05:00", "Start Timer")
        self.setupTab(self.tab3, "15:00", "Start Timer")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)

        self.current_tab = 0
        self.running = False

    def setupTab(self, tab, initial_time, button_label):
        tab.layout = QVBoxLayout()
        tab.timer_input = QLineEdit(initial_time)
        tab.timer_display = QLabel(initial_time)
        tab.start_button = QPushButton(button_label)
        tab.layout.addWidget(tab.timer_input)
        tab.layout.addWidget(tab.timer_display)
        tab.layout.addWidget(tab.start_button)
        tab.setLayout(tab.layout)
        tab.start_button.clicked.connect(lambda: self.toggle_timer())
        tab.timer_input.textChanged.connect(lambda: self.update_initial_time())

    def update_initial_time(self):
        if not self.running:
            time_text = self.tabs.currentWidget().timer_input.text()
            self.tabs.currentWidget().timer_display.setText(time_text)

    def toggle_timer(self):
        current_button = self.tabs.currentWidget().start_button
        if current_button.text() == "Start Timer":
            time_text = self.tabs.currentWidget().timer_input.text()
            minutes, seconds = map(int, time_text.split(":"))
            self.start_timer(minutes, seconds)
            current_button.setText("Stop Timer")
            self.running = True
            self.disable_tab_switching()
        else:
            self.stop_timer()
            current_button.setText("Start Timer")
            self.running = False
            self.enable_tab_switching()

    def start_timer(self, minutes, seconds):
        self.time_left = QTime(0, minutes, seconds)
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_display(self):
        self.time_left = self.time_left.addSecs(-1)
        current_display = self.tabs.currentWidget().timer_display
        current_display.setText(self.time_left.toString("mm:ss"))
        if self.time_left.toString("mm:ss") == "00:00":
            self.timer.stop()
            notification.notify(
                title='Pomodoro Timer',
                message='Time is up! Please start the next session manually.',
                app_name='Pomodoro Timer'
            )
            self.reset_current_tab()
            if self.current_tab == 0:  # Task finished, switch to Short Break
                self.current_tab = 1
                next_tab_index = 1
            elif self.current_tab == 1:  # Short Break finished, switch back to Task
                self.current_tab = 0
                next_tab_index = 0
            elif self.current_tab == 2:  # Long Break finished, switch back to Task
                self.current_tab = 0
                next_tab_index = 0
            self.tabs.setCurrentIndex(next_tab_index)

    def reset_current_tab(self):
        initial_time = self.tabs.currentWidget().timer_input.text()
        self.tabs.currentWidget().timer_display.setText(initial_time)
        self.tabs.currentWidget().start_button.setText("Start Timer")
        self.running = False
        self.enable_tab_switching()

    def disable_tab_switching(self):
        for i in range(self.tabs.count()):
            if i != self.tabs.currentIndex():
                self.tabs.setTabEnabled(i, False)

    def enable_tab_switching(self):
        for i in range(self.tabs.count()):
            self.tabs.setTabEnabled(i, True)

    
app = QApplication([])
pomodoro = PomodoroTimer()
pomodoro.show()
app.exec_()

