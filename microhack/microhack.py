import pygame
import os
import simulation
import time
import cfg
import pickle
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
grey = (128,128,128) #Define many colours used throughout rather than needing to use the rgb values
start = time.time()
end = 0
floorCost = [0,0,0,0,0]

class saveObject:
    def __init__(self, appliances,floorCosts):
        self.savedFloors = []
        self.floorCosts = floorCosts
        self.fillAllFloorList(appliances)
       
    def fillFloorList(self, floor):
        floorList = []
        for appliance in floor:
            #power, totalUsage, usageRate
            floorList.append([appliance.power, appliance.totalUsage, appliance.usageRate])
        return floorList

    def fillAllFloorList(self, appliances):
        for floor in appliances:
            self.savedFloors.append(self.fillFloorList(floor))

            
def save():
    saveObject1 = saveObject(appliances,floorCost)
    with open('simulation.pickle', 'wb') as handle:
        pickle.dump(saveObject1, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load():
    global appliances
    global floorCost
    with open('simulation.pickle', 'rb') as handle:
        saveObject1 = pickle.load(handle)
    for i, floor in enumerate(appliances):
        for j, appliance in enumerate(floor):
            appliance.load(saveObject1.savedFloors[i][j])

    floorCost = saveObject1.floorCosts
    

def calculateEnergyCost():
    global floorCost
    for index, floor in enumerate(appliances):
        for appliance in floor:
            if (appliance.fuelType == "Electricity"):
                floorCost[index] += appliance.hourlyUsage * cfg.ELECTRICITYCOSTRATE
            elif (appliance.fuelType == "Gas"):
                floorCost[index] += appliance.hourlyUsage * cfg.GASCOSTRATE

def run():
    global end
    global start
    end = time.time()
    if end - start > 5:
        start = time.time()
        hourlyUpdate()
        calculateEnergyCost()

def hourlyUpdate():
    global appliances
    for floor in appliances:
        for appliance in floor:
            if appliance.power:
                appliance.totalUsage += appliance.usageRate

                


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




pygame.init()
pygame.mixer.init() #initialises pygame and sound
pygame.font.init()
all_fonts = pygame.font.get_fonts()
myfont = pygame.font.SysFont(all_fonts[4], 30)


fps = 30 #the game's frames per second

info = pygame.display.Info()
monitorx = 1920
monitory = 1080
dispx, dispy = 1280,720
if dispx > monitorx: # scales screen down if too long
    dispy /= dispx / monitorx
    dispx = monitorx
if dispy > monitory: # scales screen down if too tall
    dispx /= dispy / monitory
    dispy = monitory
    
dispx = int(dispx) # So the resolution does not contain decimals
dispy = int(dispy)

screen = pygame.display.set_mode((dispx,dispy),pygame.FULLSCREEN)

pygame.display.set_caption("Smart Energy")
clock = pygame.time.Clock()



#buttons
quitButton = button(grey,dispx - 160,dispy - 80,160,80,"Quit")
settingsButton = button(grey,dispx - 160,dispy - 160,160,80,"Settings")
#images
folder = os.path.dirname(__file__)
floorFolder = os.path.join(folder,"Floor_Plans")
applianceFolder = os.path.join(folder,"Appliances")

#floors
largeBlanked = pygame.image.load(os.path.join(floorFolder,"large_blanked.jpg")).convert()
largeBlanked = pygame.transform.scale(largeBlanked, (980, 534))

loftBlanked = pygame.image.load(os.path.join(floorFolder,"loft_blanked.jpg")).convert()
loftBlanked = pygame.transform.scale(loftBlanked, (980, 534))

manyRooms = pygame.image.load(os.path.join(floorFolder,"many_rooms_blanked.jpg")).convert()
manyRooms = pygame.transform.scale(manyRooms, (980, 534))

mediumBlanked = pygame.image.load(os.path.join(floorFolder,"medium_blanked.jpg")).convert()
mediumBlanked = pygame.transform.scale(mediumBlanked, (980, 534))

simpleBlanked = pygame.image.load(os.path.join(floorFolder,"simple_blanked.jpg")).convert()
simpleBlanked = pygame.transform.scale(simpleBlanked, (980, 534))


largeBlankedIcon = pygame.image.load(os.path.join(floorFolder,"large_blanked_icon.jpg")).convert()

loftBlankedIcon = pygame.image.load(os.path.join(floorFolder,"loft_blanked_icon.jpg")).convert()

manyRoomsIcon = pygame.image.load(os.path.join(floorFolder,"many_rooms_blanked_icon.jpg")).convert()

mediumBlankedIcon = pygame.image.load(os.path.join(floorFolder,"medium_blanked_icon.jpg")).convert()

simpleBlankedIcon = pygame.image.load(os.path.join(floorFolder,"simple_blanked_icon.jpg")).convert()

#appliances
boilerOff = pygame.image.load(os.path.join(applianceFolder,"Boiler_Off.jpg")).convert()
boilerOn = pygame.image.load(os.path.join(applianceFolder,"Boiler_On.jpg")).convert()

lightOff = pygame.image.load(os.path.join(applianceFolder,"Light_Bulb_Off.png")).convert()
lightOn = pygame.image.load(os.path.join(applianceFolder,"Light_Bulb_On.png")).convert()

ovenOff = pygame.image.load(os.path.join(applianceFolder,"Oven_Off.png")).convert()
ovenOn = pygame.image.load(os.path.join(applianceFolder,"Oven_On.png")).convert()

radOff = pygame.image.load(os.path.join(applianceFolder,"Rad_Off.png")).convert()
radOn = pygame.image.load(os.path.join(applianceFolder,"Rad_On.png")).convert()

showerOff = pygame.image.load(os.path.join(applianceFolder,"Shower_Off2.jpg")).convert()
showerOn = pygame.image.load(os.path.join(applianceFolder,"Shower_On.jfif")).convert()

TVOff = pygame.image.load(os.path.join(applianceFolder,"TV_Image.png")).convert()
TVOn = pygame.image.load(os.path.join(applianceFolder,"TV_Image_On.png")).convert()


saveButton = button(grey,400,50,250,110,"Save")
loadButton = button(grey,700,50,250,110,"Load")

applButton = button(grey,450,250,450,70,"Load")
incrButton = button(grey,920,250,70,70,">")
decrButton = button(grey,360,250,70,70,"<")

##data stuff
currentFloor = 0
currentScroll = 0


floorImages = [largeBlanked,loftBlanked,manyRooms,mediumBlanked,simpleBlanked]
floorIcons = [largeBlankedIcon,loftBlankedIcon,manyRoomsIcon,mediumBlankedIcon,simpleBlankedIcon]
floorButtons = [button(grey,dispx - 160,dispy - 80,160,80,"")]
floorNames = ["Large Blanked","Loft Blanked","Many Rooms","Medium Blanked","Simple Blanked"]
appliances = [[],[],[],[],[]]

maxHeight = 0
for j in range(len(floorIcons)):

    maxHeight += floorIcons[j].get_height() + 70

##room 1
appliances[0].append(simulation.Appliance("Oven", "Gas", 3, ovenOn,ovenOff,(1200,88),40))

appliances[0].append(simulation.Appliance("Kitchen Light", "Electricity", 0.5, lightOn,lightOff,(900,130),40))
appliances[0].append(simulation.Appliance("Living Room Light", "Electricity", .5, lightOn,lightOff,(1000,400),40))
appliances[0].append(simulation.Appliance("Bedroom 1 Light", "Electricity", .5, lightOn,lightOff,(400,130),40))
appliances[0].append(simulation.Appliance("Bedroom 2 Light", "Electricity", .5, lightOn,lightOff,(400,400),40))
appliances[0].append(simulation.Appliance("Bedroom 3 Light", "Electricity", .5, lightOn,lightOff,(670,420),40))
appliances[0].append(simulation.Appliance("Corridor Light", "Electricity", .5, lightOn,lightOff,(700,290),40))
appliances[0].append(simulation.Appliance("Bathroom 1 Light", "Electricity", .5, lightOn,lightOff,(680,60),40))
appliances[0].append(simulation.Appliance("Bathroom 2 Light", "Electricity", .5, lightOn,lightOff,(680,200),40))

appliances[0].append(simulation.Appliance("Boiler", "Gas", 10, boilerOn,boilerOff,(810,400),40))

appliances[0].append(simulation.Appliance("Living Room Radiator", "Gas", 30, radOn,radOff,(1000,492),40))
appliances[0].append(simulation.Appliance("Kitcken Radiator", "Gas", 30, radOn,radOff,(793,150),40))
appliances[0].append(simulation.Appliance("Bedroom 1 Radiator", "Gas", 30, radOn,radOff,(283,170),40))
appliances[0].append(simulation.Appliance("Bedroom 2 Radiator", "Gas", 30, radOn,radOff,(283,450),40))
appliances[0].append(simulation.Appliance("Bedroom 3 Radiator", "Gas", 30, radOn,radOff,(580,400),40))

appliances[0].append(simulation.Appliance("TV", "Electricity", 25, TVOn,TVOff,(870,400),40))

appliances[0].append(simulation.Appliance("Shower", "Gas", 7.5, showerOn,showerOff,(615,175),40))




#room 2

appliances[1].append(simulation.Appliance("Bolier Loft", "Gas", 10, boilerOn,boilerOff,(140 + 250,486),40))
appliances[1].append(simulation.Appliance("Loft Light", "Electricity", .5, lightOn,lightOff,(620 + 250,340),40))
appliances[1].append(simulation.Appliance("Bolier Room Light", "Electricity", .5, lightOn,lightOff,(140 + 250,430),40))
appliances[1].append(simulation.Appliance("TV Room Light", "Electricity", .5, lightOn,lightOff,(140 + 250,120),40))
appliances[1].append(simulation.Appliance("Radiator Loft", "Gas", 30, radOn,radOff,(265 + 250,70),40))
appliances[1].append(simulation.Appliance("TV Loft", "Electricity", 25, TVOn,TVOff,(40 + 250,70),40))

currentAppliance = None



#other things
game = True
sim = simulation.Simulation()
settings = False
timeB = 0
while game:
    clock.tick(fps)
    screen.fill((199,199,199))
    pygame.draw.rect(screen, black, [250, 0, 6, 720], 0)#vertical
    
    pygame.draw.rect(screen, black, [250, dispy - 166, 1280 - 250, 6], 0)#across
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                currentScroll += 35

                if currentScroll > 0:
                    currentScroll = 0
                    
            elif event.button == 5:
                currentScroll -= 35
                if currentScroll < -940:
                    currentScroll = -940
    
    

    if not settings:
        screen.blit(floorImages[currentFloor],(270,10))
        for i in appliances[currentFloor]:
            i.drawImage(screen)
            if i.clickButton(event):
                currentAppliance = i
    else:
        if currentAppliance != None:
            applButton = button(grey,450,250,450,70,currentAppliance.name + ": " + str('%s' % float('%.4g' % currentAppliance.usageRate)) + " kW")

            incrButton.hover()
            decrButton.hover()
            applButton.draw(screen,(0,0,0))
            incrButton.draw(screen,(0,0,0))
            decrButton.draw(screen,(0,0,0))

            if incrButton.press(event):
                currentAppliance.usageRate += .1
                currentAppliance.hourlyUsage += .1
            if decrButton.press(event):
                currentAppliance.usageRate -= .1
                currentAppliance.hourlyUsage += .1
            

            
        saveButton.hover()
        loadButton.hover()
        saveButton.draw(screen,(0,0,0))
        loadButton.draw(screen,(0,0,0))
        if saveButton.press(event):
            save()
        if loadButton.press(event):
            load()
            

    
    if currentAppliance != None:
        currentAppliance.displayInfo(screen,event)
        if not settings:
            currentAppliance.flashing(screen)
        
    quitButton.hover()
    quitButton.draw(screen,(0,0,0))
    if quitButton.press(event):
        game = False #exits the game loop

    settingsButton.hover()
    settingsButton.draw(screen,(0,0,0))
    
    if timeB > 0:
        timeB -= 1
        
    if settingsButton.press(event) and timeB == 0:
        timeB = 15
        if not settings:
            settings = True
            settingsButton = button(grey,dispx - 160,dispy - 160,160,80,"Return")
        else:
            settings = False
            settingsButton = button(grey,dispx - 160,dispy - 160,160,80,"Settings")
    
    currentHeight = 0
    floorButtons = []
    
    for j in range(len(floorIcons)):
        floorButtons.append(button(grey,0,currentScroll + currentHeight + 4,250,floorIcons[j].get_height() + 66,""))
        
        #change button position
        if j == currentFloor:
            pygame.draw.rect(screen, (0,0,230), (0,currentScroll + currentHeight + 4,250,floorIcons[j].get_height() + 166),0)

        pygame.draw.rect(screen, (0,0,0), (0,currentScroll + currentHeight,250,4),0)
            
        textsurface = myfont.render(floorNames[j], False, (0, 0, 0))
        screen.blit(textsurface,(10,currentScroll + 10 + currentHeight))

        textsurface = myfont.render("Total Usage: ", False, (0, 0, 0))
        screen.blit(textsurface,(10,currentScroll + 60 + currentHeight))

        textsurface = myfont.render("£"+str(float('%s' % float('%.4g' % floorCost[j]))), False, (0, 0, 0))
        screen.blit(textsurface,(10,currentScroll + 110 + currentHeight))
        
        
        screen.blit(floorIcons[j],(10,currentScroll + 160 + currentHeight))

        
        currentHeight += floorIcons[j].get_height() + 170

    for i in range(len(floorButtons)):
        if floorButtons[i].press(event):
            currentFloor = i
            currentAppliance = None

    run()     
    
    pygame.display.flip()

pygame.quit()





