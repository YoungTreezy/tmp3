import sys
from scraping import *

from PyQt5 import QtSql

from uis.search_info import *
from uis.table import Ui_Form


class Gui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.form = Ui_Form()

        # открываю бд
        self.db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        self.db.setDatabaseName('postgres')
        self.db.setUserName('vlad')
        self.db.setPassword('12345')
        self.db.setHostName('localhost')

        self.model = QtSql.QSqlTableModel(db=self.db)

        self.ui.open_table.clicked.connect(self.open_table)
        self.ui.scraping.clicked.connect(self.parser)

    # обработка кнопки которая открывает таблицу
    def open_table(self):
        global table_form
        table_form = QtWidgets.QDialog()
        self.form.setupUi(table_form)
        table_form.show()
        if not self.db.open():
            self.form.plainTextEdit.setPlainText("Таблица не была открыта.\n")
        else: self.form.plainTextEdit.setPlainText("Таблица открыта.\n")
        self.db.open()
        self.model.setTable("scraping")
        self.model.select()
        self.form.tableView.setModel(self.model)

    # обработчик кнопки которая парсит сайт по заданной ссылке
    def parser(self):
        url = self.ui.lineEdit.text()
        query = QtSql.QSqlQuery(self.db)
        parser_list = hh_parser(url)
        # форма добавления данных в бд
        isOk = query.prepare('insert into scraping(title, description, url, company)'
                             'values(:title, :url, :description, :company)')
        if not isOk:
            print('соси ирод поганый')
        # бинд данных
        for parser_dict in parser_list:
            for keys, values in parser_dict.items():
                if keys == 'title':
                    query.bindValue(':title', values)
                elif keys == 'url':
                    query.bindValue(':url', values)
                elif keys == 'description':
                    query.bindValue(':description', values)
                else:
                    query.bindValue(':company', values)
            isOk = query.exec_()
            self.model.select()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Gui()
    myapp.show()
    sys.exit(app.exec_())


