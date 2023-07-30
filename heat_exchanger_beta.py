from PyQt6 import QtGui
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog, QMainWindow, QApplication
from interface2 import Ui_MainWindow
import sys
import pandas as pd
import math, json, ast

"""
Created by: Nassim LABSI
GitHub: https://github.com/Nassim-L

Correlation and Calculation Process:
Professor Nabila Labsi

Tested by:
Taibi Sid Ali

"""

""""Part1: equations and correlations"""

# DTML log mean temperature difference
DTML = lambda T1, T2, t1, t2: ((T1 - t2) - (T2 - t1)) / math.log((T1 - t2) / (T2 - t1))

# q
qcedi = lambda W1, Cp1, T1, T2: W1 * Cp1 * (T1 - T2)
qsensible = lambda W2, Cp2_i, Cp2_o, t1, t2: W2 * (t2 * Cp2_o - t1 * Cp2_i)
qvapeur = lambda qc, qs: (qc - qs)

# sizing
surface_echange = lambda nbr_t, d0, l: nbr_t * d0 * l * math.pi
# heat transfer coefficient h
hv = lambda Pc, P, q, S: 0.104 * Pc ** 0.69 * (q / S) ** 0.7 * (
        1.8 * (P / Pc) ** 0.17 + 4 * (P / Pc) ** 1.2 + 10 * (P / Pc) ** 10)
hs = lambda tw, t2: (4.8762 * (math.log10(tw - t2)) ** 3 - 8.3812 * (math.log10(tw - t2)) ** 2 + 26.18 * (
    math.log10(tw - t2)) + 12.377) * 5.6783
h0 = lambda qc, qv, hv, qs, hs: qc / ((qv / hv) + (qs / hs))
# wall temperatures
tw = lambda qv, hv, S, t2: (qv / (hv * S)) + t2
#################################################################tube###################################################
mct = lambda W1, act: W1 / act
Renolds = lambda act, do, e, u: (act * (do - 2 * e) / u)
Prendt = lambda Cp, K, u: Cp * u / K
jh = lambda Re: 0.027 * Re ** 0.8
hi = lambda K, Pr, jh, d0, e: (K / (d0 - 2 * e)) * Pr ** (1 / 3) * jh
hio = lambda hi, d0, e: hi * (d0 - 2 * e) / d0
###########################################################Rd###########################################################
#DTML Correction
def facteurC(T1, T2, t1, t2, n):
    R = (t1 - t2) / (T2 - T1)
    P = (T2 - T1) / (t1 - T1)
    S = ((R ** 2 + 1) ** 0.5) / (R - 1)
    W = ((1 - R * P) / (1 - P)) ** (1 / n)
    F = S * math.log(W) / math.log((1 + W - S + W * S) / (1 + S + W - W * S))
    return F
########################################################################################################################
#Globale heat coefficient
Us = lambda qc, nbr_tube, d0, l, dtml, f: qc / ((nbr_tube * math.pi * d0 * l) * dtml * f)
Up = lambda ho, hio: (hio * ho) / (ho + hio)
########################################################################################################################
########################################################################################################################

