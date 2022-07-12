import pygame
import sys
import cv2
import random
import pytesseract
def acomodar_palabra(palabra):
    palabra = palabra.lower()
    palabra_ascii = []
    for i in palabra:
        palabra_ascii.append(ord(i))
    return palabra_ascii
def leer_portada():
    portada = "portada.png"
    portada = cv2.imread(portada)
    cadena =  pytesseract.image_to_string(portada)
    cadena = cadena.replace(",","").replace("(","").replace(")","").replace("-","").replace("/n","")
    cadena = cadena.split(" ")
    palabras = []
    for x in range(0, len(cadena)):
        if(len(cadena[x]) >= 4 and len(cadena[x]) <= 8 and cadena[x] != int):
            palabras.append(cadena[x])
    return palabras
pygame.init()
## Fuentes de letras
arial = pygame.font.match_font("arial")
courier = pygame.font.match_font("courier")
times = pygame.font.match_font("times")
## Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
## Nombre de la ventana
pygame.display.set_caption("Proyecto")
## Creada dimension de la pantalla
pantalla = pygame.display.set_mode((550,512))
## Carga del fondo de pantalla
entorno = pygame.image.load("entorno.jpg")
## Mostrar por pantalla el fondo principal
pantalla.blit(entorno,(0, 0))
## Generar acierto o fallo
fuente = pygame.font.SysFont(courier, 35)
## Acierto o fallo
acierto = pygame.image.load("adivinaste.png")
fallo = pygame.image.load("fallaste.png")
## Generar palabra
palabras = leer_portada()
palabra = palabras[random.randint(0,len(palabras) - 1)]
palabra = acomodar_palabra(palabra)
leer_portada()
## Acierto o fallo
feliz = pygame.image.load("true.png")
triste = pygame.image.load("false.png")
## Victoria o derrota
victoria = pygame.image.load("win.png")
derrota = pygame.image.load("loss.png")
## Estadisticas generales
caracteres_encontrados = 0
fin = False
repeticiones = []
vidas = 5
vida = pygame.image.load("vida5.png")
pantalla.blit(vida,(5,5))
## Guion bajo por cantidad de letras
guion = pygame.image.load("guion.png")
for i in range(1, len(palabra) + 1):
    pantalla.blit(guion,(i * 50, 500))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif(fin == True):
            continue
        else:
            if event.type == pygame.KEYDOWN:
                presencia_letra = 0
                ya_usado = False
                letra = fuente.render(chr(event.key), True, NEGRO)
                ## algoritmo para no ingresar dos veces la misma letra
                for x in range(0, len(repeticiones)):
                    if(repeticiones[x] == event.key):
                        ya_usado = True
                if(ya_usado == False): 
                    ## algoritmo para ver las letras encontradas
                    for i in range(1, len(palabra) + 1):
                        if(event.key == palabra[i - 1]):
                            presencia_letra += 1
                            pantalla.blit(letra,(i * 52.5, 480))
                            if(presencia_letra == 1):
                                repeticiones.append(event.key)
                            ## aqui va el descubrir por pantalla los caracteres encontrados   
                    caracteres_encontrados += presencia_letra
                    ## El usuario no acerto la letra ingresada.
                    if(presencia_letra == 0):
                        resultado = fallo
                        vidas -= 1
                        vida = "vida" + str(vidas) + ".png"
                        vida = pygame.image.load(vida)
                        pantalla.blit(vida,(5,5))
                        pantalla.blit(fallo, (90, 140))
                        pantalla.blit(triste, (130, 200))
                    ## El usuario acerto, por lo menos, una letra.
                    elif(presencia_letra > 0):
                        pantalla.blit(acierto, (90, 140))
                        pantalla.blit(feliz, (130, 200))
                    ##El usuario gano la partida.
                    if(caracteres_encontrados == len(palabra)):
                        pantalla.blit(victoria, (100, 350))
                        fin = True
                    ##El usuario perdio la partida.
                    elif(vidas == 0):
                        pantalla.blit(derrota, (70, 370))
                        fin = True
    pygame.display.update()