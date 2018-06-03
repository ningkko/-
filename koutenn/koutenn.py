from PIL import Image
from graphics import*
import tkinter
from tkinter import messagebox
import random

def main():
    # Create the scene
    global frame 
    frame= 0
    global gameState
    global pause
    gamestate = 0
    pause = False

    creatwin()    
    setDirectionKeys()
    objectGenerator()

    if gameState!=0:

        while True:
        # Animation loop
            global k
            k = win.checkKey()

            if gameState == 1:

                iris.moveIris()
                player.playerMove()  
                player.checkPlayerAttributes()
                if k == 'period':
                    break

            elif gameState == 2 and pause == False:

                pause = True
                pausePanel()

            elif gameState == 4:

                selectPlayer()

            elif gameState == 0:

                tkinter.messagebox.showinfo("\u6349\u4f4f\u8001\u96e8\u5929","\u543c\uff0c\u70b9\u51fb\u7a97\u53e3\u9000\u51fa")
                break

            frame+=1
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

    def checkDistance (self,position):

        if (-80 < (position[0] - self.positionX ) < 80) and (-80 < (position[1] - self.positionY ) < 80):
            return True
        else: return False

    def checkPlayerDistance(self,thing):

        if (-200 < (thing.positionX - self.positionX ) < 200) and (-200 < (thing.positionY - self.positionY ) < 200):
            return True
        else: return False    

    def checkPlayerCaughtDistance(self,thing):

        if (-80 < (thing.positionX - self.positionX ) < 80) and (-80 < (thing.positionY - self.positionY ) < 80):
            return True
        else: return False    

class Player(Objects):
    '''Player class
    '''
    def __init__(self, px, py, name, image):

        Objects.__init__(self, px, py,name,image )
        self.step = 8

    def checkPlayerAttributes(self):

        global frame

        if self.name == "ning":   
            #=====================================================================
            # When using Ning, player can move faster for 100 frames. 
            # After one use of technique the player hsa to wait for 300 frames
            # to use the tech again.
            #=====================================================================
            if frame > 400 and k == "j":
                frame = 0
                self.step = 18

            if frame > 100:
                self.step = 10

        elif self.name == "ewon":
            # ================================================================
            # regardless of frames, when using ewon, player can set obstacles.
            # ================================================================
            if k == "j":
                # after dropping the obstacle ewon will move out of the obstacle range
                # first check if the default move will move ewon into an obstacle area.
                safeL = True
                safeR = True
                safeU = True
                safeD = True

                for positions in obstaclePositions:
                    # moving left
                    if checkNotCrash(positions,self.positionX-self.step,self.positionY):
                        pass
                    else:
                        safeL = False

                    # moving right
                    if checkNotCrash(positions,self.positionX+self.step,self.positionY):
                        pass
                    else:
                        safeR = False

                    # moving down
                    if checkNotCrash(positions,self.positionX, self.positionY-self.step):
                        pass
                    else:
                        safeD = False

                    # moving up
                    if checkNotCrash(positions,self.positionX, self.positionY+self.step):
                        pass
                    else: 
                        safeU = False

                # set obstacle according to safty status
                if safeL:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/i2.gif")
                    self.positionX-=80 

                elif safeR:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/i2.gif")
                    self.positionX+=80 

                elif safeU:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/i2.gif")
                    self.positionY+=80 

                elif safeD:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/i2.gif")
                    self.positionY-=80 

                else:
                    pass

        elif self.name == "maomao":
            # ============================================================================
            # when using maomao, player can stand and attract iris.
            # after 100 frames the tech will disappear and another 300 frames are needed
            # for the next use of tech.
            # =============================================================================
            if frame > 400 and k == "j":               
                    frame = 0
                    iris.affliateState = True
                    self.step = 0

            if frame > 100:
                iris.affliateState = False
                self.step = 10

        elif self.name == "nox":
            # ==========================================================================
            # nox has 50% chance to make either herself or iris sleep for 100 frames. 
            # another 300 frames are needed for using the tech again.
            # ==========================================================================
            chance = random.randint(0,1)

            if frame>300 and k == "j":
                if chance == 0:
                    frame = 0
                    iris.irirsStep = 0
                elif chance == 1:
                    self.step = 0

            if frame > 100:
                iris.irirsStep = 5
                self.step =10

        elif self.name == "molly":
            # ===========================================================================
            # when using molly, player can decrease iris's speed to half of the original after
            # stand for 100 frames. iris will remain the slower speed for 100 frames and then
            # another 300 frames are needed for reusing the tech.
            # ===========================================================================
            if frame>500 and k == "j":
                frame = 0
                iris.irirsStep = 2.5
                self.step = 0
           
            if frame>100: 
                self.step = 10
           
            if frame>200:
                iris.irirsStep = 5

    def playerMove(self):

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
                self.positionX -= self.step
        
        def moveRight():
          
            if (k == rightKey ) and (self.positionX < 580):
                self.positionX += self.step
        
        def moveUp():
        
            if (k == upKey) and (self.positionY < 580):
                self.positionY += self.step  
       
        def moveDown():   
       
            if (k == downKey) and (self.positionY > -580):
                self.positionY -= self.step    


        #====================================================================
        #                       Logics
        #====================================================================

        self.image.undraw()
        wrap()
       
        for positions in obstaclePositions:
        
            if checkNotCrash(positions,self.positionX-self.step,self.positionY):
                moveLeft()
       
            if checkNotCrash(positions,self.positionX+self.step,self.positionY):
                moveRight()
       
            if checkNotCrash(positions,self.positionX, self.positionY-self.step):
                moveDown()
       
            if checkNotCrash(positions,self.positionX, self.positionY+self.step):
                moveUp()

        self.image = Image(Point(self.positionX,self.positionY),self.imageID)
        self.image.draw(win)

