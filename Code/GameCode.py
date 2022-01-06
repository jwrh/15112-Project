###################                                         ###################
##                           ESCAPE FROM DUNGEON                             ##
###################                                         ###################
from cmu_112_graphics import *
import math,pandas,numpy,scipy,copy,string,random,time
import tkinter as tk
#########################################

################ caching photos #############


# def make2dList(rows, cols):
#     return [ ([0] * cols) for row in range(rows) ]

# def appStarted(app):
#     url = "theGreatImage.png"
#     app.image1 = app.loadImage(url)
#     app.margin = 20
#     app.rows = app.cols = 50
#     app.images = make2dList(app.rows, app.cols)
#     for row in range(app.rows):
#         for col in range(app.cols):
#             app.images[row][col] = app.scaleImage(app.image1, 0.1)
#     app.counter = 0
#     app.timerDelay = 1
#     app.timerResult = 'Counting to 10...'
#     app.useCachedImages = False
#     resetTimer(app)

# def resetTimer(app):
#     app.time0 = time.time()
#     app.counter = 0

# def timerFired(app):
#     app.counter += 1
#     if (app.counter == 10):
#         duration = time.time() - app.time0
#         app.timerResult = f'Last time to 10: {round(duration,1)}s'
#         app.useCachedImages = not app.useCachedImages
#         resetTimer(app)

# # from www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
# def getCellBounds(app, row, col):
#     # aka "modelToView"
#     # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
#     gridWidth  = app.width - 2*app.margin
#     gridHeight = app.height - 2*app.margin
#     columnWidth = gridWidth / app.cols
#     rowHeight = gridHeight / app.rows
#     x0 = app.margin + col * columnWidth
#     x1 = app.margin + (col+1) * columnWidth
#     y0 = app.margin + row * rowHeight
#     y1 = app.margin + (row+1) * rowHeight
#     return (x0, y0, x1, y1)

# def getCachedPhotoImage(app, image):
#     # stores a cached version of the PhotoImage in the PIL/Pillow image
#     if ('cachedPhotoImage' not in image.__dict__):
#         image.cachedPhotoImage = ImageTk.PhotoImage(image)
#     return image.cachedPhotoImage

################# initialization ###############

class person(object):
    def __init__(self,numba):
        self.number = numba
        if self.number  == 1: #  engineer
            self.speed = 20
            self.attack = 70
            self.hp = 50
            self.ammo = 50

        elif self.number  == 2 : # mercenary 
            self.speed = 35
            self.attack = 60
            self.hp = 40
            self.ammo = 50 
  
        elif self.number  == 3 : # sniper
            self.speed = 50
            self.attack = 60
            self.hp = 20
            self.ammo = 50
  
        elif self.number  == 4 : #  juggernaut
            self.speed = 30
            self.attack = 60
            self.hp = 60
            self.ammo = 50
  
        elif self.number  == 5: #  general
            self.speed = 27
            self.attack =1129
            self.hp = 35
            self.ammo = 50

        elif self.number  == 6 : # the great spartan, 117, Master Chief 
            self.speed = 35
            self.attack = 11170
            self.hp = 160
            self.ammo = 50


class enemy(person):
    def __init__(self,number,x,y):
        self.trigger = False
        self.coord = [x,y]
        if number == 7: # regular enemy
            self.number = 7
            self.speed = 2
            self.attack = 1113
            self.hp = 50
            self.hide = False
        if number == 8: # heavy enemy
            self.number = 8
            self.speed = 2
            self.attack = 16
            self.hp = 100
            self.hide = False
        if number == 9: # boss
            self.number = 8
            self.speed = 12
            self.attack = 121
            self.hp = 40
            self.hide = False
        

class item(object):
    def __init__(self,quantity):
        self.quantity = quantity

class bullet(object):
    def __init__(self,x,y,dx,dy):
        self.coord = [x,y]
        self.vector = [dx,dy]

class heal(item):
    def __init__(self,quantity,effect,lasttime,isPoison):
        self.quantity = quantity
        self.effect = effect
        self.lasttime = lasttime
        if isPoison == 1:
             self.isPoison = True
        else:
            self.isPoison = False

    def useHeal(self):


        if self.isPoison == False:
            self.quantity -= 1
            return self.effect,self.lasttime

        else:
            self.quantity -= 1
            return -self.effect,self.lasttime
    
class food(item):
    def __init__(self,quantity,effect,lasttime,isPoison):
        self.quantity = quantity
        self.effect = effect
        self.lasttime = lasttime
        if isPoison == 1:
             self.isPoison = True
        else:
            self.isPoison = False

    def useFood(self):
        if self.isPoison == False:
            self.quantity -= 1
            return self.effect,self.lasttime

        else:
            self.quantity -= 1
            return -self.effect,self.lasttime


class ammo(item):
    def __init__(self,quantity):
        self.quantity = quantity

class booster(item):
    def __init__(self,effect):
        self.effect = effect
    
    def useBooster(self):
        return True
       


class weapon(object):
    
    def __init__(self,attack,durability,range,rareness,ammo):
        self.attack = attack
        self.durability = durability
        self.range = range 
        self.rareness = rareness
        self.ammo = ammo

    def fire(self):
        self.durability -= 1
        self.ammo -=1 
        return self.attack
    
    def getAmmo(self,ammo):
        self.ammo += ammo
    
    def GunGenerade(self):
        self.durability -= 3
        self.ammo -=5
        return (self.attack*4)
    
def appStarted(app):
    app.mode = 'menu'
    app.scrollX = 0
    app.scrollMargin = 50
    app.pointer = 1
    app.pointer = 0
    app.background  = app.loadImage('welcomemenu.jpg')
    app.background2 = app.scaleImage(app.background, 1.1)
    app.select = app.loadImage('selectPlayer.jpg')
    app.player1 = person(1)
    app.background25  = app.loadImage('map.jpg')
    app.background3  = app.scaleImage(app.background25,0.3)
    app.p1coord = [app.width/2,app.height/2]
    app.playe1 = app.loadImage('rifleUp.jpg')
    app.playe2 = app.loadImage('rifleRight.jpg')
    app.playe3 = app.loadImage('rifleLeft.jpg')
    app.playe4 = app.loadImage('rifleDown.jpg')
    app.playerRifleUp = app.scaleImage(app.playe1,0.5)
    app.playerRifleRight= app.scaleImage(app.playe2,0.5)
    app.playerRifleLeft = app.scaleImage(app.playe3,0.5)
    app.playerRifleDown = app.scaleImage(app.playe4,0.5)
    app.playerImage = app.playerRifleUp
    app.play1 = app.loadImage('flashUp.jpg')
    app.play2 = app.loadImage('flashRight.jpg')
    app.play3 = app.loadImage('flashLeft.jpg')
    app.play4 = app.loadImage('flashDown.jpg')
    app.flashUp = app.scaleImage(app.play1,0.1)
    app.flashRight= app.scaleImage(app.play2,0.1)
    app.flashLeft = app.scaleImage(app.play3,0.1)
    app.flashDown = app.scaleImage(app.play4,0.1)
    app.flashImage = app.flashUp
    app.map = [app.width/2,app.height/2]
    app.enemyImag = app.loadImage('enemy.jpg')
    app.enemyImage = app.scaleImage(app.enemyImag,0.4)
    app.bossImag = app.loadImage('spider.jpg')
    app.bossImage = app.scaleImage(app.bossImag,0.6)
    app.boss = enemy(9,random.randint(-20,20),random.randint(-20,20))
    app.bossMap = app.loadImage('bossMap.jpg')
    app.spawn1 = [10,60]
    app.spawn2 = [760,73.5]
    app.spawn3 = [970,433.5]
    app.bulletImage = app.loadImage('bullet.jpg')
    app.bulletList = []
    app.direction = 'Up'
    app.IsFiring = False
    app.timerCount = 0
    app.ammo = 0
    app.health = 1000
    app.hunger = 50
    app.sleepiness = 50
    app.gunfire = [(1,1),(1,1)]
    app.enemyList = []
    app.gunNumber= 0
    app.instinct = False
    app.timerDelay = 10
    app.message = ''
    
