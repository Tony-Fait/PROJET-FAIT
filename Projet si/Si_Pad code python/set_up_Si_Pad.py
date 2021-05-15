# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PyQt5.QtWidgets import (QApplication, QAction, QWidget, QPushButton, QTextEdit, QMainWindow, QMdiSubWindow, QInputDialog, QLabel,
                             QMessageBox, QFileDialog, QDialog, QFontDialog, QColorDialog, QDial, QVBoxLayout)

from PyQt5.QtCore import *
from PyQt5.QtCore import QFileInfo, Qt

from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon, QFont, QPixmap, QTextCursor

from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog

#la classe de ma page principale se trouve dans le dossier body
from body.Page_principale_Si_Pad import grande_fenetre_principale
from body.email_sender import Boite_de_dialogue_mot_de_passe, EmailGUI #simportation des classes 

import sys, os


class editeur(QMainWindow): # la classe editeur hérite de QMainWindow

    # ----------------------- le constructeur ----------------------------------------
    
    def __init__(self, title = "Si-Pad", parent = None):
    
        super(editeur, self).__init__(parent)
        self.titre = title
    
        #la classe de ma page principale et les paramètres de sa classe enfant
    
        self.fen1 = grande_fenetre_principale() #instance de la grande_fenetre_principale
        self.fen1.creation(self)
        
        self.setWindowTitle(self.titre)
        self.setWindowIcon(QIcon('Images/SiPad'))
    
        self._initSignaux() # je l'appelle dans le constructeur sinon ça ne marchera pas
        
        self.chemin_d_acces_au_fichier = None
        
        self.isFileOpen = False #fichier déjà ouvert
        self.isFileSaved = False #fichier déjà sauvegardé
        


    def _initSignaux(self):
        
        #Slots et signaux pour definir l'action des boutons
        #triggered pour enclencher, connect pour connecter la variable action_Ouverture 
        #a la méthode Ouvrir_fichier


        #j'appelle les boutons de ma grande_fenetre_principale() et triggered.connect permet de les lier aux fonctions que je vais créer
        
        # -------------------------- pour la barre d'outils ------------------------------------------------
        
        self.fen1.actionnouveau.triggered.connect( self.Nouveau_fichier )
        
        self.fen1.actionouvrir.triggered.connect( self.Ouvrir_fichier )
        
        self.fen1.actionsauvegarder.triggered.connect( self.Sauvegarder_fichier )
        
        self.fen1.actionEnregistrer_Sous.triggered.connect( self.Sauvegarder_Sous )
        
        self.fen1.actionundo.triggered.connect( self.fen1.textEdit.undo )
    
        self.fen1.actionredo.triggered.connect( self.fen1.textEdit.redo )
        
        self.fen1.pushButton_couleur.clicked.connect( self.Couleur_de_la_police )
        
        self.fen1.pushButton_font.clicked.connect( self.choix_de_la_police )

        self.fen1.pushButton_recherche.clicked.connect( self.rechercher_du_texte )
    
        self.fen1.actionimprimer.triggered.connect( self.impression )
        
        self.fen1.actionprevisualisation.triggered.connect( self.previsualisation )
        
        # ---------------------------- pour tab accueil -------------------------------------
        
        self.fen1.pushButton_copier.clicked.connect( self.fen1.textEdit.copy) #pour copier
    
        self.fen1.pushButton_coller.clicked.connect( self.fen1.textEdit.paste )
    
        self.fen1.pushButton_couper.clicked.connect( self.fen1.textEdit.cut )
        
        self.fen1.pushButton_surbrillance.clicked.connect( self.Surbrillance_ )
        
        self.fen1.actionA_propos.triggered.connect( self.Pour_a_propos )
        
        self.fen1.pushButton_paint.clicked.connect( self.lancement_de_paint )
        
        self.fen1.actionemail.triggered.connect( self.email_militaire )
        
        self.fen1.pushButton_justifyLeft.clicked.connect( self.aligner_a_gauche )
        
        self.fen1.pushButton_justifyCenter.clicked.connect( self.aligner_au_centre )
        
        self.fen1.pushButton_justifyRight.clicked.connect( self.aligner_a_droite )
        
        self.fen1.pushButton_insert_image.clicked.connect( self.image_ )
        
        self.fen1.pushButton_date_et_heure.clicked.connect( self.date_et_heure )
        
        self.fen1.actionQuitter.triggered.connect( self.quitter )
        
        
        # ------------------ pour tab afficher -------------------------#########################
        
        self.fen1.pushButton_close.clicked.connect( self.Suppression_texte )
        
        self.fen1.pushButton_pdf.clicked.connect( self.Conversion_en_pdf )
        
        self.fen1.pushButton_zoom_plus.clicked.connect( self.pour_zoom_plus )
        
        self.fen1.pushButton_zoom_moins.clicked.connect( self.pour_zoom_moins )
        
        
       
        
    # ------------------------------fonction nouveau fichier --------------------------------------------

    def Nouveau_fichier(self):

        os.popen("python set_up_Si_Pad.py") #os.popen est un script pour generer une nouvelle fenetre identique au programme plus l'annuaire     
    

    def Ouvrir_fichier(self):

        """
      Ouvrir un fichier et afficher son contenu.
      """
        try:
            self.nom_du_fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier","", "Tous les documents wordpad (*.txt *.docx *.odt *.rtf);;\
                                                                                        Document au format RTF (*.rtf );;\
                                                                                        Document texte OOXML ( *.docx );;\
                                                                                        Document texte ODT( *.odt );;\
                                                                                        Document texte (*.txt );;\
                                                                                        Document texte MS-DOS (*.txt );;\
                                                                                        Document texte Unicode (*.txt );;\
                                                                                        Tous les fichiers(*.*)")
            if self.nom_du_fichier:
                
                ############## pour pouvoir enregistrer si un fichier a été ouvert. A voir dans la fonction Sauvegarder_fichier(self)
                self.isFileOpen = True
                ##############
                
                           
                with open(self.nom_du_fichier, 'r') as f:
                    
                    fichier_texte = f.read()
                    self.fen1.textEdit.setText(fichier_texte)
                    self.fen1.textEdit.setHtml(fichier_texte)
                    self.fen1.textEdit.toHtml()
                   
                    
            else:
                QMessageBox.information(self, "Erreur", "Impossible d'ouvrir le fichier!", QMessageBox.Ok)
        except UnicodeDecodeError:
            QMessageBox.information(self, "Erreur", "Impossible d'ouvrir ce fichier car l'encodage différent de celui de Si_Pad!\n \
            Pour tous les documents différents de l'extension(.txt), Essayer d'ouvrir un document edité par Si_Pad lui-même", QMessageBox.Ok)
            
    #-------------------------- fonction de sauvegarde ----------------------------------------
    
    def Sauvegarder_fichier(self):

        import time # pour la date et l'heure
        try:
            
            if self.isFileOpen == True: #si un fichier a été ouvert alors 
                try:
                    with open( self.nom_du_fichier, "w") as f:
                        f.write( self.fen1.textEdit.toPlainText() ) #toHtml() )
                        f.close()
                        self.fen1.statusBar.showMessage(self.nom_du_fichier + " a été enregistré " + time.strftime("%d/%m/%y %H:%M:%S",time.localtime()), 3600)
                        self.isFileSaved = True
                
                except not f:
                    self.fen1.statusBar.showMessage(" Impossible d'enregistrer ")
            
            else: # si aucun fichier n'a été ouvert alors
                
                """
                Si le boutton enregistré est appuyé, une boîte de dialogue s'affiche et enregistre le champ de texte 
                en fichier text ou autres.
                """
                
                try:
        
                    options = QFileDialog.Options()
        
                    # nous avons accès au champ texte de la grande_fenetre_principale grâce à
                    fichier_texte = self.fen1.textEdit.toPlainText()
        
                    nom_du_fichier, _ = QFileDialog.getSaveFileName(self, 'Sauvegarder le fichier', "/", " Document au format RTF (*.rtf );;\
                                                                    Document texte OOXML ( *.docx );;\
                                                                    Document texte ODT( *.odt );;\
                                                                    Document texte (*.txt );;\
                                                                    Document texte MS-DOS (*.txt );;\
                                                                    Document texte Unicode (*.txt );;\
                                                                    Fichier html (*.htm *.html);;\
                                                                    Tous les fichiers(*.*)", options = options)
                    if nom_du_fichier:
        
                        # on ouvre le fichier obtenu grace à la boçite de dialogue en écriture
                        with open(nom_du_fichier, 'w') as f:
        
                            # on peut maintenant écrire à l'intérieur
                            f.write(fichier_texte)
        
                            # nous avons accès à la barre d'état de la grande_fenetre_principale grâce à
                            self.fen1.statusBar.showMessage(nom_du_fichier + " a été enregistré " + time.strftime("%d/%m/%y %H:%M:%S",time.localtime()), 3600)
                            self.isFileSaved = True
                
                except not nom_du_fichier:
                    self.fen1.statusBar.showMessage(" Rien a été enregistré ")
        
        except TypeError:
            QMessageBox.information(self, "Erreur", "Opération impossible essayer de convertir le texte en pdf dans tab affichage!", QMessageBox.Ok)
            
            
    def Sauvegarder_Sous(self):

        import time # pour la date et l'heure

        """
      si le boutton enregistré est appuyé, une boîte de dialogue s'affiche et enregistre le champ de texte 
      en fichier text ou autres.
      """

        try:
            try:
    
                options = QFileDialog.Options()
    
                # nous avons accès au champ texte de la grande_fenetre_principale grâce à
                fichier_texte = self.fen1.textEdit.toPlainText()
    
                nom_du_fichier, _ = QFileDialog.getSaveFileName(self, 'Sauvegarder le fichier', "/", " Document au format RTF (*.rtf );;\
                                                                Document texte OOXML ( *.docx );;\
                                                                Document texte ODT( *.odt );;\
                                                                Document texte (*.txt );;\
                                                                Document texte MS-DOS (*.txt );;\
                                                                Document texte Unicode (*.txt );;\
                                                                Fichier html (*.htm *.html);;\
                                                                Tous les fichiers(*.*)", options = options)
                if nom_du_fichier:
    
                    # on ouvre le fichier obtenu grace à la boçite de dialogue en écriture
                    with open(nom_du_fichier, 'w') as f:
    
                        # on peut maintenant écrire à l'intérieur
                        f.write(fichier_texte)
    
                        # nous avons accès à la barre d'état de la grande_fenetre_principale grâce à
                        self.fen1.statusBar.showMessage(nom_du_fichier + " a été enregistré " + time.strftime("%d/%m/%y %H:%M:%S",time.localtime()), 3600)
    
            except not nom_du_fichier:
                self.fen1.statusBar.showMessage(" Rien a été enregistré ")
                
        except TypeError:
            QMessageBox.information(self, "Erreur", "Opération impossible essayer de convertir le texte en pdf dans tab affichage!", QMessageBox.Ok)
            
    
    # --------------------- fonction couleur de la police ---------------------------------------

    def Couleur_de_la_police(self):

        """
        choisir la couleur du texte
        """
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            self.fen1.textEdit.setTextColor(couleur)
            
            
            
    # --------------------- fonction choix de la police ---------------------------------------

    def choix_de_la_police(self):
        """
        choisir la police
        """
        courant = self.fen1.textEdit.currentFont()
        police, ok = QFontDialog.getFont(courant, self, options = QFontDialog.DontUseNativeDialog)

        if ok:
            self.fen1.textEdit.setCurrentFont(police) # Use setFont() to set all  text to one type of font
    
    
    # ----------------------------------- fonction rechercher ---------------------------------------

    def rechercher_du_texte(self):
        """
        Rechercher un element dans QTextEdit widget
        """
        # Afficher input dialog et demander à l'user d'écrire le mot à chercher

        trouve_texte, ok = QInputDialog.getText(self, "recherche de texte", "Trouve:")
        extra_selections = []

        # vérifier si le texte peut être modifier

        if ok and not self.fen1.textEdit.isReadOnly():

            # set the cursor in the textedit field to the beginning

            self.fen1.textEdit.moveCursor(QTextCursor.Start)
            couleur = QColor(Qt.yellow)

            # les occurences du texte

            while(self.fen1.textEdit.find(trouve_texte)):

                # utiliseExtraSelections pour marquer le texte que tu cherches en jaune


                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(couleur)

                # établi le curseur de la selection

                selection.cursor = self.fen1.textEdit.textCursor()

                # Ajoute selection à la liste

                extra_selections.append(selection)

                # Hsurbrillance de selections danstext edit widget

            for i in extra_selections:
                self.fen1.textEdit.setExtraSelections(extra_selections)

            
            
            
    # ----------------------------------- fonction imprimer ---------------------------------------

    def impression(self):

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.fen1.textEdit.print_(printer)
            
            
    def previsualisation(self):

        imprimeur = QPrinter(QPrinter.HighResolution)
        boite_de_dialogue_previsualisation = QPrintPreviewDialog(imprimeur, self)
        boite_de_dialogue_previsualisation.paintRequested.connect(self.previsualisation_2)
        boite_de_dialogue_previsualisation.exec_()

    def previsualisation_2(self, imprimeur):

        self.fen1.textEdit.print_(imprimeur)            
            
            
    # --------------------- fonction de suppression ---------------------------------------

    def Suppression_texte(self):
        """
        Si le bouton est cliqué, affiche la boîte de dialogue demandant à l'user d'effacer le texte ou pas.
        """
        reponse = QMessageBox.question(self, "Effacer le texte", "Voulez-vous tout effacer?", QMessageBox.No | QMessageBox.Yes, QMessageBox.Yes)
        if reponse == QMessageBox.Yes:

            # puisque c'est le champ texte de la grande_fenetre_principale qui doit etre vidée alors
            self.fen1.textEdit.clear()

        else:
            pass
        
    # --------------------- fonction Conversion_en_pdf ---------------------------------------
    
    def Conversion_en_pdf(self):

        fn, _ = QFileDialog.getSaveFileName(self, "exporter en pdf", None, "PDF files (.pdf)")
        if fn != '':
            if QFileInfo(fn).suffix() == "":
                fn += '.pdf'

            imprimeur = QPrinter(QPrinter.HighResolution)
            imprimeur.setOutputFormat(QPrinter.PdfFormat)
            imprimeur.setOutputFileName(fn)
            self.fen1.textEdit.document().print_(imprimeur)
            
            
    def Pour_a_propos(self):
        
        """
        afficher une information
        """
        QMessageBox.about(self, "A propos de SI-Pad", 
                          "<p>SI-PAD est un editeur de texte développé par l'équipe 13.</p>")            
            
    
    def Surbrillance_(self):
        
        """
        choix de la couleur de surbrillance
        """
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            self.fen1.textEdit.setTextBackgroundColor(couleur)
     
     
            
    def lancement_de_paint(self):
        
        import subprocess
        
        # chemin d'accès du logiciel à ouvrir
        chemin_d_acces = 'C:\Windows\system32\mspaint.exe' # ou '/bin/myapp' sous Linux
        
        subprocess.check_call( ('start', chemin_d_acces), shell = True )    
            
            
    def email_militaire(self):
        self.fen2 = EmailGUI() #fonction des classes de email_sender
        self.fen2.Initialisation()
        
        pass
    
    def quitter(self):
        sys.exit()
    
    #pour les alignements#########################################################
    
    def aligner_a_gauche(self):
        self.fen1.textEdit.setAlignment(Qt.AlignLeft)
        pass
    
    def aligner_au_centre(self):
        self.fen1.textEdit.setAlignment(Qt.AlignCenter)
        pass
            
    def aligner_a_droite(self):
        self.fen1.textEdit.setAlignment(Qt.AlignRight)
        pass
    #################################################################################
    
    
    ##########################################################################################
    def Sauvegarder_le_fichier_courant(self):
        if not self.chemin_d_acces_au_fichier:
            nouveau_chemin_d_acces_au_fichier, filter_type = QFileDialog.getSaveFileName(self, "Enregistrer ce fichier en tant que...", "", "Tous les fichiers (*.*)")
            if nouveau_chemin_d_acces_au_fichier:
                self.chemin_d_acces_au_fichier = nouveau_chemin_d_acces_au_fichier
            else:
                self.Message_d_alerte_chemin_d_acces_invalide()
                return False
        contenu_du_fichier = self.fen1.textEdit.toPlainText()
        with open(self.chemin_d_acces_au_fichier, "w") as f:
            f.write(contenu_du_fichier)
        self.titre.setText(self.chemin_d_acces_au_fichier)

    def closeEvent(self, event):
        messageBox = QMessageBox()
        title = "Quitter l'Application?"
        message = "ATTENTION !!\n\nSi vous quittez sans sauvegarder, les modifications seront perdues.\n\nSuvegarder avant de quitter?"
        
        if self.isFileSaved == False: # Demander au programme si aucun n'enregistrement n'a été fait alors qu'il incite à le faire
            
            reponse = messageBox.question(self, title, message, messageBox.Yes | messageBox.No |
                    messageBox.Cancel, messageBox.Cancel)
            if reponse == messageBox.Yes:
                return_value = self.Sauvegarder_le_fichier_courant()
                if return_value == False:
                    event.ignore()
            elif reponse == messageBox.No:
                event.accept()
            else:
                event.ignore()
            
    def Message_d_alerte_chemin_d_acces_invalide(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Fichier invalide")
        messageBox.setText("Aucun enregistrement effectué.")
        messageBox.exec()
        
    ###############################################################################################""""""
            
    # pour zoomer #####################################################################################""
    
    def pour_zoom_plus(self):
        self.fen1.textEdit.zoomIn(1)
    
    def pour_zoom_moins(self):
        self.fen1.textEdit.zoomOut(1)
    
    #############################################################################################################
    
    def image_(self):
       
        filePath, _ = QFileDialog.getOpenFileName(self, "Selectionnez une image", ".", "Image Files(*.png *.gif *.jpg *jpeg *.bmp)")
        
        #if not filePath.isEmpty():
        if filePath:
            self.insertImage(filePath)
        
    def insertImage(self, filePath):
        self.fen1.textEdit.setPlainText
        imageUri = QtCore.QUrl("file://{0}".format(filePath))
        image    = QtGui.QImage(QtGui.QImageReader(filePath).read())

        self.fen1.textEdit.document().addResource(QtGui.QTextDocument.ImageResource, imageUri, QtCore.QVariant(image))

        imageFormat = QtGui.QTextImageFormat()
        imageFormat.setWidth(image.width())
        imageFormat.setHeight(image.height())
        imageFormat.setName(imageUri.toString())

        textCursor = self.fen1.textEdit.textCursor()
        textCursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        textCursor.insertImage(imageFormat)

        # Il cachera le curseur
        blankCursor = QtGui.QCursor(QtCore.Qt.BlankCursor)
        self.fen1.textEdit.setCursor(blankCursor)
        
        
    def date_et_heure(self):
        import time # pour la date et l'heure
    
        f = time.strftime("%d/%m/%y %H:%M:%S",time.localtime())
        self.fen1.textEdit.toPlainText()
        cursor = self.fen1.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        cursor.insertText(f)
        
        
    
                  
# instruction final
if __name__ == "__main__":

    #chaque programme doit disposer d’une instance de QApplication gerant l’ensemble des widgets
    mon_application = QApplication(sys.argv)

    edi = editeur() #création d'une instance de editeur

    edi.show() #pour afficher la classe

    sys.exit(mon_application.exec_()) #boucle principale de traitement des evenements 
