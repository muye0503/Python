#!/usr/bin/env python

from itertools import combinations
from collections import deque
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from ssq_ui.ssq_main import Ui_Form as Ui_Main
from ssq_ui.result import Ui_Form as Ui_Result


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.l_dan = deque(maxlen=2)
        self.l_tuo = deque(maxlen=5)
        self.l_lan = deque(maxlen=1)

    @staticmethod
    def l_list_add(l_list, qiu):
        item = qiu.text()
        if item in l_list:
            l_list.remove(item)
            print(l_list)
        else:
            l_list.append(item)
            print(l_list)

    def dan_display(self):
        for i in range(2):
            eval('self.ui.dan_lcd_' + str(i) + '.display(0)')
        for i in range(1, 34):
            eval('self.ui.t_' + str(i).zfill(2) + '.setEnabled(True)')
        if len(self.l_dan):
            for i in range(len(self.l_dan)):
                eval('self.ui.dan_lcd_' + str(i) + '.display(self.l_dan[i])')
                eval('self.ui.t_' + self.l_dan[i] + '.setEnabled(False)')

    def tuo_display(self):
        for i in range(5):
            eval('self.ui.tuo_lcd_' + str(i) + '.display(0)')
        for i in range(1, 34):
            eval('self.ui.d_' + str(i).zfill(2) + '.setEnabled(True)')
        if len(self.l_tuo):
            for i in range(len(self.l_tuo)):
                eval('self.ui.tuo_lcd_' + str(i) + '.display(self.l_tuo[i])')
                eval('self.ui.d_' + self.l_tuo[i] + '.setEnabled(False)')

    def lan_display(self):
        self.ui.lan_lcd.display(0)
        if len(self.l_lan):
            self.ui.lan_lcd.display(self.l_lan[0])

    @pyqtSlot()
    def on_d_01_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_01)
        self.dan_display()

    @pyqtSlot()
    def on_d_02_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_02)
        self.dan_display()

    @pyqtSlot()
    def on_d_03_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_03)
        self.dan_display()

    @pyqtSlot()
    def on_d_04_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_04)
        self.dan_display()

    @pyqtSlot()
    def on_d_05_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_05)
        self.dan_display()

    @pyqtSlot()
    def on_d_06_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_06)
        self.dan_display()

    @pyqtSlot()
    def on_d_07_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_07)
        self.dan_display()

    @pyqtSlot()
    def on_d_08_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_08)
        self.dan_display()

    @pyqtSlot()
    def on_d_09_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_09)
        self.dan_display()

    @pyqtSlot()
    def on_d_10_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_10)
        self.dan_display()

    @pyqtSlot()
    def on_d_11_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_11)
        self.dan_display()

    @pyqtSlot()
    def on_d_12_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_12)
        self.dan_display()

    @pyqtSlot()
    def on_d_13_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_13)
        self.dan_display()

    @pyqtSlot()
    def on_d_14_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_14)
        self.dan_display()

    @pyqtSlot()
    def on_d_15_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_15)
        self.dan_display()

    @pyqtSlot()
    def on_d_16_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_16)
        self.dan_display()

    @pyqtSlot()
    def on_d_17_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_17)
        self.dan_display()

    @pyqtSlot()
    def on_d_18_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_18)
        self.dan_display()

    @pyqtSlot()
    def on_d_19_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_19)
        self.dan_display()

    @pyqtSlot()
    def on_d_20_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_20)
        self.dan_display()

    @pyqtSlot()
    def on_d_21_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_21)
        self.dan_display()

    @pyqtSlot()
    def on_d_22_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_22)
        self.dan_display()

    @pyqtSlot()
    def on_d_23_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_23)
        self.dan_display()

    @pyqtSlot()
    def on_d_24_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_24)
        self.dan_display()

    @pyqtSlot()
    def on_d_25_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_25)
        self.dan_display()

    @pyqtSlot()
    def on_d_26_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_26)
        self.dan_display()

    @pyqtSlot()
    def on_d_27_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_27)
        self.dan_display()

    @pyqtSlot()
    def on_d_28_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_28)
        self.dan_display()

    @pyqtSlot()
    def on_d_29_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_29)
        self.dan_display()

    @pyqtSlot()
    def on_d_30_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_30)
        self.dan_display()

    @pyqtSlot()
    def on_d_31_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_31)
        self.dan_display()

    @pyqtSlot()
    def on_d_32_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_32)
        self.dan_display()

    @pyqtSlot()
    def on_d_33_clicked(self):
        self.l_list_add(self.l_dan, self.ui.d_33)
        self.dan_display()

    @pyqtSlot()
    def on_t_01_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_01)
        self.tuo_display()

    @pyqtSlot()
    def on_t_02_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_02)
        self.tuo_display()

    @pyqtSlot()
    def on_t_03_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_03)
        self.tuo_display()

    @pyqtSlot()
    def on_t_04_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_04)
        self.tuo_display()

    @pyqtSlot()
    def on_t_05_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_05)
        self.tuo_display()

    @pyqtSlot()
    def on_t_05_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_05)
        self.tuo_display()

    @pyqtSlot()
    def on_t_06_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_06)
        self.tuo_display()

    @pyqtSlot()
    def on_t_07_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_07)
        self.tuo_display()

    @pyqtSlot()
    def on_t_08_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_08)
        self.tuo_display()

    @pyqtSlot()
    def on_t_09_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_09)
        self.tuo_display()

    @pyqtSlot()
    def on_t_10_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_10)
        self.tuo_display()

    @pyqtSlot()
    def on_t_11_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_11)
        self.tuo_display()

    @pyqtSlot()
    def on_t_12_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_12)
        self.tuo_display()

    @pyqtSlot()
    def on_t_13_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_13)
        self.tuo_display()

    @pyqtSlot()
    def on_t_14_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_14)
        self.tuo_display()

    @pyqtSlot()
    def on_t_15_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_15)
        self.tuo_display()

    @pyqtSlot()
    def on_t_16_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_16)
        self.tuo_display()

    @pyqtSlot()
    def on_t_17_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_17)
        self.tuo_display()

    @pyqtSlot()
    def on_t_18_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_18)
        self.tuo_display()

    @pyqtSlot()
    def on_t_19_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_19)
        self.tuo_display()

    @pyqtSlot()
    def on_t_20_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_20)
        self.tuo_display()

    @pyqtSlot()
    def on_t_21_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_21)
        self.tuo_display()

    @pyqtSlot()
    def on_t_22_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_22)
        self.tuo_display()

    @pyqtSlot()
    def on_t_23_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_23)
        self.tuo_display()

    @pyqtSlot()
    def on_t_24_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_24)
        self.tuo_display()

    @pyqtSlot()
    def on_t_25_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_25)
        self.tuo_display()

    @pyqtSlot()
    def on_t_25_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_25)
        self.tuo_display()

    @pyqtSlot()
    def on_t_26_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_26)
        self.tuo_display()

    @pyqtSlot()
    def on_t_27_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_27)
        self.tuo_display()

    @pyqtSlot()
    def on_t_28_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_28)
        self.tuo_display()

    @pyqtSlot()
    def on_t_29_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_29)
        self.tuo_display()

    @pyqtSlot()
    def on_t_30_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_30)
        self.tuo_display()

    @pyqtSlot()
    def on_t_31_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_31)
        self.tuo_display()

    @pyqtSlot()
    def on_t_32_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_32)
        self.tuo_display()

    @pyqtSlot()
    def on_t_33_clicked(self):
        self.l_list_add(self.l_tuo, self.ui.t_33)
        self.tuo_display()

    @pyqtSlot()
    def on_b_1_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_1)
        self.lan_display()

    @pyqtSlot()
    def on_b_2_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_2)
        self.lan_display()

    @pyqtSlot()
    def on_b_3_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_3)
        self.lan_display()

    @pyqtSlot()
    def on_b_4_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_4)
        self.lan_display()

    @pyqtSlot()
    def on_b_5_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_5)
        self.lan_display()

    @pyqtSlot()
    def on_b_6_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_6)
        self.lan_display()

    @pyqtSlot()
    def on_b_7_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_7)
        self.lan_display()

    @pyqtSlot()
    def on_b_8_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_8)
        self.lan_display()

    @pyqtSlot()
    def on_b_9_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_9)
        self.lan_display()

    @pyqtSlot()
    def on_b_10_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_10)
        self.lan_display()

    @pyqtSlot()
    def on_b_11_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_11)
        self.lan_display()

    @pyqtSlot()
    def on_b_12_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_12)
        self.lan_display()

    @pyqtSlot()
    def on_b_13_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_13)
        self.lan_display()

    @pyqtSlot()
    def on_b_14_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_14)
        self.lan_display()

    @pyqtSlot()
    def on_b_15_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_15)
        self.lan_display()

    @pyqtSlot()
    def on_b_16_clicked(self):
        self.l_list_add(self.l_lan, self.ui.b_16)
        self.lan_display()

    def display_hongqiu(self):
        list_dan = list(self.l_dan)
        list_tuo = list(self.l_tuo)
        list_tuo.sort()
        list_result = []
        for item in combinations(list_tuo, 4):
            result = list(item)
            result.extend(list_dan)
            result.sort()
            print(result)
            list_result.extend(result)
        return list_result

    @pyqtSlot()
    def on_pushButton_clicked(self):
        dlg = QDialog()
        self.result = Ui_Result()
        self.result.setupUi(dlg)
        lan = self.l_lan[0]
        result_str = self.display_hongqiu()
        result_int = [int(x) for x in result_str]
        zhu_1 = slice(0, 6)
        zhu_2 = slice(6, 12)
        zhu_3 = slice(12, 18)
        zhu_4 = slice(18, 24)
        zhu_5 = slice(24, 30)
        str_zhu_1 = str(result_int[zhu_1]).replace('[', '')
        str_zhu_1 = str_zhu_1.replace(']', '')
        str_zhu_2 = str(result_int[zhu_2]).replace('[', '')
        str_zhu_2 = str_zhu_2.replace(']', '')
        str_zhu_3 = str(result_int[zhu_3]).replace('[', '')
        str_zhu_3 = str_zhu_3.replace(']', '')
        str_zhu_4 = str(result_int[zhu_4]).replace('[', '')
        str_zhu_4 = str_zhu_4.replace(']', '')
        str_zhu_5 = str(result_int[zhu_5]).replace('[', '')
        str_zhu_5 = str_zhu_5.replace(']', '')
        suffix = ' | ' + lan + '\n'
        result_str = str_zhu_1 + suffix + str_zhu_2 + suffix + str_zhu_3 + \
            suffix + str_zhu_4 + suffix + str_zhu_5 + suffix
        self.result.label.setText(result_str)
        self.result.label.setWordWrap(True)
        dlg.exec_()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    my_window = MainWindow()
    my_window.show()
    sys.exit(app.exec_())