######################## game AI part #################
    #Given Naive Bayes only work on different intervals
    # We have different range to test out
    app.overallFireCount = 0
    app.overallHitCount = 0
    app.interval1 = [] # -25 closest range
    app.interval2 = [] # -40
    app.interval3 = [] # -60

def distance(x1,x2,y1,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
    
################# the menu screen ###############


def menu_keyPressed(app,event):
    if event.key == "Down":
        app.pointer += 1
    if event.key == 'Up':
        app.pointer -= 1
    if event.key == 'F':
        app.mode = 'prePlay'

def menu_redrawAll(app,canvas):
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.background2))
    #canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(woo))
    canvas.create_text(app.width/2,4*app.height/7,text = 'Press F to play', fill = 'white',font = 'impact 40 bold')

################# the prePlay mode ###################

def prePlay_mousePressed(app, event):
    x,y =  event.x,event.y
    if 0<x and x< app.width/4:
        app.player1 = person(1)
        app.mode = 'preprePlay'
    elif app.width/4<x and x< 2*(app.width/4):
        app.player1 = person(2)
        app.mode = 'preprePlay'
    elif 2*(app.width/4)< x and x<3*(app.width/4):
        app.player1 = person(3)
        app.mode = 'preprePlay'
    elif 3*(app.width/4)<x and x< app.width:
        app.player1 = person(4)
        app.mode = 'preprePlay'
    
def prePlay_redrawAll(app, canvas):
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.select))
    canvas.create_text(app.width/2,  30,
                       text='Choose Character 1', font='impact 30 bold')

################# the preprePlay mode ###################

def prePlay_mousePressed(app, event): # choose player 2.
    x,y =  event.x,event.y
    if 0<x and x< app.width/4:   
        app.player1 = person(1)
        app.mode = 'play'
    elif app.width/4<x and x< 2*(app.width/4):
        app.player1 = person(2)
        app.mode = 'play'
    elif 2*(app.width/4)< x and x<3*(app.width/4):
        app.player1 = person(3)
        app.mode = 'play'
    elif 3*(app.width/4)<x and x< app.width:
        app.player1 = person(4)
        app.mode = 'play'
    
def prePlay_redrawAll(app, canvas):
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.select))
    canvas.create_text(app.width/2,  30,
                       text='Choose Character ', font='impact 30 bold')

################ choose Terrain ##################

def terrain_mousePressed(app,event): # under construction.
    x = event.x
    y = event.y
    app.mode = 'play'

############################  game AI 1 ######################################



def map1(x,y,a,b): # the is the hardcoded map 
    cx, cy = x+a,y+b
    if cx > 1000 or cx < -1000 or cy > 1000 or cy < -1000:
        return False
    elif cx<240 and cx > 90 and cy < 323.5 and cy > -81.5:
        return False
    elif -130 < cx and cx < 340 and 373.5 < cy and cy < 523.5:
        return False
    elif 220 < cx and cx < 360 and 618.5 < cy and cy < 758.5:
        return False
    elif 535 < cx and cx < 640 and 303.5 < cy and cy < 7000:
        return False
    elif 395 < cx and cx < 570 and 58.5 < cy and cy < 198.5:
        return False
    elif 745 < cx and cx < 920 and 198.5 < cy and cy < 373.5:
        return False
    elif 885 < cx and cx < 9000 and 23.5 < cy and cy < 128.5:
        return False
    elif 750 < cx and cx < 1190 and 573.5 < cy and cy < 673.5:
        return False
    elif 1090 < cx and cx < 1190 and 423.5 < cy and cy < 5000:
        return False
    else:
        return True
    


def pathfinder(app):
    for enemy in app.enemyList:
        ex, ey = enemy.coord[0],enemy.coord[1]
        v = enemy.speed
        if map1(ex,ey,0,v) == False :
            enemy.coord[0] += v
        else:
            enemy.coord[1] += v
            


def convergeOnPlayer(app):
    px,py = app.p1coord[0],app.p1coord[1]
    for enemies in app.enemyList:
        d = distance(enemies.coord[0],enemies.coord[1],app.p1coord[0],app.p1coord[1])
        dx = ((enemies.coord[0] -app.p1coord[0])*enemies.speed)/d
        dy = ((enemies.coord[1] -app.p1coord[1])*enemies.speed)/d
        if map1(enemies.coord[0],enemies.coord[1],dx,dy):
            enemies.coord[0] -= dx
            enemies.coord[1] -= dy

############################  game AI 2 ###################################### 


def bayes(app,a,b):
    p1 = app.overallHitCount/app.overallFireCount
    p2 = a/b
    return (p1*p2)

def bayesAI(app,x):
    prob1 = bayes(app,app.interval1[0],app.interval1[1])
    prob2 = bayes(app,app.interval2[0],app.interval2[1])
    prob3 = bayes(app,app.interval3[0],app.interval3[1])
    if prob1 ==  max(prob1,prob2,prob3):
        return 1
    elif prob2 == max(prob1,prob2,prob3):
        return 2
    else:
        return 3
    


############################  game AI 3 ###################################### 



def bossAI(app):
    d = distance(app.boss.coord[0],app.boss.coord[1],app.p1coord[0],app.p1coord[1])
    if app.IsFiring == False:
        dx = ((app.boss.coord[0] -app.p1coord[0])*app.boss.speed)/d
        dy = ((app.boss.coord[1] -app.p1coord[1])*app.boss.speed)/d
        app.boss.coord[0] -= dx
        app.boss.coord[1] -= dy
    else:  
        for bullet in app.bulletList:
            if (bullet.vector[0] == 0 and 
            bullet.coord[1] -30<= app.boss.coord[1] 
            and app.boss.coord[1] <= bullet.coord[1]+30):
                app.boss.coord[1] += random.randint(-60,-30)
            elif (bullet.vector[1] == 0 and 
            bullet.coord[0] -30<= app.boss.coord[0] 
            and app.boss.coord[0] <= bullet.coord[1]+30):
                app.boss.coord[0] += random.randint(40,100)


 ######################### play mode ##############################

# we employ the second sidescroller method, which involves a player margin.


