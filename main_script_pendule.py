# name:      main_script_pendule
# author:    Lundrih (https://github.com/EyumLundrih)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# importation du module PyOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# importation du module contenant la class générée par Qtdesigner
import Equa_diff
from pendule_designer import Ui_Dialog

from Equa_diff import *

Po = Equa_diff.postition(l, Oi)  # position solution de notre equa diff sous forme de liste


# chaque coordonnee est un triplet (x,y,z), avec x postion horizontale, y position verticale et z la profondeur

class mainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.angle = 0  # utilisé pour tourner la camera
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.openGLWidget = self.ui.openGLWidget  # raccourci
        self.increment = 0  # on cree un increment qui va nous permettre de nous deplacer dans la liste de coordonnes cree par la resolution de l'equa diff
        self.graphicsView = self.ui.graphicsView  # raccourci
        self.graphicsView2 = self.ui.graphicsView_2  # raccourci
        self.graphicsView3 = self.ui.graphicsView_3  # raccourci
        self.graphicsView4 = self.ui.graphicsView_4  # raccourci

    def setupUI(self):  # initialisation de la vue et création du timer
        self.openGLWidget.initializeGL()  # appelé au premier affichage uniquement
        self.openGLWidget.resizeGL(800, 600)
        self.openGLWidget.paintGL = self.paintGL  # raccourci
        timer = QTimer(self)  # Le timer
        timer.timeout.connect(self.openGLWidget.update)  # appelle la fonction en argument (sans parenthèse )
        # ici update appelle la fonction resizeGL et paintGL
        timer.start(1)  # lance le timer pour un temps de 1 ms entre chaque timeout

    def paintGL(self):
        self.increment += 1
        x, y, z = Po[self.increment]  # on recupere les coodonnes sur x,y,z
        self.angle += 0
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)  # définition de la couleur du font,le dernier nombre est l'alpha/la transparence

        glEnable(GL_POINT_SMOOTH)  # rond plus smooth, tout ou rien
        glPointSize(40)  # taille initiale
        glColor3f(0, 1, 0)  # couleur du point en (r,g,b)
        # pour avoir un pendule rgb
        '''if self.increment%30==0:
            glColor3f(1, 0, 0)  
        elif self.increment%30==10:
            glColor3f(0,1,0)
        elif self.increment%30==20:
            glColor3f(0,0,1)'''
        # on affichage de la "corde" a l'aide d' un polygone a 4 cotes
        glBegin(GL_POLYGON)
        glVertex3f(0.015, 0, 0)
        glVertex3f(-0.015, 0, 0)
        glVertex3f(x - 0.015, y - 0.015, z)
        glVertex3f(x + 0.015, y + 0.0015, z)
        glEnd()

        glBegin(GL_POINTS)  # début de l'affichage
        glVertex3f(x, y, z)  # affichage du point
        glEnd()  # fin de l'affichage

        glMatrixMode(GL_PROJECTION)  # charge la matrice de projection
        """ on change ici les options de la projection sur l'écran """
        glLoadIdentity()  # charge une matrice identité
        gluPerspective(45.0, 4.0 / 3.0, 1, 40)  # fov , ratio , distance de vue proche, distance de vue de loin

        glMatrixMode(GL_MODELVIEW)  # charge la matrice de caméra
        """ on change ici la position de la caméra """
        glLoadIdentity()  # charge une matrice identité
        gluLookAt(0, -0.5, 4,
                  0, -0.2, 0,
                  0, 1, 0)
        # coordonnées de la position de la caméra  ,coordonnées du point vers lequel elle est dirigée, axe vertical de la caméra
        glRotatef(-pi / 4, 0, 0, 1)  # permet de tourner la caméra autour de l'axe x ,y ,z

        # glTranslatef( 0, 0.001*self.angle, 0)#permet de déplacer la camera ,
        # mais est impacté par la rotation de la camera

    def graph(self):
        self.graphicsView.plot(Equa_diff.temps, Equa_diff.l_angle, pen=3)  # on affiche les graphes de position
        self.graphicsView2.plot(Equa_diff.temps, Equa_diff.ec, pen=1)  # d'energie cinetique
        self.graphicsView3.plot(Equa_diff.temps, Equa_diff.ep, pen=5)  # d'energie potentielle
        self.graphicsView4.plot(Equa_diff.l_angle, Equa_diff.vsol1, pen=9)  # le portrait de phase


app = QApplication(sys.argv)
window = mainWindow()
window.graph()
window.setupUI()  # on initialize le QOpenGLwidget
window.show()
sys.exit(app.exec_())