""""Part2: Graphical user interface"""
class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        # self.ui = Ui_Form()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.jpg'))
        self.mode_set = 0

        """ tab1: Simple calculator"""
        self.input1 = self.ui.lineEdit_1
        self.input2 = self.ui.lineEdit_2
        self.input3 = self.ui.lineEdit_3
        self.input4 = self.ui.lineEdit_4
        self.input5 = self.ui.lineEdit_5
        self.input6 = self.ui.lineEdit_6
        self.input7 = self.ui.lineEdit_7
        self.input8 = self.ui.lineEdit_8
        self.input9 = self.ui.lineEdit_9
        self.input10 = self.ui.lineEdit_10
        self.input11 = self.ui.lineEdit_11
        self.input12 = self.ui.lineEdit_12
        self.input13 = self.ui.lineEdit_13
        self.input16 = self.ui.lineEdit_16
        self.input17 = self.ui.lineEdit_17
        self.input18 = self.ui.lineEdit_18
        self.input19 = self.ui.lineEdit_19
        self.input20 = self.ui.lineEdit_20
        self.input21 = self.ui.lineEdit_21
        self.input22 = self.ui.lineEdit_22
        self.input23 = self.ui.lineEdit_23
        self.input24 = self.ui.lineEdit_result
        self.line_edits = [self.input1,
                           self.input2,
                           self.input3,
                           self.input4,
                           self.input5,
                           self.input6,
                           self.input7,
                           self.input8,
                           self.input9,
                           self.input10,
                           self.input11,
                           self.input12,
                           self.input13,
                           self.input16,
                           self.input17,
                           self.input18,
                           self.input19,
                           self.input20,
                           self.input21,
                           self.input22,
                           self.input23,
                           ]
        self.button1 = self.ui.pushButton
        self.button1.setEnabled(False)
        self.button1.clicked.connect(self.simple)

        for el in self.line_edits:
            el.textChanged.connect(self.line_edit_check)

        ################################################################################################################
        """ Tab2: Advanced Calculator """

        self.default_header = ['DATE', 'T1', 'T2', 'Q1', 'Cp1', 'Ro1', 'μ1', 'k1', 't1', 't2', 'Q2', 'Cp1_in',
                               'Cp2_out',
                               'Ro2']
        self.button2 = self.ui.pushButton_2
        self.button2.clicked.connect(self.clicked)
        self.table1 = self.ui.tableWidget
        self.table2 = self.ui.tableWidget_2
        # hot fluid
        self.cb1 = self.ui.comboBox_1
        self.cb2 = self.ui.comboBox_2
        self.cb3 = self.ui.comboBox_3
        self.cb4 = self.ui.comboBox_4
        self.cb5 = self.ui.comboBox_5
        self.cb6 = self.ui.comboBox_6
        self.cb7 = self.ui.comboBox_7
        self.cb8 = self.ui.comboBox_8
        self.cb9 = self.ui.comboBox_9
        self.cb10 = self.ui.comboBox_10
        self.cb11 = self.ui.comboBox_11
        self.cb12 = self.ui.comboBox_12
        self.cb13 = self.ui.comboBox_13
        self.cb14 = self.ui.comboBox_14
        self.cb_m3 = self.ui.comboBox_m_3
        self.cb_m4 = self.ui.comboBox_m_4
        self.cb_m5 = self.ui.comboBox_m_5
        self.cb_m6 = self.ui.comboBox_m_6
        self.cb_m7 = self.ui.comboBox_m_7
        self.cb_m8 = self.ui.comboBox_m_8
        ###################################
        self.hot_fuid_set = [
            self.cb1,
            self.cb2,
            self.cb3,
            self.cb4,
            self.cb5,
            self.cb6,
            self.cb7,
            self.cb8,
            self.cb9,
            self.cb10,
            self.cb11,
            self.cb12,
            self.cb13,
            self.cb14,
            self.cb_m3,
            self.cb_m4,
            self.cb_m5,
            self.cb_m6,
            self.cb_m7,
            self.cb_m8,
        ]
        self.button3 = self.ui.pushButton_3
        self.button3.clicked.connect(self.start)
        self.button4 = self.ui.pushButton_4
        self.button4.setEnabled(False)
        self.button4.clicked.connect(self.save)
        """ Graphical tab"""
        self.button5 = self.ui.pushButton_5
        self.button5.setEnabled(False)
        self.button5.clicked.connect(self.trace_un_graph2)
        self.button6 = self.ui.pushButton_6
        self.button6.clicked.connect(self.trace_un_graph)
        """ Chose mode Tab"""
        self.mode1 = self.ui.radioButton_1
        self.mode2 = self.ui.radioButton_2
        self.mode1.toggled.connect(self.mode_function1)
        self.mode2.toggled.connect(self.mode_function2)
        self.tabwdiget_4 = self.ui.tabWidget_4
        self.tabwdiget_4.setTabEnabled(1, False)
        self.tabwdiget_4.setTabEnabled(2, False)
        self.cb_mode_1 = self.ui.comboBox_m_1
        self.cb_mode_2 = self.ui.comboBox_m_2

        with open("equations1.json", "r") as json_file:
            self.equations1 = json.load(json_file)

        with open("equations2.json", "r") as json_file:
            self.equations2 = json.load(json_file)

        x_list = [x for x in self.equations1]
        y_list = [y for y in self.equations2]
        self.cb_mode_1.addItems(x_list)
        self.cb_mode_2.addItems(y_list)

    """"Part3: Functions"""
    # Draw a scatter plot from a file
    def trace_un_graph(self):
        filen, _ = QFileDialog.getOpenFileName(self, "choisis un fichier", "", "Excel file (*.xlsx);;Csv file (*.csv)")
        if filen:
            if _ == "Excel file (*.xlsx)":
                df1 = pd.read_excel(filen)
                print(df1)
                x = df1["DATE"]
                y = df1['Rd']
                self.ui.MplWidget.plotG(x, y)
            elif _ == "Csv file (*.csv)":
                df1 = pd.read_csv(filen)
                print(df1)
                x = df1["DATE"]
                y = df1['Rd']
                self.ui.MplWidget.plotG(x, y)

    # Draw a scatter plot from last data
    def trace_un_graph2(self):
        df1 = self.all_date
        print(df1)
        x = df1["DATE"]
        y = df1['Rd']
        self.ui.MplWidget.plotG(x, y)


    # check all fields is they are not empty
    def line_edit_check(self, ):
        all_valide = True
        for line_edit in self.line_edits:
            text = line_edit.text()
            try:
                float(text)
            except:
                all_valide = False
        self.button1.setEnabled(all_valide)


    # Function that loads a file and prints it on the widgetable
    def clicked(self):
        print("working")
        fname, _ = QFileDialog.getOpenFileName(self, "chose a a data file", "",
                                               "all file (*);;Python file(*.py);;Excel file (*.xslx);;Csv file (*.csv)")
        if fname:
            print(fname)
            self.all_date = pd.read_excel(fname)
            print(self.all_date.columns)
            self.table1.setRowCount(len(self.all_date.index))
            self.table1.setColumnCount(len(self.all_date.columns))
            self.table1.setHorizontalHeaderLabels(self.all_date.columns)
            for i in range(len(self.all_date.index)):
                for j in range(len(self.all_date.columns)):
                    self.table1.setItem(i, j, QTableWidgetItem(str(self.all_date.iat[i, j])))
            print(all(element in self.default_header for element in self.all_date.columns))
            for cb in self.hot_fuid_set:
                cb.addItems(self.all_date.columns)