def map(app,a,b): # the is the hardcoded map 
    cx,cy = app.p1coord[0]+a,app.p1coord[1]+b
    # if cx < -100 and cx >
    if cx<240 and cx > 90 and cy < 323.5 and cy > -81.5:
        return False
    elif -130 < cx and cx < 340 and 373.5 < cy and cy < 523.5:
        return False
    elif 220 < cx and cx < 360 and 618.5 < cy and cy < 758.5:
        return False
    elif 535 < cx and cx < 640 and 303.5 < cy and cy < 7000:
        return False
    elif 395 < cx and cx < 570 and 58.5 < cy and cy < 198.5:
        return False
    elif 745 < cx and cx < 920 and 198.5 < cy and cy < 373.5:
        return False
    elif 885 < cx and cx < 9000 and 23.5 < cy and cy < 128.5:
        return False
    elif 750 < cx and cx < 1190 and 573.5 < cy and cy < 673.5:
        return False
    elif 1090 < cx and cx < 1190 and 423.5 < cy and cy < 5000:
        return False
    else:
        return True
    

def win(app):
    if app.p1coord[0] >1200 and app.p1coord[1] > 688.5:
        app.bulletList = []
        app.p1coord[0],app.p1coord[1] = app.width/2,app.height/2
        app.mode = 'boss'


def traj(app):
    for bullet in app.bulletList:
        cx,cy = bullet.coord[0],bullet.coord[1]
        vx, vy= bullet.vector[0],bullet.vector[1]
        if map1(cx,cy,vx,vy) == False:
            bullet.coord[0],bullet.coord[1] = -500,-500
            bullet.vector[0],bullet.vector[1] = 0,0
        else:
            bullet.coord[0] += bullet.vector[0]
            bullet.coord[1]+= bullet.vector[1]
        
def hit(app):
    for bullet in app.bulletList:
        for enemy in app.enemyList:
            if (bullet.coord[0] < enemy.coord[0]+20 and bullet.coord[0] > enemy.coord[0]-20
            and bullet.coord[1] < enemy.coord[1] +20 and bullet.coord[1] >enemy.coord[1] -20):
                enemy.hp -= app.player1.attack
    for enemy in app.enemyList:
        if(app.p1coord[0] < enemy.coord[0]+10 and app.p1coord[0] > enemy.coord[0]-10
            and app.p1coord[1] < enemy.coord[1] +10 and app.p1coord[1] > enemy.coord[1] -10):
                app.player1.hp -= app.boss.attack


def spawnEnemy(app):
    randomX = app.spawn1[0]+random.randint(-7,7)
    randomY = app.spawn1[1]+random.randint(-7,7)
    newEnemy = enemy(7,randomX,randomY)
    app.enemyList.append(newEnemy)
    randommX = app.spawn2[0]+random.randint(-7,7)
    randommY = app.spawn2[1]+random.randint(-7,7)
    newEnmy = enemy(8,randommX,randommY)
    app.enemyList.append(newEnmy)
    randommmX = app.spawn3[0]+random.randint(-7,7)
    randommmY = app.spawn3[1]+random.randint(-7,7)
    newEnemmy = enemy(8,randommmX,randommmY)
    app.enemyList.append(newEnemmy)


def play_timerFired(app):
    app.IsFiring = False
    app.timerCount += 1
    convergeOnPlayer(app)
    traj(app)
    hit(app)
    win(app)
    for enemy in app.enemyList:
        if enemy.hp <= 0:
            enemy.coord[0],enemy.coord[1] = -300,-300
    if app.timerCount % 18 == 0:
        spawnEnemy(app)
    
 
def play_keyPressed(app,event):
    print(app.p1coord[0],app.p1coord[1]) # Maybe use pygame to smoothen the control

    if event.key == 'W' :
        app.playerImage = app.playerRifleUp
        app.flashImage = app.flashUp
        app.direction = 'Up'
        v = -app.player1.speed
        if map(app,0,v) :
            for enemy in app.enemyList:
                enemy.coord[1] += app.player1.speed 
            for enemy in app.bulletList:
                enemy.coord[1] += app.player1.speed
            app.p1coord[1] -= app.player1.speed 
            app.spawn1[1] += app.player1.speed 
            app.map[1] += app.player1.speed 
    if event.key == 'S':
        app.playerImage = app.playerRifleDown
        app.flashImage = app.flashDown
        app.direction = 'Down'
        v = app.player1.speed
        if map(app,0,v):
            for enemy in app.enemyList:
                enemy.coord[1] -= app.player1.speed
            for enemy in app.bulletList:
                enemy.coord[1] -= app.player1.speed
            app.spawn1[1] -= app.player1.speed 
            app.p1coord[1] += app.player1.speed 
            app.map[1]-= app.player1.speed 
    if event.key == 'A':
        app.playerImage = app.playerRifleLeft
        app.flashImage = app.flashLeft
        app.direction = 'Left'
        v = -app.player1.speed
        if map(app,v,0):
            for enemy in app.enemyList:
                enemy.coord[0] += app.player1.speed
            for enemy in app.bulletList:
                enemy.coord[0] += app.player1.speed
            app.spawn1[0] += app.player1.speed 
            app.p1coord[0] -= app.player1.speed 
            app.map[0] += app.player1.speed   
    if event.key == 'D':
        app.playerImage = app.playerRifleRight
        app.flashImage = app.flashRight
        app.direction = 'Right'
        v = app.player1.speed
        if map(app,v,0):
            for enemy in app.enemyList:
                enemy.coord[0] -= app.player1.speed
            for enemy in app.bulletList:
                enemy.coord[0] -= app.player1.speed
            app.spawn1[0] -= app.player1.speed 
            app.p1coord[0] += app.player1.speed 
            app.map[0]-= app.player1.speed  
    if event.key == 'E':
        app.IsFiring = True
        if app.playerImage == app.playerRifleRight:
            app.bulletList.append(bullet(app.width/2+70,app.height/2+20,70,0))
        if app.playerImage == app.playerRifleLeft:
            app.bulletList.append(bullet(app.width/2-70,app.height/2-20,-70,0))
        if app.playerImage == app.playerRifleUp:
            app.bulletList.append(bullet(app.width/2+20,app.height/2-70,0,-70))
        if app.playerImage == app.playerRifleDown:
            app.bulletList.append(bullet(app.width/2-20,app.height/2+70,0,70))

    ###############################


    # if event.key == 'W' and 'A' :
    #     app.p1coord[1] -= app.player1.speed 
    #     app.p1coord[0] -= app.player1.speed 
    # if event.key == 'W' and 'D':
    #     app.p1coord[1] -= app.player1.speed
    #     app.p1coord[0] += app.player1.speed
    # if event.key == 'S' and 'A' :
    #     app.p1coord[1] -= app.player1.speed
    #     app.p1coord[0] -= app.player1.speed  
    # if event.key == 'S' and 'D':
    #     app.p1coord[1] -= app.player1.speed
    #     app.p1coord[0] += app.player1.speed

    # # the control console of player 2
    # if event.key == 'Up':
    #     app.p1coord[0] += app.player1.speed 
    # if event.key == 'Down':
    #     app.p1coord[0] -= app.player1.speed
    # if event.key == 'Left':
    #     app.p1coord[1] -= app.player1.speed 
    # if event.key == 'Right':
    #     app.p1coord[1] += app.player1.speed

