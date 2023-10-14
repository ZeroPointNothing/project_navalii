import sys
import subprocess
import traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon


# C:\Users\username\AppData\Local\Navalii Browser\QtWebEngine\Default

class MainWindow(QMainWindow):
    def __init__(self):
        sys.excepthook = self.excepthook

        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()

        self.setCentralWidget(self.browser)

        self.home = "https://zeropointnothing.github.io"
        self.version = "v0.0.1 ALPHA"

        self.browser.setUrl(QUrl(self.home))

        self.showMaximized()

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.setToolTip("Go back to the previous page.")
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        foreward_btn = QAction('Foreward', self)
        foreward_btn.setToolTip("Go foreward one page.")
        foreward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(foreward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.setToolTip("Reload the page.")
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)
        self.browser.titleChanged.connect(self.update_title)
        self.browser.page().profile().downloadRequested.connect(self.on_downloadRequested)

    def navigate_home(self):
        """
        Return to home page.
        :return:
        """
        # self.update_title("Loading...")

        self.browser.setUrl(QUrl(self.home))

    def update_title(self, title=None):
        self.browser.window().setWindowTitle(f"{title} - Navalii Web Browser")

    def update_url(self, q):
        """
        Update the url so it can display correctly in the url bar.
        :param q:
        :return:
        """
        self.url_bar.setText(q.toString())

        # self.update_title()

    def navigate_url(self):
        """
        Navigate to the url contained in the url_bar.
        :return:
        """
        url: str = self.url_bar.text()

        self.update_title("Loading...")

        if not url.startswith("https://"):
            url = "https://www.google.com/search?q=" + url

        self.browser.setUrl(QUrl(url))

        # raise AttributeError("men")
        #
        # page = self.browser.page()
        #
        # page.profile().cookieStore().deleteAllCookies()

    def on_downloadRequested(self, download):
        old_path = download.path()
        suffix = QFileInfo(old_path).suffix()
        path, _ = QFileDialog.getSaveFileName(self.browser.page().view(), "Save File", old_path, "*."+suffix)
        if path:
            download.setPath(path)
            download.accept()

    def excepthook(self, exctype, value, tb):
        """
        Hook for all exceptions so that the VoxelEngine may shut down and have the error handling be taken over.
        """

        # Don't handle CTRL+C errors.
        if exctype == KeyboardInterrupt:
            sys.exit()

        # Obtain the full exception details as a string
        full_exception = "".join(traceback.format_exception(exctype, value, tb))

        # Replace line breaks with lnbrk
        full_exception = full_exception.replace("\n", "lnbrk")

        # Hand over the error handling to error.py so the VoxelEngine can completely shut down.
        subprocess.Popen(
            ["start", "cmd", "/k", "python", "./assets/error.py", "--fullexc", full_exception, "--details",
             f"{exctype.__name__}: {value}"],
            shell=True,
        )

        sys.exit()


app = QApplication(sys.argv)
QApplication.setApplicationName("Navalii Browser")
app.setWindowIcon(QIcon("assets/navalii_icon.png"))

window = MainWindow()

print("Welcome to Navalii!")
print()
print(f"Running version {window.version}")
print("Note: This is a debug console tied to the main window. You may see many errors or warnings from Javascript.")
print("You can ignore these unless they are crash related.")
print("In future versions, this console window will be hidden.")
print()

app.exec_()
