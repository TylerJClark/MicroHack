# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 12:09:42 2019

@author: shume
"""
import pygame
import cfg
import time
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
grey = (128,128,128) #Define many colours used throughout rather than needing to use the rgb values
pygame.font.init()
all_fonts = pygame.font.get_fonts()
myfont = pygame.font.SysFont(all_fonts[4], 25)

class button():  #class to quickly make buttons
    def __init__(self,colour, x,y,width,height, text='',active_colour = (0,0,230)):
        self.current_colour = colour
        self.colour = colour #button colour
        self.active_colour = active_colour #colour of the button while the mouse hovers over it.
        self.x = x #x coordinate of top left corner of the button
        self.y = y #y coordinate of top left corner of the button
        self.width = width       #button width
        self.height = height     #button height
        self.text = text         #button text

        #these are the different button options. 
        #these options allow many different buttons to be created from this class
        
    def draw(self,screen,outline=None):  #method to draw the button
        if outline:   #decides if the button has an outline.
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0) #draws the button outline.
            #the outline is a black box which is slighly bigger than the button. This appears as an outline
            
        pygame.draw.rect(screen,self.current_colour, (self.x,self.y,self.width,self.height),0)
        #draws the button
        
        if self.text != "":   #only adds text if there is text to add
            all_fonts = pygame.font.get_fonts()
            font = pygame.font.SysFont(all_fonts[4], 30)
            text = font.render(self.text, 1, (0,0,0))      #renders the text
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))) 
            #puts the text in the center of the button.
            
    def clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False  #A method to check if the mouse is over the button.
                      #This is run when th user presses the mouse button.


    def hover(self): #makes the button change colour when the mouse is hovered over it.
            if self.clicked(pygame.mouse.get_pos()):
                self.current_colour = self.active_colour
            else:
                self.current_colour = self.colour   

    def press(self,event):#checks if the mouse button is pressed.
        if self.clicked(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True 
        return False

class Appliance:
    def __init__(self, name, fuelType, usageRate, imageOn,imageOff,pos,size):
        self.name = name
        self.fuelType = fuelType
        self.usageRate = usageRate
        self.power = False;
        self.totalUsage = 0
        self.hourlyUsage = 0
        self.imageOff = imageOff
        self.imageOn = imageOn
        self.currImage = imageOff
        self.pos = pos
        self.size = size
        self.currImage = pygame.transform.scale(self.currImage, (size, size))
        self.iconSize = 150
        self.iconImage = pygame.transform.scale(self.currImage, (self.iconSize, self.iconSize))
        self.button = button(grey,pos[0],pos[1],size,size,"")
        self.timer = 0
        self.toggleButton = button(red,420,600,130,100,"Turn On")
        self.prevent = 0

    def load(self, saveObject):
        self.power = saveObject[0]
        self.totalUsage = saveObject[1]
        self.usageRate = saveObject[2]


        if self.power:
            self.toggleButton = button(red,420,600,130,100,"Turn Off")
            self.currImage = self.imageOn
            self.iconImage = pygame.transform.scale(self.currImage, (self.iconSize, self.iconSize))
            self.currImage = pygame.transform.scale(self.currImage, (self.size, self.size))
            self.hourlyUsage = self.usageRate
        else:
            self.toggleButton = button((0,130,0),420,600,130,100,"Turn On")
            self.currImage = self.imageOff
            self.iconImage = pygame.transform.scale(self.currImage, (self.iconSize, self.iconSize))
            self.currImage = pygame.transform.scale(self.currImage, (self.size, self.size))
            self.hourlyUsage = 0
    
    def togglePower(self):
        
        self.power = not self.power
        self.toggleImage()

    def toggleImage(self):
        if power:
            self.currImage = self.imageOn
            self.iconImage = pygame.transform.scale(self.currImage, (self.iconSize, self.iconSize))
        else:
            self.currImage = self.imageOff
            self.iconImage = pygame.transform.scale(self.currImage, (self.iconSize, self.iconSize))

    def drawImage(self,screen):
        self.button.draw(screen,(0,0,0))
        screen.blit(self.currImage, self.pos)

    def clickButton(self,event):
        
        if self.button.press(event):
            return True
        return False

    def displayInfo(self,screen,event):
        screen.blit(self.iconImage, (260,565))
        self.toggleButton.hover()
        self.toggleButton.draw(screen,(0,0,0))
        if self.toggleButton.press(event) and self.prevent <= 0:
            self.prevent = 30
            if not self.power:
                self.power = True
                self.toggleButton = button(red,420,600,130,100,"Turn Off")
                self.currImage = self.imageOn
                self.iconImage = pygame.transform.scale(self.currImage, (self.iconSize, self.iconSize))
                self.currImage = pygame.transform.scale(self.currImage, (self.size, self.size))
                self.hourlyUsage = self.usageRate
            else:
                self.power = False
                self.toggleButton = button((0,130,0),420,600,130,100,"Turn On")
                self.currImage = self.imageOff
                self.iconImage = pygame.transform.scale(self.currImage, (self.iconSize, self.iconSize))
                self.currImage = pygame.transform.scale(self.currImage, (self.size, self.size))
                self.hourlyUsage = 0
                
        if self.prevent > 0:
            self.prevent -= 1
        
        textsurface = myfont.render("Name: " + str(self.name), False, (0, 0, 0))
        screen.blit(textsurface,(560,560))

        textsurface = myfont.render("Fuel Type: " + self.fuelType, False, (0, 0, 0))
        screen.blit(textsurface,(560,610))

        textsurface = myfont.render("Usage Rate: " + str('%s' % float('%.4g' % self.usageRate)), False, (0, 0, 0))
        screen.blit(textsurface,(560,660))

        textsurface = myfont.render("Turned on?: " + str(self.power), False, (0, 0, 0))
        screen.blit(textsurface,(890,560))

        textsurface = myfont.render("Total Usage: " + str('%s' % float('%.4g' % self.totalUsage)), False, (0, 0, 0))
        screen.blit(textsurface,(890,610))

        textsurface = myfont.render("Hourly Usage: " + str('%s' % float('%.4g' % self.hourlyUsage)), False, (0, 0, 0))
        screen.blit(textsurface,(890,660))

    def flashing(self,screen):
        self.timer += 1
        if self.timer % 30 < 15:    
            s = pygame.Surface((self.size,self.size))  # the size of your rect
            s.set_alpha(96)                # alpha level
            s.fill((0,0,230))           # this fills the entire surface
            screen.blit(s, (self.pos[0],self.pos[1]))

class Simulation:
    def __init__(self):
        self.timer = 0
        self.floorCost = [0,0,0,0,0]
        self.start = time.time()
       

    
    
