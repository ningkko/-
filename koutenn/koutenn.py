from PIL import Image
from graphics import*
import tkinter
from tkinter import messagebox
import random


def main():
    # Create the scene
    # fram for monitoring the time
    global frame 
    frame= 0
    global gameState
    gamestate = 0
    global pause
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
                pause = False
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
        if image!="":
            self.image = Image( Point(px, py), image)
        else: self.image=""
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

        if self.name == "p1":   
            #=====================================================================
            # When using p1, player can move faster for 200 frames. 
            # After one use of technique the player hsa to wait for 300 frames
            # to use the tech again.
            #=====================================================================
            if frame > 400 and k == "j":
                frame = 0
                self.step = 20

            if frame > 200:
                self.step = 12

        elif self.name == "p2":
            # ================================================================
            # regardless of frames, when using p2, player can set obstacles.
            # ================================================================
            if k == "j":
                # after dropping the obstacle p2 will move out of the obstacle range
                # first check if the default move will move p2 into an obstacle area.
                safeL = True
                safeR = True
                safeU = True
                safeD = True

                for positions in obstaclePositions:
                    # moving left
                    if not checkNotCrash(positions,self.positionX-80,self.positionY) or (self.positionX-80<=-580):
                        safeL = False

                    # moving right
                    if not checkNotCrash(positions,self.positionX+80,self.positionY) or (self.positionX+80>=580):
                        safeR = False

                    # moving down
                    if not checkNotCrash(positions,self.positionX, self.positionY-80) or (self.positionY-80<=-580):
                        safeD = False

                    # moving up
                    if not checkNotCrash(positions,self.positionX, self.positionY+80) or (self.positionX-80>=580):
                        safeU = False

                # set obstacle according to safty status
                if safeL:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/lsf.gif")
                    self.positionX-=80 

                elif safeR:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/lsf.gif")
                    self.positionX+=80 

                elif safeU:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/lsf.gif")
                    self.positionY+=80 

                elif safeD:
                    obstaclePositions.append([self.positionX,self.positionY])
                    drawObject(self.positionX,self.positionY,"img/lsf.gif")
                    self.positionY-=80 

                else:
                    pass

                crash = False
                for positions in obstaclePositions:
                    if not checkNotCrash(positions,self.positionX,self.positionY):
                        tkinter.messagebox.showinfo("你挂了","你在尝试困住小雨天的时候把自己困住了")
                        tkinter.messagebox.showinfo("你挂了","点击任意位置退出")
                        if win.getMouse():
                            pausePanel()

        elif self.name == "p3":
            # ============================================================================
            # when using p3, player can stand and attract iris.
            # after 100 frames the tech will disappear and another 300 frames are needed
            # for the next use of tech.
            # =============================================================================
            if frame > 400 and k == "j":               
                    frame = 0
                    iris.affliateState = True
                    self.step = 0
                    iris.irirsStep = 3

            if frame > 100:
                iris.affliateState = False
                iris.irisStep = 5
                self.step = 12

        elif self.name == "p4":
            # ==========================================================================
            # p4 has 50% chance to make either herself or iris sleep for 100 frames. 
            # another 300 frames are needed for using the tech again.
            # ==========================================================================
            if frame>300 and k == "j":
                chance = random.randint(0,1)

                if chance == 0:
                    frame = 0
                    iris.irirsStep = 0
                elif chance == 1:
                    frame = 0
                    self.step = 0

            if frame > 100:
                iris.irirsStep = 5
                self.step =12

        elif self.name == "p5":
            # ===========================================================================
            # when using p5, player can decrease iris's speed to half of the original after
            # stand for 100 frames. iris will remain the slower speed for 100 frames and then
            # another 300 frames are needed for reusing the tech.
            # ===========================================================================
            if frame>500 and k == "j":
                frame = 0
                iris.irirsStep = 2
                self.step = 0
           
            if frame>70: 
                self.step = 14
           
            if frame>200:
                iris.irirsStep = 5

        elif self.name == "p6":
            # ===========================================================================
            # when using p6, player can change iris positions pressing j or k
            # ===========================================================================
            if frame>100:
                if k == "j":
                    frame = 0
                    iris.positionX = -iris.positionX
                elif k == "k":
                    frame = 0
                    iris.positionY = -iris.positionY

        elif self.name == "p7":
            # ===========================================================================
            # when using p7, player can change self positions pressing j or k
            # ===========================================================================
            if frame>100:

                safe = True
                if k == "j":
                
                    for positions in obstaclePositions:
                        if not checkNotCrash(positions,-self.positionX,self.positionY):
                            safe = False
                    
                    if safe == True:
                        frame = 0
                        self.positionX = -self.positionX
                
                elif k == "k":

                    for positions in obstaclePositions:
                        if not checkNotCrash(positions,self.positionX,-self.positionY):
                            safe = False
                    if safe == True: 
                        frame = 0
                        self.positionY = -self.positionY

        elif self.name == "p8":
            # ===========================================================================
            # when using p9, after standing for 50 frame,player can move to the place 
            # near where iris was
            # ===========================================================================
            if frame>200 and k == "j":
                targetx = iris.positionX
                targety = iris.positionY
                self.step = 0
                iris.irisStep = 8

            if frame>250:
                frame = 0
                self.positionX = random.randint(0,100)*targetx/100
                self.positionY = random.randint(0,100)*targety/100
                self.step = 12
                iris.step = 5


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

        # check if moving will crash with obstacles
        safeL = True
        safeR = True
        safeU = True
        safeD = True

        for positions in obstaclePositions:
            # moving left
            if not checkNotCrash(positions,self.positionX-self.step,self.positionY):
                safeL = False

            # moving right
            if not checkNotCrash(positions,self.positionX+self.step,self.positionY):
                safeR = False

            # moving down
            if not checkNotCrash(positions,self.positionX, self.positionY-self.step):
                safeD = False

            # moving up
            if not checkNotCrash(positions,self.positionX, self.positionY+self.step):
                safeU = False

        #-----------check safe status and move---------------------
        if safeL:
            moveLeft()

        if safeR:
            moveRight()

        if safeU:
            moveUp()

        if safeD:
            moveDown()

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

            # move iris and player to new positions
            # generate random player and iris positions
            x1,y1 = random.randint(-500,0),random.randint(-500,0)
            x2,y2 = random.randint(0,500),random.randint(0,500)
            xChance = random.randint(0,1)
            if xChance == 0:
                px=x1
                ix=x2
            else:
                px=x2
                ix=x1
            yChance = random.randint(0,1)
            if yChance == 0:
                py=y1
                iy=y2
            else:
                py=y2
                iy=y1       

            # add to obstacle positions for avoiding creating obstacles on players 
            global characterPositions
            characterPositions = []
            characterPositions.append([px,py])
            characterPositions.append([ix,iy])
            iris.positionX, iris.positionY = ix,iy
            player.positionX, player.positionY = px,py

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
        iris.image.undraw()
        player.image.undraw()
        global obstaclePositions
        obstaclePositions = []
        global characterPositions
        resetScreen()
        initialize(characterID,characterImage)
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