class Iris(Objects):
    ''' subclass of objects, has chat function
    '''

    def __init__(self, px, py, name, image):
       
        Objects.__init__(self,px,py,name,image)
        self.direction = "up"
        self.affliateState = False
        self.irirsStep=5

    def moveIris(self):
      
        self.image.undraw()
        self.checkCaught()


        if (self.direction == "left" ) and (self.positionX > -580):
            self.positionX -= self.irirsStep

        elif self.positionX<=-580:
            self.positionX = 539

        elif (self.direction == "right") and (self.positionX < 580):
            self.positionX += self.irirsStep

        elif self.positionX>= 580:
            self.positionX = -539

        elif (self.direction == "up") and (self.positionY < 580):
            self.positionY += self.irirsStep

        elif self.positionY >= 580:
            self.positionY = -539

        elif (self.direction == "down") and (self.positionY > -580):
            self.positionY -= self.irirsStep

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
        global notCrash
        notCrash = False
      
        if self.checkPlayerCaughtDistance(player):
        
            tkinter.messagebox.showinfo( "\u8001\u96e8\u5929\u88ab\u6293\u4f4f\u4e86", "\u4f60\u6293\u4f4f\u4e86\u8001\u96e8\u5929")
            tkinter.messagebox.showinfo( "\u8001\u96e8\u5929\u88ab\u6293\u4f4f\u4e86", "\u4f60\u62a2\u8d70\u4e86\u8001\u96e8\u5929\u7684\u87ba\u72ee\u7c89")
            tkinter.messagebox.showinfo( "\u8001\u96e8\u5929\u88ab\u6293\u4f4f\u4e86", "\u8001\u96e8\u5929\u628a\u4f60\u66b4\u6253\u4e86\u4e00\u987f")
            #
            #End game
            #

            # generate a new position to avoid catching iris at the beginning
            def generateValidNewPositions():
                
                global newix
                global newiy
                global newpx
                global newpy
                global notCrash
                notCrash = True

                # first create new random positions
                newix,newiy = random.randint(-500,500),random.randint(-500,500)
                newpx,newpy = random.randint(-500,500),random.randint(-500,500)   
                
                #check if it's in the catching area of obstacles
                for positions in obstaclePositions:
                    if not checkNotCrash(positions,newix,newiy) or not checkNotCrash(positions,newpx,newpy):
                        notCrash = False

            # generate valid new positions
            while notCrash == False:
                generateValidNewPositions()
            # move iris and player to new positions
            iris.positionX, iris.positionY = newix,newiy
            player.positionX, player.positionY = newpx,newpy

            # change to the selecting state.
            gameState = 2
    
    def checkPlayer(self):
       
        # iris has 2 states, one is to avoid the player, the other one is to touch the player 
        if self.affliateState == False:

            if self.checkPlayerDistance(player):
         
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

        elif self.affliateState == True:
            #tries to touch the player
            if self.direction == "right" or self.direction == "left": 
                if player.positionY-self.positionY > 0:
                    self.direction = "up"
                elif player.positionY-self.positionY < 0 :
                    self.direction = "down"
                else:
                    pass

            elif self.direction == "up" or self.direction == "down":
                if player.positionX-self.positionX > 0:
                    self.direction = "right"
                elif player.positionX-self.positionX < 0 :
                    self.direction = "left"
                else:
                    pass

    def checkObstacle(self):

        for positions in obstaclePositions:
           
            if self.checkDistance(positions):
             
                if self.direction == "up" or self.direction == "down":
              
                    if positions[0]<self.positionX:
                        self.direction = "right"
                
                    elif positions[0]>=self.positionX:
                        self.direction = "left"

                elif self.direction == "left" or self.direction == "right":
                  
                    if positions[1]>self.positionY:
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

  
    def newGame():
        
        global pause
        global gameState
        # go to game 
        gameState = 1
        pause == False
       
        box2.destroy()        

    def fin():
       
        global gameState
        gameState = 0
       
        box2.destroy()

    def newPlayer():
        #reset screen
        iris.image.undraw()
        player.image.undraw()
        resetScreen()

        global pasuse
        global gameState
        # go to player selection
        gameState = 4
        pause == False
       
        box2.destroy()

    #=======================================================================
    tkinter.messagebox.showinfo("\u6349\u4f4f\u8001\u96e8\u5929", "\u518d\u6765\u4e00\u5c40\uff1f")
    #======================================================================
    global box2
   
    box2 = tkinter.Tk()
    b1 = tkinter.Button(box2, text = "\u6765", command = newGame)
    b2 = tkinter.Button(box2, text = "选择其他角色", command = newPlayer)
    b3 = tkinter.Button(box2, text = "\u4e0d\u4e86", command = fin)
  
    b1.pack()        
    b2.pack()
    b3.pack()

