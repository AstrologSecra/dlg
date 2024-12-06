import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QSplitter, QTreeWidget, QTreeWidgetItem

class UtilityInstallerApp(QMainWindow):
    def __init__(self, categories):
        super().__init__()
        self.setWindowTitle("DLG Soft collection ")
        
        # Устанавливаем геометрию окна:
        # 100 - координата X верхнего левого угла окна относительно левого края экрана
        # 100 - координата Y верхнего левого угла окна относительно верхнего края экрана
        # 800 - ширина окна в пикселях
        # 600 - высота окна в пикселях
        self.setGeometry(100, 100, 500, 300)

        self.categories = categories
        self.buttons = []  # Список для хранения всех кнопок

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by utility name")
        self.search_bar.textChanged.connect(self.filter_utilities)
        search_layout.addStretch()
        search_layout.addWidget(self.search_bar)
        main_layout.addLayout(search_layout)

        # Создаем QSplitter для разделения окна на две части
        splitter = QSplitter()

        # Левая часть: дерево утилит
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Utilities"])
        self.populate_tree_widget()
        splitter.addWidget(self.tree_widget)

        # Правая часть: вывод команды
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        splitter.addWidget(self.output_text)

        main_layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def populate_tree_widget(self):
        for category, commands in self.categories.items():
            category_item = QTreeWidgetItem(self.tree_widget, [category])
            for label, command in commands.items():
                utility_item = QTreeWidgetItem(category_item, [label])
                self.buttons.append((utility_item, command))

        self.tree_widget.itemClicked.connect(self.show_command)

    def show_command(self, item, column):
        for tree_item, command in self.buttons:
            if tree_item == item:
                self.output_text.setPlainText(command)
                break

    def filter_utilities(self, text):
        for item, command in self.buttons:
            if text.lower() in item.text(0).lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

if __name__ == "__main__":
    # Структура данных для хранения категорий и команд
    categories = {
        "Python3 base": {
            "Git": "sudo apt install git -y",
            "Python3": "sudo apt install python3 -y",
            "Python3-pip": "sudo apt install python3-pip -y"
        },
        "Web": {
            "npm": "sudo apt install npm -y",
            "TypeScript": "sudo npm install -g typescript",
            "Apache2": "sudo apt install apache2",
            "Node.js": "sudo apt install nodejs -y"
        },
        "IDE": {
            "vim": "sudo apt install vim -y",
            "Emacs": "sudo apt install emacs -y",
            "Nano": "sudo apt install nano -y",
            "Geany": "sudo apt install geany -y",
            "Jed": "sudo apt install jed -y"
        },
        "C-like languages": {
            "GCC": "sudo apt install gcc -y",
            "G++": "sudo apt install g++ -y",
            "Clang": "sudo apt install clang -y",
            "Make": "sudo apt install make -y",
            "C#": "sudo apt install mono-complete -y"
        }
    }

    # Сортировка категорий и команд
    sorted_categories = dict(sorted(categories.items()))
    for category in sorted_categories:
        sorted_categories[category] = dict(sorted(sorted_categories[category].items()))

    app = QApplication(sys.argv)
    window = UtilityInstallerApp(sorted_categories)
    window.show()
    sys.exit(app.exec_())
