# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:27:06 2024

@author: Mrang
"""

import pygame, random, simpleGE

class Car (simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("redCR.png")
        self.setSize(90,50)
        self.position = (300,400)
        self.moveSpeed = 10
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
class pScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100,30)
        
class pTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500,30)
        
class menuM(simpleGE.Scene):
   def __init__(self):
       super().__init__()
       self.menuMUSIC = simpleGE.Sound("pamperS.mp3")
       self.play()
       
        
        
class Gas(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("gasC.png")
        self.setSize(20,20)
        self.reset()
        
        
    def Bounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
        
    def reset(self):
      self.y = 12
      self.x = random.randint(0, self.screenWidth)
      self.dy = random.randint(3, 8)
      
class Stone(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("stoneOB.png")
        self.setSize(20,20)
        self.reset() 

    def Bounds(self):
      if self.bottom > self.screenHeight:
          self.reset()
          
      
    def reset(self):
     self.y = 12
     self.x = random.randint(0, self.screenWidth)
     self.dy = random.randint(3, 8)              
     
class Trash(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("trashOB.png")
        self.setSize(20,20)
        self.reset()
        
    def Bounds(self):
         if self.bottom > self.screenHeight:
            self.reset()
            
        
    def reset(self):
         self.y = 12
         self.x = random.randint(0, self.screenWidth)
         self.dy = random.randint(3, 8)      
    

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("natureRoad.jpg")
        self.sndGas = simpleGE.Sound("pingS.mp3")
        self.sndStone = simpleGE.Sound("stoneS.mp3")
        self.sndTrash = simpleGE.Sound("trashCS.mp3")
        
        self.score = 0
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.pTime = pTime()
        
        self.car = Car(self)
       
        self.pScore = pScore()
        
        self.gases = []
        for i in range(7):
            self.gases.append(Gas(self))
            
        self.stones = []
        for i in range(5):
            self.stones.append(Stone(self))
            
        self.trashs = []
        for i in range(5):
            self.trashs.append(Trash(self))
            
        self.sprites = [self.car,
                        self.trashs,
                        self.stones,
                        self.gases,
                        self.pScore,
                        self.pTime]
        
        
    def process(self):
      
        for gas in self.gases:
            if self.car.collidesWith(gas):
                self.sndGas.play()
                self.score += 1
                self.pScore.text = f"Score: {self.score}"
                gas.reset() 
                
        for stone in self.stones:
            if self.car.collidesWith(stone):
                self.sndStone.play()
                self.score -= 1
                self.pScore.text = f"Score: {self.score}"
                stone.reset()
                
        for trash in self.trashs:
            if self.car.collidesWith(trash):
                self.sndTrash.play()
                self.score -= 2
                self.pScore.text = f"Score: {self.score}"
                trash.reset()

        self.pTime.text =f"Time Left: {self.timer.getTimeLeft():.2}"
        if self.timer.getTimeLeft() <0:
            print(f"Score: {self.score}")
            self.stop()
            
class gameInstr(simpleGE.Scene):
    def __init__(self, preScore):
        super().__init__()
        
        self.preScore = preScore
        
        self.setImage("warningS.jpg")
        self.response ="Quit"
        
        
        self.Instructions = simpleGE.MultiLabel()
        self.Instructions.textLines = [
            "You are low on gas in a country road.",
            "Grab as much gas you can to make it home!",
            "Use the Left and Right arrows to control your car.",
            "MAKE IT HOME"]
        
        self.Instructions.center = (320,240)
        self.Instructions.size = (500,250)
        
        self.bPlay = simpleGE.Button()
        self.bPlay.text = "Play"
        self.bPlay.center = (100,400)
        
        self.bQuit = simpleGE.Button()
        self.bQuit.text = "Quit"
        self.bQuit.center = (540,400)
        
        self.LblScore = simpleGE.Label()
        self.LblScore.text = "Last score: 0"
        self.LblScore.center = (320,400)
        
        self.LblScore.text = f"Last score: {self.preScore}"
        
        self.sprites = [self.Instructions,
                        self.bPlay,
                        self.bQuit,
                        self.LblScore]
          
        
    def process(self):
        if self.bPlay.clicked:
            self.response ="Play"
            self.stop()
            
        if self.bQuit.clicked:
            self.response ="Quit"
            self.stop()
        
def main():
    
    keepGoing = True
    lastScore = 0 
    
    while keepGoing:
        instructions = gameInstr(lastScore)
        instructions.start()
        
        if instructions.response =="Play":
            game = Game()
            game.start()
            lastScore = game.score
            
        else:
            keepGoing = False
            
if __name__ == "__main__":
    main()