def clearObstacles():
   
    global obstaclePositions
    obstaclePositions = []

def resetScreen():
    
    cover = Rectangle(Point(-650,-650),Point(650,650))
    cover.setFill("white")
    cover.draw(win)

def checkNotCrash(position,selfPositionX,selfPositionY):

    #  if crash into obstacles, return false.
    if (-60 < (position[0] - selfPositionX ) < 60) and (-60 < (position[1]- selfPositionY ) < 60):
        return False
    
    else: return True

# For people who have broken keyboards 
def setDirectionKeys():
   
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
     
        global gameState
        gameState = 4
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

def drawObject(px, py, imageID):
   
    image = Image( Point(px, py), imageID )
    image.draw(win)

# Create the window.
def creatwin():
  
    global win
    win = GraphWin( '\u6349\u4f4f\u8001\u96e8\u5929', 800, 800, autoflush = False)
    win.setBackground( 'white' )
    win.setCoords( -600, -600, 600, 600 )

def selectPlayer():
    # initialize
    character = ""
    global gameState
    selected = False
    # draw title
    title = Text(Point(0,150), "选择角色")
    title.setSize(36)
    title.setTextColor("black")
    title.setStyle("bold")
    title.draw(win)
    # draw characters
    drawObject(-400,0,"img/ning2.gif")
    drawObject(-200,0,"img/ewon.gif")
    drawObject(0,0,"img/maomao.gif")
    drawObject(200,0,"img/nox.gif")
    drawObject(400,0,"img/molly.gif")    
    # draw button
    button = Rectangle(Point(-80,-180),Point(80,-120))
    button.setWidth(3)
    button.setFill("snow")
    button.draw(win)
    # draw selection text
    text = Text(Point(0,-150), "确认")
    text.setSize(24)
    text.setTextColor("black")
    text.setStyle("bold")
    text.draw(win)

    while selected == False:

        mouse = win.getMouse( )
        xp,yp = mouse.getX(),mouse.getY()

        if -460<=xp<=-340 and -60<=yp<=60:
            character = "老宁"    
            characterID = "ning"
            characterImage = "img/ning2.gif"
            tkinter.messagebox.showinfo("老宁","飞一般的感觉")

        elif -260<=xp<=-140 and -60<=yp<=60:

            character = "小鹅"
            characterID = "ewon"
            characterImage = "img/ewon.gif"    
            tkinter.messagebox.showinfo("小鹅","使用食物诱惑")

        elif -60<=xp<=60 and -60<=yp<=60:
            character = "毛毛"
            characterID = "maomao"
            characterImage = "img/maomao.gif"
            tkinter.messagebox.showinfo("毛毛","会让老雨天忍不住揍一顿")

        elif 140<=xp<=260 and -60<=yp<=60:
            character = "nox"
            characterID = "nox"
            characterImage = "img/nox.gif"
            tkinter.messagebox.showinfo("nox","百分之五十几率让自己或对方陷入沉睡")        
        
        elif 340<=xp<=460 and -60<=yp<=60:
            character = "茉莉"
            characterID = "molly"
            characterImage = "img/molly.gif"
            tkinter.messagebox.showinfo("茉莉","笑声威慑")

        elif -80<=xp<=80 and -260<=yp<=-100 and character:
            tkinter.messagebox.showinfo("选中角色","你已选中"+character)
            selected = True
            resetScreen()
            print(characterImage)
            initialize(characterID,characterImage)
            print(characterImage)
            tkinter.messagebox.showinfo("选择角色","点击屏幕开始游戏。")
            if win.getMouse():
                gameState = 1

        elif -80<=xp<=80 and -260<=yp<=-100 and not character:
            tkinter.messagebox.showinfo("选择角色","快点选一个")

        # set player position
        xp,yp = -600,-600

def initialize(characterID,characterImage):
    '''sets up the window.
    '''
    global obstaclePositions
    player.name = characterID
    player.imageID = characterImage
  
    player.image.draw(win)
    
    iris.image.draw(win)
    x1,y1 = random.randint(-500,500),random.randint(-500,500)
    obstaclePositions = [[x1,y1]]
    drawObject(x1,y1,"img/i2.gif")

def objectGenerator():
   
    global player
    player = Player(100,100,"ning","img/ning2.gif")
   
    global iris
    iris = Iris(-50,-50, "iris", "img/i1.gif")
  
    global obstaclePositions
    x1,y1 = random.randint(-500,500),random.randint(-500,500)
    #Check if irirs tends to touch the player or walk away from the player


if __name__ == '__main__':
    main()