def spawnItem(app):
    r = random.randint(1,4)
    parameters = random.randint(1,30)
    x = random.randint(app.width)
    y = random.randint(app.height)
    if r == 1:
        app.items.append([food(parameters),x,y])
    elif r == 2:
        app.items.append([heal,x])

def play_redrawAll(app,canvas):
    canvas.create_rectangle(-5000,-5000,5000,5000,fill = 'black')
    canvas.create_image(app.map[0],app.map[1],image = ImageTk.PhotoImage(app.background3))
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.playerImage))
    for bullet in app.bulletList:
        canvas.create_image(bullet.coord[0],bullet.coord[1],image = ImageTk.PhotoImage(app.bulletImage))
    for enemy in app.enemyList:
        canvas.create_image(enemy.coord[0],enemy.coord[1],image = ImageTk.PhotoImage(app.enemyImage))
    if app.IsFiring == True:
        if app.direction == 'Left':
            canvas.create_image(app.width/2-70,app.height/2-20,image = ImageTk.PhotoImage(app.flashImage))
        if app.direction == 'Right':
            canvas.create_image(app.width/2+70,app.height/2+20,image = ImageTk.PhotoImage(app.flashImage))
        if app.direction == 'Up':
            canvas.create_image(app.width/2+20,app.height/2-70,image = ImageTk.PhotoImage(app.flashImage))
        if app.direction == 'Down':
            canvas.create_image(app.width/2-20,app.height/2+70,image = ImageTk.PhotoImage(app.flashImage))


############################## boss mode ################################

def boss_timerFired(app):
    app.IsFiring = False
    trajBoss(app)
    bossAI(app)
    isHHit(app)
    if app.boss.hp <= 0:
        app.boss.speed = 0
        app.message = 'You Won'
    elif app.player1.hp<= 0:
        app.message = 'You lost'

def isHHit(app):
    for bullet in app.bulletList:
        if (bullet.coord[0] < app.boss.coord[0]+10 and bullet.coord[0] > app.boss.coord[0]-10
        and bullet.coord[1] < app.boss.coord[1] +10 and bullet.coord[1] > app.boss.coord[1] -10):
            app.boss.hp -= app.player1.attack
    if(app.p1coord[0] < app.boss.coord[0]+10 and app.p1coord[0] > app.boss.coord[0]-10
        and app.p1coord[1] < app.boss.coord[1] +10 and app.p1coord[1] > app.boss.coord[1] -10):
            app.player1.hp -= app.boss.attack




def trajBoss(app):
    for bullet in app.bulletList:
        cx,cy = bullet.coord[0],bullet.coord[1]
        vx, vy= bullet.vector[0],bullet.vector[1]
        if cx > 1500 or cy > 800:
            bullet.coord[0],bullet.coord[1] = -500,-500
            bullet.vector[0],bullet.vector[1] = 0,0
        else:
            bullet.coord[0] += bullet.vector[0]
            bullet.coord[1]+= bullet.vector[1]


def boss_keyPressed(app,event):
    print(app.p1coord[0],app.p1coord[1]) # Maybe use pygame to smoothen the control

    if event.key == 'W' :
        app.playerImage = app.playerRifleUp
        app.flashImage = app.flashUp
        app.direction = 'Up'
        v = -app.player1.speed
       
        app.p1coord[1] -= app.player1.speed 

    if event.key == 'S':
        app.playerImage = app.playerRifleDown
        app.flashImage = app.flashDown
        app.direction = 'Down'
        v = app.player1.speed
        app.p1coord[1] += app.player1.speed 
            
    if event.key == 'A':
        app.playerImage = app.playerRifleLeft
        app.flashImage = app.flashLeft
        app.direction = 'Left'
        v = -app.player1.speed
        app.p1coord[0] -= app.player1.speed 
    if event.key == 'D':
        app.playerImage = app.playerRifleRight
        app.flashImage = app.flashRight
        app.direction = 'Right'
        v = app.player1.speed
        app.p1coord[0] += app.player1.speed  
    if event.key == 'E':
        app.IsFiring = True
        if app.playerImage == app.playerRifleRight:
            app.bulletList.append(bullet(app.p1coord[0]+70,app.p1coord[1]+20,70,0))
        if app.playerImage == app.playerRifleLeft:
            app.bulletList.append(bullet(app.p1coord[0]-70,app.p1coord[1]-20,-70,0))
        if app.playerImage == app.playerRifleUp:
            app.bulletList.append(bullet(app.p1coord[0]+20,app.p1coord[1]-70,0,-70))
        if app.playerImage == app.playerRifleDown:
            app.bulletList.append(bullet(app.p1coord[0]-20,app.p1coord[1]+70,0,70))
        
                
def boss_redrawAll(app,canvas):
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.bossMap))
    canvas.create_image(app.p1coord[0],app.p1coord[1],image = ImageTk.PhotoImage(app.playerImage))
    for bullet in app.bulletList:
        canvas.create_image(bullet.coord[0],bullet.coord[1],image = ImageTk.PhotoImage(app.bulletImage))
    canvas.create_image(app.boss.coord[0],app.boss.coord[1],image = ImageTk.PhotoImage(app.bossImage))
    if app.IsFiring == True:
        if app.direction == 'Left':
            canvas.create_image(app.p1coord[0]-70,app.p1coord[1]-20,image = ImageTk.PhotoImage(app.flashImage))
        if app.direction == 'Right':
            canvas.create_image(app.p1coord[0]+70,app.p1coord[1]+20,image = ImageTk.PhotoImage(app.flashImage))
        if app.direction == 'Up':
            canvas.create_image(app.p1coord[0]+20,app.p1coord[1]-70,image = ImageTk.PhotoImage(app.flashImage))
        if app.direction == 'Down':
            canvas.create_image(app.p1coord[0]-20,app.p1coord[1]+70,image = ImageTk.PhotoImage(app.flashImage))
    canvas.create_text(app.width/2,app.height/2,text = app.message, font = 'impact 100 bold',fill = 'white')


    
runApp(width = 1280, height =747)
# ###################                                         ###################
# ##                           ESCAPE FROM DUNGEON                             ##
# ###################                                         ###################
# from cmu_112_graphics import *
# import math,pandas,numpy,scipy,copy,string,random,time
# import tkinter as tk
# #########################################

# ################ caching photos #############

# #from https://www.cs.cmu.edu/~112/syllabus.html
# # images from https://opengameart.org

# # def make2dList(rows, cols):
# #     return [ ([0] * cols) for row in range(rows) ]

# # def appStarted(app):
# #     url = "theGreatImage.png"
# #     app.image1 = app.loadImage(url)
# #     app.margin = 20
# #     app.rows = app.cols = 50
# #     app.images = make2dList(app.rows, app.cols)
# #     for row in range(app.rows):
# #         for col in range(app.cols):
# #             app.images[row][col] = app.scaleImage(app.image1, 0.1)
# #     app.counter = 0
# #     app.timerDelay = 1
# #     app.timerResult = 'Counting to 10...'
# #     app.useCachedImages = False
# #     resetTimer(app)

