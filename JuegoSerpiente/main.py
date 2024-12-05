from tkinter import *

class Serpiente():
    def __init__(self):
        self.cx = 104 # coordenadas de x de la cabeza
        self.cy = 154 # coordenadas de y de la cabeza
        self.dx, self.dy = 0, 0 # direcciones

        self.cabeza = areaJugable.create_rectangle([(0, 0), (40, 40)], fill = "green")
        areaJugable.moveto(self.cabeza, self.cx, self.cy)

        self.cuerpo = [self.cabeza] # lista de miembros de la serpiente
        self.coordenadas = [[self.cx, self.cy]] # lista de coordenadas de cada miembro
        self.movimientos = [] # lista de direcciones/movimientos de la serpiente
        self.tamaño = 1 # longitud de las 3 listas anteriores

        self.chocar = False

        self.manzana = Manzana() # creo la manzana
        self.manzana.mover_manzana(self.coordenadas) # muevo la manzana para aleatoriezar su posición

    def crecer(self):
        nuevoMiembro = areaJugable.create_rectangle([(0, 0), (40, 40)], fill = "green")

        # El nuevo miembro debe ser colocado atrás de la cola (self.coordenadas[self.tamaño - 1])
        # en dirección contraria al que ésta se movió por última vez (self.movimientos[self.tamaño - 1])
        nuevasCoordsX = self.coordenadas[self.tamaño - 1][0] - self.movimientos[self.tamaño - 1][0]
        nuevasCoordsY = self.coordenadas[self.tamaño - 1][1] - self.movimientos[self.tamaño - 1][1]
        self.tamaño += 1

        areaJugable.moveto(nuevoMiembro,
                           nuevasCoordsX, nuevasCoordsY)
        self.cuerpo.append(nuevoMiembro)
        self.coordenadas.append([nuevasCoordsX, nuevasCoordsY])

    def direccion(self, event):
    # Cambio la dirección en base a la tecla apretada,
    # primero verificando que la nueva dirección ingresada no sea contraria a la anterior
        if event.keysym == 'w' and self.dy != 50:
            self.dx, self.dy = 0, -50
        elif event.keysym == 's' and self.dy != -50:
            self.dx, self.dy = 0, 50
        elif event.keysym == 'a' and self.dx != 50:
            self.dx, self.dy = -50, 0
        elif event.keysym == 'd' and self.dx != -50:
            self.dx, self.dy = 50, 0
    def mover_serpiente(self):
    # Actualizo la lista de movimientos y elimino el último elemento
        self.actualizar_movimientos()

    # Actualizo las coordenadas de cada miembro del cuerpo de la serpiente
    # el rango va de -1 a len(self.cuerpo) porque sino la serpiente no podría moverse al principio de la partida
        self.actualizar_coordenadas()

    # Compruebo si la cabeza (self.coordenadas[0]) y la manzana están en el mismo lugar
    # En caso de ser afirmativo, invoco la función crecer() y mover_manzana()
    # Para esto, tengo que "ajustar" las coordenadas de la cabeza ya que la manzana es de menor tamaño
        self.verificar_manzana()

        if self.coordenadas.count(self.coordenadas[0]) > 1 \
            or self.coordenadas[0][0] < 0 or self.coordenadas[0][0] > 400\
            or self.coordenadas[0][1] < 0 or self.coordenadas[0][1] > 400:
            labelDerrota = Label(window, text = "DERROTA\n¡Chocaste!", font = ("Consolas", 20, "bold"), bg = "dark grey")
            labelDerrota.place(x = 170, y = 210)
        else:
            window.after(350, self.mover_serpiente)

    def actualizar_movimientos(self):
        self.movimientos.insert(0, [self.dx, self.dy])
        if len(self.movimientos) > self.tamaño:
            self.movimientos.pop(len(self.movimientos) - 1)
    def actualizar_coordenadas(self):
        for i in range(-1, len(self.movimientos) - 1):
            self.coordenadas[i][0] += self.movimientos[i][0]
            self.coordenadas[i][1] += self.movimientos[i][1]
            areaJugable.moveto(self.cuerpo[i],
                               self.coordenadas[i][0], self.coordenadas[i][1])
    def verificar_manzana(self):
        if ((self.coordenadas[0][0] + 11) == self.manzana.mx) and ((self.coordenadas[0][1] + 11) == self.manzana.my):
            self.crecer()
            self.manzana.mover_manzana(self.coordenadas)

class Manzana(): # (punto)
    def __init__(self):
        self.manzana = areaJugable.create_rectangle([(15, 15), (35, 35)], fill="dark red")
        self.mx, self.my = 0, 0 # coordenadas de la manzana

    def mover_manzana(self, coordenadas):
        import random
        self.mx = random.randrange(0, 400, 50) + 15
        self.my = random.randrange(0, 400, 50) + 15

    # Evito que la manzana se genere en un bloque ocupado por el cuerpo de la serpiente
    # Por algún motivo, esto no funciona siempre
        if [self.mx, self.my] in coordenadas:
            self.mover_manzana(coordenadas)
        else:
            sumar_punto()
            areaJugable.moveto(self.manzana, self.mx, self.my)


puntuacion = -1
tiempo = 0
def sumar_punto():
    global puntuacion, tiempo
    puntuacion += 1
    labelInfo.config(text = "PUNTUACION: {}    |    TIEMPO: {}".format(puntuacion, tiempo))
def actualizar_cronometro():
    global tiempo, puntuacion
    tiempo += 1
    labelInfo.config(text="PUNTUACION: {}    |    TIEMPO: {}".format(puntuacion, tiempo))
    window.after(1000, actualizar_cronometro)

def crear_grilla():

    for i in range(0, 400, 50): # eje y, 8 cuadrados
        for j in range(0, 400, 50): # eje x, 8 cuadrados
            if i % 100 == 0: # filas impares
                if j % 100 == 0: # columnas impares
                    areaJugable.create_rectangle([(j, i), (50 + j, 50 + i)], fill = "#224C98")
                else: # columnas impares
                    areaJugable.create_rectangle([(j, i), (50 + j, 50 + i)], fill = "#4682B4")
            else: # filas pares
                if j % 100 == 0: # columnas impares
                    areaJugable.create_rectangle([(j, i), (50 + j, 50 + i)], fill = "#4682B4")
                else: # columnas impares
                    areaJugable.create_rectangle([(j, i), (50 + j, 50 + i)], fill = "#224C98")

window = Tk()
window.geometry("500x500")
window.title("JUEGO SERPIENTE")
window.config(background = "dark grey")
window.resizable(False, False)

labelInfo = Label(window, text = "PUNTOS: 0\t|TIEMPO: 0", font = ("Consolas", 15),
                  bg = "dark blue", fg = "light blue")
labelInfo.pack()

# Creo un frame solo para darle un borde exterior al juego. Para que quede más lindo
frame = Frame(window, height = 450, width = 450, bg = "light grey", bd = 10, relief = RAISED)
frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

areaJugable = Canvas(frame, height = 400, width = 400, bg = "white")
areaJugable.place(relx = 0.5, rely = 0.5, anchor = CENTER)
crear_grilla()

serpiente = Serpiente()
window.bind("<Key>", serpiente.direccion)
serpiente.mover_serpiente()

actualizar_cronometro()

window.mainloop()

# Faltaría agregar un botón que, una vez que se termine el juego,
# te permita volver a jugar sin necesidad de cerrar y abrir la aplicación
# Pero bueno ¯\_(ツ)_/¯
