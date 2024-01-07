from copy import deepcopy
from PIL import Image, ImageTk
import tkinter as Tk

class echequier:
    def __init__(self):
        self.tab = [] ## contient toutes les pieces
        self.hist = [] ## garde en memoire les coups précédents
        self.echec = False  ### ne suprime pas les pieces lorsque il est True

    def case_vide(self, x, y):
        """
        x, y : des nombres entiers positifs definissant une position sur l'echequier
        renvoie False si une piece est presente sur le x et le y renseigné
        """
        for piece in self.tab:
            if piece.x == x and piece.y == y:
                return False ### case n'est pas vide
        return True ## case est vide
    
    def case_occupe_ennemi(self, x, y, couleur):
        """
        x, y des nombres entiers positifs definissant une position sur l'echequier et couleur une chaine de caractere definissant la couleur de la piece
        renvoie False si une piece se trouve sur le x et le y et que sa couleur est similaire
        """
        for piece in self.tab:
            if piece.x == x and piece.y == y and piece.couleur == couleur:
                return False
        return True

    def generer_plateau(self):
        ## roi
        self.tab.append(roi(3, 0, 'BLANC', "piece echec\\roi_blanc.png"))
        self.tab.append(roi(3, 7, 'NOIR', "piece echec\\roi_noir.png"))
        for i in range(8): ### pion
            self.tab.append(pion(i, 1, 'BLANC', "piece echec\\pion_blanc.png"))
        for i in range(8):
            self.tab.append(pion(i, 6, 'NOIR', "piece echec\\pion_noir.png"))
        for i in range(2): ### tour
            self.tab.append(tour(i*7, 0, 'BLANC', "piece echec\\tour_blanc.png"))
        for i in range(2):
            self.tab.append(tour(i*7, 7, 'NOIR', "piece echec\\tour_noir.png"))
        # fou
        self.tab.append(fou(2, 0, 'BLANC', "piece echec\\fou_blanc.png"))
        self.tab.append(fou(5, 0, 'BLANC', "piece echec\\fou_blanc.png"))
        self.tab.append(fou(2, 7, 'NOIR', "piece echec\\fou_noir.png"))
        self.tab.append(fou(5, 7, 'NOIR', "piece echec\\fou_noir.png"))
        ## cavalier
        self.tab.append(cavalier(1, 0, 'BLANC', "piece echec\\cavalier_blanc.png"))
        self.tab.append(cavalier(6, 0, 'BLANC', "piece echec\\cavalier_blanc.png"))
        self.tab.append(cavalier(1, 7, 'NOIR', "piece echec\\cavalier_noir.png"))
        self.tab.append(cavalier(6, 7, 'NOIR', "piece echec\\cavalier_noir.png"))
        ### dame
        self.tab.append(dame(4, 0, 'BLANC', "piece echec\\dame_blanc.png"))
        self.tab.append(dame(4, 7, 'NOIR', "piece echec\\dame_noir.png"))

    def case_piece(self, x, y):
        """
        x, y une position sur l'echequier
        renvoie la piece presente a la position x, y
        """
        for piece in self.tab:
            if piece.x == x and piece.y == y:
                return piece

    def ajouter_piece(self, piece):
        self.tab.append(piece)

    def retirer_piece(self, pos):
        self.tab.pop(pos)
    
    def ajout_historique(self):
        """
        ajoute dans une liste la position actuelle de toutes les piece
        """
        self.hist.append([])
        for piece in self.tab:
            self.hist[-1].append([piece.x, piece.y, piece])
    
    def reorganisation_historique(self, version):
        """
        version , un entier definisant la version de l'historique a mettre
        met a jour la position de toute les pieces a partir de la position de l'historique / en gros on reviens en arriere
        """
        if self.hist != []:
            self.tab = []
            for piece in self.hist[version]:
                self.tab.append(piece[2])
                self.tab[-1].x, self.tab[-1].y = piece[0], piece[1]
    
    def mange_piece(self, x, y):
        """
        x, y : deux entiers positifs.
        suprime l'objet present sur le x et le y renseigné
        """
        if self.case_vide(x, y) != True and self.echec == False:
            self.tab.pop(self.tab.index(self.case_piece(x, y)))
        
    def est_echec(self, roi):
        """
        roi : l'objet correspondant au roi.
        renvoi False si le roi est en echec, True sinon
        """
        self.echec = True
        for piece in self.tab:
            if piece.couleur != roi.couleur:
                if piece.peut_manger().count([roi.x, roi.y]):
                    return False
        self.echec = False
        return True
    
    def coup_possibles(self, roi):
        self.echec = True
        print(roi.peut_manger())
                
    
    def case_piece_hist(self, x, y, v=-2):
        """
        x, y deux entiers positifs definissant une position sur l'echequier
        v un nombre entier definissant la version de l'historique a rechercher
        retourne la piece presente au x et au y dans la version de l'historique donné
        """
        for piece in self.hist[v]:
            if piece[0] == x and piece[1] == y:
                return type(piece[2])