# # def resetTimer(app):
# #     app.time0 = time.time()
# #     app.counter = 0

# # def timerFired(app):
# #     app.counter += 1
# #     if (app.counter == 10):
# #         duration = time.time() - app.time0
# #         app.timerResult = f'Last time to 10: {round(duration,1)}s'
# #         app.useCachedImages = not app.useCachedImages
# #         resetTimer(app)

# # # from www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
# # def getCellBounds(app, row, col):
# #     # aka "modelToView"
# #     # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
# #     gridWidth  = app.width - 2*app.margin
# #     gridHeight = app.height - 2*app.margin
# #     columnWidth = gridWidth / app.cols
# #     rowHeight = gridHeight / app.rows
# #     x0 = app.margin + col * columnWidth
# #     x1 = app.margin + (col+1) * columnWidth
# #     y0 = app.margin + row * rowHeight
# #     y1 = app.margin + (row+1) * rowHeight
# #     return (x0, y0, x1, y1)

# # def getCachedPhotoImage(app, image):
# #     # stores a cached version of the PhotoImage in the PIL/Pillow image
# #     if ('cachedPhotoImage' not in image.__dict__):
# #         image.cachedPhotoImage = ImageTk.PhotoImage(image)
# #     return image.cachedPhotoImage

# ################# initialization ###############

# class person(object):
#     def __init__(self,numba):
#         self.number = numba
#         if self.number  == 1: #  engineer
#             self.speed = 20
#             self.attack = 70
#             self.hp = 50
#             self.ammo = 50

#         elif self.number  == 2 : # mercenary 
#             self.speed = 35
#             self.attack = 60
#             self.hp = 40
#             self.ammo = 50 
  
#         elif self.number  == 3 : # sniper
#             self.speed = 50
#             self.attack = 60
#             self.hp = 20
#             self.ammo = 50
  
#         elif self.number  == 4 : #  juggernaut
#             self.speed = 30
#             self.attack = 60
#             self.hp = 60
#             self.ammo = 50
  
#         elif self.number  == 5: #  general
#             self.speed = 27
#             self.attack =1129
#             self.hp = 35
#             self.ammo = 50

#         elif self.number  == 6 : # the great spartan, 117, Master Chief 
#             self.speed = 35
#             self.attack = 11170
#             self.hp = 160
#             self.ammo = 50


# class enemy(person):
#     def __init__(self,number,x,y):
#         self.trigger = False
#         self.coord = [x,y]
#         if number == 7: # regular enemy
#             self.number = 7
#             self.speed = 2
#             self.attack = 1113
#             self.hp = 50
#             self.hide = False
#         if number == 8: # heavy enemy
#             self.number = 8
#             self.speed = 2
#             self.attack = 16
#             self.hp = 100
#             self.hide = False
#         if number == 9: # boss
#             self.number = 8
#             self.speed = 12
#             self.attack = 121
#             self.hp = 10000
#             self.hide = False
        

# class item(object):
#     def __init__(self,quantity):
#         self.quantity = quantity

# class bullet(object):
#     def __init__(self,x,y,dx,dy):
#         self.coord = [x,y]
#         self.vector = [dx,dy]

# class heal(item):
#     def __init__(self,quantity,effect,lasttime,isPoison):
#         self.quantity = quantity
#         self.effect = effect
#         self.lasttime = lasttime
#         if isPoison == 1:
#              self.isPoison = True
#         else:
#             self.isPoison = False

#     def useHeal(self):


#         if self.isPoison == False:
#             self.quantity -= 1
#             return self.effect,self.lasttime

#         else:
#             self.quantity -= 1
#             return -self.effect,self.lasttime
    
# class food(item):
#     def __init__(self,quantity,effect,lasttime,isPoison):
#         self.quantity = quantity
#         self.effect = effect
#         self.lasttime = lasttime
#         if isPoison == 1:
#              self.isPoison = True
#         else:
#             self.isPoison = False

#     def useFood(self):
#         if self.isPoison == False:
#             self.quantity -= 1
#             return self.effect,self.lasttime

#         else:
#             self.quantity -= 1
#             return -self.effect,self.lasttime


# class ammo(item):
#     def __init__(self,quantity):
#         self.quantity = quantity

# class booster(item):
#     def __init__(self,effect):
#         self.effect = effect
    
#     def useBooster(self):
#         return True
       


# class weapon(object):
    
#     def __init__(self,attack,durability,range,rareness,ammo):
#         self.attack = attack
#         self.durability = durability
#         self.range = range 
#         self.rareness = rareness
#         self.ammo = ammo

#     def fire(self):
#         self.durability -= 1
#         self.ammo -=1 
#         return self.attack
    
#     def getAmmo(self,ammo):
#         self.ammo += ammo
    
#     def GunGenerade(self):
#         self.durability -= 3
#         self.ammo -=5
#         return (self.attack*4)
    
# def appStarted(app):
#     app.mode = 'menu'
#     app.scrollX = 0
#     app.scrollMargin = 50
#     app.pointer = 1
#     app.pointer = 0
#     app.background  = app.loadImage('welcomemenu.jpg')
#     app.background2 = app.scaleImage(app.background, 1.1)
#     app.select = app.loadImage('selectPlayer.jpg')
#     app.player1 = person(1)
#     app.background25  = app.loadImage('map.jpg')
#     app.background3  = app.scaleImage(app.background25,0.3)
#     app.p1coord = [app.width/2,app.height/2]
#     app.playe1 = app.loadImage('rifleUp.jpg')
#     app.playe2 = app.loadImage('rifleRight.jpg')
#     app.playe3 = app.loadImage('rifleLeft.jpg')
#     app.playe4 = app.loadImage('rifleDown.jpg')
#     app.playerRifleUp = app.scaleImage(app.playe1,0.5)
#     app.playerRifleRight= app.scaleImage(app.playe2,0.5)
#     app.playerRifleLeft = app.scaleImage(app.playe3,0.5)
#     app.playerRifleDown = app.scaleImage(app.playe4,0.5)
#     app.playerImage = app.playerRifleUp
#     app.play1 = app.loadImage('flashUp.jpg')
#     app.play2 = app.loadImage('flashRight.jpg')
#     app.play3 = app.loadImage('flashLeft.jpg')
#     app.play4 = app.loadImage('flashDown.jpg')
#     app.flashUp = app.scaleImage(app.play1,0.1)
#     app.flashRight= app.scaleImage(app.play2,0.1)
#     app.flashLeft = app.scaleImage(app.play3,0.1)
#     app.flashDown = app.scaleImage(app.play4,0.1)
#     app.flashImage = app.flashUp
#     app.map = [app.width/2,app.height/2]
#     app.enemyImag = app.loadImage('enemy.jpg')
#     app.enemyImage = app.scaleImage(app.enemyImag,0.4)
#     app.bossImag = app.loadImage('spider.jpg')
#     app.bossImage = app.scaleImage(app.bossImag,0.6)
#     app.boss = enemy(9,random.randint(-20,20),random.randint(-20,20))
#     app.bossMap = app.loadImage('bossMap.jpg')
#     app.spawn1 = [10,60]
#     app.spawn2 = [760,73.5]
#     app.spawn3 = [970,433.5]
#     app.bulletImage = app.loadImage('bullet.jpg')
#     app.bulletList = []
#     app.direction = 'Up'
#     app.IsFiring = False
#     app.timerCount = 0
#     app.ammo = 0
#     app.health = 1000
#     app.hunger = 50
#     app.sleepiness = 50
#     app.gunfire = [(1,1),(1,1)]
#     app.enemyList = []
#     app.gunNumber= 0
#     app.instinct = False
#     app.timerDelay = 1
#     app.message = ''
    
