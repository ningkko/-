from PIL import Image
from graphics import*
import tkinter
from tkinter import messagebox
import random

def main():
    # Create the scene
    global gameState
    global pause
    gamestate = 0
    pause = False
    creatwin()    
    preset()
    setDirectionKeys()
    if gameState!=0:
        while True:
        # Animation loop
            global k
            k = win.checkKey()

            if gameState == 1:
                iris.moveIris()
                player.playerMove()  
                if k == 'period':
                    print( 'Quit the game.' )
                    break
            elif gameState == 2 and pause == False:
                pause = True
                pausePanel()

            elif gameState == 0:
                tkinter.messagebox.showinfo("\u6349\u4f4f\u8001\u96e8\u5929","\u543c\uff0c\u70b9\u51fb\u7a97\u53e3\u9000\u51fa")
                break

    #---------------------------------------------------------------
    win.getMouse( )
    win.close( )

#=========== Classes ====================

class Objects:
    '''This is a class for all objects that interact with the main character.
    '''
    def __init__(self, px, py, name,image):
        self.positionX = px
        self.positionY = py
        self.imageID = image
        self.image = Image( Point(px, py), image)
        self.name = name

    def checkDistance (self,thing):
        if (-80 < (thing.positionX - self.positionX ) < 80) and (-80 < (thing.positionY - self.positionY ) < 80):
            return True
        else: return False
    def checkBiggerDistance(self,thing):
        if (-200 < (thing.positionX - self.positionX ) < 200) and (-200 < (thing.positionY - self.positionY ) < 200):
            return True
        else: return False    



class Player(Objects):
    '''Player class
    '''
    def __init__(self, px, py, name, image):
        Objects.__init__(self, px, py,name,image )


    def playerMove(self):
        step = 13

        #====================================================================
        #                       Functions
        #====================================================================

        def wrap():
            # wrap when touches borders
            if self.positionX<=-580:
                self.positionX =539
            elif self.positionX>= 580:
                self.positionX = -539
            elif self.positionY >= 580:
                self.positionY = -539
            elif self.positionY <=-580:
                self.positionY = 539
        def moveLeft():
            if (k == leftKey ) and (self.positionX > -580):
                self.positionX -= step
        def moveRight():
            if (k == rightKey ) and (self.positionX < 580):
                self.positionX += step
        def moveUp():
            if (k == upKey) and (self.positionY < 580):
                self.positionY += step  
        def moveDown():   
            if (k == downKey) and (self.positionY > -580):
                self.positionY -= step    
        def setObstacles():
            if k == "j":
                if checkNotCrash(obstacle,self.positionX-step,self.positionY):
                    self.positionX-=60
                    global obstacle 
                    obstacle = Objects(self.positionX,self.positionY,"i2","i2.gif")
                    obstacle.image.draw(win)

                elif checkNotCrash(obstacle,self.positionX+step,self.positionY):
                    self.positionX+=60
                    global obstacle 
                    obstacle = Objects(self.positionX,self.positionY,"i2","i2.gif")
                    obstacle.image.draw(win)          

                elif checkNotCrash(obstacle,self.positionX, self.positionY-step):
                    self.positionY-=60
                    global obstacle 
                    obstacle = Objects(self.positionX,self.positionY,"i2","i2.gif")
                    obstacle.image.draw(win)

                elif checkNotCrash(obstacle,self.positionX, self.positionY+step):

                    self.positionY+=60
                    global obstacle 
                    obstacle =  Objects(self.positionX,self.positionY,"i2","i2.gif")
                    obstacle.image.draw(win)

                else:
                    pass

        def checkNotCrash(thing,selfPositionX,selfPositionY):

            #  if crash into obstacles, return false.
            if (-60 < (thing.positionX - selfPositionX ) < 60) and (-60 < (thing.positionY - selfPositionY ) < 60):
                return False
            else: return True
        #====================================================================
        #                       Logics
        #====================================================================

        self.image.undraw()
        #setObstacles()
        wrap()

        if checkNotCrash(obstacle,self.positionX-step,self.positionY):
            moveLeft()
        if checkNotCrash(obstacle,self.positionX+step,self.positionY):
            moveRight()
        if checkNotCrash(obstacle,self.positionX, self.positionY-step):
            moveDown()
        if checkNotCrash(obstacle,self.positionX, self.positionY+step):
            moveUp()

        self.image = Image(Point(self.positionX,self.positionY),self.imageID)
        self.image.draw(win)