########################################################################################################################
    """ tested , 100% working without any bug """
    # General Calculation Function for part 1
    def simple(self):
        T1 = float(self.input1.text())
        T2 = float(self.input2.text())
        t1 = float(self.input8.text())
        t2 = float(self.input9.text())
        t_moy = (t1 + t2) / 2

        # Debit des 2 fluide:
        Q1 = float(self.input3.text())
        Q2 = float(self.input10.text())

        # la masse volumique:
        Ro1 = float(self.input4.text())
        Ro2 = float(self.input11.text())

        # Cp
        Cp1 = float(self.input5.text())
        Cp2_i = float(self.input12.text())
        Cp2_o = float(self.input13.text())

        # u
        u1 = float(self.input6.text())

        # k
        k1 = float(self.input7.text())

        # sizing
        epaisseur_de_tube = float(self.input23.text())
        pression = float(self.input16.text())
        pression_critique = float(self.input17.text())
        nombre_de_tube = float(self.input18.text())
        nombre_de_passe_f = float(self.input19.text())
        nombre_de_passe_c = float(self.input20.text())
        diametre_externe_de_tube = float(self.input21.text())
        longeur_de_tube = float(self.input22.text())

        S = surface_echange(nombre_de_tube, diametre_externe_de_tube, longeur_de_tube)
        act = (math.pi / 4) * (diametre_externe_de_tube - 2 * epaisseur_de_tube) ** 2 * (
                nombre_de_tube / nombre_de_passe_f)

        # DTML
        try:
            dtml = DTML(T1, T2, t1, t2)
        except:
            dtml = 0

        # q fuide 1
        W1 = (Q1 / 3600) * Ro1
        qc = qcedi(W1, Cp1, T1, T2)

        W2 = (Q2 / 3600) * Ro2
        qs = qsensible(W2, Cp2_i, Cp2_o, t1, t2)

        qv = qvapeur(qc, qs)

        # coef de tranfer:

        try:
            h_vapeur = hv(pression_critique, pression, qc, S)
        except:
            h_vapeur = 0
        # temperature de paroi
        try:
            twall = tw(qv, h_vapeur, S, t2)
        except:
            twall = 0
        try:
            h_sensible = hs(twall, t_moy)
        except:
            h_sensible = 0
        try:
            h_o = h0(qc, qv, h_vapeur, qs, h_sensible)
        except:
            h_o = 0
        print(qv, h_vapeur, twall, h_sensible, h_o)
        ######################Calandre##################################################################################
        m_ct = mct(W1, act)
        nbr_Re = Renolds(m_ct, diametre_externe_de_tube, epaisseur_de_tube, u1)
        nbr_Pr = Prendt(Cp1, k1, u1)
        nbr_jh = jh(nbr_Re)
        h_i = hi(k1, nbr_Pr, nbr_jh, diametre_externe_de_tube, epaisseur_de_tube)
        h_io = hio(h_i, diametre_externe_de_tube, epaisseur_de_tube)
        try:
            f_c = facteurC(T1, T2, t1, t2, nombre_de_passe_c)
        except:
            f_c = 0

        try:
            u_s = Us(qc, nombre_de_tube, diametre_externe_de_tube, longeur_de_tube, dtml, f_c)
        except:
            u_s = 0

        try:
            u_p = Up(h_o, h_io)
        except:
            u_p = 0

        try:
            rd = (1 / u_s) - (1 / u_p)
        except:
            rd = 0
        self.input24.setText(f"Rd ={rd} [w/m^2.C]")
