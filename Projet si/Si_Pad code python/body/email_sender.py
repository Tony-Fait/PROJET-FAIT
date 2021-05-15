# -*- coding: utf-8 -*-
# Import necessary modules
import sys, smtplib
from email.message import EmailMessage

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
QPushButton, QLineEdit, QTextEdit, QDialog, QMessageBox, QDialogButtonBox,
QStatusBar, QGridLayout, QHBoxLayout, QVBoxLayout)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Boite_de_dialogue_mot_de_passe(QDialog):
    def __init__(self, parent):
        
        super().__init__()
        """[INFO] Cette ligne de code vÃ©rifie si l'envoie et la rÃ©ception sont non vide. \
            Il y'a d'autres vÃ©rification que vous pouvez faire comme par exemple l'existence \
                du @ ou si l'extension du mail est valide."""
        
        if parent.address_expediteur.text() != "" and parent.address_receveur.text() != "":
            
            self.setWindowTitle("Soumettre mot de passe Gmail")
            self.setFixedSize(300, 100)
            self.setModal(True)
            label_entrer_mot_de_passe = QLabel("Entrer mot de passe:")
            self.ligne_entrer_mot_de_passe = QLineEdit()
            self.ligne_entrer_mot_de_passe.setEchoMode(QLineEdit.Password)
            
        # Create nested layout for widgets to enter the password and for the QDialogButtonBox
            mot_de_passe_h_box = QHBoxLayout()
            mot_de_passe_h_box.addWidget(label_entrer_mot_de_passe)
            mot_de_passe_h_box.addWidget(self.ligne_entrer_mot_de_passe)
            bouttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            boite_bouttons = QDialogButtonBox(bouttons)
            boite_bouttons.accepted.connect(self.accept)
            boite_bouttons.rejected.connect(self.reject)
            dialog_v_box = QVBoxLayout()
            dialog_v_box.addLayout(mot_de_passe_h_box)
            dialog_v_box.addWidget(boite_bouttons)
            self.setLayout(dialog_v_box)
        
        else:
            QMessageBox.information(self, "Information Manquante",
            " L'nformation des expediteur ou Receveur est vide.", QMessageBox.Ok)
    
class EmailGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.Initialisation()
        
    def Initialisation(self):
        
        """Initialise la fenetre et affiche son contenu."""
        self.setMinimumSize(800, 500)
        self.setWindowTitle('Email GUI')
        self.set_up_fenetre()
        self.show()
        
    def set_up_fenetre(self):
        
        """Organise les widgets différentes saisies del'email."""
        label_fenetre = QLabel("Envoyer un Simple Email")
        label_fenetre.setFont(QFont("Courier", 24))
        label_fenetre.setAlignment(Qt.AlignCenter)
        label_expediteur = QLabel("De:")
        self.address_expediteur = QLineEdit()
        self.address_expediteur.setPlaceholderText("Votre_email@gmail.com")
        label_receveur = QLabel("A:")
        self.address_receveur  = QLineEdit()
        self.address_receveur .setPlaceholderText("ami@email.com")
        label_sujet = QLabel("Sujet:")
        self.line_sujet = QLineEdit()
        
        # Layout pour les widgets expediteur, receveur, sujet
        
        header_grid = QGridLayout()
        header_grid.addWidget(label_expediteur, 0, 0)
        header_grid.addWidget(self.address_expediteur, 0, 1)
        header_grid.addWidget(label_receveur, 1, 0)
        header_grid.addWidget(self.address_receveur, 1, 1)
        header_grid.addWidget(label_sujet, 2, 0)
        header_grid.addWidget(self.line_sujet, 2, 1)
        self.corps_de_l_email = QTextEdit() # widget de saisie pour la creation de contenues
        Boutton_envoi = QPushButton("Envoi")
        Boutton_envoi.clicked.connect(self.saisie_du_mot_de_passe)
        enBas_h_box = QHBoxLayout()
        enBas_h_box.addWidget(QWidget(), 1)
        enBas_h_box.addWidget(Boutton_envoi)
        
        # widget emboîté pour tous les widgets et layouts
        
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(label_fenetre)
        main_v_box.addSpacing(10)
        main_v_box.addLayout(header_grid)
        main_v_box.addWidget(self.corps_de_l_email)
        main_v_box.addLayout(enBas_h_box)
        conteneur = QWidget()
        conteneur.setLayout(main_v_box)
        self.setCentralWidget(conteneur)
        self.barre_d_etat = QStatusBar(self)
        self.setStatusBar(self.barre_d_etat) # Crée une barre d'état
        
    def saisie_du_mot_de_passe(self):
        
        """Crée une instance de la classe de la Boite_de_dialogue_mot_de_passe et saisie le mot de passe du Gmail."""
        self.dialog_mot_de_passe = Boite_de_dialogue_mot_de_passe(self)
        
        if self.dialog_mot_de_passe.exec_() and self.dialog_mot_de_passe.ligne_entrer_mot_de_passe.text() != "":
            
            self.dialog_mot_de_passe.close()
            self.Envoi_de_l_Email()
            
        else:
            pass

    def Envoi_de_l_Email(self):
        
        """Compose les en-têtes et contenus de l'email. Utilise smtplib to login votre
        compte Gmail et envoie un email. Le succès ou les erreurs seront affichés dans la barre d'etat convenablement
        """
        # Definit les en-têtes et contenu de l'email
        message = EmailMessage()
        message['Subject'] = self.line_sujet.text()
        message['From'] = self.address_expediteur.text()
        message['To'] = self.address_receveur.text()
        # Converttion du texte  du QTextEdit en HTML
        message.add_alternative(self.corps_de_l_email.toHtml(), subtype="html")
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            try:
                
                # Login to your Gmail username and password
                
                smtp.login(self.address_expediteur.text(), self.dialog_mot_de_passe.ligne_entrer_mot_de_passe.text())
                smtp.send_message(message)
                
                # Affiche feedback dans la barre d'etat et efface les widgets de saisie
                
                self.barre_d_etat.showMessage("Email envoyé!", 5000)
                self.line_sujet.clear()
                self.address_receveur.clear()
                self.corps_de_l_email.clear()
                
            except smtplib.SMTPResponseException as error:
                
                message_d_erreur = "Email échoué: {}, {}".format(error.smtp_code, error.smtp_error)
                self.barre_d_etat.showMessage(message_d_erreur, 20000) # Affiche l'erreur pendant 20 secondes

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailGUI()
    sys.exit(app.exec_())