import sys
import os.path
import resource
import PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic,QtCore, QtGui
from PyQt5.QtWidgets import *
import pandas,re
import mysql as ms
import DataBase_Mysql_Python as db
from datetime import datetime
import random as rd
from datetime import datetime
#from INVENTAIRE import Ui_Dialog
PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,True)
syn_nb = "[0-9]"
syn_mail = "^[a-zA-Z0-9]+[@]\w+[a-zA-Z]+[.]\w{2,3}$"
syn_text = "[a-zA-Z]"
#partie bd
bd1 = db.connetion()
cmd_handeler = bd1.cursor(buffered=True)
db.delete_tab(bd1, "frais", cmd_handeler)
db.create_frais_table(bd1, cmd_handeler)
#db.delete_tab(bd1, "enfant", cmd_handeler)
db.create_enfant_table(bd1, cmd_handeler)
#db.delete_tab(bd1, "parents", cmd_handeler)
db.create_parents_table(bd1, cmd_handeler)
#db.delete_tab(bd1, "employes", cmd_handeler)
db.create_employes_table(bd1,cmd_handeler)
#db.delete_tab(bd1, "inventaire", cmd_handeler)
db.create_inventaire_table(bd1, cmd_handeler)
db.delete_tab(bd1, "dashboard", cmd_handeler)
db.create_dashboard_table(bd1,cmd_handeler)
db.delete_tab(bd1, "menu", cmd_handeler)
db.create_menu_table(bd1, cmd_handeler)
db.delete_tab(bd1, "plat_dej", cmd_handeler)
db.delete_tab(bd1, "plat_gout", cmd_handeler)
db.create_plat_dej_table(bd1, cmd_handeler)
db.create_plat_gout_table(bd1, cmd_handeler)
#db.delete_tab(bd1, "admin", cmd_handeler)
db.create_admin_table(bd1,cmd_handeler)
#db.delete_tab(bd1, "programme", cmd_handeler)
db.create_programme_table(bd1, cmd_handeler)
db.create_mat_table(bd1,cmd_handeler)
db.create_classe_table(bd1, cmd_handeler)
db.create_edu_table(bd1, cmd_handeler)
db.create_niv_table(bd1, cmd_handeler)
db.delete_tab(bd1, "archEnf", cmd_handeler)
db.create_archEnf_table(bd1, cmd_handeler)
db.delete_tab(bd1, "stock", cmd_handeler)
db.create_stock_table(bd1, cmd_handeler)
lyoum = str(datetime.now())[:10]

#afficher n'importe quel message
def show_popup(message,titre):
        msg = QMessageBox()
        msg.setWindowTitle(titre)
        msg.setText(message)
        msg.setStyleSheet("font: 87 10pt \"Segoe UI Regular\";")
        x = msg.exec_() # executer le msg info manquante
#verification de la syntaxe
def verifier(texte,syntaxe,message):
    if re.search(syntaxe,texte):
        print("yay ")
        return True
    show_popup(message,"Erreur")
    return False    

class login(QDialog):
    def __init__(self):
        super(login,self).__init__()
        loadUi("pages\login.ui",self)
        self.seconnecter.clicked.connect(self.connecter)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.afficherMotDePasse.stateChanged.connect(self.cocher)
        self.effacer.clicked.connect(self.eff)
        self.cocher()
    def connecter(self):
        query = "SELECT * from admin"
        cmd_handeler.execute(query)
        record = cmd_handeler.fetchone()
        if(len(self.identifiant.text())==0 or len(self.password.text())==0):
                show_popup("Veuillez compléter les informations manquantes","Erreur")
        else:
            if(str(self.identifiant.text())==record[1] and str(self.password.text())==record[2]):
                pagePrincipale = page_principal()
                widget.addWidget(pagePrincipale)
                widget.setFixedSize(1100,700)
                qr = widget.frameGeometry()
                cp = QDesktopWidget().availableGeometry().center()
                qr.moveCenter(cp)
                widget.move(qr.topLeft())
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                show_popup("Informations Incorrectes","Erreur")
    def eff(self):
        self.identifiant.setText("")
        self.password.setText("")
    def cocher(self):
        if self.afficherMotDePasse.isChecked() == True:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)

