import math
import os
import msvcrt

class tateti:
    def __init__(self):
        while True:
            try: 
                self.numero = int(input("Ingrese 1 si quiere jugar solo, si no ingrese 2: "))
            except ValueError: 
                continue
            else:
                try: 
                    if self.numero == 1:
                        self.eleccion()
                        self.start1()
                        break
                    elif self.numero == 2:
                        self.eleccion()
                        self.start2()
                        break
                except ValueError: 
                    continue

    def eleccion(self):
        self.tablero = ["-" for _ in range(9)]
        
        while True:
            try:
                if self.numero==2:
                    self.jugador1 = "x"
                    self.jugador2 = "o"
                    break
                self.jugador1 = str(input("Si quiere ser el primer jugador presione la x, sino oprima o: "))
                if self.jugador1 == "x":
                    print("Usted comienza")
                    print("Presione una tecla para continuar...")
                    msvcrt.getch()
                    if self.numero == 1:
                        self.bot = "o"
                    break
                elif self.jugador1 == "o":
                    print("Usted juega despues que la X")
                    print("Presione una tecla para continuar...")
                    msvcrt.getch()
                    if self.numero == 1:
                        self.bot = "x"
                    break
            except ValueError:
                continue
        
    def ver_tablero(self):
        print("")
        for i in range(3):
            print("  ",self.tablero[0+(i*3)]," | ",self.tablero[1+(i*3)]," | ",self.tablero[2+(i*3)])
            print("")
            
    def esta_lleno(self,estado):
        return not "-" in estado
    
    def ganador(self,estado,jugador):
        if estado[0]==estado[1]==estado[2] == jugador: return True
        if estado[3]==estado[4]==estado[5] == jugador: return True
        if estado[6]==estado[7]==estado[8] == jugador: return True
        if estado[0]==estado[3]==estado[6] == jugador: return True
        if estado[1]==estado[4]==estado[7] == jugador: return True
        if estado[2]==estado[5]==estado[8] == jugador: return True
        if estado[0]==estado[4]==estado[8] == jugador: return True
        if estado[2]==estado[4]==estado[6] == jugador: return True

        return False
    
    def check_Ganador(self):
        if self.ganador(self.tablero,self.jugador1):
            os.system("cls")
            print(f"   El ganador es: {self.jugador1}!!!")
            return True
        if self.numero==1:    
            if self.ganador(self.tablero,self.bot):
                os.system("cls")
                print(f"   El ganador es: {self.bot}!!!")
                return True
        if self.numero==2:
            if self.ganador(self.tablero,self.jugador2):
                os.system("cls")
                print(f"   El ganador es: {self.jugador2}!!!")
                return True

        if self.esta_lleno(self.tablero):
            os.system("cls")
            print("   Empate!!!")
            return True
        return False
    
    def start1(self):
        bot = computadora(self.bot)
        persona1 = jugador1(self.jugador1)
        while True:
            os.system("cls")
            if self.bot=="x":
                self.tablero[4]="x"
            self.ver_tablero()
            
                
            #persona1
            print(f"   Es el turno de: {self.jugador1}")
            puntucacion = persona1.movimiento(self.tablero)
            self.tablero[puntucacion] = self.jugador1
            if self.check_Ganador():
                break
                
            #Bot
            puntucacion = bot.movimiento(self.tablero)
            self.tablero[puntucacion] = self.bot
            if self.check_Ganador():
                break

        print()
        self.ver_tablero()
         
    def start2(self): 
        persona2 = jugador2(self.jugador2)
        persona1 = jugador1(self.jugador1)
        while True:
            os.system("cls")
            self.ver_tablero()
                
            #persona1
            print(f"   Es el turno de: x")
            puntucacion = persona1.movimiento(self.tablero)
            self.tablero[puntucacion] = self.jugador1
            if self.check_Ganador():
                break
            
            os.system("cls")
            self.ver_tablero()
                
            #persona2
            print(f"   Es el turno de: o")
            puntucacion = persona2.movimiento(self.tablero)
            self.tablero[puntucacion] = self.jugador2
            if self.check_Ganador():
                break

        print()
        self.ver_tablero()

class jugador1:
    def __init__(self,letra):
        self.jugador1 = letra
        
    
    def movimiento(self,estado):
        
        while True:
            puntacion =  int(input("Ingrese el valor de la casilla que desea(1-9): "))
            print()
            if estado[puntacion-1] == "-":
                break
        return puntacion-1

class jugador2:
    def __init__(self,letra):
        self.jugador2 = letra
    
    def movimiento(self,estado):
        
        while True:
            puntuacion =  int(input("Ingrese el valor de la casilla que desea(1-9): "))
            print()
            if estado[puntuacion-1] == "-":
                break
        return puntuacion-1

class computadora(tateti):
    def __init__(self,letra):
        self.bot = letra
        self.jugador1 = "x" if letra == "o" else "o"
        

    def jugadores(self,estado):
        n = len(estado)
        x = 0
        o = 0
        for i in range(9):
            if(estado[i] == "x"):
                x = x+1
            if(estado[i] == "o"):
                o = o+1
        
        if(self.jugador1 == "x"):
            return "x" if x==o else "o"
        if(self.jugador1 == "o"):
            return "o" if x==o else "x"
    
    def acciones(self,estado):
        return [i for i, x in enumerate(estado) if x == "-"]
    
    def resultado(self,estado,action):
        nuevo_estado = estado.copy()
        player = self.jugadores(estado)
        nuevo_estado[action] = player
        return nuevo_estado
    
    def terminal(self,estado):
        if(self.ganador(estado,"x")):
            return True
        if(self.ganador(estado,"o")):
            return True
        return False

    def minimax(self, estado, jugador):
        max_jugador = self.jugador1  
        otro_jugador = 'o' if jugador == 'x' else 'x'


        if self.terminal(estado):
            return {'posicion': None, 'puntuacion': 1 * (len(self.acciones(estado)) + 1) if otro_jugador == max_jugador else -1 * (
                        len(self.acciones(estado)) + 1)}
        elif self.esta_lleno(estado):
            return {'posicion': None, 'puntuacion': 0}

        if jugador == max_jugador:
            mejor = {'posicion': None, 'puntuacion': -math.inf}  
        else:
            mejor = {'posicion': None, 'puntuacion': math.inf}  
        for posible_movimiento in self.acciones(estado):
            nuevo_estado = self.resultado(estado,posible_movimiento)
            sim_score = self.minimax(nuevo_estado, otro_jugador)  

            sim_score['posicion'] = posible_movimiento  

            if jugador == max_jugador:  
                if sim_score['puntuacion'] > mejor['puntuacion']:
                    mejor = sim_score
            else:
                if sim_score['puntuacion'] < mejor['puntuacion']:
                    mejor = sim_score
        return mejor

    def movimiento(self,estado):
        puntuacion = self.minimax(estado,self.bot)['posicion']
        return puntuacion      

inicio=tateti()

    
        