# ######################## game AI part #################
#     #Given Naive Bayes only work on different intervals
#     # We have different range to test out
#     app.overallFireCount = 0
#     app.overallHitCount = 0
#     app.interval1 = [] # -25 closest range
#     app.interval2 = [] # -40
#     app.interval3 = [] # -60

# def distance(x1,x2,y1,y2):
#     return math.sqrt((x1-x2)**2+(y1-y2)**2)
    
# ################# the menu screen ###############


# def menu_keyPressed(app,event):
#     if event.key == "Down":
#         app.pointer += 1
#     if event.key == 'Up':
#         app.pointer -= 1
#     if event.key == 'F':
#         app.mode = 'prePlay'

# def menu_redrawAll(app,canvas):
#     canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.background2))
#     #canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(woo))
#     canvas.create_text(app.width/2,4*app.height/7,text = 'Press F to play', fill = 'white',font = 'impact 40 bold')

# ################# the prePlay mode ###################

# def prePlay_mousePressed(app, event):
#     x,y =  event.x,event.y
#     if 0<x and x< app.width/4:
#         app.player1 = person(1)
#         app.mode = 'preprePlay'
#     elif app.width/4<x and x< 2*(app.width/4):
#         app.player1 = person(2)
#         app.mode = 'preprePlay'
#     elif 2*(app.width/4)< x and x<3*(app.width/4):
#         app.player1 = person(3)
#         app.mode = 'preprePlay'
#     elif 3*(app.width/4)<x and x< app.width:
#         app.player1 = person(4)
#         app.mode = 'preprePlay'
    
# def prePlay_redrawAll(app, canvas):
#     canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.select))
#     canvas.create_text(app.width/2,  30,
#                        text='Choose Character 1', font='impact 30 bold')

# ################# the preprePlay mode ###################

# def prePlay_mousePressed(app, event): # choose player 2.
#     x,y =  event.x,event.y
#     if 0<x and x< app.width/4:   
#         app.player1 = person(1)
#         app.mode = 'play'
#     elif app.width/4<x and x< 2*(app.width/4):
#         app.player1 = person(2)
#         app.mode = 'play'
#     elif 2*(app.width/4)< x and x<3*(app.width/4):
#         app.player1 = person(3)
#         app.mode = 'play'
#     elif 3*(app.width/4)<x and x< app.width:
#         app.player1 = person(4)
#         app.mode = 'play'
    
# def prePlay_redrawAll(app, canvas):
#     canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.select))
#     canvas.create_text(app.width/2,  30,
#                        text='Choose Character ', font='impact 30 bold')

# ################ choose Terrain ##################

# def terrain_mousePressed(app,event): # under construction.
#     x = event.x
#     y = event.y
#     app.mode = 'play'

# ############################  game AI 1 ######################################



# def map1(x,y,a,b): # the is the hardcoded map 
#     cx, cy = x+a,y+b
#     if cx > 1000 or cx < -1000 or cy > 1000 or cy < -1000:
#         return False
#     elif cx<240 and cx > 90 and cy < 323.5 and cy > -81.5:
#         return False
#     elif -130 < cx and cx < 340 and 373.5 < cy and cy < 523.5:
#         return False
#     elif 220 < cx and cx < 360 and 618.5 < cy and cy < 758.5:
#         return False
#     elif 535 < cx and cx < 640 and 303.5 < cy and cy < 7000:
#         return False
#     elif 395 < cx and cx < 570 and 58.5 < cy and cy < 198.5:
#         return False
#     elif 745 < cx and cx < 920 and 198.5 < cy and cy < 373.5:
#         return False
#     elif 885 < cx and cx < 9000 and 23.5 < cy and cy < 128.5:
#         return False
#     elif 750 < cx and cx < 1190 and 573.5 < cy and cy < 673.5:
#         return False
#     elif 1090 < cx and cx < 1190 and 423.5 < cy and cy < 5000:
#         return False
#     else:
#         return True
    


# def pathfinder(app):
#     for enemy in app.enemyList:
#         ex, ey = enemy.coord[0],enemy.coord[1]
#         v = enemy.speed
#         if map1(ex,ey,0,v) == False :
#             enemy.coord[0] += v
#         else:
#             enemy.coord[1] += v
            


# def convergeOnPlayer(app):
#     px,py = app.p1coord[0],app.p1coord[1]
#     for enemies in app.enemyList:
#         d = distance(enemies.coord[0],enemies.coord[1],app.p1coord[0],app.p1coord[1])
#         dx = ((enemies.coord[0] -app.p1coord[0])*enemies.speed)/d
#         dy = ((enemies.coord[1] -app.p1coord[1])*enemies.speed)/d
#         if map1(enemies.coord[0],enemies.coord[1],dx,dy):
#             enemies.coord[0] -= dx
#             enemies.coord[1] -= dy

# ############################  game AI 2 ###################################### 


# def bayes(app,a,b):
#     p1 = app.overallHitCount/app.overallFireCount
#     p2 = a/b
#     return (p1*p2)

# def bayesAI(app,x):
#     prob1 = bayes(app,app.interval1[0],app.interval1[1])
#     prob2 = bayes(app,app.interval2[0],app.interval2[1])
#     prob3 = bayes(app,app.interval3[0],app.interval3[1])
#     if prob1 ==  max(prob1,prob2,prob3):
#         return 1
#     elif prob2 == max(prob1,prob2,prob3):
#         return 2
#     else:
#         return 3
    


# ############################  game AI 3 ###################################### 



# def bossAI(app):
#     d = distance(app.boss.coord[0],app.boss.coord[1],app.p1coord[0],app.p1coord[1])
#     if app.IsFiring == False:
#         dx = ((app.boss.coord[0] -app.p1coord[0])*app.boss.speed)/d
#         dy = ((app.boss.coord[1] -app.p1coord[1])*app.boss.speed)/d
#         app.boss.coord[0] -= dx
#         app.boss.coord[1] -= dy
#     else:  
#         for bullet in app.bulletList:
#             if (bullet.vector[0] == 0 and 
#             bullet.coord[1] -10<= app.boss.coord[1] 
#             and app.boss.coord[1] <= bullet.coord[1]+10):
#                 app.boss.coord[1] += random.randint(-10,10)
#             elif (bullet.vector[1] == 0 and 
#             bullet.coord[0] -10<= app.boss.coord[0] 
#             and app.boss.coord[0] <= bullet.coord[1]+10):
#                 app.boss.coord[0] += random.randint(-10,10)