plateau = echequier()

class piece:
    """
    caractéristiques communes a toutes les pieces
    """
    def __init__(self, x, y, couleur, img):
        self.x = x
        self.y = y 
        self.couleur = couleur
        self.img = ImageTk.PhotoImage(Image.open(img))
        self.en_passant = False

class pion(piece):
    def __init__(self, x, y, couleur, img):
        super().__init__(x, y, couleur, img)

    def deplacer(self, x, y):
        """
        x, y : des nombres entiers positifs definissant une position sur l'echequier ou le pion est sensé se deplacer
        """
        ## prise en passant 
        if self.couleur == 'BLANC' and self.y == 4:
            plateau.case_piece_hist(0, 0)
            if self.y + 1 == y and self.x + 1 == x:
                if type(plateau.case_piece(self.x+1, self.y)) == type(self):
                    if plateau.case_piece_hist(self.x+1, self.y) == None:
                        plateau.mange_piece(self.x+1, self.y)
                        self.y += 1
                        self.x += 1
                        return True
            elif self.y + 1 == y and self.x - 1 == x:
                if type(plateau.case_piece(self.x-1, self.y)) == type(self):
                    if plateau.case_piece_hist(self.x-1, self.y) == None:
                        plateau.mange_piece(self.x-1, self.y)
                        self.y += 1
                        self.x -= 1
                        return True
        elif self.couleur == 'NOIR' and self.y == 3:
            if self.y - 1 == y and self.x + 1 == x:
               if type(plateau.case_piece(self.x+1, self.y)) == type(self):
                    if plateau.case_piece_hist(self.x+1, self.y) == None:
                        plateau.mange_piece(self.x+1, self.y)
                        self.y += 1
                        self.x += 1
                        return True
            elif self.y - 1 == y and self.x - 1 == x:
                if type(plateau.case_piece(self.x-1, self.y)) == type(self):
                    if plateau.case_piece_hist(self.x-1, self.y) == None:
                        plateau.mange_piece(self.x-1, self.y)
                        self.y += 1
                        self.x -= 1
                        return True
                    
        ## deplacement basique 

        if self.couleur == "BLANC": param = [y, self.y, 1, lambda u : u] ## position pour les blancs
        else: param = [self.y, y, 6, lambda u : -u] ## position pour les noirs

        if plateau.case_vide(x, y) and self.x == x: 
            if param[0]-param[1] == 2 and self.y == param[2] and self.x == x: ## si pion n'a pas encore bougé et que demande pour se deplacer de 2 case
                if plateau.case_vide(x, self.y+param[3](1)) != True:
                    return False
                self.y = y
                return True
            elif param[0]-param[1] == 1 and self.x == x: ## test si le coup demandé est legal
                self.y = y
                return True
            return False
        elif x!=self.x:
            if self.couleur == 'BLANC' and y-self.y == 1 or self.couleur == 'NOIR' and self.y-y == 1:
                if x > self.x and x-self.x == 1 or x < self.x and self.x-x == 1:
                    if plateau.case_piece(x, y) != None:
                        if plateau.case_piece(x, y).couleur != self.couleur:
                            plateau.mange_piece(x, y)
                            self.x = x
                            self.y = y
                            return True
        return False
    
    def peut_manger(self):
        """
        retourne un tableau contenant toutes les cases que le pion controle
        """
        if self.couleur == 'BLANC':
            return [[self.x+1, self.y+1], [self.x-1, self.y+1]]
        return [[self.x+1,self.y-1], [self.x-1, self.y-1]]