def resetScreen():
    
    iris.irirsStep= 5
    iris.affliateState=False
    player.step=10
    cover = Rectangle(Point(-650,-650),Point(650,650))
    cover.setFill("white")
    cover.draw(win)

def checkNotCrash(position,selfPositionX,selfPositionY):

    #  if crash into obstacles, return false.
    if (-80 < (position[0] - selfPositionX ) < 80) and (-80 < (position[1]- selfPositionY ) < 80):
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

    title = Text(Point(0,0), "抓 住 老 雨 天")
    title.setSize(36)
    title.setTextColor("black")
    title.setStyle("bold")
    title.draw(win)

def selectPlayer():
    # initialize
    resetScreen()
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
    drawObject(-500,0,"img/p1.gif")
    drawObject(-350,0,"img/p2.gif")
    drawObject(-200,0,"img/p3.gif")
    drawObject(-50,0,"img/p4.gif")
    drawObject(100,0,"img/p5.gif")  
    drawObject(250,0,"img/p6.gif")  
    drawObject(400,0,"img/p7.gif")  
    drawObject(550,0,"img/p8.gif")  
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
        global characterID
        global characterImage
        if -550<=xp<=-450 and -60<=yp<=60:
            character = "老宁"    
            characterID = "p1"
            characterImage = "img/p1.gif"
            tkinter.messagebox.showinfo("老宁","飞一般的感觉")

        elif -400<=xp<-300 and -60<=yp<=60:

            character = "小鹅"
            characterID = "p2"
            characterImage = "img/p2.gif"    
            tkinter.messagebox.showinfo("小鹅","使用食物诱惑")

        elif -250<=xp<=-150 and -60<=yp<=60:
            character = "毛毛"
            characterID = "p3"
            characterImage = "img/p3.gif"
            tkinter.messagebox.showinfo("毛毛","会让老雨天忍不住揍一顿")

        elif -100<=xp<=0 and -60<=yp<=60:
            character = "p4"
            characterID = "p4"
            characterImage = "img/p4.gif"
            tkinter.messagebox.showinfo("p4","百分之五十几率让自己或对方陷入沉睡")        
        
        elif 50<=xp<=150 and -60<=yp<=60:
            character = "茉莉"
            characterID = "p5"
            characterImage = "img/p5.gif"
            tkinter.messagebox.showinfo("茉莉","笑声威慑")

        elif 200<=xp<=300 and -60<=yp<=60:
            character = "Elaine"
            characterID = "p6"
            characterImage = "img/p6.gif"
            tkinter.messagebox.showinfo("Elaine","可爱粉红小猪猪")        

        elif 350<=xp<=450 and -60<=yp<=60:
            character = "老雷"
            characterID = "p7"
            characterImage = "img/p7.gif"
            tkinter.messagebox.showinfo("老雷","瞬身战士")

        elif 500<=xp<=600 and -60<=yp<=60:
            character = "阿比"
            characterID = "p8"
            characterImage = "img/p8.gif"
            tkinter.messagebox.showinfo("阿比","冷静观察者")

        elif -80<=xp<=80 and -260<=yp<=-100 and character:
            tkinter.messagebox.showinfo("选中角色","你已选中"+character)
            selected = True
            resetScreen()
            initialize(characterID,characterImage)
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
    obstaclePositions = []
    player.name = characterID
    player.imageID = characterImage
    player.image = Image( Point(player.positionX, player.positionY), characterImage)
    player.image.draw(win)
    
    iris.image.draw(win)
    for i in range(0,15):
        x1,y1 = random.randint(-500,500),random.randint(-500,500)

        safe = True

        for positions in characterPositions:
            if not checkNotCrash(positions,x1,y1):
                safe = False
        for positions in obstaclePositions:
            if not checkNotCrash(positions,x1,y1):
                safe = False

        if safe == True:
            obstaclePositions.append([x1,y1])
            drawObject(x1,y1,"img/obstacle.gif")

def objectGenerator():

    # generate random player and iris positions
    x1,y1 = random.randint(-500,0),random.randint(-500,0)
    x2,y2 = random.randint(0,500),random.randint(0,500)
    xChance = random.randint(0,1)
    if xChance == 0:
        px=x1
        ix=x2
    else:
        px=x2
        ix=x1
    yChance = random.randint(0,1)
    if yChance == 0:
        py=y1
        iy=y2
    else:
        py=y2
        iy=y1       

    # add to obstacle positions for avoiding creating obstacles on players 
    global characterPositions
    characterPositions = []
    characterPositions.append([px,py])
    characterPositions.append([ix,iy])

    # create player and iris
    global player
    player = Player(px,py,"","")
   
    global iris
    iris = Iris(ix,iy, "iris", "img/i1.gif")

    global obstaclePositions
    obstaclePositions=[]


if __name__ == '__main__':
    main()