#  ######################### play mode ##############################

# # we employ the second sidescroller method, which involves a player margin.


# def map(app,a,b): # the is the hardcoded map 
#     cx,cy = app.p1coord[0]+a,app.p1coord[1]+b
#     # if cx < -100 and cx >
#     if cx<240 and cx > 90 and cy < 323.5 and cy > -81.5:
#         return False
#     elif -130 < cx and cx < 340 and 373.5 < cy and cy < 523.5:
#         return False
#     elif 220 < cx and cx < 360 and 618.5 < cy and cy < 758.5:
#         return False
#     elif 535 < cx and cx < 640 and 303.5 < cy and cy < 7000:
#         return False
#     elif 395 < cx and cx < 570 and 58.5 < cy and cy < 198.5:
#         return False
#     elif 745 < cx and cx < 920 and 198.5 < cy and cy < 373.5:
#         return False
#     elif 885 < cx and cx < 9000 and 23.5 < cy and cy < 128.5:
#         return False
#     elif 750 < cx and cx < 1190 and 573.5 < cy and cy < 673.5:
#         return False
#     elif 1090 < cx and cx < 1190 and 423.5 < cy and cy < 5000:
#         return False
#     else:
#         return True
    

# def win(app):
#     if app.p1coord[0] >1200 and app.p1coord[1] > 688.5:
#         app.bulletList = []
#         app.p1coord[0],app.p1coord[1] = app.width/2,app.height/2
#         app.mode = 'boss'


# def traj(app):
#     for bullet in app.bulletList:
#         cx,cy = bullet.coord[0],bullet.coord[1]
#         vx, vy= bullet.vector[0],bullet.vector[1]
#         if map1(cx,cy,vx,vy) == False:
#             bullet.coord[0],bullet.coord[1] = -500,-500
#             bullet.vector[0],bullet.vector[1] = 0,0
#         else:
#             bullet.coord[0] += bullet.vector[0]
#             bullet.coord[1]+= bullet.vector[1]
        
# def hit(app):
#     for bullet in app.bulletList:
#         for enemy in app.enemyList:
#             if (bullet.coord[0] < enemy.coord[0]+20 and bullet.coord[0] > enemy.coord[0]-20
#             and bullet.coord[1] < enemy.coord[1] +20 and bullet.coord[1] >enemy.coord[1] -20):
#                 enemy.hp -= app.player1.attack
#     for enemy in app.enemyList:
#         if(app.p1coord[0] < enemy.coord[0]+10 and app.p1coord[0] > enemy.coord[0]-10
#             and app.p1coord[1] < enemy.coord[1] +10 and app.p1coord[1] > enemy.coord[1] -10):
#                 app.player1.hp -= app.boss.attack


# def spawnEnemy(app):
#     randomX = app.spawn1[0]+random.randint(-7,7)
#     randomY = app.spawn1[1]+random.randint(-7,7)
#     newEnemy = enemy(7,randomX,randomY)
#     app.enemyList.append(newEnemy)
#     randommX = app.spawn2[0]+random.randint(-7,7)
#     randommY = app.spawn2[1]+random.randint(-7,7)
#     newEnmy = enemy(8,randommX,randommY)
#     app.enemyList.append(newEnmy)
#     randommmX = app.spawn3[0]+random.randint(-7,7)
#     randommmY = app.spawn3[1]+random.randint(-7,7)
#     newEnemmy = enemy(8,randommmX,randommmY)
#     app.enemyList.append(newEnemmy)


# def play_timerFired(app):
#     print(app.bulletList)
#     app.IsFiring = False
#     app.timerCount += 1
#     convergeOnPlayer(app)
#     traj(app)
#     hit(app)
#     win(app)
#     for enemy in app.enemyList:
#         if enemy.hp <= 0:
#             enemy.coord[0],enemy.coord[1] = -300,-300
#     if app.timerCount % 180 == 0:
#         spawnEnemy(app)
    
 
# def play_keyPressed(app,event):
# # Maybe use pygame to smoothen the control
#     if event.key == 'W' :
#         app.playerImage = app.playerRifleUp
#         app.flashImage = app.flashUp
#         app.direction = 'Up'
#         v = -app.player1.speed
#         if map(app,0,v) :
#             for enemy in app.enemyList:
#                 enemy.coord[1] += app.player1.speed 
#             for enemy in app.bulletList:
#                 enemy.coord[1] += app.player1.speed
#             app.p1coord[1] -= app.player1.speed 
#             app.spawn1[1] += app.player1.speed 
#             app.map[1] += app.player1.speed 
#     if event.key == 'S':
#         app.playerImage = app.playerRifleDown
#         app.flashImage = app.flashDown
#         app.direction = 'Down'
#         v = app.player1.speed
#         if map(app,0,v):
#             for enemy in app.enemyList:
#                 enemy.coord[1] -= app.player1.speed
#             for enemy in app.bulletList:
#                 enemy.coord[1] -= app.player1.speed
#             app.spawn1[1] -= app.player1.speed 
#             app.p1coord[1] += app.player1.speed 
#             app.map[1]-= app.player1.speed 
#     if event.key == 'A':
#         app.playerImage = app.playerRifleLeft
#         app.flashImage = app.flashLeft
#         app.direction = 'Left'
#         v = -app.player1.speed
#         if map(app,v,0):
#             for enemy in app.enemyList:
#                 enemy.coord[0] += app.player1.speed
#             for enemy in app.bulletList:
#                 enemy.coord[0] += app.player1.speed
#             app.spawn1[0] += app.player1.speed 
#             app.p1coord[0] -= app.player1.speed 
#             app.map[0] += app.player1.speed   
#     if event.key == 'D':
#         app.playerImage = app.playerRifleRight
#         app.flashImage = app.flashRight
#         app.direction = 'Right'
#         v = app.player1.speed
#         if map(app,v,0):
#             for enemy in app.enemyList:
#                 enemy.coord[0] -= app.player1.speed
#             for enemy in app.bulletList:
#                 enemy.coord[0] -= app.player1.speed
#             app.spawn1[0] -= app.player1.speed 
#             app.p1coord[0] += app.player1.speed 
#             app.map[0]-= app.player1.speed  
#     if event.key == 'E':
#         app.IsFiring = True
#         if app.playerImage == app.playerRifleRight:
#             app.bulletList.append(bullet(app.width/2+70,app.height/2+20,70,0))
#         if app.playerImage == app.playerRifleLeft:
#             app.bulletList.append(bullet(app.width/2-70,app.height/2-20,-70,0))
#         if app.playerImage == app.playerRifleUp:
#             app.bulletList.append(bullet(app.width/2+20,app.height/2-70,0,-70))
#         if app.playerImage == app.playerRifleDown:
#             app.bulletList.append(bullet(app.width/2-20,app.height/2+70,0,70))

#     ###############################