class tour(piece):
    def __init__(self, x, y, couleur, img):
        super().__init__(x, y, couleur, img)
        self.roque = False
    
    def deplacer(self, x, y, test = False):
        """
        x, y : des nombres entiers positifs definissant une position sur l'echequier ou la tour est censé se deplacer
        renvoie True si s'est déplacé, False si non
        """
        deplacement = [[lambda : self.x != x and self.y == y, [lambda : self.x > x, self.x-x, [lambda a : self.x-a, lambda a : y]], [lambda : self.x < x, x-self.x, [lambda a : self.x+a, lambda a : y]]],
                       [lambda : self.y != y and self.x == x, [lambda : self.y > y, self.y-y, [lambda a : x, lambda a : self.y-a]], [lambda: self.y < y, y-self.y, [lambda a : x, lambda a : self.y+a]]]]
        for dep in deplacement:
            if dep[0]():
                for al in dep[1:3]:
                    if al[0]():
                        for i in range(1,al[1]):
                            if plateau.case_vide(al[2][0](i), al[2][1](i)) != True:
                                return False ## trouve une piece sur son passage
                        if plateau.case_occupe_ennemi(x, y, self.couleur):
                            if test == False:
                                self.roque = True
                                plateau.mange_piece(x, y)
                                self.x = x
                                self.y = y
                            return True
        return False

    def peut_manger(self):
        """
        retourne un tableau contenant toutes les cases que la tour controle
        """
        cap = []
        for i in range(1, self.x+1):
            if self.deplacer(self.x-i, self.y, True) and self.x >= 0:
                cap.append([self.x-i, self.y])
        for i in range(1, 8-self.x):
            if self.deplacer(self.x+i, self.y, True) and self.x+i <= 7:
                cap.append([self.x+i, self.y])
        for i in range(1, self.y+1):
            if self.deplacer(self.x, self.y-i, True) and self.y-i >= 0:
                cap.append([self.x, self.y-i])
        for i in range(1, 8-self.y):
            if self.deplacer(self.x, self.y+i, True) and self.y <= 7:
                cap.append([self.x, self.y+i])
        return cap

class cavalier(piece):
    def __init__(self, x, y, couleur, img):
        super().__init__(x, y, couleur, img)

    def deplacer(self, x, y):
        """
        x, y : des nombres entiers positifs definissant une position sur l'echequier ou la tour est censé se deplacer
        renvoie True si s'est déplacé, False si non
        """
        possibilite = [lambda : self.x+1 == x and self.y+2 == y, lambda : self.x+1 == x and self.y-2 == y, 
                       lambda : self.x-1 == x and self.y+2 == y, lambda : self.x-1 == x and self.y-2 == y,
                       lambda : self.x+2 == x and self.y-1 == y, lambda : self.x+2 == x and self.y+1 == y,
                       lambda : self.x-2 == x and self.y-1 == y, lambda : self.x-2 == x and self.y+1 == y]
        for pos in possibilite:
            if pos():
                if plateau.case_occupe_ennemi(x, y, self.couleur):
                    plateau.mange_piece(x, y)
                    self.x = x 
                    self.y = y
                    return True
        return False
    
    def peut_manger(self):
        """
        retourne un tableau contenant toutes les cases que le cavalier controle
        """
        return [[self.x+1, self.y+2], [self.x+1, self.y-2], [self.x-1, self.y+2], [self.x-1, self.y-2],
                [self.x+2, self.y-1], [self.x+2, self.y+1], [self.x-2, self.y-1], [self.x-2, self.y+1]]