class Iris(Objects):
    ''' subclass of objects, has chat function
    '''
    def __init__(self, px, py, name, image):
        Objects.__init__(self,px,py,name,image)
        self.direction = "up"

    def moveIris(self):
        self.image.undraw()
        step = 5

        self.checkCaught()


        if (self.direction == "left" ) and (self.positionX > -580):
            self.positionX -= step

        elif self.positionX<=-580:
            self.positionX = 539

        elif (self.direction == "right") and (self.positionX < 580):
            self.positionX += step

        elif self.positionX>= 580:
            self.positionX = -539

        elif (self.direction == "up") and (self.positionY < 580):
            self.positionY += step

        elif self.positionY >= 550:
            self.positionY = -539

        elif (self.direction == "down") and (self.positionY > -580):
            self.positionY -= step

        elif self.positionY <=-580:
            self.positionY = 539

        elif self.direction == "none":
            pass

        self.image = Image(Point(self.positionX,self.positionY),self.imageID)
        self.image.draw(win)

        self.randomDirection()
        self.checkPlayer()
        self.checkObstacle()

    def checkCaught(self):
        global gameState
        if self.checkDistance(player):
            tkinter.messagebox.showinfo( "\u8001\u96e8\u5929\u88ab\u6293\u4f4f\u4e86", "\u4f60\u6293\u4f4f\u4e86\u8001\u96e8\u5929")
            tkinter.messagebox.showinfo( "\u8001\u96e8\u5929\u88ab\u6293\u4f4f\u4e86", "\u4f60\u62a2\u8d70\u4e86\u8001\u96e8\u5929\u7684\u87ba\u72ee\u7c89")
            tkinter.messagebox.showinfo( "\u8001\u96e8\u5929\u88ab\u6293\u4f4f\u4e86", "\u8001\u96e8\u5929\u628a\u4f60\u66b4\u6253\u4e86\u4e00\u987f")
            #
            #End game
            #
            player.positionX,player.positionY = 0,0
            iris.positionX,iris.positionY = -400,400
            gameState = 2
            
    def checkPlayer(self):
        if self.checkBiggerDistance(player):
            if self.direction == "right" or self.direction == "left": 
                #
                # see if the player is above or under
                #
                if player.positionY-self.positionY > 0:
                    self.direction = "down"
                elif player.positionY-self.positionY < 0 :
                    self.direction = "up"
                else:
                    chance = random.randint(0,1)
                    if chance == 0:
                        self.direction = "up"
                    else:
                        self.direction = "down"     

            if self.direction == "up" or self.direction == "down":
                #
                # see if the player is above or under
                #
                if player.positionX-self.positionX > 0:
                    self.direction = "left"
                elif player.positionX-self.positionX < 0 :
                    self.direction = "right"
                else:
                    chance = random.randint(0,1)
                    if chance == 0:
                        self.direction = "left"
                    else:
                        self.direction = "right"

    def checkObstacle(self):
        if self.checkBiggerDistance(obstacle):
            if self.direction == "up" or self.direction == "down":
                if obstacle.positionX<self.positionX:
                    self.direction = "right"
                elif obstacle.positionX>=self.positionX:
                    self.direction = "left"

            elif self.direction == "left" or self.direction == "right":
                if obstacle.positionY>self.positionY:
                    self.direction = "down"
                else:
                    self.direction = "up" 

    def randomDirection(self):
        chance = random.randint(0,35) 
        if chance == 5:
            if self.direction == "right" or self.direction == "left" or self.direction == "none": 
                #====================================================================
                # see if the player is above or under
                #====================================================================
                if player.positionY-self.positionY > 0:
                    self.direction = "down"
                elif player.positionY-self.positionY < 0 :
                    self.direction = "up"
                else:
                    chance = random.randint(0,1)
                    if chance == 0:
                        self.direction = "up"
                    else:
                        self.direction = "down"


            elif self.direction == "up" or self.direction == "down" or self.direction=="none":
                #====================================================================
                #             See if the player if on the left or right
                #====================================================================
                if player.positionX-self.positionX > 0:
                    self.direction = "left"
                elif player.positionX-self.positionX < 0 :
                    self.direction = "right"
                else:
                    chance = random.randint(0,1)
                    if chance == 0:
                        self.direction = "left"
                    else:
                        self.direction = "right"  

        elif chance == 6 or chance == 7 :
            if not -350<self.positionX-player.positionX<350  and not 800<= self.positionX-player.positionX<= 1200 and not -350<self.positionY-player.positionY<350 and not -1200<= self.positionX-player.positionX<=1200:
                self.direction = "none"

