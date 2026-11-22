import tkinter as tk
import random
import math
import time
import sys
import config as CONFIG


class Create_Graphe:
    
    
    RAYON = 20
    MARGE = 40 
    DIST_MIN = 90
    
    def __init__(self, nom, nbNodes, oriented, weighted, neg_weighted):
        
        self.edge_items = {}
        self.node_items = {}
        self.text_items = {}
        self.node_weight_items = {}
        
        self.oriented = oriented
        self.weighted = weighted
        self.neg_weighted = neg_weighted
        
        
        self.nomAlgo = nom
        self.nbNodes = nbNodes
        self.Nodes = []
        self.parcours = []
        self.weight = {}
        
        
        
        
                
        self.largeur, self.hauteur = 1000, 800
        self.fenetre = tk.Tk()
        self.fenetre.title(self.nomAlgo)
        self.fenetre.geometry("1000x800")
        self.canvas = tk.Canvas(self.fenetre, width=self.largeur, height=self.hauteur) 
        self.canvas.pack()
        
        
    def init_stats(self):
        self.etape_txt = self.canvas.create_text(50, 30, text=f"Etape : {self.i}", font=("Arial", 16))
        self.canvas.create_text(70, 50, text=f"Decouverte : ", font=("Arial", 16))
        self.decouv_txt = self.canvas.create_text(200, 50, text="", font=("Arial", 16))
        self.current_node_txt = self.canvas.create_text(90, 70, text=f"Noeud courant : {self.i}", font=("Arial", 16))
        self.current_passe_txt = self.canvas.create_text(90, 90, text=f"Passe 0", font=("Arial", 16))
        
        
    
    def create_nods(self):
        letters = random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", self.nbNodes)
        tries = 0
        for letter in letters:
            while True:
                position_x = random.randint(self.MARGE, self.largeur - self.MARGE)
                position_y = random.randint(self.MARGE, self.hauteur - self.MARGE)
                if all(math.dist((position_x, position_y), n[1]) >= self.DIST_MIN for n in self.Nodes):
                    self.Nodes.append([letter, (position_x, position_y)])
                    self.node_weight_items[letter] = None
                    break
                tries += 1
                if tries > 10000:
                    raise RuntimeError("Trop de nœuds pour la taille de la fenêtre")
    
    
   
            

    
    
    def create_edges(self):
        self.edges = {n[0]: [] for n in self.Nodes}
        for node in self.Nodes:
            u = node[0]
            nb_neighbours = random.randint(0, self.nbNodes - 1)
            candidats = [n[0] for n in self.Nodes if n[0] != u]
            for v in random.sample(candidats, nb_neighbours):
                if v in self.edges[u] or u in self.edges[v]:
                    continue                    # déjà reliés, dans un sens ou l'autre

                self.edges[u].append(v)
                if not self.oriented:
                    self.edges[v].append(u)

                if self.weighted:
                    bas = -20 if self.neg_weighted else 0
                    p = random.randint(bas, 20)
                    self.weight[(u, v)] = p
                    if not self.oriented:
                        self.weight[(v, u)] = p
                
                
            
    def draw_line(self, x1,x2,y1,y2, color, w, oriented):
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d   

        
        start = (x1 + ux * self.RAYON, y1 + uy * self.RAYON)
        end = (x2 - ux * self.RAYON, y2 - uy * self.RAYON)

        return self.canvas.create_line(*start, *end,fill= color, width=w, arrow=tk.LAST if oriented else None,
        arrowshape=(16, 20, 4))
    
    def draw_nods(self):
        for node in self.Nodes:
            x, y = node[1]
            self.text_items[node[0]] = self.canvas.create_text(x, y, text=node[0], font=("Arial", 16))
            self.node_items[node[0]] = self.canvas.create_oval(x - self.RAYON, 
                                                y - self.RAYON, 
                                                x + self.RAYON,
                                                y + self.RAYON,
                                                width=3)
            
    
    def draw_edges(self):
        positions = {n[0]: n[1] for n in self.Nodes}
        for node, voisins in self.edges.items():
            x1, y1 = positions[node]
            for voisin in voisins:
                x2, y2 = positions[voisin]
                if (voisin, node) in self.edge_items:   # déjà dessinée dans l'autre sens
                    continue
                
                self.edge_items[(node, voisin)] = self.draw_line(x1, x2, y1, y2, "black", 3, self.oriented)
            
                if self.weighted:
                    poids = self.weight.get((node, voisin), self.weight.get((voisin, node)))
                    dx = x2 - x1
                    dy = y2 - y1
                    longueur = math.hypot(dx, dy)
                    
                    if longueur == 0:
                        # boucle (nœud vers lui-même) : on décale simplement vers le haut
                        offset_x, offset_y = 0, -25
                    else:
                        decalage = 15
                        offset_x = -dy / longueur * decalage
                        offset_y = dx / longueur * decalage
        
        
                    self.canvas.create_text((x1+x2)/2 + offset_x, (y1+y2)/2 + offset_y, text=poids, font=("Arial", 16))
                
    def draw_weight(self, node, poids ,color):
        pos_x, pos_y = next(pos for nom, pos in self.Nodes if nom == node)
        pos_xp = pos_x
        pos_yp = pos_y - self.RAYON - 20
        return self.canvas.create_text(pos_xp, pos_yp, text=poids, fill = color, font=("Arial", 16))
        
        
    def color_edge(self, edge, color, width):
       a, b = edge
       item = self.edge_items.get((a,b)) or self.edge_items.get((b,a))
       self.canvas.itemconfig(item, fill=color, width=width)
        
    def color_node(self, name, color, w):
        self.canvas.itemconfig(self.node_items[name], outline=color,width = w)
        
        
        
    def lancer_anim(self, etapes):
        self.etapes = etapes
        self.i = 0
        self.init_stats()
        self.jouer_etape()

    def jouer_etape(self):
        if self.i >= len(self.etapes):
            # sys.exit(0)
            print('Fin')
            return     
        

        
        for etape in self.etapes[self.i]:
            
            kind, cible, etat , poids = (*etape, None)[:4]
            
        
            if kind == "node":
                
                NodeIsAlreadyBlack = self.canvas.itemcget(self.node_items[cible], "outline") == CONFIG.END
                
                
                if not NodeIsAlreadyBlack: # Si le noeud est deja noir on laisse.    / Sert a éviter de recolorier en gris alors que N a fini tous ses voisins
                    self.color_node(cible, etat,5)
                    
                    if etat == CONFIG.DECOUVERTE and cible not in self.parcours :
                        self.parcours.append(cible)
                        print("parcours : ", self.parcours)
                        self.canvas.itemconfig(self.decouv_txt, text=" → ".join(self.parcours))
                    if etat == CONFIG.CURRENT_NODE:
                        self.canvas.itemconfig(self.current_node_txt, text=f"Noeud courant : {cible}")
                    if etat == CONFIG.END:
                        for voisin in self.edges[cible]:
                            self.color_edge((cible,voisin), CONFIG.END, 5)
                            
                if cible not in self.parcours:     
                   
                    self.canvas.itemconfig(self.decouv_txt,text = " → ".join(self.parcours))
            elif kind == "edge":
                
                edge = self.edge_items.get(cible) or self.edge_items.get((cible[1], cible[0]))
                if edge == None:
                    continue
                EdgeIsAlreadyBlack = self.canvas.itemcget(edge, "fill") == CONFIG.END
                #if not EdgeIsAlreadyBlack:
                self.color_edge(cible, etat, 3)
            elif kind == "weight": # poids
                
                if not self.node_weight_items[cible]:
                    self.node_weight_items[cible] = self.draw_weight(cible, poids ,etat)
                else:
                    self.canvas.itemconfig(self.node_weight_items[cible],text = poids, fill= etat)
            else: #Up_passe
                self.canvas.itemconfig(self.current_passe_txt,text = etat)
                
                
                            
        self.canvas.itemconfig(self.etape_txt,text=f"Etape : {self.i}")
        self.i += 1
        self.fenetre.after(4000, self.jouer_etape)  
        
            
    
    def gener_graphe(self):
        self.create_nods()
        print("Noeuds : ",self.Nodes)
        self.create_edges()
        print("Arêtes : ",self.edges)
        print("Poids : ", self.weight)
        self.draw_nods()
        self.draw_edges()

        
        
        
    def launch(self,algo):
        
        etapes = algo 
        
        
        
        self.fenetre.after(5000, self.lancer_anim, etapes)  
        self.fenetre.mainloop()
        
    