class fou(piece):
    def __init__(self, x, y, couleur, img):
        super().__init__(x, y, couleur, img)
    
    def deplacer(self, x, y, test=False):
        """
        x, y : des nombres entiers positifs definissant une position sur l'echequier ou le fou est censé se deplacer
        renvoie True si s'est déplacé, False si non
        """
        deplacement = [[lambda : self.x > x and self.y > y and self.x-x == self.y-y, self.x-x, [lambda a: self.x-a, lambda a: self.y-a]],
                       [lambda : self.x > x and self.y < y and self.x-x == y-self.y, self.x-x, [lambda a: self.x-a, lambda a: self.y+a]],
                       [lambda : self.x < x and self.y < y and x-self.x == y-self.y, x-self.x, [lambda a: self.x+a, lambda a: self.y+a]],
                       [lambda : self.x < x and self.y > y and x-self.x == self.y-y, x-self.x, [lambda a: self.x+a, lambda a: self.y-a]]]
        for dep in deplacement:
            if dep[0]():
                for i in range(1,dep[1]):
                    if plateau.case_vide(dep[2][0](i), dep[2][1](i)) != True:
                        return False
                if plateau.case_occupe_ennemi(x, y, self.couleur) :
                    if test == False:
                        plateau.mange_piece(x, y)
                        self.x = x 
                        self.y = y
                    return True
        return False

    def peut_manger(self):
        cap = []
        for i in range(1, self.x+1):
            if self.deplacer(self.x-i, self.y-i, True) and self.x-i >= 0 and self.y-i >=0:
                cap.append([self.x-i, self.y-i])
        for i in range(1, self.x+1):
            if self.deplacer(self.x-i, self.y+i, True) and self.x-i >= 0 and self.y+i <= 7:
                cap.append([self.x-i, self.y+i])
        for i in range(1, 7-self.x+1):
            if self.deplacer(self.x+i, self.y+i, True) and self.x+i <= 7 and self.y+i <= 7:
                cap.append([self.x+i, self.y+i])
        for i in range(1, 7-self.x+1):
            if self.deplacer(self.x+i,self.y-i, True) and self.x+i <= 7 and self.y > 0:
                cap.append([self.x+i, self.y-i])
        return cap

class dame(tour, fou):
    def __init__(self,x, y, couleur, img):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.img = ImageTk.PhotoImage(Image.open(img))
        self.test = False

    def deplacer(self, x, y, test = False):
        """
        x, y : des nombres entiers positifs definissant une position sur l'echequier ou la tour est censé se deplacer
        renvoie True si s'est déplacé, False si non
        """
        if self.test == True:
            if tour.deplacer(self, x, y, True):
                return True
            elif fou.deplacer(self, x, y, True):
                return True
            return False
        else:
            if tour.deplacer(self, x, y):
                return True
            elif fou.deplacer(self, x, y):
                return True
            return False
    
    def peut_manger(self):
        self.test = True
        cap =  tour.peut_manger(self) + fou.peut_manger(self)
        self.test = False
        return cap

class roi(piece):
    def __init__(self, x, y, couleur, img):
        super().__init__(x, y, couleur, img)
        self.roque = False

    def deplacer(self, x, y):
        """
        x, y : des nombres entiers positifs definissant une position sur l'echequier ou la tour est censé se deplacer
        renvoie True si s'est déplacé, False si non
        """
        deplacement = [lambda : self.x+1 == x and self.y == y, lambda : self.x+1 == x and self.y+1 == y,
                       lambda : self.x+1 == x and self.y-1 == y, lambda : self.x-1 == x and self.y == y,
                       lambda : self.x-1 == x and self.y+1 == y, lambda : self.x-1 == x and self.y-1 == y,
                       lambda : self.x == x and self.y-1 == y, lambda : self.x == x and self.y+1 == y]

        if self.x + 2 == x and self.roque == False and self.y == y:
            for i in range(1,4):
                if plateau.case_vide(self.x+i, y) != True:
                    return False
            if type(plateau.case_piece(x+2, y)) == type(tour(0,0,'BLANC', "piece echec\\tour_blanc.png")):
                if plateau.case_piece(x+2, y).roque == False:
                    self.x = x
                    self.roque = True
                    plateau.case_piece(x+2, y).x = x-1
                    return True
            return False

        elif self.x - 2 == x and self.roque == False and self.y == y:
            for i in range(1, 3):
                if plateau.case_vide(self.x-i, y) != True:
                    return False
            if type(plateau.case_piece(x-1, y)) == type(tour(0,0,'BLANC', "piece echec\\tour_blanc.png")):
                if plateau.case_piece(x-1, y).roque == False:
                    self.x = x
                    self.roque = True
                    plateau.case_piece(x-1, y).x = x+1
                    return True
            return False

        for dep in deplacement:
            if dep():
                if plateau.case_occupe_ennemi(x, y, self.couleur):
                    plateau.mange_piece(x, y)
                    self.x = x
                    self.y = y
                    self.roque = True
                    return True
        return False

    def peut_manger(self):
        return [[self.x+1, self.y], [self.x+1, self.y+1], [self.x+1, self.y-1], [self.x-1, self.y], [self.x-1, self.y+1], [self.x-1, self.y-1], [self.x, self.y-1], [self.x, self.y+1]]