#     # if event.key == 'W' and 'A' :
#     #     app.p1coord[1] -= app.player1.speed 
#     #     app.p1coord[0] -= app.player1.speed 
#     # if event.key == 'W' and 'D':
#     #     app.p1coord[1] -= app.player1.speed
#     #     app.p1coord[0] += app.player1.speed
#     # if event.key == 'S' and 'A' :
#     #     app.p1coord[1] -= app.player1.speed
#     #     app.p1coord[0] -= app.player1.speed  
#     # if event.key == 'S' and 'D':
#     #     app.p1coord[1] -= app.player1.speed
#     #     app.p1coord[0] += app.player1.speed

#     # # the control console of player 2
#     # if event.key == 'Up':
#     #     app.p1coord[0] += app.player1.speed 
#     # if event.key == 'Down':
#     #     app.p1coord[0] -= app.player1.speed
#     # if event.key == 'Left':
#     #     app.p1coord[1] -= app.player1.speed 
#     # if event.key == 'Right':
#     #     app.p1coord[1] += app.player1.speed

# def spawnItem(app):
#     r = random.randint(1,4)
#     parameters = random.randint(1,30)
#     x = random.randint(app.width)
#     y = random.randint(app.height)
#     if r == 1:
#         app.items.append([food(parameters),x,y])
#     elif r == 2:
#         app.items.append([heal,x])

# def play_redrawAll(app,canvas):
#     canvas.create_rectangle(-5000,-5000,5000,5000,fill = 'black')
#     canvas.create_image(app.map[0],app.map[1],image = ImageTk.PhotoImage(app.background3))
#     canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.playerImage))
#     for bullet in app.bulletList:
#         canvas.create_image(bullet.coord[0],bullet.coord[1],image = ImageTk.PhotoImage(app.bulletImage))
#     for enemy in app.enemyList:
#         canvas.create_image(enemy.coord[0],enemy.coord[1],image = ImageTk.PhotoImage(app.enemyImage))
#     if app.IsFiring == True:
#         if app.direction == 'Left':
#             canvas.create_image(app.width/2-70,app.height/2-20,image = ImageTk.PhotoImage(app.flashImage))
#         if app.direction == 'Right':
#             canvas.create_image(app.width/2+70,app.height/2+20,image = ImageTk.PhotoImage(app.flashImage))
#         if app.direction == 'Up':
#             canvas.create_image(app.width/2+20,app.height/2-70,image = ImageTk.PhotoImage(app.flashImage))
#         if app.direction == 'Down':
#             canvas.create_image(app.width/2-20,app.height/2+70,image = ImageTk.PhotoImage(app.flashImage))


# ############################## boss mode ################################

# def boss_timerFired(app):
#     app.IsFiring = False
#     trajBoss(app)
#     bossAI(app)
#     isHHit(app)
#     if app.boss.hp <= 0:
#         app.boss.speed = 0
#         app.message = 'You Won'
#     elif app.player1.hp<= 0:
#         app.message = 'You lost'

# def isHHit(app):
#     for bullet in app.bulletList:
#         if (bullet.coord[0] < app.boss.coord[0]+30 and bullet.coord[0] > app.boss.coord[0]-30
#         and bullet.coord[1] < app.boss.coord[1] +30 and bullet.coord[1] > app.boss.coord[1] -30):
#             app.boss.hp -= app.player1.attack
#     if(app.p1coord[0] < app.boss.coord[0]+10 and app.p1coord[0] > app.boss.coord[0]-10
#         and app.p1coord[1] < app.boss.coord[1] +10 and app.p1coord[1] > app.boss.coord[1] -10):
#             app.player1.hp -= app.boss.attack

# def trajBoss(app):
#     for bullet in app.bulletList:
#         cx,cy = bullet.coord[0],bullet.coord[1]
#         vx, vy= bullet.vector[0],bullet.vector[1]
#         if cx > 1500 or cy > 800:
#             bullet.coord[0],bullet.coord[1] = -500,-500
#             bullet.vector[0],bullet.vector[1] = 0,0
#         else:
#             bullet.coord[0] += bullet.vector[0]
#             bullet.coord[1]+= bullet.vector[1]


# def boss_keyPressed(app,event):
#     # Maybe use pygame to smoothen the control

#     if event.key == 'W' :
#         app.playerImage = app.playerRifleUp
#         app.flashImage = app.flashUp
#         app.direction = 'Up'
#         v = -app.player1.speed
       
#         app.p1coord[1] -= app.player1.speed 

#     if event.key == 'S':
#         app.playerImage = app.playerRifleDown
#         app.flashImage = app.flashDown
#         app.direction = 'Down'
#         v = app.player1.speed
#         app.p1coord[1] += app.player1.speed 
            
#     if event.key == 'A':
#         app.playerImage = app.playerRifleLeft
#         app.flashImage = app.flashLeft
#         app.direction = 'Left'
#         v = -app.player1.speed
#         app.p1coord[0] -= app.player1.speed 
#     if event.key == 'D':
#         app.playerImage = app.playerRifleRight
#         app.flashImage = app.flashRight
#         app.direction = 'Right'
#         v = app.player1.speed
#         app.p1coord[0] += app.player1.speed  
#     if event.key == 'E':
#         app.IsFiring = True
#         if app.playerImage == app.playerRifleRight:
#             app.bulletList.append(bullet(app.p1coord[0]+70,app.p1coord[1]+20,70,0))
#         if app.playerImage == app.playerRifleLeft:
#             app.bulletList.append(bullet(app.p1coord[0]-70,app.p1coord[1]-20,-70,0))
#         if app.playerImage == app.playerRifleUp:
#             app.bulletList.append(bullet(app.p1coord[0]+20,app.p1coord[1]-70,0,-70))
#         if app.playerImage == app.playerRifleDown:
#             app.bulletList.append(bullet(app.p1coord[0]-20,app.p1coord[1]+70,0,70))
        
                
# def boss_redrawAll(app,canvas):
#     canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.bossMap))
#     canvas.create_image(app.p1coord[0],app.p1coord[1],image = ImageTk.PhotoImage(app.playerImage))
#     for bullet in app.bulletList:
#         canvas.create_image(bullet.coord[0],bullet.coord[1],image = ImageTk.PhotoImage(app.bulletImage))
#     canvas.create_image(app.boss.coord[0],app.boss.coord[1],image = ImageTk.PhotoImage(app.bossImage))
#     if app.IsFiring == True:
#         if app.direction == 'Left':
#             canvas.create_image(app.p1coord[0]-70,app.p1coord[1]-20,image = ImageTk.PhotoImage(app.flashImage))
#         if app.direction == 'Right':
#             canvas.create_image(app.p1coord[0]+70,app.p1coord[1]+20,image = ImageTk.PhotoImage(app.flashImage))
#         if app.direction == 'Up':
#             canvas.create_image(app.p1coord[0]+20,app.p1coord[1]-70,image = ImageTk.PhotoImage(app.flashImage))
#         if app.direction == 'Down':
#             canvas.create_image(app.p1coord[0]-20,app.p1coord[1]+70,image = ImageTk.PhotoImage(app.flashImage))
#     canvas.create_text(app.width/2,app.height/2,text = app.message, font = 'impact 100 bold',fill = 'white')


    
# runApp(width = 1280, height =747)

