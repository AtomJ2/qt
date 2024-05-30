import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, \
    QMessageBox, QFileDialog, QDialog, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import keyboard


class DataInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input data for graph")
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-size: 14px;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: #333333;
                font-size: 16px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton#openFileButton {
                background-color: #28a745;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.x_label = QLabel("Enter data for the X axis (separated by comma):")
        layout.addWidget(self.x_label)

        self.x_edit = QLineEdit()
        layout.addWidget(self.x_edit)

        self.y_label = QLabel("Enter data for the Y axis (separated by comma):")
        layout.addWidget(self.y_label)

        self.y_edit = QLineEdit()
        layout.addWidget(self.y_edit)

        self.plot_button = QPushButton("Plot graph")
        self.plot_button.clicked.connect(self.accept)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def get_data(self):
        return self.x_edit.text(), self.y_edit.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MyApp")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #73008e;
                font-family: Arial, sans-serif;
            }
            QMenuBar {
                background-color: #cf00ff;
                color: white;
                font-size: 16px;
            }
            QMenuBar::item {
                background-color: #cf00ff;
                color: white;
            }
            QMenuBar::item::selected {
                background-color: #73008e;
            }
            QMenu {
                background-color: #cf00ff;
                color: white;
            }
            QMenu::item::selected {
                background-color: #73008e;
            }
        """)

        self.create_menu()
        self.show_message()

    def set_view(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

    def show_message(self):
        welcome_label = QLabel("WELCOME!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 40px; color: #ffffff; padding: 20px;")
        self.setCentralWidget(welcome_label)

    def create_menu(self):
        main_menu = self.menuBar()

        file_menu = main_menu.addMenu("File")
        graph_menu = main_menu.addMenu("Early-prepared graphs")
        custom_graph_menu = main_menu.addMenu("Plot graph")
        additional_menu = main_menu.addMenu("Additionally")

        plot_linear_action = QAction("Linear graph", self)
        plot_linear_action.triggered.connect(self.plot_linear_graph)
        graph_menu.addAction(plot_linear_action)

        plot_sin_action = QAction("Sinus graph", self)
        plot_sin_action.triggered.connect(self.plot_sin_graph)
        graph_menu.addAction(plot_sin_action)

        plot_cos_action = QAction("Cosine graph", self)
        plot_cos_action.triggered.connect(self.plot_cos_graph)
        graph_menu.addAction(plot_cos_action)

        plot_quad_action = QAction("Squared graph", self)
        plot_quad_action.triggered.connect(self.plot_quadratic_graph)
        graph_menu.addAction(plot_quad_action)

        plot_exp_action = QAction("Exp graph", self)
        plot_exp_action.triggered.connect(self.plot_exponential_graph)
        graph_menu.addAction(plot_exp_action)

        plot_log_action = QAction("Log graph", self)
        plot_log_action.triggered.connect(self.plot_logarithmic_graph)
        graph_menu.addAction(plot_log_action)

        plot_scatter_action = QAction("Dotty graph", self)
        plot_scatter_action.triggered.connect(self.plot_scatter_graph)
        graph_menu.addAction(plot_scatter_action)

        save_action = QAction(QIcon("save.png"), "Save graph", self)
        save_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_action)

        export_data_action = QAction("Export data to CSV", self)
        export_data_action.triggered.connect(self.export_data_to_csv)
        file_menu.addAction(export_data_action)

        load_image_action = QAction("Open graph", self)
        load_image_action.triggered.connect(self.load_image)
        file_menu.addAction(load_image_action)

        custom_plot_action = QAction("Custom", self)
        custom_plot_action.triggered.connect(self.show_custom_plot_dialog)
        custom_graph_menu.addAction(custom_plot_action)

        random_plot_action = QAction("Random graph", self)
        random_plot_action.triggered.connect(self.plot_random_graph)
        additional_menu.addAction(random_plot_action)

        reset_view_action = QAction("Reset view", self)
        reset_view_action.triggered.connect(self.show_message)
        additional_menu.addAction(reset_view_action)

    def show_custom_plot_dialog(self):
        dialog = DataInputDialog(self)
        if dialog.exec_():
            x_data, y_data = dialog.get_data()
            self.plot_custom_graph(x_data, y_data)

    def plot_custom_graph(self, x_data, y_data):
        self.set_view()
        try:
            x_list = [float(x) for x in x_data.split(",")]
            y_list = [float(y) for y in y_data.split(",")]
            if len(x_list) != len(y_list):
                QMessageBox.warning(self, "Error", "The lengths of the data lists for X and Y must be the same.")
                return
            self.plot_graph(x_list, y_list, "Your graph", color='m')
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter numeric data separated by commas.")

    def plot_linear_graph(self):
        self.set_view()
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        self.plot_graph(x, y, "Linear graph", color='m')

    def plot_sin_graph(self):
        self.set_view()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y = np.sin(x)
        self.plot_graph(x, y, "Sinus graph", color='m')

    def plot_cos_graph(self):
        self.set_view()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y = np.cos(x)
        self.plot_graph(x, y, "Cosine graph", color='m')

    def plot_quadratic_graph(self):
        self.set_view()
        x = np.linspace(-10, 10, 100)
        y = x ** 2
        self.plot_graph(x, y, "Squared graph", color='m')

    def plot_exponential_graph(self):
        self.set_view()
        x = np.linspace(0, 10, 100)
        y = np.exp(x)
        self.plot_graph(x, y, "Exp graph", color='m')

    def plot_logarithmic_graph(self):
        self.set_view()
        x = np.linspace(0.1, 10, 100)
        y = np.log(x)
        self.plot_graph(x, y, "Log graph", color='m')

    def plot_scatter_graph(self):
        self.set_view()
        x = np.random.rand(100)
        y = np.random.rand(100)
        self.plot_scatter(x, y, "Dotty graph", color='m')

    def plot_random_graph(self):
        self.set_view()
        x = np.linspace(0, 10, 100)
        y = np.random.rand(100)
        self.plot_graph(x, y, "Random graph", color='m')

    def plot_graph(self, x, y, title, color='m'):
        self.set_view()
        self.scene.clear()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, color=color)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        canvas.draw()

        self.scene.addWidget(canvas)

    def plot_scatter(self, x, y, title, color='m'):
        self.set_view()
        self.scene.clear()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(x, y, color=color)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        canvas.draw()

        self.scene.addWidget(canvas)

    def save_graph(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save graph", "",
                                                   "PNG files (*.png);;JPEG files (*.jpg *.jpeg)")
        if file_name:
            plt.savefig(file_name)
            QMessageBox.information(self, "Success", "Graph saved successfully!")

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load graph", "", "Image files (*.png *.jpg *.jpeg)")
        if file_name:
            self.set_view()
            pixmap = QPixmap(file_name)
            label = QLabel()
            label.setPixmap(pixmap)
            self.scene.addWidget(label)
            QMessageBox.information(self, "Success", "Graph loaded successfully!")

    def export_data_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export data", "",
                                                   "CSV files (*.csv)")
        if file_name:
            x = np.linspace(0, 10, 100)
            y = np.random.rand(100)
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["X", "Y"])
                writer.writerows(zip(x, y))
            QMessageBox.information(self, "Success", "Data exported successfully to CSV file!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