nbr_clic = 0
piece_selec = None
position = [0,90,180,270,360,450,540,630,720,810]
retour_arriere = 0

def mise_a_jour(pos=[], pos_e=[]):
    global afichage, nbr_clic, img_vert
    afichage.delete('all')
    afichage.create_image(0,0, anchor = Tk.NW, image = photo)
    afichage.pack()
    position = [0,90,180,270,360,450,540,630,720,810]
    for piece in plateau.tab:
        afichage.create_image(position[piece.x], position[piece.y], anchor = Tk.NW, image=piece.img)
        afichage.pack()
    if pos != []:
        afichage.create_image(position[pos[0]], position[pos[1]], anchor = Tk.NW, image=img_vert)
        afichage.pack()

def clic(event):
    global nbr_clic, piece_selec, position, tour_jouer, retour_arriere, afichage

    x = event.x
    y = event.y

    ### conversion en x et y pour les pieces
    pos = []
    c = [x, y]
    for j in range(2):
        i = 0
        test = False
        while test != True:
            if c[j] < position[i]:
                pos.append(i-1)
                test = True
            i += 1
    
    if retour_arriere != 0:
        retour_arriere = 0
        plateau.reorganisation_historique(-1)
        mise_a_jour()
    elif nbr_clic == 0:
        piece_selec = plateau.case_piece(pos[0], pos[1])
        if piece_selec != None:
            if tour_jouer % 2 == 0 and piece_selec.couleur == 'BLANC' or tour_jouer % 2 != 0 and piece_selec.couleur == 'NOIR':
                nbr_clic += 1
    elif nbr_clic == 1:
        if piece_selec.deplacer(pos[0], pos[1]): ### bouge la piece
            
            ## test si le roi est en echec
            if piece_selec.couleur == 'BLANC': roi_selec = plateau.tab[0]
            else: roi_selec = plateau.tab[1]

            if plateau.est_echec(roi_selec):
                plateau.ajout_historique()
                tour_jouer += 1
            else:
                plateau.reorganisation_historique(-1)

        nbr_clic = 0
        piece_selec = None
    ### creation du plateau
    
    if nbr_clic == 1:
        mise_a_jour([pos[0], pos[1]])
    else: mise_a_jour()


def retour(event):
    global retour_arriere
    retour_arriere += 1
    if retour_arriere <= len(plateau.hist):
        plateau.reorganisation_historique(-retour_arriere)
        afichage.delete('all')
        mise_a_jour()
    
def remise(event):
    global retour_arriere
    retour_arriere = 0
    plateau.reorganisation_historique(-1)
    mise_a_jour()
    

tour_jouer = 0

root = Tk.Tk()
img_vert = ImageTk.PhotoImage(Image.open("piece echec\\vert.png"))     ### defnini le bg
image = Image.open("piece echec\\bg.png")
photo = ImageTk.PhotoImage(image)     ### defnini le bg
afichage = Tk.Canvas(root, width = image.size[0], height = image.size[1])  #genere le canvas

img_rouge = ImageTk.PhotoImage(Image.open('piece echec\\rouge.png'))

## generation plateau
plateau.generer_plateau()
plateau.ajout_historique()

mise_a_jour()

afichage.bind('<Button-1>', clic)
afichage.bind_all('<Left>', retour)
afichage.bind('<Button-3>', remise)
afichage.pack()

root.mainloop()
