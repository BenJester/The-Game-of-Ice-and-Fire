__author__ = 'BenYang'


from Tkinter import *
import random

root = Tk()


"""
Update log

V1.1

Major bugs fixed
Completed instructions
Improved pause shortcut
Changed title

Upcoming

A global clearing ability


"""

class canvasi():

    def test(self):

        pass

    def __init__(self):

        self.counter_press = 0
        self.ebposleft = 175
        self.ebposright = 500 - self.ebposleft
        self.eblen = 500 - 2 * self.ebposleft
        self.energy = 100.0
        self.ebdrawright = self.ebposleft + (self.energy / 100.0) * self.eblen

        self.bombradius = 22.5
        self.bombposx1 = 67.5 - self.bombradius
        self.bombposy1 = 155.5 + self.bombradius
        self.bombposx2 = 67.5 + self.bombradius
        self.bombposy2 = 155.5 - self.bombradius
        self.bombcheck = False
        self.bombcost = 0

        self.energyincrease = 10
        self.immunecost = 200


        self.started = False
        self.startjumping = False
        self.pause = True
        self.dead = False
        self.waited = False
        self.immune = False
        self.afterId = None

        self.energychange()

        self.color = "black"

        self.jumprefresh = 0
        self.posa, self.posb, self.posc, self.posd = 45.0, 175.0, 90.0, 130.0
        self.x1 = 500.0
        self.x2 = 525.0
        self.score = 0
        self.scoretext = StringVar()
        self.pausestr = StringVar()
        self.highscore = 0
        self.highscorestr = StringVar()

        self.pausebutton = Button(textvariable=self.pausestr,command=self.pausegame)
        self.pausebutton.pack(anchor=NE)
        self.pausestr.set("Pause!")

        self.scoreboard = Label(textvariable=self.scoretext)
        self.scoreboard.pack(side=TOP)

        self.highscoredraw = Label(textvariable=self.highscorestr)
        self.highscoredraw.pack(anchor=NW)

        self.instruction = Label(text="Press F to start immuning\nPress E to use bomb\nPress D to pause")
        self.instruction.pack(anchor=CENTER)

        self.drawALL()
        root.bind("<KeyPress>", self.keyPressed)
        root.bind("<KeyRelease>", self.keyReleased)

        self.rects = []

        self.rectspeed = 8.0

        self.update()

        #self.circlepos = (50,155,90,120)

    def keyPressed(self,event):


        if event.keysym == "f":

            self.instruction.destroy()
            self.started = True

            if not self.dead:

                self.pause = False

            elif self.dead and self.waited:

                self.waited = False
                self.respawn()


            if self.afterId != None:

                root.after_cancel(self.afterId)
                self.afterId = None

            else:

                self.immuning()


        if event.keysym == "d":

            self.pausegame()

        if event.keysym == "e" and self.energy >= self.bombcost:
            self.energy -= self.bombcost
            self.bombcheck = True

    def keyReleased(self,event):

        if event.keysym == "f":

            self.afterId = root.after_idle(self.process_release, event)

    def process_release(self, event):

        self.stopimmuning()
        self.afterId = None

    def energybar(self):

        self.ebdrawright = self.ebposleft + (self.energy / 100.0) * self.eblen

        if self.energy < 0:
            self.energy = 0.0
        self.canvasi.create_rectangle(self.ebposleft,80, self.ebposright,85, outline="grey")
        self.canvasi.create_rectangle(self.ebposleft,80, self.ebdrawright,85, outline="grey", fill="grey")

    def energychange(self):

        if self.immune and self.energy > 0:

            self.energy -= (self.immunecost / 100.0)

        elif not self.immune and self.energy < 100.0:

            #self.energy += 0.5 * (self.immunecost / 100.0)
            self.energy += 0.1 + ((100 - self.energy) ** 2) * (self.energyincrease / 10000.0)

    def drawALL(self):

        self.canvasi = Canvas(width=500,height=220)
        self.canvasi.pack()
        self.canvasi.create_line(0,175, 500,175, width=1)
        #self.canvasi.create_line(45,175,95,125,width=1)

        self.canvasi.create_rectangle(self.posa, self.posb, self.posc, self.posd, outline=self.color) #Ball size 45*45

        self.energybar()

        if self.bombcheck:

            self.bomb()


    def destroyALL(self):

        self.canvasi.destroy()

    def speed(self):

        if self.posb < 175 or self.jumprefresh < 5:
            return 5.7 - 0.3 * (self.jumprefresh - 1)
        if int(self.posb) == 175 and self.jumprefresh > 5:
            self.startjumping = False
            self.jumprefresh = 0
            return 0

    def update(self):

        if not self.pause:
            self.destroyALL()
            self.drawALL()
            if self.startjumping:
                self.jumprefresh += 1
                self.posb = self.posb -  self.speed()
                self.posd = self.posd -  self.speed()

            elif not self.startjumping:
                self.posb = 175.0
                self.posd = 130.0

            self.spawnrects()
            self.rectmove()
            self.collision()
            self.energychange()
            self.scoring()
            self.test()

            if self.energy == 0:

                self.stopimmuning()

        root.after(10, self.update)

    def spawnrects(self):

        self.rand = random.randint(1,100)
        if self.rand > 97:
            self.rects.append([500.0, 175.0, 525.0, 150.0, self.rectspeed])

    def rectmove(self):

        for x in range(0, len(self.rects)):


            if self.rects[x][2] <= 0.0:
                self.rects.remove([525 % self.rectspeed - self.rectspeed - 25.0,
                                   175.0,
                                   525 % self.rectspeed - self.rectspeed, 150.0,
                                   self.rectspeed])
                return self.rects
            else:
                self.canvasi.create_rectangle(self.rects[x][0], 175.0, self.rects[x][2], 150.0)
                self.rects[x][0] -= self.rectspeed
                self.rects[x][2] -= self.rectspeed

    def collision(self):

        if not self.immune:

            for x in range(0, len(self.rects)):

                if self.posb > 150.0 and self.rects[x][0] < 90.0 and self.rects[x][2] > 45.0:

                    self.pause = True
                    self.dead = True
                    self.highscroredisplay()
                    self.pausebutton.config(state=DISABLED)

                    root.after(500, self.waiting)

    def respawn(self):

            self.canvasi.destroy()
            self.startjumping = False
            self.pause = False
            self.dead = False
            self.bombcheck = False
            self.bombradius = 22.5
            self.score = 0
            self.energy = 100

            self.jumprefresh = 0
            self.posa, self.posb, self.posc, self.posd = 45.0, 175.0, 90.0, 130.0
            self.x1 = 500.0
            self.x2 = 525.0
            self.pausebutton.config(state=ACTIVE)

            self.drawALL()


            self.rects = []

            self.rectspeed = 8.0

    def waiting(self):

        self.waited = True

    def scoring(self):

        self.score += 1
        self.scoretext.set(str(self.score))

    def highscroredisplay(self):

        if self.score > self.highscore:
            self.highscore = self.score
            self.highscorestr.set(" Highscore: "+str(self.highscore + 1))

    def pausegame(self):

        if not self.pause:

            self.pause = True
            self.pausestr.set("Resume")

        elif self.pause and not self.dead and self.started:

            self.pause = False
            self.pausestr.set("Pause!")

    def immuning(self):

            self.immune = True
            self.color = "grey"

    def stopimmuning(self):

        self.immune = False
        self.color = "black"

    def bomb(self):

        self.score -= 5
        #myrect dimensions: 45.0, 175.0, 90.0, 130.0, center = 67.5, 155.5
        self.bombradius += 10
        self.bombposx1 = 67.5 - self.bombradius
        self.bombposy1 = (self.posb + self.posd) / 2 + self.bombradius
        self.bombposx2 = 67.5 + self.bombradius
        self.bombposy2 = (self.posb + self.posd) / 2 - self.bombradius

        if self.bombposx2 <= 600:
            self.canvasi.create_oval(self.bombposx1,self.bombposy1,self.bombposx2, self.bombposy2)

            for x in range(0,len(self.rects)):

                if self.rects[x][0] <= self.bombposx2:

                    self.rects.pop(x)
                    return self.rects

        else:
            self.bombradius = 22.5
            self.bombcheck = False


game = canvasi()
game2 = canvasi()

root.mainloop()
