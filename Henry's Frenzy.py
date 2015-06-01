__author__ = 'BenYang'

from Tkinter import *

class Gameboard:
    def __init__(self,dimenY,dimenX):
        class Struct:pass
        self.data = Struct()
        self.data.obj=[]
        self.data.dimension = [dimenY,dimenX]
        self.data.ct = float(0)
        self.data.root = Tk()
        self.data.root.resizable(0, 0)
        self.data.canvas = Canvas(self.data.root,width=dimenX,height=dimenY,bg='white')
        self.data.canvas.pack()
        self.data.root.bind("<Key>", self.keyPressed)
        self.data.refreshT = 1 #IN ms
        self.data.root.bind("<KeyRelease>", self.keyReleased)

    def keyPressed(self,event):
        if(event.keysym == "Down"):
            self.data.obj[0].velY=5*self.data.obj[0].isSlow
        elif(event.keysym =="Left"):
            self.data.obj[0].velX=-5*self.data.obj[0].isSlow
        elif(event.keysym == "Right"):
            self.data.obj[0].velX=5*self.data.obj[0].isSlow
        elif(event.keysym=="Up"):
            self.data.obj[0].velY=-5*self.data.obj[0].isSlow

    def keyReleased(self,event):
        if(event.keysym == "Down"):
            self.data.obj[0].velY=0
        elif(event.keysym =="Left"):
            self.data.obj[0].velX=0
        elif(event.keysym == "Right"):
            self.data.obj[0].velX=0
        elif(event.keysym=="Up"):
            self.data.obj[0].velY=0

    def startGame(self):
        self.createGame()
        self.refresh()


    def createGame(self):
        self.data.obj.append(Player(500,300,0,0,0,0,5,5,self.data.ct,3,3,10))


    def makeMove(self):
        for obj in self.data.obj:
            obj.makeMove()

    def refresh(self):
        self.data.ct += 1
        self.makeMove()
        #self.changestate
        self.drawCanvas()
        self.data.canvas.after(self.data.refreshT, self.refresh)




    def deleteobj(self):
        i=0
        while(i<len(self.data.obj)):
            if(self.data.obj.isExist()):
                self.data.obj.remove(i)

    def createobj(self):
        pass

    def changeobj(self):
        self.deleteobj()
        self.createobj()

    def drawCanvas(self):
        self.data.canvas.delete(ALL)
        for obj in self.data.obj:
            obj.drawSelf()

#problem here



class Gameobj:
    def __init__(self,posY,posX,velY,velX,accY,accX,height,length,ct):
        self.posY=float(posY)
        self.posX=float(posX)
        self.initT = float(ct)
        self.velY=float(velY)
        self.velX=float(velX)
        self.accY=float(accY)
        self.accX=float(accX)
        self.height=float(height)
        self.length=float(length)


    def drawSelf(self):
        myboard.data.canvas.create_oval((self.posX-self.length/2),(self.posY-self.height/2),(self.posX+self.length/2),(self.posY+self.height/2),fill="white")

    def dacc(self):
        pass

    def dvel(self):
        pass

    def dpos(self):
        self.posX += self.velX
        self.posY += self.velY

    def upState(self):
        pass

    def lu(self):
        return tuple([(self.posX-self.length/2),(self.posY-self.height/2)])

    def rb(self):
        return tuple([(self.posX+self.length/2),(self.posY+self.height/2)])

    def makeMove(self):
        self.dacc()
        self.dvel()
        self.dpos()
        self.upState()

class Player(Gameobj):
    def __init__(self,posY,posX,velY,velX,accY,accX,height,length,ct,life,bomb,hp):
        #delete self if needed
        Gameobj.__init__(self, posY, posX, velY, velX, accY, accX, height, length, ct)
        self.life=life
        self.bomb=bomb
        self.hp=hp
        self.isSlow = 1


    def upState(self):
        pass


    def fire(self):
        pass

class Bullet(Gameobj):
    def __init__(self,posY,posX,velY,velX,accY,accX,height,length,ct,damage):
        Gameobj.__init__(self,posY,posX,velY,velX,accY,accX,height,length,ct)
        self.damage = damage

    def dacc(self):
        pass

    def dvel(self):
        pass

    def dpos(self):
        pass

    def upState(self):
        pass


    def makeMove(self):
        self.dacc()
        self.dvel()
        self.dpos()
        self.upState()

class Boss(Gameobj):
    def __init__(self,posY,posX,velY,velX,accY,accX,height,length,ct,hp):
        #delete self if needed
        Gameobj.__init__(self, posY, posX, velY, velX, accY, accX, height, length, ct)
        self.hp=hp

    def dacc(self):
        pass

    def dvel(self):
        pass

    def dpos(self):
        pass

    def upState(self):
        pass

    def fire(self):
        pass

    def makeMove(self):
        self.dacc()
        self.dvel()
        self.dpos()
        self.upState()
        self.fire()

global myboard
myboard = Gameboard(800,600)
myboard.startGame()
myboard.data.root.mainloop()