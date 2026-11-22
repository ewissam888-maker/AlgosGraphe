import tkinter as tk
import math

largeur, hauteur = 1000, 800
fenetre = tk.Tk()
fenetre.title("")
fenetre.geometry("1000x800")
canvas = tk.Canvas(fenetre, width=largeur, height=hauteur) 
canvas.pack()

RAYON = 20

def draw_line(x1,x2,y1,y2, color, w):
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d   

        
        start = (x1 + ux * RAYON, y1 + uy * RAYON)
        end = (x2 - ux * RAYON, y2 - uy * RAYON)

        return canvas.create_line(*start, *end,fill= color, width=w)


x1 = 180
y1 = 180

x2 = 80
y2 = 460

def draw_point(x, y, rayon ,r=5, color="black"):
    return canvas.create_oval(
        x - rayon - r, y - rayon -  r,   # coin haut-gauche
        x + rayon + r, y + rayon + r,   # coin bas-droit
        fill=color, outline=color
    )

angle = math.radians(30)
xf = x2 + 30 * math.cos(angle)
yf = y2 + 30 * math.sin(angle)
draw_line(x1, x2, y1, y2, "black", 3)
draw_point(x2,y2, RAYON)
canvas.create_line(x2, y2, xf, yf, fill = "black", width=3)

fenetre.mainloop()