########################################################################################################################
    # General Calculation Function for part 2
    def start(self):

        l_qc = []
        l_qv = []
        l_qs = []
        l_fc = []
        l_dtml = []
        l_ho = []
        l_hio = []
        l_up = []
        l_us = []
        l_rd = []

        # sizing

        nombre_de_tube = float(self.ui.lineEdit_26.text())
        nombre_de_passe_c = float(self.ui.lineEdit_28.text())
        nombre_de_passe_f = float(self.ui.lineEdit_27.text())
        longeur_de_tube = float(self.ui.lineEdit_30.text())
        diametre_externe_de_tube = float(self.ui.lineEdit_29.text())
        epesseur_de_tube = float(self.ui.lineEdit_40.text())
        pression = float(self.ui.lineEdit_24.text())
        pression_critique = float(self.ui.lineEdit_25.text())

        # nombre_de_tube = 574
        # nombre_de_passe_c = 1
        # nombre_de_passe_f = 14
        # longeur_de_tube = 4.88
        # diametre_externe_de_tube = 0.0254
        # epesseur_de_tube = 0.00277
        # pression = 37
        # pression_critique = 220.64

        # surface d'echange

        S = surface_echange(nombre_de_tube, diametre_externe_de_tube, longeur_de_tube)
        act = (math.pi / 4) * (diametre_externe_de_tube - 2 * epesseur_de_tube) ** 2 * (
                nombre_de_tube / nombre_de_passe_f)

        # Date
        date = self.cb8.currentText()

        for index, row in self.all_date.iterrows():

            # temperature:
            if self.mode_set == 1:
                T1 = float(row[self.cb1.currentText()])
                T2 = float(row[self.cb2.currentText()])
                t1 = float(row[self.cb9.currentText()])
                t2 = float(row[self.cb10.currentText()])
                t_moy = (t1 + t2) / 2
                # Debit des 2 fluide:
                Q1 = float(row[self.cb3.currentText()])
                Q2 = float(row[self.cb11.currentText()])
                # la masse volumique:
                Ro1 = float(row[self.cb4.currentText()])
                Ro2 = float(row[self.cb12.currentText()])
                # Cp
                Cp1 = float(row[self.cb5.currentText()])
                Cp2_i = float(row[self.cb13.currentText()])
                Cp2_o = float(row[self.cb14.currentText()])
                # u
                u1 = float(row[self.cb6.currentText()])
                # k
                k1 = float(row[self.cb7.currentText()])
            elif self.mode_set == 2:

                ##-----------load equation------------##
                # tube:
                self.equation_tube = self.equations1[self.cb_mode_1.currentText()]

                # calandre
                self.equation_calandre = self.equations2[self.cb_mode_2.currentText()]

                ########################################

                T1 = float(row[self.cb_m3.currentText()])
                T2 = float(row[self.cb_m4.currentText()])
                T_moy = (T1 + T2) / 2
                t1 = float(row[self.cb_m6.currentText()])
                t2 = float(row[self.cb_m7.currentText()])
                t_moy = (t1 + t2) / 2

                # Debit des 2 fluide:
                Q1 = float(row[self.cb_m5.currentText()])
                Q2 = float(row[self.cb_m8.currentText()])

                print(T1, T2, t1, t2, Q1, Q2)

                # la masse volumique:
                Ro1 = self.safe_eval(self.equation_tube['Ro_eq'], T_moy)
                Ro2 = self.safe_eval(self.equation_calandre['Ro_eq'], t_moy)

                # Cp
                Cp1 = self.safe_eval(self.equation_tube['Cp_eq'], T_moy)
                Cp2_i = self.safe_eval(self.equation_calandre['Cp_eq'], t_moy)
                Cp2_o = self.safe_eval(self.equation_calandre['Cp_eq'], t_moy)

                # u
                u1 = self.safe_eval(self.equation_tube['u_eq'], T_moy)

                # k
                k1 = self.safe_eval(self.equation_tube['k_eq'], T_moy)

            ###########################################################################################################
            # DTML
            try:
                dtml = DTML(T1, T2, t1, t2)
            except:
                dtml = 0

            l_dtml.append(dtml)

            # q fuide 1
            W1 = (Q1 / 3600) * Ro1
            qc = qcedi(W1, Cp1, T1, T2)
            l_qc.append(qc)
            W2 = (Q2 / 3600) * Ro2
            qs = qsensible(W2, Cp2_i, Cp2_o, t1, t2)
            l_qs.append(qs)
            qv = qvapeur(qc, qs)
            l_qv.append(qv)

            # coef de tranfert:

            try:
                h_vapeur = hv(pression_critique, pression, qc, S)
            except:
                h_vapeur = 0

            # temperature de paroi

            try:
                twall = tw(qv, h_vapeur, S, t2)
            except:
                twall = 0

            try:
                h_sensible = hs(twall, t_moy)
            except:
                h_sensible = 0

            try:
                h_o = h0(qc, qv, h_vapeur, qs, h_sensible)
            except:
                h_o = 0
            l_ho.append(h_o)

            print(qv, h_vapeur, twall, h_sensible, h_o)
            ######################Calandre##############################################################################
            ############################################################################################################
            m_ct = mct(W1, act)
            nbr_Re = Renolds(m_ct, diametre_externe_de_tube, epesseur_de_tube, u1)
            nbr_Pr = Prendt(Cp1, k1, u1)
            nbr_jh = jh(nbr_Re)
            h_i = hi(k1, nbr_Pr, nbr_jh, diametre_externe_de_tube, epesseur_de_tube)
            h_io = hio(h_i, diametre_externe_de_tube, epesseur_de_tube)
            l_hio.append(h_io)
            try:
                f_c = facteurC(T1, T2, t1, t2, nombre_de_passe_c)
            except:
                f_c = 0

            l_fc.append(f_c)
            try:
                u_s = Us(qc, nombre_de_tube, diametre_externe_de_tube, longeur_de_tube, dtml, f_c)
            except:
                u_s = 0

            l_us.append(u_s)
            try:
                u_p = Up(h_o, h_io)
            except:
                u_p = 0
            l_up.append(u_p)
            try:
                rd = (1 / u_s) - (1 / u_p)
            except:
                rd = 0
            l_rd.append(rd)

            print(m_ct, nbr_Re, nbr_Pr, nbr_jh, h_i, h_io, f_c, u_s, u_p, rd)

        self.all_date['Fc'] = l_fc
        self.all_date['DTML'] = l_dtml
        self.all_date['Hio'] = l_hio
        self.all_date['Ho'] = l_ho
        self.all_date['Us'] = l_us
        self.all_date['Up'] = l_up
        self.all_date['Rd'] = l_rd

        self.all_date.to_excel('text.xlsx')
        self.button3.setDisabled(False)

        data_for_table2 = self.all_date[[date, "Rd"]]
        self.table2.setRowCount(len(data_for_table2.index))
        self.table2.setColumnCount(len(data_for_table2.columns))
        self.table2.setHorizontalHeaderLabels(data_for_table2.columns)

        for i in range(len(data_for_table2.index)):
            for j in range(len(data_for_table2.columns)):
                self.table2.setItem(i, j, QTableWidgetItem(str(data_for_table2.iat[i, j])))

        self.button4.setEnabled(True)
        self.button5.setEnabled(True)

    # save result
    def save(self):
        filep, _ = QFileDialog().getSaveFileName(None, "sauvegarder le fichier", "",
                                                 "Fichier Excel (*.xlsx);;Fichier Csv (*.csv)")
        if _ == "Fichier Excel (*.xlsx)":
            self.all_date.to_excel(filep)

        if _ == "Fichier Csv (*.csv)":
            self.all_date.to_csv(filep)

    ####################################################################################################################
    #Mode configuration
    def mode_function1(self):
        self.mode_set = 1
        self.tabwdiget_4.setTabEnabled(2, False)
        self.tabwdiget_4.setTabEnabled(1, True)
        print("working1")
        print(self.mode_set)

    def mode_function2(self):
        self.mode_set = 2
        self.tabwdiget_4.setTabEnabled(1, False)
        self.tabwdiget_4.setTabEnabled(2, True)
        print("working2")
        print(self.mode_set)
    ####################################################################################################################
    # load equation from json file
    def safe_eval(self, expression, x_value):
        try:
            environment = {'math': math, 'x': x_value}
            parsed_expression = ast.parse(expression, mode='eval')
            evaluated_expression = ast.fix_missing_locations(parsed_expression)
            compiled_expression = compile(evaluated_expression, '<string>', mode='eval')
            result = eval(compiled_expression, environment)
            return result
        except (SyntaxError, NameError):
            return "error 0"


app = QApplication(sys.argv)

ui = window()
ui.show()
app.exec()