def pausePanel():

    global pause
    global gameState

    def newgame():
        global pause
        global gameState
        gameState = 1
        pause == False
        iris.image.undraw()
        iris.positionX, iris.positionY = random.randint(-500,500),random.randint(-500,500)
        iris.image.draw(win)
        player.image.undraw()
        player.positionX, player.positionY = random.randint(-500,500),random.randint(-500,500)
        player.image.draw(win)
        box2.destroy()        

    def fin():
        global gameState
        gameState = 0
        box2.destroy()

    tkinter.messagebox.showinfo("\u6349\u4f4f\u8001\u96e8\u5929", "\u518d\u6765\u4e00\u5c40\uff1f")
    global box2
    box2 = tkinter.Tk()
    b1 = tkinter.Button(box2, text = "\u6765", command = newgame)
    b2 = tkinter.Button(box2, text = "\u4e0d\u4e86", command = fin)
    b1.pack()        
    b2.pack()

# For people who have broken keyboards 
def setDirectionKeys():

    #====================================================================
    #                           Variables
    #====================================================================
    global gameState
    global upKey
    global leftKey
    global rightKey
    global downKey

    upKey = ''
    leftKey = ''
    rightKey = ''
    downKey = ''

    #====================================================================
    #                           Functions
    #====================================================================
    def wsad():
        global upKey
        global leftKey
        global rightKey
        global downKey

        upKey = "w"
        downKey = "s"
        leftKey = "a"
        rightKey = "d"


        tkinter.messagebox.showinfo( "\u9009\u62e9\u64cd\u4f5c\u952e\u76d8", '\u4f60\u9009\u4e86\u0077\u0073\u0061\u0064')

    def udlr():
        global upKey
        global leftKey
        global rightKey
        global downKey

        upKey = "Up"
        downKey = "Down"
        leftKey = "Left"
        rightKey = "Right"

        tkinter.messagebox.showinfo( "\u9009\u62e9\u64cd\u4f5c\u952e\u76d8", '\u4f60\u9009\u4e86\u4e0a\u4e0b\u5de6\u53f3')



    # Change the game state when click on again or end,
    def gameState():
        print(" gameState called")
        global gameState
        gameState = True
        top.destroy()

    #====================================================================
    #                           Logics
    #====================================================================
    tkinter.messagebox.showinfo( "\u9009\u62e9\u64cd\u4f5c\u952e\u76d8", '\u4f60\u597d\uff0c\u56e0\u4e3a\u6211\u7535\u8111\u6ca1\u6709\u4e0b\u952e\uff0c\u6240\u4ee5\u7279\u6b64\u7167\u987e\u5176\u4ed6\u6ca1\u6709\u4e0b\u952e\u7684\u670b\u53cb\u4eec')
    global top
    top = tkinter.Tk()
    b1 = tkinter.Button(top, text = "WSAD", command = wsad)
    b1.pack()
    b2 = tkinter.Button(top, text = "上下左右", command= udlr)
    b2.pack()
    b3 = tkinter.Button(top, text="选好了", command = gameState)
    b3.pack()

# Create the window.
def creatwin():
    global win
    win = GraphWin( '\u6349\u4f4f\u8001\u96e8\u5929', 800, 800, autoflush = False)
    win.setBackground( 'white' )
    win.setCoords( -600, -600, 600, 600 )


def preset():
    '''sets up the window.
    '''
    global player
    player = Player(100,100,"ning","ning2.gif")
    player.image.draw(win)
    global iris
    iris = Iris(-50,-50, "iris", "i1.gif")
    iris.image.draw(win)
    global obstacle 
    obstacle =  Objects(random.randint(-490,490),random.randint(-490,490),"i2","i2.gif")
    obstacle.image.draw(win)



if __name__ == '__main__':
    main()