class page_principal(QDialog):
    def __init__(self):
        super(page_principal,self).__init__()
        loadUi("pages\pagePrincipale.ui",self)
        self.sedeconnecter.clicked.connect(self.deconnecter)
        self.dash_board.clicked.connect(self.dashboard_f)
        self.enfant.clicked.connect(self.enf)
        self.menu_tt.clicked.connect(self.men)
        self.compte_tt.clicked.connect(self.compt)
        self.personnel.clicked.connect(self.personel)
        self.invantaire.clicked.connect(self.inve)
    def inve(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def compt(self):
        s=compte()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def men(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def enf(self):
        s=enfant()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
class compte(QDialog):
    def __init__(self):
        super(compte,self).__init__()
        loadUi("pages\compte.ui",self)
        self.loadData()
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.pers.clicked.connect(self.personel)
        self.home.clicked.connect(self.pp)
        self.btn_modi.clicked.connect(self.modi)
        self.btn_reni.clicked.connect(self.reini)
    
    def loadData(self):
        record = db.recupe_data(bd1,"admin",cmd_handeler)
        self.id.setText(record[0][1])
        self.nom.setText(record[0][3])      
    def reini(self):
        self.lineEdit_1.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
    def modi(self):
        iden = self.lineEdit_1.text()
        name = self.lineEdit_2.text()
        name2 = self.lineEdit_3.text()
        mdp = self.lineEdit_4.text()
        if iden !="" :
            query = "UPDATE admin SET id_admin = %s WHERE id = %s"
            cmd_handeler.execute(query,(iden,1))
            print("normalement maintenant id == ",iden)
        if name !="" :
            query = "UPDATE admin SET nom = %s WHERE id =%s"
            cmd_handeler.execute(query,(name,1))
            print("normalement maintenant nom == ",name)
        if name2 !="" :
            query = "UPDATE admin SET prénom = %s WHERE id =%s"
            cmd_handeler.execute(query,(name2,1))
            print("normalement maintenant prénom == ",name2)
        if mdp !="" :
            query = "UPDATE admin SET mot_de_passe = %s WHERE id =%s"
            cmd_handeler.execute(query,(mdp,1))
            print("normalement maintenant mdp == ",mdp)
        bd1.commit()
        self.loadData()          
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
class dashbord(QDialog):
    def __init__(self):
        super(dashbord,self).__init__()
        loadUi("pages\DASHBOARD V2.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.inve.clicked.connect(self.invse)
        self.pers.clicked.connect(self.personel)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com) 
        self.tabl.clicked.connect(self.dashboard_f)
        db.mj_montant_tt_dash(bd1,cmd_handeler)
        self.loadData()
    def loadData(self):
        query = "SELECT * from dashboard WHERE id =%s"
        cmd_handeler.execute(query,(1,))
        record = cmd_handeler.fetchone()
        self.label_1.setText(str(record[1])) #nb_enfant
        self.label_2.setText(str(record[2])) #nb_perso
        self.label_3.setText(str(record[4]))
        self.label_4.setText(str(record[3]))#montant inv
        self.label_5.setText(str(record[6]))
        self.label_6.setText(str(record[7]))
    def com(self):
        s=compte()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def imp(self):
        dasssshs = frai()
        widget.addWidget(dasssshs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
class enfant(QDialog):
    def __init__(self):
        super(enfant,self).__init__()
        loadUi("pages\enfant.ui",self)
        self.btn_parents.clicked.connect(self.par)
        self.deco.clicked.connect(self.deconnecter)
        self.menu.clicked.connect(self.menus)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.pers.clicked.connect(self.personel)
        self.enfant.clicked.connect(self.ennfant)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(9, delegate)# les frais
        self.tableWidget.setItemDelegateForColumn(0, delegate) # le numero
        self.tableWidget.doubleClicked.connect(self.fen_parent)
        self.loadData()
        #boutons
        self.btn_prog.clicked.connect(self.progr)
        self.btn_export.clicked.connect(self.exporte)
        self.btn_ajout.clicked.connect(self.ajouter_ligne)
        self.btn_supp.clicked.connect(self.delete_ligne)
        self.btn_sauv.clicked.connect(self.enrg_base)
        self.btn_archive.clicked.connect(self.arch)
        self.btn_frais.clicked.connect(self.frais)
        #verifier les criteres de la recherche d'apres le combobox
        if self.critere.currentText() == "Nom" :
            self.lineEdit.textChanged.connect(self.findNom)
        elif self.critere.currentText() == "Prenom":
            self.lineEdit.textChanged.connect(self.findPrenom)
        elif self.critere.currentText() == "Niveau" :
            self.lineEdit.textChanged.connect(self.findNiveau)
    def findNom(self):
        nom = self.lineEdit.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 1)
            self.tableWidget.setRowHidden(row, nom not in item.text().lower())
    def findPrenom(self):
        prenom = self.lineEdit.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 2)
            self.tableWidget.setRowHidden(row, prenom not in item.text().lower())
    def findNiveau(self):
        niveau = self.lineEdit.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 7)
            self.tableWidget.setRowHidden(row, niveau not in item.text().lower())
    def loadData(self) : 
        records = db.recup_data(bd1,"enfant",cmd_handeler)
        print(self.tableWidget.rowCount())
        nb_colonnes = self.tableWidget.columnCount()
        rowcount = 0
        try:
            for row in records:
                self.tableWidget.setRowCount(rowcount + 1)
                for col in range(0,nb_colonnes):
                    self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(str(row[col])))  
                rowcount += 1
                print(row)
            db.mj_enf_dash(bd1, cmd_handeler) #quand je load les info y'a une mise a jour de la base dashborad
        except Exception as x :
            print(x)
    def enrg_base(self):
            nb_lignes = self.tableWidget.rowCount()
            nb_colonnes = self.tableWidget.columnCount()
            print(nb_colonnes)
            for ligne in range(nb_lignes):
                donne_ligne =[]
                for colonne in range(1,nb_colonnes):
                    item = self.tableWidget.item(ligne,colonne)
                    if item != None:
                        donne_ligne.append(item.text())
                    else:
                        donne_ligne.append("/")
                try:
                    pr = (donne_ligne[14],donne_ligne[0]) # on recupe id par et le nom
                    if pr[0] != "/":
                        db.add_data_parents(bd1,pr, cmd_handeler)
                except Exception as x:
                    print(x) 
                iden = self.tableWidget.item(ligne,0) # on recupe id si il existe
                if iden != None:
                    donne_ligne.append(iden.text()) # on ajoute le id a la fin si il existe  car y'aurra un update
                    db.up_data_enfant(bd1,tuple(donne_ligne),cmd_handeler)
                else:
                    print("donne_ligne exjj ",donne_ligne)
                    db.add_data_enfant(bd1,tuple(donne_ligne),cmd_handeler)
            self.loadData()
    def delete_ligne(self):
        cr = self.tableWidget.currentRow() # in recupe la ligne selectionnee
        if cr >= 0:
            iden  = self.tableWidget.item(cr,0)
            if iden != None :
                db.supp_data_enfant(bd1,(iden.text(),),cmd_handeler)
            self.tableWidget.removeRow(cr)
    def ajouter_ligne(self):
        rowcount =  self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowcount+1)
    def exporte(self):
        columnHeaders = []
        #creation d'un liste column header
        print(self.tableWidget.columnCount())
        r = self.tableWidget.rowCount()
        c = self.tableWidget.columnCount()
        for j in range(0,c): # will send the table self.tableWidget.model().columnCount()
            columnHeaders.append(self.tableWidget.horizontalHeaderItem(j).text())
        data_f = pandas.DataFrame(columns = columnHeaders)
         #creation de data frame object recordset
        for row in range(r): 
            for col in range(0,c):
                item = self.tableWidget.item(row, col)
                if item != None:
                    data_f.at[row, columnHeaders[col]] = item.text()
                else:
                    data_f.at[row, columnHeaders[col]] = "/"

        data_f.to_excel(f'Liste_Enfant_{lyoum[:4]}.xlsx', index= False)
        show_popup(f"Création du fichier 'Liste_Enfant_{lyoum[:4]}.xlsx' réussite","Message")
    def fen_parent(self):
        try:
            pr = self.tableWidget.item(self.tableWidget.currentRow(),15).text()
            f = fen_parent(pr)
            f.exec()
        except Exception as x :print(x)       
    def arch(self):
        archii=archive()
        widget.addWidget(archii)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def frais(self):
        frrrais=frais()
        widget.addWidget(frrrais)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)     
    def progr(self):
        sqssd=program()
        widget.addWidget(sqssd)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def par(self):
        dashs = parents()
        widget.addWidget(dashs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)  
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)    
    def com(self):
        s=compte()
        widget.addWidget(ssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
class frais(QDialog):
    def __init__(self):
        super(frais,self).__init__()
        loadUi("pages\\frais.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com)
        self.pers.clicked.connect(self.personel)
        self.inve.clicked.connect(self.invse)
        self.tabl.clicked.connect(self.dashboard_f)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.btn_sauv.clicked.connect(self.enrg_base)
        self.btn_prog.clicked.connect(self.progr)
        self.btn_parents.clicked.connect(self.par)
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(9, delegate)# le montant
        self.tableWidget.setItemDelegateForColumn(0, delegate)#id
        self.tableWidget.setItemDelegateForColumn(1, delegate)#non
        self.tableWidget.setItemDelegateForColumn(2, delegate)#non
        self.tableWidget.setItemDelegateForColumn(3, delegate)#non
        self.tableWidget.setItemDelegateForColumn(4, delegate)#non
        self.loadData()
    def loadData(self):
        records = db.recup_data(bd1,"frais",cmd_handeler)
        nb_colonnes = self.tableWidget.columnCount()
        rowcount = 0
        try:
            for row in records:
                self.tableWidget.setRowCount(rowcount+1)
                for col in range(0,nb_colonnes-1):
                    self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(str(row[col])))
                item = QtWidgets.QTableWidgetItem("Payé")
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsTristate)
                if row[10] == 1:
                    item.setCheckState(QtCore.Qt.Checked)  
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)  
                self.tableWidget.setItem(rowcount, 10, item)
                rowcount += 1
                print(row)
        except Exception as x :
            print(x)  
    def enrg_base(self):
        nb_lignes = self.tableWidget.rowCount()
        nb_colonnes = self.tableWidget.columnCount()
        print(nb_lignes,nb_colonnes)
        mon_dash = 0
        for ligne in range(nb_lignes): 
            donne_ligne =[]
            for colonne in range(5,nb_colonnes-2):
                item = self.tableWidget.item(ligne,colonne)
                try :
                    donne_ligne.append(int(item.text()))
                except:
                    donne_ligne.append(0)
            try:
                donne_ligne.append(sum(donne_ligne))
            except Exception as x:
                print(x)
                donne_ligne.append(0)
            if self.tableWidget.item(ligne,10).checkState() == QtCore.Qt.Checked:
                mon_dash = mon_dash + donne_ligne[len(donne_ligne) - 1] #c la somme
                db.mj_montant_frais_dash(bd1,mon_dash,cmd_handeler) # on update le dashboad le monatnat
                donne_ligne.append(1) #cheked
            else:
                donne_ligne.append(0)
            try:
                donne_ligne.append(self.tableWidget.item(ligne,0).text()) # id
                db.up_data_frais_nb(bd1,tuple(donne_ligne),cmd_handeler)
                db.up_data_enfant_montant(bd1,(donne_ligne[4],donne_ligne[6]),cmd_handeler) # montant
            except Exception as x:
                print(x)
            print("donne ligne",donne_ligne)
        self.loadData()
    def par(self):
        dashs = parents()
        widget.addWidget(dashs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def progr(self):
        sqssd=program()
        widget.addWidget(sqssd)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        ssfsff=compte()
        widget.addWidget(ssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
class parents(QDialog):
    def __init__(self):
        super(parents,self).__init__()
        loadUi("pages\parents.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.pers.clicked.connect(self.personel)
        self.compte.clicked.connect(self.com)  
        self.home.clicked.connect(self.pp)
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)# lid
        self.tableWidget.setItemDelegateForColumn(1, delegate)
        self.btn_frais.clicked.connect(self.frais)
        self.btn_prog.clicked.connect(self.progr)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.loadData()
        # partie boutons
        self.btn_supp.clicked.connect(self.delete_ligne)
        self.btn_sauv.clicked.connect(self.enrg_base)
    def loadData(self) : 
        records = db.recup_data(bd1,"parents",cmd_handeler)
        print(records)
        print(self.tableWidget.rowCount())
        nb_colonnes = self.tableWidget.columnCount()
        rowcount = 0
        if records != None and len(records) != 0 :
            for row in records:
                self.tableWidget.setRowCount(rowcount+1)
                for col in range(nb_colonnes):
                    donne = str(row[col])
                    self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(donne))
                rowcount += 1
                print(row)
    def enrg_base(self):
        nb_lignes = self.tableWidget.rowCount()
        nb_colonnes = self.tableWidget.columnCount()
        for ligne in range(nb_lignes):
            donne_ligne =[]
            for colonne in range(1,nb_colonnes):
                item = self.tableWidget.item(ligne,colonne)
                if item!= None and item != '':
                    donne_ligne.append(item.text())
                else:
                    donne_ligne.append("/")
            donne_ligne.append(self.tableWidget.item(ligne,0).text())
            print(donne_ligne)
            db.up_data_parents(bd1,donne_ligne,cmd_handeler)
        self.loadData()
    def delete_ligne(self):
        cr = self.tableWidget.currentRow()
        if cr >= 0:
            db.supp_data_parents(bd1,(self.tableWidget.item(cr,0).text(),),cmd_handeler)
            self.tableWidget.removeRow(cr)
    def ajouter_ligne(self):
        rowcount =  self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowcount+1)
    def frais(self):
        frrrais=frais()
        widget.addWidget(frrrais)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    def progr(self):
        sqssd=program()
        widget.addWidget(sqssd)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        ssfsff=compte()
        widget.addWidget(ssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
class fen_parent(QDialog):
    def __init__(self,i):
        super(fen_parent,self).__init__()
        loadUi("pages\\fenetre_parent.ui",self)
        self.setFixedSize(331,281)
        self.loadData(i) 
        self.setWindowTitle("Parent")
    def loadData(self,i):
        query = " SELECT * FROM parents WHERE id = %s"
        cmd_handeler.execute(query,(i,))
        records = cmd_handeler.fetchone()
        print(records)
        try:
            self.label_0.setText(f"{records[1]} {records[2]}")
            self.label_1.setText(f"{records[3]}")
            self.label_2.setText(f"{records[4]}")
            self.label_3.setText(f"{records[5]}")
            self.label_4.setText(f"{records[6]}")
        except Exception as x:
            print(x)
class archive(QDialog):
    def __init__(self):
        super(archive,self).__init__()
        loadUi("pages\\archive_2.ui", self)
        self.deco.clicked.connect(self.deconnecter)
        self.menu.clicked.connect(self.menus)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com)
        self.tabl.clicked.connect(self.dashboard_f)
        self.enfant.clicked.connect(self.ennfant)
        self.pers.clicked.connect(self.personel)
        self.btn_rech.clicked.connect(self.rech)
        self.btn_load.clicked.connect(self.load)
        self.btn_arch.clicked.connect(self.arch)
    def load(self) : 
        records = db.recup_data(bd1,"enfant",cmd_handeler)
        print("record load ",records)
        if (records != None) and (len(records) != 0):
            nb_colonnes = self.tableWidget.columnCount()
            rowcount = 0
            for row in records:
                    self.tableWidget.setRowCount(rowcount+1)
                    self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(row[9])))
                    rowcount += 1
                    print(row)
    def arch(self):
        r = self.rech_mini()
        if r == None or len(r) == 0:
            nb_lignes = self.tableWidget.rowCount()
            nb_colonnes = self.tableWidget.columnCount()
            print(nb_colonnes)
            for ligne in range(nb_lignes):
                donne_ligne =[ligne+1]
                for colonne in range(1,nb_colonnes-1):
                    item = self.tableWidget.item(ligne,colonne)
                    donne_ligne.append(item.text())
                    print("donne ligne",donne_ligne)
                donne_ligne.append(str(self.date_1.date().toPyDate())[:4])
                db.add_data_archEnf(bd1,tuple(donne_ligne), cmd_handeler)
            self.rech()
        else:
            show_popup("La table existe deja","Erreur") 
    def rech_mini(self):
        d = (str(self.date_1.date().toPyDate())[:4],)
        cmd_handeler.execute("SELECT * FROM archEnf WHERE date = %s",d)
        return cmd_handeler.fetchall()
    def rech(self):
        records = self.rech_mini()
        if records != None and len(records) != 0 :
            nb_colonnes = self.tableWidget.columnCount()
            rowcount = 0
            for row in records:
                self.tableWidget.setRowCount(rowcount+1)
                for col in range(nb_colonnes):
                    self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(str(row[col])))
                rowcount += 1
                print(row)
        else:
            show_popup("Aucune table n'existe ","Erreur") 
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        s=compte()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        s=enfant()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
class inventaire(QDialog):
    def __init__(self):
        super(inventaire,self).__init__()
        loadUi("pages\Inventaire_2.ui",self)
        self.date_1.setDate(QtCore.QDate.fromString(lyoum,'yyyy-MM-dd'))
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.tabl.clicked.connect(self.dashboard_f)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com)
        self.pers.clicked.connect(self.personel)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(6, delegate)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.btn_export.clicked.connect(self.exporte)
        self.btn_ajout.clicked.connect(self.ajouter_ligne)
        self.btn_supp_ligne.clicked.connect(self.delete_ligne)
        self.btn_sauv.clicked.connect(self.show_popup_yn_sauv)
        self.btn_rech.clicked.connect(self.loadData)
        self.tableWidget.doubleClicked.connect(self.stoc)

    def rech_mini(self):
        d = str(self.date_1.date().toPyDate())[:7]
        cmd_handeler.execute("SELECT * FROM inventaire WHERE date = %s",(d,))
        r = cmd_handeler.fetchall()
        return r
    #on enregistre le mois et l'annee c tout
    def loadData(self) : 
        records = self.rech_mini()
        if records != None and len(records) != 0:
            nb_colonnes = self.tableWidget.columnCount()
            rowcount = 0
            for row in records:
                self.tableWidget.setRowCount(rowcount+1)
                for col in range(nb_colonnes):
                    try: 
                        self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(str(row[col])))
                    except:
                        self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem("0"))
                rowcount += 1
        else:
            show_popup("Aucune table n'existe pour cette date","Erreur")
    def enrg_base(self):
        #r = self.rech_mini() #l'enregistrement ne se fait pas si la table exisre deja
        #if (r == None) or(len(r) == 0):
            d = str(self.date_1.date().toPyDate())[:7]
            nb_lignes = self.tableWidget.rowCount()
            nb_colonnes = self.tableWidget.columnCount()
            nom_produit = []
            nb_produit = []
            for ligne in range(nb_lignes):
                donne_ligne_mini =[]
                for colonne in range(1,nb_colonnes-1):
                    item = self.tableWidget.item(ligne,colonne)
                    if colonne == 1:
                        try:
                            nom_produit.append(item.text())
                        except:
                            nom_produit.append("/")
                    if colonne == 3:
                        try:
                            nb_produit.append(item.text())
                        except:
                            nb_produit.append(0)
                    if item != None :
                        donne_ligne_mini.append(item.text())
                    else:
                        donne_ligne_mini.append("/")
                try: # on enregistre le montant automatiquement
                    donne_ligne_mini.append(int(donne_ligne_mini[2])*int(donne_ligne_mini[3]))  #le produit entre les deux
                except:
                    donne_ligne_mini.append(0)
                donne_ligne_mini.append(d)
                print(donne_ligne_mini)
                iden = self.tableWidget.item(ligne,0)
                if iden != None:
                    donne_ligne_mini.append(iden.text()) # on ajoute le id a la fin si il existe  car y'aurra un update
                    print("upppp",donne_ligne_mini)
                    db.up_data_inventaire(bd1,tuple(donne_ligne_mini),cmd_handeler)
                else:
                    print("ukncdkjnp",donne_ligne_mini)
                    db.add_data_inventaire(bd1,tuple(donne_ligne_mini),cmd_handeler)
                if d == lyoum[:7]: # si c'est le mois actuelle on fera une mise a jour du dashboard et du stock
                    db.mj_inv_dash(bd1, cmd_handeler)
            self.loadData()
            for i in range(len(nom_produit)):
                db.up_data_stock(bd1,(nom_produit[i],nb_produit[i]),cmd_handeler)
    def delete_ligne(self):
        cr = self.tableWidget.currentRow()
        if cr >= 0:
            d = str(self.date_1.date().toPyDate())[:7]
            query = "DELETE FROM inventaire WHERE date = %s and id = %s"
            cmd_handeler.execute(query,(d,self.tableWidget.item(cr,0).text()))
            bd1.commit()
            self.tableWidget.removeRow(cr)
    def ajouter_ligne(self):
        rowcount =  self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowcount+1)
    def delete_bd(self):
        records = self.rech_mini()
        print("record load ",records)
        if (records != None) and (len(records) != 0):
            item = str(self.date_1.date().toPyDate())[:7]
            query = "DELETE FROM inventaire WHERE date = %s"
            cmd_handeler.execute(query,(item,))
            show_popup("Suppression terminer","Message")
        else:
            show_popup("Aucune table n'existe pour cette date","Erreur")
    def update(self):
            cr = self.tableWidget.rowCount()
            d = str(self.date_1.date().toPyDate())[:7]
            for i in range(0,cr):
                ligne = []
                for j in range(1,7):
                    try:
                        ligne.append(self.tableWidget.item(i,j).text())
                    except:
                        ligne.append(0)
                ligne.append(d)
                iden = self.tableWidget.item(i,0)
                if iden != None:
                    ligne.append(iden.text()) # on ajoute le id a la fin si il existe 
                    print("ligne try donc mj ",ligne)
                    db.up_data_inventaire(bd1,tuple(ligne),cmd_handeler)
                else:
                    ligne.append(i+1 )
                    print("ligne exjj ",ligne)
                    db.add_data_inventaire(bd1,tuple(ligne),cmd_handeler)
    def show_popup_yn_sauv(self):
        resu = QMessageBox.question(self,"Message","Avez vous verifier tous vos elements ?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if resu == QMessageBox.Yes:
            self.enrg_base()
    def exporte(self):
        columnHeaders = ["Numero","Produit","Fournisseur","Nombre d'unite","Produit de l'unite","Unite de stockage","Montant",]
        data_f = pandas.DataFrame(columns = columnHeaders)
        #creation de data frame object recordset
        for row in range(self.tableWidget.rowCount()): #self.tableWidget.rowCount()
            for col in range(self.tableWidget.columnCount()):
                try:
                    data_f.at[row, columnHeaders[col]] = self.tableWidget.item(row, col).text()
                except:
                     data_f.at[row, columnHeaders[col]] = "/"
       
        data_f.to_excel(f'Inventaire_{lyoum}.xlsx', index= False)
        show_popup(f"Fichier Inventaire_{lyoum}.xlsx créé  avec succes", "Message")
        print("yay exported")    
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        s=compte()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def stoc(self): 
        try:
            pr = self.tableWidget.item(self.tableWidget.currentRow(),1).text()
            f = stock(pr)
            f.exec()
        except:
            show_popup("Pas d'elements","Erreur")
    def imp(self):
        dasssshs = frai()
        widget.addWidget(dasssshs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
class stock(QDialog):
    def __init__(self,i):
        super(stock,self).__init__()
        loadUi("pages/stock_2.ui",self)
        self.setFixedSize(335,230)
        self.loadData(i)
        self.btn_sauv.clicked.connect(self.sauv)
        self.setWindowTitle("Stock")

    def loadData(self,i):
        records = db.recup_data(bd1,"stock",cmd_handeler)
        print(records)
        try:
            for record in records :
                self.combo_choix.addItem(record[0])
            self.combo_choix.setCurrentText(i)
            nb = db.recup_nb_stock(bd1,(i,),cmd_handeler)
            print(nb)
            self.spinBox.setValue(nb[0])

        except Exception as x:
            print(x)
            self.spinBox.setValue(0)
    def sauv(self):
        try:
            query_vals= (self.spinBox.value(),self.combo_choix.currentText())
            query = "UPDATE stock SET nb = %s WHERE produit = %s"
            cmd_handeler.execute(query,query_vals)
            bd1.commit()
        except Exception as x:
            print(x)
class program(QDialog):
    def __init__(self):
        super(program,self).__init__()
        loadUi("pages\programme.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.pers.clicked.connect(self.personel)
        self.compte.clicked.connect(self.com)  
        self.home.clicked.connect(self.pp)
        self.btn_modi_elem.clicked.connect(self.modi_elem)
        #btn
        self.btn_supp.clicked.connect(self.delete)
        self.btn_rech.clicked.connect(self.rech)
        self.btn_sauv.clicked.connect(self.enrg_base)
        self.btn_export.clicked.connect(self.export)
        self.loadData()
    def rech_mini(self):
        print(self.dateEdit_1.date().toPyDate())
        query = "SELECT * FROM programme WHERE date = %s AND edu = %s AND niv = %s AND classe = %s"
        query_val = (str(self.dateEdit_1.date().toPyDate())[:4],self.combo_edu.currentText(),self.combo_niv.currentText(),self.combo_classe.currentText())
        print(query_val)
        cmd_handeler.execute(query,query_val)
        record = cmd_handeler.fetchone()
        return record
    def rech(self):
        r = self.rech_mini()
        if (r != None) and (len(r) != 0):
            self.comboBox_1.setCurrentText(r[1])
            self.comboBox_2.setCurrentText(r[2])
            self.comboBox_3.setCurrentText(r[3])
            self.comboBox_4.setCurrentText(r[4])
            self.comboBox_5.setCurrentText(r[5])
            self.comboBox_6.setCurrentText(r[6])
            self.comboBox_7.setCurrentText(r[7])
            self.comboBox_8.setCurrentText(r[8])
            self.comboBox_9.setCurrentText(r[9])
            self.comboBox_10.setCurrentText(r[10])
            self.comboBox_11.setCurrentText(r[11])
            self.comboBox_12.setCurrentText(r[12])
            self.comboBox_13.setCurrentText(r[13])
            self.comboBox_14.setCurrentText(r[14])
            self.comboBox_15.setCurrentText(r[15])
            self.comboBox_16.setCurrentText(r[16])
            self.comboBox_17.setCurrentText(r[17])
            self.comboBox_18.setCurrentText(r[18])
            self.comboBox_19.setCurrentText(r[19])
            self.comboBox_20.setCurrentText(r[20])
            self.comboBox_21.setCurrentText(r[21])
            self.comboBox_22.setCurrentText(r[22])
            self.comboBox_23.setCurrentText(r[23])
            self.comboBox_24.setCurrentText(r[24])
            self.comboBox_25.setCurrentText(r[25])
        else:
            show_popup("Aucun programme n'existe pour cette date",("Erreur"))
    def loadData(self):
        #on load d'ab les diff mat
        try:
            records = db.recup_data(bd1,"mat",cmd_handeler)
            for record in records :
                self.comboBox_1.addItem(record[0])
                self.comboBox_2.addItem(record[0])
                self.comboBox_3.addItem(record[0])
                self.comboBox_4.addItem(record[0])
                self.comboBox_5.addItem(record[0])
                self.comboBox_6.addItem(record[0])
                self.comboBox_7.addItem(record[0])
                self.comboBox_8.addItem(record[0])
                self.comboBox_9.addItem(record[0])
                self.comboBox_10.addItem(record[0])
                self.comboBox_11.addItem(record[0])
                self.comboBox_12.addItem(record[0])
                self.comboBox_13.addItem(record[0])
                self.comboBox_14.addItem(record[0])
                self.comboBox_15.addItem(record[0])
                self.comboBox_16.addItem(record[0])
                self.comboBox_17.addItem(record[0])
                self.comboBox_18.addItem(record[0])
                self.comboBox_19.addItem(record[0])
                self.comboBox_20.addItem(record[0])
                self.comboBox_21.addItem(record[0])
                self.comboBox_22.addItem(record[0])
                self.comboBox_23.addItem(record[0])
                self.comboBox_24.addItem(record[0])
                self.comboBox_25.addItem(record[0])
                self.comboBox_14.addItem(record[0])
        except Exception as x:
            print(x)
        try:
            records = db.recup_data(bd1,"edu",cmd_handeler)
            print("edu reco",records)
            for record in records :
                self.combo_edu.addItem(record[0])
        except Exception as x:
            print(x)
        try:
            records = db.recup_data(bd1,"niv",cmd_handeler)
            for record in records :
                self.combo_niv.addItem(record[0])
        except Exception as x:
            print(x)
        try:
            records = db.recup_data(bd1,"classe",cmd_handeler)
            for record in records :
                self.combo_classe.addItem(record[0])
        except Exception as x:
            print(x)
    def enrg_base(self):
        resu = self.rech_mini()
        if (resu == None) or (len(resu) == 0): #pas d'element
            try:
                item = []
                item.append(self.comboBox_1.currentText())
                item.append(self.comboBox_2.currentText())
                item.append(self.comboBox_3.currentText())
                item.append(self.comboBox_4.currentText())
                item.append(self.comboBox_5.currentText())
                item.append(self.comboBox_6.currentText())
                item.append(self.comboBox_7.currentText())
                item.append(self.comboBox_8.currentText())
                item.append(self.comboBox_9.currentText())
                item.append(self.comboBox_10.currentText())
                item.append(self.comboBox_11.currentText())
                item.append(self.comboBox_12.currentText())
                item.append(self.comboBox_13.currentText())
                item.append(self.comboBox_14.currentText())
                item.append(self.comboBox_15.currentText())
                item.append(self.comboBox_16.currentText())
                item.append(self.comboBox_17.currentText())
                item.append(self.comboBox_18.currentText())
                item.append(self.comboBox_19.currentText())
                item.append(self.comboBox_20.currentText())
                item.append(self.comboBox_22.currentText())
                item.append(self.comboBox_21.currentText())
                item.append(self.comboBox_23.currentText())
                item.append(self.comboBox_24.currentText())
                item.append(self.comboBox_25.currentText())
                item.append(str(self.dateEdit_1.date().toPyDate())[:4])
                item.append(self.combo_edu.currentText())
                item.append(self.combo_niv.currentText())
                item.append(self.combo_classe.currentText())
            except Exception as x: print(x)
            print(item)
            try:
                db.add_data_prog(bd1, tuple(item), cmd_handeler)
                show_popup(f"Eregistrement du programme_{item[25]} reussi","Message")
            except Exception as x:
                print(x)
        else:
            show_popup(f"Programme existe deja","Erreur")
    def export(self):
        columnHeaders = ["DIMANCHE","LUNDI","MARDI","MERCREDI","JEUDI"]
        data_f = pandas.DataFrame(columns = columnHeaders)
        d = str(self.dateEdit_1.date().toPyDate())[:4]
        try:
            data_f.at[0,columnHeaders[0]] = self.comboBox_1.currentText()
            data_f.at[0,columnHeaders[1]] = self.comboBox_2.currentText()
            data_f.at[0,columnHeaders[2]] = self.comboBox_3.currentText()
            data_f.at[0,columnHeaders[3]] = self.comboBox_4.currentText()
            data_f.at[0,columnHeaders[4]] = self.comboBox_5.currentText()
            data_f.at[1,columnHeaders[0]] = self.comboBox_6.currentText()
            data_f.at[1,columnHeaders[1]] = self.comboBox_7.currentText()
            data_f.at[1,columnHeaders[2]] = self.comboBox_8.currentText()
            data_f.at[1,columnHeaders[3]] = self.comboBox_9.currentText()
            data_f.at[1,columnHeaders[4]] = self.comboBox_10.currentText()
            data_f.at[2,columnHeaders[0]] = self.comboBox_11.currentText()
            data_f.at[2,columnHeaders[1]] = self.comboBox_12.currentText()
            data_f.at[2,columnHeaders[2]] = self.comboBox_13.currentText()
            data_f.at[2,columnHeaders[3]] = self.comboBox_14.currentText()
            data_f.at[2,columnHeaders[4]] = self.comboBox_15.currentText()
            data_f.at[3,columnHeaders[0]] = self.comboBox_16.currentText()
            data_f.at[3,columnHeaders[1]] = self.comboBox_17.currentText()
            data_f.at[3,columnHeaders[2]] = self.comboBox_18.currentText()
            data_f.at[3,columnHeaders[3]] = self.comboBox_19.currentText()
            data_f.at[3,columnHeaders[4]] = self.comboBox_20.currentText()
            data_f.at[4,columnHeaders[0]] = self.comboBox_21.currentText()
            data_f.at[4,columnHeaders[1]] = self.comboBox_22.currentText()
            data_f.at[4,columnHeaders[2]] = self.comboBox_23.currentText()
            data_f.at[4,columnHeaders[3]] = self.comboBox_24.currentText()
            data_f.at[4,columnHeaders[4]] = self.comboBox_25.currentText()
            e = self.combo_edu.currentText()
            n = self.combo_niv.currentText()
            c = self.combo_classe.currentText()
            data_f.to_excel(f'programme_{d}_{e}_{n}_{c}.xlsx', index= False)
            show_popup(f"Creation du fichier programme_{d}_{e}_{n}_{c}.xlsx reussie","Message")
        except Exception as x:
            print(x)
            show_popup(f"Creation du fichier impossible","Erreur")
    def delete(self):
        query_vals = (str(self.dateEdit_1.date().toPyDate())[:4],self.combo_edu.currentText(),self.combo_niv.currentText(),self.combo_classe.currentText())
        r = db.supp_data_prog(bd1,query_vals,cmd_handeler)
        if r > 0:
            show_popup("Suppression reussie","Message")
        else:
            show_popup("Aucun programme n'existe pour cette date","Erreur")
  
    def modi_elem(self):
        s=ajouter_programme()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        s=compte()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
class ajouter_programme(QDialog):
    def __init__(self):
        super(ajouter_programme,self).__init__()
        loadUi("pages\\ajouter_programme.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com)
        self.pers.clicked.connect(self.personel)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.btn_prog.clicked.connect(self.progs)
        self.btn_ajout.clicked.connect(self.enrg_elem)
        self.btn_supp.clicked.connect(self.supp_elem)

    def enrg_elem(self):
        item = self.lineEdit_1.text().lower()
        choix = self.combo_choix_ajout.currentText().lower()
        if item != None:
            if choix == "educateur":
                db.add_data_edu(bd1,(item,),cmd_handeler)
            elif choix == "classe":
                db.add_data_classe(bd1,(item,),cmd_handeler)
            elif choix == "niveau":
                db.add_data_niv(bd1,(item,),cmd_handeler)
            elif choix == "matiere":
                db.add_data_mat(bd1,(item,),cmd_handeler)
    def supp_elem(self):
        item = self.lineEdit_2.text()
        choix = self.combo_choix_supp.currentText()
        if item != None:
            if choix == "educateur":
                db.supp_data_edu(bd1,(item,),cmd_handeler)
            elif choix == "classe":
                db.supp_data_classe(bd1,(item,),cmd_handeler)
            elif choix == "niveau":
                db.supp_data_niv(bd1,(item,),cmd_handeler)
            elif choix == "matiere":
                db.supp_data_mat(bd1,(item,),cmd_handeler)
    def progs(self):
        s=program()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        s=compte()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def imp(self):
        dasssshs = frai()
        widget.addWidget(dasssshs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        print("well mt9drich teketbi lol")
        return
class menu(QDialog): 
    def __init__(self):
        super(menu,self).__init__()
        loadUi("pages\menu_2.ui",self)
        self.date_1.setDate(QtCore.QDate.fromString(lyoum,'yyyy-MM-dd'))
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com)
        self.pers.clicked.connect(self.personel)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.menu.clicked.connect(self.menus)
        #btn
        self.btn_ajout_plat.clicked.connect(self.ajout_plat)
        self.btn_supp_plat.clicked.connect(self.supp_plat)
        self.btn_sauv.clicked.connect(self.enrg_menu)
        self.date_1.dateChanged.connect(self.cherche_menu)
        self.btn_gen.clicked.connect(self.generer)
        self.btn_supp.clicked.connect(self.supp)
        self.btn_export.clicked.connect(self.export)
        self.loadData()
    
    def loadData(self): 
        # c'est pour recupe les diff plat qui existe dans la base et non un menu precis
        records2 = db.recup_data(bd1,"plat_dej",cmd_handeler)
        records1 = db.recup_data(bd1,"plat_gout",cmd_handeler)
        print("plat gout ",records1)
        try:
            for record in records1 :
                self.comboBox_1.addItem(record[0])
                self.comboBox_4.addItem(record[0])
                self.comboBox_7.addItem(record[0])
                self.comboBox_10.addItem(record[0])
                self.comboBox_13.addItem(record[0])
                self.comboBox_3.addItem(record[0])
                self.comboBox_6.addItem(record[0])
                self.comboBox_9.addItem(record[0])
                self.comboBox_12.addItem(record[0])
                self.comboBox_15.addItem(record[0])
            for record in records2:
                self.comboBox_2.addItem(record[0])
                self.comboBox_5.addItem(record[0])
                self.comboBox_8.addItem(record[0])
                self.comboBox_11.addItem(record[0])
                self.comboBox_14.addItem(record[0])
        except Exception as x:
            print(x)
        #si il existe un menu pour cette date on l'affiche directement 
        record = self.rech_mini()
        if record != None and len(record) != 0:
            self.loadMenu(record)
            print("done")
    def loadMenu(self,record):
            self.comboBox_1.setCurrentText(record[1])
            self.comboBox_2.setCurrentText(record[2])
            self.comboBox_3.setCurrentText(record[3])
            self.comboBox_4.setCurrentText(record[4])
            self.comboBox_5.setCurrentText(record[5])
            self.comboBox_6.setCurrentText(record[6])
            self.comboBox_7.setCurrentText(record[7])
            self.comboBox_8.setCurrentText(record[8])
            self.comboBox_9.setCurrentText(record[9])
            self.comboBox_10.setCurrentText(record[10])
            self.comboBox_11.setCurrentText(record[11])
            self.comboBox_12.setCurrentText(record[12])
            self.comboBox_13.setCurrentText(record[13])
            self.comboBox_14.setCurrentText(record[14])
            self.comboBox_15.setCurrentText(record[15])
    def rech_mini(self):
        query_val = (str(self.date_1.date().toPyDate()),)
        record = db.recup_data_menu(bd1,query_val,cmd_handeler) ##fetchone
        print(record)
        return record
    def cherche_menu(self):
        record = self.rech_mini()
        if record != None and len(record) != 0:
            self.loadMenu(record)
        else:
            show_popup("Aucun menu existant pour cette date",("Erreur"))
    def export(self):
        try:
            columnHeaders = ["GOUTER","DEJEUNER","GOUTER"]
            data_f = pandas.DataFrame(columns = columnHeaders)
            d = str(self.date_1.date().toPyDate())
            data_f.at[0,columnHeaders[0]] = self.comboBox_1.currentText()
            data_f.at[0,columnHeaders[1]] = self.comboBox_2.currentText()
            data_f.at[0,columnHeaders[2]] = self.comboBox_3.currentText()
            data_f.at[1,columnHeaders[0]] = self.comboBox_4.currentText()
            data_f.at[1,columnHeaders[1]] = self.comboBox_5.currentText()
            data_f.at[1,columnHeaders[2]] = self.comboBox_6.currentText()
            data_f.at[2,columnHeaders[0]] = self.comboBox_7.currentText()
            data_f.at[2,columnHeaders[1]] = self.comboBox_8.currentText()
            data_f.at[2,columnHeaders[2]] = self.comboBox_9.currentText()
            data_f.at[3,columnHeaders[0]] = self.comboBox_10.currentText()
            data_f.at[3,columnHeaders[1]] = self.comboBox_11.currentText()
            data_f.at[3,columnHeaders[2]] = self.comboBox_12.currentText()
            data_f.at[4,columnHeaders[0]] = self.comboBox_13.currentText()
            data_f.at[4,columnHeaders[1]] = self.comboBox_14.currentText()
            data_f.at[4,columnHeaders[2]] = self.comboBox_15.currentText()
            data_f.to_excel(f'Menu_{d}.xlsx', index= True)
            show_popup(f"Creation du fichier Menu_{d}.xlsx' reussie","Message")
            print("yay exported")
        except Exception as x:
            print(x)
            show_popup(f"Creation du fichier Menu_{d}.xlsx' echouee","Erreur")
    def generer(self):
        record1 = db.recup_data(bd1,"plat_gout",cmd_handeler)
        l1 = len(record1)
        print(record1)
        record2 = db.recup_data(bd1,"plat_dej",cmd_handeler)
        l2 = len(record2)
        print(record2)
        print(l2)
        if (l1  != 0) and (l2 != 0 ): 
            r = rd.randint(0,l1-1)
            print(r)
            self.comboBox_1.setCurrentText(record1[r][0])
            self.comboBox_2.setCurrentText(record2[rd.randint(0,l2-1)][0])
            self.comboBox_3.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_4.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_5.setCurrentText(record2[rd.randint(0,l2-1)][0])
            self.comboBox_6.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_7.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_8.setCurrentText(record2[rd.randint(0,l2-1)][0])
            self.comboBox_9.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_10.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_11.setCurrentText(record2[rd.randint(0,l2-1)][0])
            self.comboBox_12.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_13.setCurrentText(record1[rd.randint(0,l1-1)][0])
            self.comboBox_14.setCurrentText(record2[rd.randint(0,l2-1)][0])
            self.comboBox_15.setCurrentText(record1[rd.randint(0,l1-1)][0])
        else:
            show_popup("Vous n'avez aucun ELEMENTS pour l'instant","Erreur")           
    def enrg_menu(self):
        item = [str(self.date_1.date().toPyDate())]
        item.append(self.comboBox_1.currentText())
        item.append(self.comboBox_2.currentText())
        item.append(self.comboBox_3.currentText())
        item.append(self.comboBox_4.currentText())
        item.append(self.comboBox_5.currentText())
        item.append(self.comboBox_6.currentText())
        item.append(self.comboBox_7.currentText())
        item.append(self.comboBox_8.currentText())
        item.append(self.comboBox_9.currentText())
        item.append(self.comboBox_10.currentText())
        item.append(self.comboBox_11.currentText())
        item.append(self.comboBox_12.currentText())
        item.append(self.comboBox_13.currentText())
        item.append(self.comboBox_14.currentText())
        item.append(self.comboBox_15.currentText())
        print(item)
        try:
            db.add_data_menu(bd1, item, cmd_handeler) # si la date existe alors y'aurra un update  
            show_popup(f"Eregistrement du menu {item[0]} reussi","Message")
        except Exception as x:
            print(x)
            show_popup(f"L'Eregistrement du menu echouee","Erreur")
    def supp(self):
        query_vals = (str(self.date_1.date().toPyDate()),)
        r = db.supp_data_menu(bd1,query_vals,cmd_handeler)
        if r > 0:
            show_popup("Suppression reussie","Message")
        else : 
            show_popup("Aucun menu trouve ","Erreur")
    def ajout_plat(self):
        f = ajouter_plats()
        f.exec()
    def supp_plat(self):
        f = supprimer_plats()
        f.exec()
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        s=compte()
        widget.addWidget(ssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def imp(self):
        dasssshs = frai()
        widget.addWidget(dasssshs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
class ajouter_plats(QDialog):
    def __init__(self):
        super(ajouter_plats,self).__init__()
        loadUi("pages\\ajouter_plats.ui",self)
        self.setFixedSize(291,265)
        self.btn_ajout.clicked.connect(self.ajout)
        self.setWindowTitle("Ajouter plats")
    def ajout(self):
        item = self.lineEdit_1.text().lower()
        choix = self.combo_choix.currentText().lower()
        if item != None:
            if choix == "gouter":
                db.add_data_plat_gout(bd1,(item,),cmd_handeler)
            elif choix == "dejeuner":
                db.add_data_plat_dej(bd1,(item,),cmd_handeler)
class supprimer_plats(QDialog):
    def __init__(self):
        super(supprimer_plats,self).__init__()
        loadUi("pages\\supprimer_plats.ui",self)
        self.setFixedSize(291,265)
        self.btn_supp.clicked.connect(self.supp)
        self.setWindowTitle("Supprimer plats")
    def supp(self):
        item = self.lineEdit_1.text().lower()
        choix = self.combo_choix.currentText().lower()
        if item != None:
            if choix == "gouter":
                db.supp_data_plat_gout(bd1,(item,),cmd_handeler)
            elif choix == "dejeuner":
                db.supp_data_plat_dej(bd1,(item,),cmd_handeler)
class perso(QDialog):
    def __init__(self):
        super(perso,self).__init__()
        loadUi("pages\employes.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.home.clicked.connect(self.pp)
        self.compte.clicked.connect(self.com)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.setItemDelegateForColumn(9, delegate)
        #boutons
        self.btn_pres.clicked.connect(self.prese)
        self.btn_export.clicked.connect(self.exporte)
        self.loadData()
        self.btn_ajout.clicked.connect(self.ajouter_ligne)
        self.btn_supp.clicked.connect(self.delete_ligne)
        self.btn_sauv.clicked.connect(self.enrg_base)

    def loadData(self):
        records = db.recup_data(bd1,"employes",cmd_handeler)
        if records != None and len(records) != 0:
            nb_colonnes = self.tableWidget.columnCount()
            rowcount = 0
            for row in records:
                self.tableWidget.setRowCount(rowcount+1)
                for col in range(0,nb_colonnes):
                    self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(str(row[col]))) 
                rowcount += 1
            db.mj_perso_dash(bd1,cmd_handeler)
            #db.mj_rev_perso_dash(bd1,cmd_handeler)
    def delete_ligne(self):
        cr = self.tableWidget.currentRow()
        if cr >= 0:
            iden  = self.tableWidget.item(cr,0)
            if iden != None:
                db.supp_data_employes(bd1,(iden.text(),),cmd_handeler)
            self.tableWidget.removeRow(cr)
    def enrg_base(self):
        nb_lignes = self.tableWidget.rowCount()
        nb_colonnes = self.tableWidget.columnCount()
        for ligne in range(nb_lignes):
            donne_ligne =[]
            for colonne in range(1,nb_colonnes - 1):
                item = self.tableWidget.item(ligne,colonne)
                if item != None:
                    donne_ligne.append(item.text())
                else:
                    donne_ligne.append("/")
            print(donne_ligne)
            try:
                donne_ligne.append(donne_ligne[5] * donne_ligne[7])
            except:
                donne_ligne.append(0)
            iden = self.tableWidget.item(ligne,0) 
            if iden != None:
                donne_ligne.append(iden.text()) # on ajoute le id a la fin si il existe  car y'aurra un update
                db.up_data_employes(bd1,tuple(donne_ligne),cmd_handeler)
            else:
                db.add_data_employes(bd1,tuple(donne_ligne),cmd_handeler)
        self.loadData()
    def ajouter_ligne(self):
        rowcount =  self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowcount+1)
    def exporte(self):
        columnHeaders = []
        for j in range(self.tableWidget.model().columnCount()): # will send the table self.tableWidget.model().columnCount()
            columnHeaders.append(self.tableWidget.horizontalHeaderItem(j).text())
        data_f = pandas.DataFrame(columns = columnHeaders)
        for row in range(self.tableWidget.rowCount()): #self.tableWidget.rowCount()
            for col in range(self.tableWidget.columnCount()):
                try:
                    data_f.at[row, columnHeaders[col]] = self.tableWidget.item(row, col).text()
                except:
                     data_f.at[row, columnHeaders[col]] = "/"
        data_f.to_excel(f'Liste_Personnel_{lyoum[:4]}.xlsx', index= False)
        show_popup(f"Fichier 'Liste_Personnel_{lyoum[:4]}.xlsx' créé avec reussite","Message")

    def com(self):
        ssfsff=compte()
        widget.addWidget(ssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def imp(self):
        dasssshs = frai()
        widget.addWidget(dasssshs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def sal(self):
        logins1 = sall()
        widget.addWidget(logins1)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def prese(self):
        logsins1 = presence()
        widget.addWidget(logsins1)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
class sall(QDialog):
    def __init__(self):
        super(sall,self).__init__()
        loadUi("pages\employes_salaire.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.bouton_presence.clicked.connect(self.prese)
        self.pers.clicked.connect(self.personel)
        self.bouton_employes.clicked.connect(self.personel)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.compte.clicked.connect(self.com)  
        self.home.clicked.connect(self.pp)
        self.loadData() 
    '''def ajouter_ligne(self) :
        rowcount =  self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowcount+1)
        
        self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(rowcount[0])))
        item = QtWidgets.QTableWidgetItem("Payé")
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsTristate)
        if rowcount[0] == 1:
            item.setCheckState(QtCore.Qt.Checked)  
        else:
            item.setCheckState(QtCore.Qt.Unchecked)  
        self.tableWidget.setItem(rowcount, 0, item)'''


    def loadData(self) : 
        records = db.recup_data(bd1,"employes",cmd_handeler)
        nb_colonnes = self.tableWidget.columnCount()
        rowcount = 0
        try:
            for row in records:
                self.tableWidget.setRowCount(rowcount+1)
                for col in range(0,nb_colonnes-1):
                    self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(str(row[col])))
                item = QtWidgets.QTableWidgetItem("Payé")
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsTristate)
                if row[0] == 1:
                    item.setCheckState(QtCore.Qt.Checked)  
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)  
                self.tableWidget.setItem(rowcount, 0, item)
                print(item)
                rowcount += 1
                print(row)
        except Exception as x :
            print(x)  
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def com(self):
        ssfsff=compte()
        widget.addWidget(ssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        sssfsff=dashboard()
        widget.addWidget(sssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    def imp(self):
        dasssshs = frai()
        widget.addWidget(dasssshs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        s=perso()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def prese(self):
        logsins1 = presence()
        widget.addWidget(logsins1)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)
    '''def loadData(self):
        records = db.recup_data(bd1,"employes",cmd_handeler)
        print("coucou madame ",records)
        nb_colonnes = self.tableWidget.columnCount()
        rowcount = 0
        try:
            for row in records:
                self.tableWidget.setRowCount(rowcount+1)
                print(row)
                for col in range(0,nb_colonnes-1):
                    self.tableWidget.setItem(rowcount,col,QtWidgets.QTableWidgetItem(str(row[col])))
                item = QtWidgets.QTableWidgetItem("Payé")
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsTristate)
                if row[0] == 1:
                    item.setCheckState(QtCore.Qt.Checked)  
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)  
                self.tableWidget.setItem(rowcount, 0, item)
                print(item)
                rowcount += 1
                print(row)
        except Exception as x :
            print(x)'''
class presence(QDialog):
    def __init__(self):
        super(presence,self).__init__()
        loadUi("pages\employes_presence.ui",self)
        self.deco.clicked.connect(self.deconnecter)
        self.btn_emlp.clicked.connect(self.personel)
        self.pers.clicked.connect(self.personel)
        self.enfant.clicked.connect(self.ennfant)
        self.menu.clicked.connect(self.menus)
        self.tabl.clicked.connect(self.dashboard_f)
        self.inve.clicked.connect(self.invse)
        self.compte.clicked.connect(self.com)
        self.home.clicked.connect(self.pp)
    def pp(self):
        pagePrincipale = page_principal()
        widget.addWidget(pagePrincipale)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)  
    def com(self):
        ssfsff=compte()
        widget.addWidget(ssfsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def invse(self):
        s=inventaire()
        widget.addWidget(sqssds)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def dashboard_f(self):
        dash = dashbord()
        widget.addWidget(dash)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    def imp(self):
        dasssshs = frai()
        widget.addWidget(dasssshs)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def menus(self):
        s=menu()
        widget.addWidget(s)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def ennfant(self):
        fsff=enfant()
        widget.addWidget(fsff)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def personel(self):
        sqsd=perso()
        widget.addWidget(sqsd)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def sal(self):
        logins1 = sall()
        widget.addWidget(logins1)
        widget.setFixedSize(1100,700)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def deconnecter(self):
        login1 = login()
        widget.addWidget(login1)
        widget.setFixedSize(450,400)
        widget.setCurrentIndex(widget.currentIndex()+1)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    login1 = login()
    widget = QtWidgets.QStackedWidget()
    widget.setWindowTitle("LE ROI KLIFA")
    widget.addWidget(login1)
    widget.setFixedSize(450,400)
    qr = widget.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    widget.move(qr.topLeft())

    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        cmd_handeler.close()
        sys.exit(app.exec_())
        print("exiting")