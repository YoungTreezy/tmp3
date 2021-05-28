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
        self.db.setUserName('postgres')
        self.db.setPassword('12345')
        self.db.setHostName('localhost')
        self.db.open()

        # запуск таймера
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_tick)

        self.model = QtSql.QSqlTableModel(db=self.db)

        # обработка сигналов
        self.ui.open_table.clicked.connect(self.open_table)
        self.ui.start_scraping.clicked.connect(self.start_parse)
        self.ui.stop_scraping.clicked.connect(self.stop_parse)

        # настойки элементов
        self.ui.stop_scraping.setVisible(False)

    # обработка кнопки которая открывает таблицу
    def open_table(self):
        global table_form
        # открывает новое окно
        table_form = QtWidgets.QDialog()
        self.form.setupUi(table_form)
        table_form.show()
        # если бд не открылась, то выдает "ошибку"
        if not self.db.open():
            self.form.textBrowser.append("Таблица не была открыта.")
        else: self.form.textBrowser.append("Таблица открыта.")
        # передает таблицу scraping в форму tableView
        self.model.setTable("scraping")
        self.model.select()
        self.form.tableView.setModel(self.model)

    def timer_tick(self):
        # берется url из строки и вставляется в ф-цию
        url = self.ui.lineEdit.text()
        parser_list = hh_parser(url)
        # форма добавления данных в бд
        query = QtSql.QSqlQuery(self.db)
        isOk = query.prepare('insert into scraping(title, url, description, company)'
                             'values(:title, :url, :description, :company)')
        # бинд данных
        for parser_dict in parser_list:
            for keys, values in parser_dict.items():
                if keys == 'title':
                    query.bindValue(':title', values)
                    self.form.textBrowser.append(f'Был добавлен title: {values}')
                elif keys == 'url':
                    query.bindValue(':url', values)
                    self.form.textBrowser.append(f'Был добавлен url: {values}')
                elif keys == 'description':
                    query.bindValue(':description', values)
                    self.form.textBrowser.append(f'Был добавлен description: {values}')
                else:
                    query.bindValue(':company', values)
                    self.form.textBrowser.append(f'Был добавлен company: {values}')
                self.form.textBrowser.append('')
            self.form.textBrowser.append('-----------------------------------------------------------------'
                                         '-----------------------------------------------------------------')
            self.form.textBrowser.append('')
            # добавление данных
            isOk = query.exec_()
            self.model.select()

    # обработчик кнопки которая парсит сайт по заданной ссылке
    def start_parse(self):
        # запускает таймер
        time_scraping = self.ui.time_scraping.text()
        self.timer.start(int(time_scraping) * 6000)
        # делает видимой кнопку "остановить скрапинг"
        self.ui.stop_scraping.setVisible(True)
        # делает невидимой некнопку "включить скрапинг"
        self.ui.start_scraping.setVisible(False)

    def stop_parse(self):
        # выключает таймер
        self.timer.stop()
        # делает невидимой кнопку "остановить скрапинг"
        self.ui.stop_scraping.setVisible(False)
        # делает видимой некнопку "включить скрапинг"
        self.ui.start_scraping.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Gui()
    myapp.show()
    sys.exit(app.exec_())


