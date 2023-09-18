import os

# ------------------

# SCENARIES
# 5x5 SCENARY (OUTSIDE)
outside = [
    ['-', '~', '~', '~', '-', '-', '-'],
    ['|', ' ', ' ', '✮', '/', ' ', '|'],
    ['|', '✮', ' ', '/', '|', '∆', '|'],
    ['|', ' ', ' ', ' ', '|', '#', '|'],
    ['|', '∆', ' ', ' ', ' ', ' ', '|'],
    ['|', 'π', ' ', 'O', ' ', ' ', '|'],
    ['-', '-', '-', '-', '-', '-', '-']
]

# 5x5 SCENARY (FOREST)
outside2 = [
    ['-', '~', '~', '~', '~', '~', '-'],
    ['|', ' ', '∆', ' ', ' ', ' ', '|'],
    ['|', ' ', 'π', ' ', ' ', '∆', '|'],
    ['|', ' ', ' ', ' ', ' ', 'π', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', 'O', ' ', ' ', ' ', '|'],
    ['-', '~', '~', '~', '-', '-', '-']
]

# 5x5 SCENARY (FOREST)
outside3 = [
    ['-', '-', '-', '-', '-', '-', '-'],
    ['|', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', '∆', ' ', ' ', ' ', ' ', '|'],
    ['|', 'π', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', ' ', ' ', '∆', ' ', '|'],
    ['|', ' ', 'O', ' ', 'π', ' ', '|'],
    ['-', '~', '~', '~', '~', '~', '-']
]

# 5x5 SCENARY (HOUSE)
scenary_house = [
    ['-', '-', '-', '-', '-', '-', '-'],
    ['|', '=', '=', ' ', '✮', '#', '|'],
    ['|', '=', '=', '✮', ' ', ' ', '|'],
    ['|', '✮', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', '#', 'O', ' ', ' ', '✮', '|'],
    ['-', '-', '-', '-', '-', '-', '-']
]

# 5x5 SCENARY (CAVERN)
scenary_cavern = [
    ['-', '-', '-', '-', '-', '-', '-'],
    ['|', '^', ' ', ' ', ' ', '✮', '|'],
    ['|', '✮', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', ' ', ' ', ' ', '^', '|'],
    ['|', ' ', '^', ' ', '✮', ' ', '|'],
    ['|', '✮', ' ', ' ', 'O', '#', '|'],
    ['-', '-', '-', '-', '-', '-', '-']
]

actual_scenary = outside

# ------------------

class gameFunctions:
    def __init__(self):
        self.SPECIAL_CHARACTERS = ["#", "✮", "~"]
        self.SCENARIES = { # Y and X
            (5, 1): outside,
            (3, 5): scenary_house,
            (1, 5): scenary_cavern,
            (5, 5): scenary_house,
            "Forest": { # Positions can teleport (Y & X): actualScenary / nextScenary
                ((0, 0), (1, 3)): (outside, outside2),
                ((6, 6), (1, 3)): (outside2, outside),
                ((0, 0), (1, 5)): (outside2, outside3),
                ((6, 6), (1, 5)): (outside3, outside2)
            }    
        }

        self.INITIAL_HP = 100
        self.INITIAL_STAMINA = 10
        self.INITIAL_STARS = 0
        self.playerStats = {
            "HP": self.INITIAL_HP,
            "STAMINA": self.INITIAL_STAMINA,
            "STARS": self.INITIAL_STARS
        }
        
    def runGame(self) -> None:
        while True:
            os.system('clear')
            self.showStats()
            self.showScenary()
            y, x = self.findPlayer()
            keyBind = input("Select an key WASD: ")
    
            if keyBind in "Aa":
                if x >= 2:
                    self.movementPlayer(y, x - 1)
            
            elif keyBind in "Dd":
                if x <= 4:
                    self.movementPlayer(y, x + 1)
            
            elif keyBind in "Ww":
                if y <= 5:
                    self.movementPlayer(y - 1, x)
            
            elif keyBind in "Ss":
                if y >= 1:
                    self.movementPlayer(y + 1, x)    
        
    def showScenary(self) -> None:
        for line in actual_scenary:
            print(' '.join(line))

    def scenaryChange(self, newScenary) -> None:
        global actual_scenary
        actual_scenary = newScenary
        
    def scenaryChangeForest(self, nextPosition: tuple) -> None:
        y, x = nextPosition
        for position in self.SCENARIES["Forest"].keys():
            yDeli, xDeli = position
            if (y >= yDeli[0] and y <= yDeli[1]) and (x >= xDeli[0] and x <= xDeli[1]) and (actual_scenary == self.SCENARIES["Forest"][position][0]):
                self.scenaryChange(self.SCENARIES["Forest"][position][1])
                return   
    
    def pickStar(self) -> None:
        self.playerStats['STARS'] += 1
    
    def loseStaminaHp(self) -> None:
        self.playerStats["STAMINA"] = self.INITIAL_STAMINA
        self.playerStats["HP"] -= 1
        
    def findPlayer(self) -> tuple:
        for line in range(len(actual_scenary)):
            if 'O' in actual_scenary[line]:
                for column in range(len(actual_scenary[line])):
                    if actual_scenary[line][column] == 'O':
                        return line, column

    def changePosition(self, newLine: int, newColumn: int) -> None:
        actual_scenary[self.findPlayer()[0]][self.findPlayer()[1]] = ' '
        actual_scenary[newLine][newColumn] = 'O'

    def movementPlayer(self, newLine: int, newColumn: int) -> None:
        if actual_scenary[newLine][newColumn] in self.SPECIAL_CHARACTERS:
            if actual_scenary[newLine][newColumn] == "#":
                self.scenaryChange(self.SCENARIES[(newLine, newColumn)])
            elif actual_scenary[newLine][newColumn] == "~":
                self.scenaryChangeForest((newLine, newColumn))
            elif actual_scenary[newLine][newColumn] == "✮":
                self.pickStar()
                if not self.playerStats["STAMINA"]:
                    self.loseStaminaHp()
                    self.changePosition(newLine, newColumn)
                else:    
                    self.changePosition(newLine, newColumn)
                    self.playerStats["STAMINA"] -= 1
        elif actual_scenary[newLine][newColumn] == ' ':
            if not self.playerStats["STAMINA"]:
                self.loseStaminaHp()
                self.changePosition(newLine, newColumn)
            else:    
                self.changePosition(newLine, newColumn)
                self.playerStats["STAMINA"] -= 1
                    
    def showStats(self) -> None:
        print(f"X: {self.findPlayer()[1]} / Y: {self.findPlayer()[0]}")
        print(f"❤️: {self.playerStats['HP']}\n💧: {self.playerStats['STAMINA']}\n✮: {self.playerStats['STARS']}")
        
p = gameFunctions()
p.runGame()