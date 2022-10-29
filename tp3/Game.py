from cmu_112_graphics import *
import module_manager
module_manager.review()
from PIL import Image
import random
import time
import pygame

#from TA
pygame.init()

#from https://soundimage.org/fantasywonder/

def play():
    pygame.mixer.music.load("Netherplace_Looping.mp3")
    pygame.mixer.music.play(loops = -1)

play()

scale = 0.75
 
width = int(1416*scale)
height = int(918*scale)    
class Plate():
    def __init__(self, cx, cy):
        scale = 1/5
        self.image = Image.open('plate.png')
        self.image = self.image.resize((int(self.image.width*scale), int(self.image.height*scale)), Image.ANTIALIAS)
        self.cx = cx
        self.cy = cy
        self.cached_image = None
    def drawImage(self, canvas):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

        if self.cached_image is None:
            self.cached_image = ImageTk.PhotoImage(self.image)
        canvas.create_image(self.cx, self.cy, image = self.cached_image)
 
class TrashCan:
 
    def __init__(self, cx, cy):
        scale = 1/3
        
        self.image = Image.open('trashcan.png')
        self.image = self.image.resize((int(self.image.width*scale), int(self.image.height*scale)), Image.ANTIALIAS)
        self.width, self.height = self.image.size
        self.cx = cx
        self.cy = cy
        self.cached_image = None
    def drawImage(self, canvas):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

        if self.cached_image is None:
            self.cached_image = ImageTk.PhotoImage(self.image)
        canvas.create_image(self.cx, self.cy, image = self.cached_image)
 
 
    def getBounds(self, x, y):
        halfWidth = self.width//2
        halfHeight = self.height//2
 
        if (x > self.cx-halfWidth and x < self.cx + halfWidth) and (y > self.cy - halfHeight and y < self.cy + halfHeight):
            return True
 
    def getPoints(self):
 
        halfWidth = self.width//2 
        halfHeight = self.height//2
        
        topleftx = self.cx - halfWidth
        toplefty = self.cy - halfHeight
        
        return (topleftx, toplefty, self.width, self.height)
 
class Ingredient():
    def __init__(self, name, url, cx, cy):
        scale = 1/5
        self.name = name
        self.url = url
        self.image = Image.open(url)
        self.image = self.image.resize((int(self.image.width*scale), int(self.image.height*scale)), Image.ANTIALIAS)
        self.width, self.height = self.image.size
        self.isBurger= False
        self.cx = cx
        self.cy = cy
        self.cached_image = None
 
    def drawImage(self, canvas):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

        if self.cached_image is None:
            self.cached_image = ImageTk.PhotoImage(self.image)
        canvas.create_image(self.cx, self.cy, image = self.cached_image)
    

    def changeImage(self, new):

        self.image = Image.open(new)
        self.image = self.image.resize((int(self.image.width*(1/5)), int(self.image.height*(1/5))), Image.ANTIALIAS)
        self.cached_image = ImageTk.PhotoImage(self.image)

    def move(self, x, y):
        self.cx = x
        self.cy = y
    
    def getBounds(self, x, y):
        halfWidth = self.width//2
        halfHeight = self.height//2
 
        if (x > self.cx-halfWidth and x < self.cx + halfWidth) and (y > self.cy - halfHeight and y < self.cy + halfHeight):
            return True

    def getPoints(self):
 
        halfWidth = self.width//2
        halfHeight = self.height//2
        
        topleftx = self.cx - halfWidth
        toplefty = self.cy - halfHeight
        
        return (topleftx, toplefty, self.width, self.height)
 
    def duplicate(self):
        return Ingredient(self.name, self.url, self.cx, self.cy)
 
class MainPlate():
    
    def __init__(self, cx, cy, ingredients):
        scale = 1/5
        #from https://www.target.com/p/glass-dinner-plate-10-7-white-made-by-design-153/-/A-53312329

        self.image = Image.open('roundtable.png')
        #from https://www.epicurious.com/recipes/food/views/the-ultimate-hamburger-232191

        self.image2 = Image.open('hamburgerr.png')
        
        self.image = self.image.resize((int(self.image.width*scale), int(self.image.height*scale)), Image.ANTIALIAS)
        self.image2 = Image.open('hamburgerr.png')

        self.width, self.height = self.image.size
        self.cx = cx
        self.cy = cy
        self.ingredients = ingredients
        self.cached_image = None
        self.cached_image2= None

    def add(self, x):
        self.ingredients.append(x)

    def move(self, x, y):
        self.cx = x
        self.cy = y
    def drawImage(self, canvas):
                
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

        if self.cached_image is None:
            self.cached_image = ImageTk.PhotoImage(self.image)
        canvas.create_image(self.cx, self.cy, image = self.cached_image)
        
        if(len(self.ingredients) == 6):
            if self.cached_image2 is None:
                self.cached_image2 = ImageTk.PhotoImage(self.image2)

            canvas.create_image(self.cx, self.cy, image = self.cached_image2)
        else:
            for i in range(len(self.ingredients)):
                self.ingredients[i].move(self.cx, self.cy - 10*i)
                self.ingredients[i].drawImage(canvas)
    
    def getPoints(self):

        halfWidth = self.width//2
        halfHeight = self.height//2
        
        topleftx = self.cx - halfWidth
        toplefty = self.cy - halfHeight
        
        return (topleftx, toplefty, self.width, self.height)

class Pot():
    
    def __init__(self, cx, cy):
 
        scale = 1/5
        #from https://madeincookware.com/products/blue-carbon-steel-frying-pan

        self.image = Image.open('potr.png')
        self.image = self.image.resize((int(self.image.width*scale), int(self.image.height*scale)), Image.ANTIALIAS)
        self.width, self.height = self.image.size
        self.cx = cx
        self.cy = cy
        self.hasBurger = False
        self.cached_image = None
        self.spritestrip = Image.open('boiling.png') 
        self.sprite = 0
        self.sprites = []
        self.spriteCounter = 0
        self.cooked = False
        self.burnt = False

        self.hamburgTime = 0
        self.clock = 0
        #############################
        
        self.time = 0

        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

        for i in range(5):
            self.sprite = self.spritestrip.crop((62*i, 0, 60+60*i, 135))
            self.sprites.append(ImageTk.PhotoImage(self.sprite))


    def timerFired(self):
        
  
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
                
        self.clock += 1
        '''while(self.hasBurger):
            if(self.clock%10== 1):

                self.hamburgTime+=1'''

        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)


    def getPoints(self):
 
        halfWidth = self.width//2
        halfHeight = self.height//2
        
        topleftx = self.cx - halfWidth
        toplefty = self.cy - halfHeight
        
        return (topleftx, toplefty, self.width, self.height)
 
    
    def drawImage(self, canvas):
        
        self.sprite = self.sprites[self.spriteCounter]
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

        if self.cached_image is None:
            self.cached_image = ImageTk.PhotoImage(self.image)
        canvas.create_image(self.cx, self.cy, image = self.cached_image)

        if(self.hasBurger):
            canvas.create_image(self.cx, self.cy-40, image=self.sprite)

class Customer():
 
    def __init__(self, x, y):
        #from https://www.spriters-resource.com/pc_computer/cherrytreehighcomedyclub/sheet/51852/
        #from https://www.spriters-resource.com/pc_computer/cherrytreehighcomedyclub/sheet/51863/

        customeroptions = [('boyleft.png', 'boyright.png'), ('girlleft.png', 'girlright.png'), ('kimonoleft.png', 'kimonoright.png'), ('menleft.png', 'menright.png')]
        
        number = random.randint(0, 3)
        self.seat = False
        self.url = customeroptions[number]
        self.name = random.randint(0, 1000)
        spritestrip = Image.open(self.url[0]) 
         
        self.sprite = 0
        self.sprites = []
        self.spriteCounter = 0
        self.x = x
        self.y = y
        
        self.target = [x, y]
        self.b = None
        self.h = None
        self.preferredDish()
        self.preferredBurger()
        self.isTwo = False
        allDuration = [10, 15, 10]
        self.duration =  allDuration[random.randint(0,2)]

        self.startTime = time.time()
        self.endTime = self.startTime + self.duration
        
        self.angry = False
        self.superangry = False
        self.angryTime = self.startTime + self.duration/2
        self.superAngryTime = self.startTime + self.duration*3/4
        self.currentTime = 0
        #after i seat customer, self.currentTime = 0, startTime and endTime
        
        #self.doors = [(231, 255), (260, 572), (855, 538)]
        
        self.isMovingOut = False
        self.isSeated = False
        #self.seat = None
        self.clock = 0
        self.generatesSprites(spritestrip)
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        #from https://www.nicepng.com/ourpic/u2q8e6a9e6y3r5q8_dialog-box-circle-ring-outline/

        self.dialog_box = ImageTk.PhotoImage(Image.open('dialogue box.png'))
        #from https://tvtropes.org/pmwiki/pmwiki.php/Main/CrossPoppingVeins

        self.angrypic = ImageTk.PhotoImage(Image.open('angry.png'))
    
    
    def generatesSprites(self, spritestrip):

        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

        for i in range(7):
            self.sprite = spritestrip.crop((51.5*i, 0, 51+51*i, 87))
            self.sprites.append(ImageTk.PhotoImage(self.sprite))

    def move(self, x, y):

        self.target[0] = x
        self.target[1] = y


    def isMovedOut(self):

        if(self.x == self.target[0] and self.y == self.target[1] and self.isMovingOut):
            return True
        else: return False

    def timerFired(self):

        self.clock += 1
       
        if time.time()> self.superAngryTime:
            self.superangry = True
        if time.time() > self.angryTime:
            self.angry = True

        if (self.x > self.target[0] + 10):
            self.x -= 10

        elif(self.x < self.target[0] - 10):
            spritestrip = Image.open(self.url[1]) 
            self.generatesSprites(spritestrip)
            self.x += 10

        else:
            self.x = self.target[0]

        if(self.y > self.target[1]+10): 
            self.y -=10
        elif(self.y < self.target[1]-10): 
            self.y += 10
        else:
            self.y = self.target[1]
    
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)

 
    def drawImage(self, canvas):
        self.sprite = self.sprites[self.spriteCounter]
        canvas.create_image(self.x, self.y, image=self.sprite)
        canvas.create_image(self.x+40, self.y-50, image=self.dialog_box)
 
       
        if(self.isTwo):

            self.h.move(self.x + 20, self.y -70)
            self.h.drawImage(canvas)

        else: 
            self.b.move(self.x+20, self.y-70)
            self.b.drawImage(canvas)
            
        if(self.angry):
            canvas.create_image(self.x+15, self.y-30, image = self.angrypic)
    

    def preferredDish(self):
        self.h = Dish(0,0)
        #from https://twitter.com/bigbowlbeef
        #from https://www.alamy.com/asian-noodle-soup-ramen-with-shrimp-vegetables-and-egg-in-black-bowl-on-gray-concrete-background-flat-lay-top-view-mockup-overhead-healthy-food-image333806059.html

        rice = [Ingredient("Rice", 'rice.png', self.x, self.y), None]
        #from https://www.alamy.com/asian-noodle-soup-ramen-with-shrimp-vegetables-and-egg-in-black-bowl-on-gray-concrete-background-flat-lay-top-view-mockup-overhead-healthy-food-image333806059.html
        ramen = [Ingredient("Ramen", 'ramen.png', self.x, self.y), None, None]
        #from https://livejapan.com/en/article-a0000370/
        sushi = [Ingredient("Sushi", 'sushi.png', self.x, self.y), None, None]
        #from https://www.alamy.com/stock-photo/baozi.html
        baozi = [Ingredient("Baozi", 'baozi.png', self.x, self.y), None, None]
        #from https://www.spriters-resource.com/ds_dsi/cookingmama/sheet/27621/

        cake = [Ingredient("Cake", 'cake.png', self.x, self.y), None, None]
       
        number = random.randint(0,1)
        rice = rice[number]
        snumber = random.randint(0, 2)
        ramen = ramen[snumber]
        snumber = random.randint(0, 2)
        sushi = sushi[snumber]
        number = random.randint(0, 2)
        baozi = baozi[number]
        number = random.randint(0, 2)
        cake = cake[number]
        
        if(rice):
            self.h.add(rice)
            
        if (ramen):
            self.h.add(ramen)
        if(sushi):
            self.h.add(sushi)
        if(baozi):
            self.h.add(baozi)
        if(cake):
            self.h.add(cake)
        
    def preferredBurger(self):
        
        self.b = Burger(0, 0)
        #from https://clip.cookdiary.net/lettuce-clipart/lettuce-clipart-kangkong

        lettuce = [Ingredient("Lettuce", 'lettucer.png', self.x,self.y), None]
        #from https://physicsworld.com/a/reality-check/

        tomato = [Ingredient("Tomato", 'tomato.png', self.x, self.y), None]
        #from http://www.eatfunfoods.com/Products-Pre-Cooked_Hamburger_Beef_Patty_1_4_lb_10_lb_case.html
        patty = [Ingredient("Patty", 'patty.png', self.x, self.y), None]
        #from https://www.humphreysfarm.com/productcart/pc/viewPrd.asp?idproduct=11593

        cheese = [Ingredient("Cheese",'cheese slicer.png', self.x, self.y), None]
        

        number = random.randint(0, 1)


        #tripod and everything else
        lettuce = lettuce[number]

        number = random.randint(0, 1)

        tomato = tomato[number]      

        number = random.randint(0, 1)

        patty = patty[number] 

        number = random.randint(0, 1)

        cheese = cheese[number]


      
        if (lettuce):
            self.b.add(lettuce)

        if(tomato):
            self.b.add(tomato)
        if(patty):
            self.b.add(patty)
        if(cheese):
            self.b.add(cheese)
 

class Dish():
    
    def __init__(self, cx, cy):
        self.ingredients = []
        self.cx = cx
        self.cy = cy
        #self.ingredients.append(Ingredient("Rice", 'rice.png', 100000, 10000))

    def getIngredientsList(self):
        return self.ingredients
 
    def len(self):
        return len(self.ingredients)

    def add(self, x):
        self.insert(len(self.ingredients), x)

    
    def insert(self, index, elem):
        self.ingredients.insert(index, elem)

    def move(self, x, y):
        self.cx = x
        self.cy = y
    
    def drawImage(self, canvas):
 
        for i in range(0, len(self.ingredients)):
            self.ingredients[i].move(self.cx, self.cy - 22*i)
            self.ingredients[i].drawImage(canvas)

 
class Burger():
 
    def __init__(self, cx, cy):
        self.ingredients = []
        self.cx = cx
        self.cy = cy


        self.ingredients.append(Ingredient("Bun", 'bunr.png', 100000, 100000))
        self.ingredients.append(Ingredient("Bun", 'bunr.png', 100000, 100000))

    def getIngredientsList(self):
        return self.ingredients
 
    def len(self):
        return len(self.ingredients)

    def add(self, x):
        self.insert(len(self.ingredients) - 1, x)
    
    def insert(self, index, elem):
        self.ingredients.insert(index, elem)

    def move(self, x, y):
        self.cx = x
        self.cy = y
    
    def drawImage(self, canvas):
 
        for i in range(1, len(self.ingredients)-1):
            self.ingredients[i].move(self.cx, self.cy - 10*i)
            self.ingredients[i].drawImage(canvas)

#from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

class SplashScreenMode(Mode):
    def appStarted(mode):
        mode.background = Image.open('sushihamburger.png').resize((width, height), Image.ANTIALIAS)#mode.loadImage('largekitchen.png')
        mode.background = ImageTk.PhotoImage(mode.background)
   
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text = 'This demos a ModalApp!', font = font)
        canvas.create_image(mode.width/2, mode.height/2, image = mode.background)

    def mousePressed(mode, event):
     
        if(event.x > 283 and event.x < 800 and event.y > 342 and event.y < 550):
            mode.app.setActiveMode(mode.app.setUpMode)
        
        elif(event.x > 283 and event.x < 800 and event.y > 576 and event.y < 681):
            mode.app.setActiveMode(mode.app.instructionsMode)

class InstructionsMode(Mode):

    def appStarted(mode):
        mode.background = Image.open('instructions.png').resize((width, height), Image.ANTIALIAS)#mode.loadImage('largekitchen.png')
        mode.background = ImageTk.PhotoImage(mode.background)

    def redrawAll(mode, canvas):
        
        canvas.create_image(mode.width/2, mode.height/2, image = mode.background)

    def keyPressed(mode, event):
        
        if(event.key == 'b'):
            mode.app.setActiveMode(mode.app.splashScreenMode)

class Picture():
    def __init__(self, url, x, y):
        self.x = x
        self.y = y
        self.url = url
        self.image = Image.open(self.url)#.resize((width, height), Image.ANTIALIAS)
        self.image = self.image.resize((int(self.image.width*scale), int(self.image.height*scale)), Image.ANTIALIAS)
        self.width, self.height = self.image.size
       
        self.cached_image = None        

        self.halfwidth = self.width//2
        self.halfheight = self.height//2

        self.x1 = self.x - self.halfwidth
        self.y1 = self.y - self.halfheight
        self.x2 = self.width
        self.y2 = self.height
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.url == other.url

    def redrawAll(self, canvas):
        #canvas.create_image(self.x, self.y, image = self.image)
        
        if self.cached_image is None:
            self.cached_image = ImageTk.PhotoImage(self.image)
        
        canvas.create_image(self.x, self.y, image = self.cached_image)

class SetUpMode(Mode): 

    #from homework #1
    def rectanglesOverlap(mode, x1, y1, w1, h1, x2, y2, w2, h2):
        
        if(x1 < x2 and x1 + w1 > x2) and (y1 < y2 and y1+ h1> y2):
            return True
        elif(x1 < x2 and x1 + w1 > x2) and (y2 < y1 and y2 + h2 > y1):
            return True
        elif(x2< x1 and x2 + w2 > x1) and(y2 < y1 and y2 + h2 > y1):
            return True
        elif(x2 < x1 and x2 + w2 > x1) and (y1 < y2 and y1+ h1> y2):
            return True
        else:return False

    def randomGenerate(mode):
    
        number = random.randint(0, len(mode.tables)-1)
        mode.table = mode.tables[number]
        mode.objects.append(mode.table)


        while(len(mode.couches) > 0):
            thirdnumber = random.randint(0, len(mode.couches)-1)
            mode.couch = mode.couches[thirdnumber]
            if(not mode.rectanglesOverlap(mode.couch.x1, mode.couch.y1, mode.couch.x2, mode.couch.y2, mode.table.x1, mode.table.y1, mode.table.x2, mode.table.y2)):
                mode.objects.append(mode.couch)
                break
            else: 

                mode.couches.remove(mode.couch)
        if(len(mode.couches) ==0):
            mode.original = True
        
        if (mode.original):
            mode.trashcanx = 500
            mode.trashcany = 180
            mode.table.x
            mode.table.y
            mode.mainplatex = 584
            mode.mainplatey = 223
            mode.lettucex = 574
            mode.lettucey = 108
            mode.tomatox = 631
            mode.tomatoy = 142
            mode.pattyx = 530
            mode.pattyy =240
            mode.cheesex =430
            mode.cheesey =247
            mode.bunx = 474
            mode.buny = 270
            
            mode.plate1x = 424
            mode.plate1y = 258
            mode.plate2x = 474
            mode.plate2y = 286
            mode.plate3x = 530
            mode.plate3y = 258
            mode.plate4x = 574
            mode.plate4y = 123
            mode.plate5x = 634
            mode.plate5y = 150

        elif(mode.table.url == 'kitchentable.png'):
            mode.trashcanx = mode.table.x + 60
            mode.trashcany = mode.table.y - 130
            
            mode.mainplatex = mode.table.x + 65
            mode.mainplatey = mode.table.y -45
            
            mode.pattyx = mode.table.x + 34
            mode.pattyy =mode.table.y -10
            mode.cheesex =mode.table.x -66
            mode.cheesey =mode.table.y -19
            mode.bunx = mode.table.x -17
            mode.buny = mode.table.y 
            
            mode.plate1x = mode.table.x-72
            mode.plate1y = mode.table.y -3
            mode.plate2x = mode.table.x -22
            mode.plate2y = mode.table.y + 25
            mode.plate3x = mode.table.x + 34
            mode.plate3y = mode.table.y -3

        elif(mode.table.url == 'kitchentableL.png'):
            
            mode.trashcanx = mode.table.x + 60
            mode.trashcany = mode.table.y - 100
            
            mode.mainplatex = mode.table.x - 65
            mode.mainplatey = mode.table.y -60
            
            mode.pattyx = mode.table.x + 80
            mode.pattyy =mode.table.y -10
            mode.cheesex =mode.table.x -35
            mode.cheesey =mode.table.y -19
            mode.bunx = mode.table.x 
            mode.buny = mode.table.y 
            
            mode.plate1x = mode.table.x- 44
            mode.plate1y = mode.table.y -3
            mode.plate2x = mode.table.x + 15
            mode.plate2y = mode.table.y + 25
            mode.plate3x = mode.table.x + 66
            mode.plate3y = mode.table.y -3

        
        secondnumber = random.randint(0, 4)
        mode.secondtable = mode.secondtables[secondnumber]  
        mode.objects.append(mode.secondtable)

        if(mode.secondtable.url == 'cabinetright.png'):
            mode.plate4x = mode.secondtable.x -20
            mode.plate4y = mode.secondtable.y -7
            mode.plate5x = mode.secondtable.x + 17
            mode.plate5y = mode.secondtable.y + 20
            mode.lettucex = mode.secondtable.x -20 
            mode.lettucey = mode.secondtable.y -15
            mode.tomatox = mode.secondtable.x + 15
            mode.tomatoy = mode.secondtable.y + 13
        
        elif(mode.secondtable.url =='cabinetleft.png'):
            mode.plate4x = mode.secondtable.x -60
            mode.plate4y = mode.secondtable.y + 30
            mode.plate5x = mode.secondtable.x + 36
            mode.plate5y = mode.secondtable.y 
            mode.lettucex = mode.secondtable.x - 60
            mode.lettucey = mode.secondtable.y + 20
            mode.tomatox = mode.secondtable.x + 36
            mode.tomatoy = mode.secondtable.y -5
                
    
        while(len(mode.fridges) > 0):
            woahnumber = random.randint(0,4)
            mode.fridge = mode.fridges[random.randint(0, len(mode.fridges)-1)]        
            if(not mode.rectanglesOverlap(mode.secondtable.x1, mode.secondtable.y1, mode.secondtable.x2, mode.secondtable.y2, mode.fridge.x1, mode.fridge.y1, mode.fridge.x2, mode.fridge.y2)):
                mode.objects.append(mode.fridge)
                break
            else: 
                mode.fridges.remove(mode.fridge)

        if(len(mode.fridges) ==0):
            mode.original = True

        if(mode.fridge.url == 'fridgeright.png'):
            mode.potx = mode.fridge.x + 40
            mode.poty = mode.fridge.y + 15

        elif(mode.fridge.url == 'fridgeleft.png'):

            mode.potx = mode.fridge.x - 40
            mode.poty = mode.fridge.y + 15
        fifthnumber = random.randint(0, len(mode.leftdoors)-1)
        sixthnumber = random.randint(0, len(mode.downdoors)-1)
        seventhnumber = random.randint(0, len(mode.opendoors)-1)
        
        mode.leftdoor = mode.leftdoors[fifthnumber]
        mode.downdoor = mode.downdoors[sixthnumber]
        mode.opendoor = mode.opendoors[seventhnumber]

        while(len(mode.rightdoors) > 0):
            fourthnumber = random.randint(0, 3)
            mode.rightdoor = mode.rightdoors[random.randint(0, len(mode.rightdoors)-1)] 
            if(not mode.rectanglesOverlap(mode.rightdoor.x1, mode.rightdoor.y1, mode.rightdoor.x2, mode.rightdoor.y2, mode.fridge.x1, mode.fridge.y1, mode.fridge.x2, mode.fridge.y2)
                and (not mode.rightdoor.x1, mode.rightdoor.y1, mode.rightdoor.x2, mode.rightdoor.y2, mode.secondtable.x1, mode.secondtable.y1, mode.secondtable.x2, mode.secondtable.y2)):
                mode.objects.append(mode.rightdoor)
                mode.doorss.append(mode.rightdoor)
                break
            else: 
                mode.rightdoors.remove(mode.rightdoor)
        while(len(mode.leftdoors) > 0):
            fifth = random.randint(0, 3)
            mode.leftdoor = mode.leftdoors[random.randint(0, len(mode.leftdoors)-1)]
            if(not mode.rectanglesOverlap(mode.leftdoor.x1, mode.leftdoor.y1, mode.leftdoor.x2, mode.leftdoor.y2, mode.fridge.x1, mode.fridge.y1, mode.fridge.x2, mode.fridge.y2)
                and (not mode.leftdoor.x1, mode.leftdoor.y1, mode.leftdoor.x2, mode.leftdoor.y2, mode.secondtable.x1, mode.secondtable.y1, mode.secondtable.x2, mode.secondtable.y2)
                and (not mode.leftdoor.x1, mode.leftdoor.y1, mode.leftdoor.x2, mode.leftdoor.y2, mode.rightdoor.x1, mode.rightdoor.y1, mode.rightdoor.x2, mode.rightdoor.y2)):
                mode.objects.append(mode.leftdoor)
                mode.doorss.append(mode.leftdoor)
                break
            else: 
                mode.leftdoors.remove(mode.leftdoor)

        mode.doorss.append(mode.downdoor)
        mode.objects.append(mode.downdoor)

        mode.doorss.append(mode.opendoor)
        mode.objects.append(mode.opendoor)
        
        mode.doors = mode.doorss[1:]        

        mode.startingx = mode.doorss[0].x
        mode.startingy = mode.doorss[0].y

    
    def appStarted(mode):
        
        mode.initrestart()
        
    def initrestart(mode):

        mode.kitchenbackground = Image.open('kitchenbackground.png').resize((width, height), Image.ANTIALIAS)#mode.loadImage('largekitchen.png')
        
        mode.kitchenbackground = ImageTk.PhotoImage(mode.kitchenbackground)
        
        mode.seatCoords = []
        mode.seatTaken = []
        mode.length = 1
    
        mode.objects = []
        mode.doorss = []
        mode.original = False
        
        #used one image and paint.net to crop 
        #https://webkinznewz.ganzworld.com/announcements/fred-rover%E2%80%99s-kitchen-makeover/

        mode.tables = [Picture('kitchentable.png', 496, 256), Picture('kitchentableL.png', 496, 256), Picture('kitchentable.png', 225, 370), Picture('kitchentableL.png', 225, 370), Picture('kitchentable.png', 726, 400), Picture('kitchentableL.png', 726, 400),Picture('kitchentable.png', 480, 444), Picture('kitchentableL.png', 480, 444)] 
        mode.secondtables = [Picture('cabinetright.png', 620, 130), Picture('cabinetright.png', 620, 132), Picture('cabinetleft.png', 419, 110), Picture('cabinetleft.png', 229, 208),Picture('cabinetleft.png', 229, 208)]
        mode.leftdoors = [Picture('doorleft.png', 394, 117), Picture('doorleft.png',118, 260), Picture('doorleft.png', 469, 90)]
        mode.rightdoors = [Picture('doorright.png', 783, 181), Picture('doorright.png', 938, 254)]
        mode.downdoors = [Picture('doordown.png', 140, 415), Picture('doordown.png', 296, 498), Picture('doordown.png', 426, 558) ]
        mode.opendoors = [Picture('dooropen.png', 675, 534), Picture('dooropen.png', 829, 458), Picture('dooropen.png', 586, 581)]
        
        mode.couches = [Picture('couch.png', 496, 256), Picture('othercouch.png', 496, 256), Picture('couch.png', 726, 400), Picture('othercouch.png', 726, 400),Picture('couch.png', 812, 366), Picture('othercouch.png', 812, 366), Picture('couch.png', 225, 370)]
        
        mode.fridges = [Picture('fridgeright.png', 626, 116), Picture('fridgeright.png', 690, 132), Picture('fridgeleft.png', 419, 110), Picture('fridgeleft.png', 229, 208), Picture('fridgeleft.png', 229, 208)]
        
        mode.randomGenerate()
        mode.ok = False
        
        mode.background = Image.open('newback.png').resize((width, height), Image.ANTIALIAS)#mode.loadImage('largekitchen.png')
        mode.background = ImageTk.PhotoImage(mode.background)

     
        mode.ok = True
        

    def keyPressed(mode, event):

        if(event.key == 's'):
            mode.app.setActiveMode(mode.app.gameMode)
            mode.ok = False

        elif(event.key == 'b'):
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def mousePressed(mode, event):

        newPosition = (event.x, event.y)
        mode.seatCoords.append(newPosition)
        mode.seatTaken.append(False)
        mode.length += 1
         
    def redrawAll(mode, canvas):
 
        canvas.create_image(mode.width/2, mode.height/2, image = mode.background)
        
        if(mode.original == True):
            canvas.create_image(mode.width/2, mode.height/2, image = mode.kitchenbackground)
        
        else:
            for i in range(len(mode.objects)):
                mode.objects[i].redrawAll(canvas)
    
        if(mode.ok):
            font = 'Arial 22 bold'
            canvas.create_text(mode.width/2, 150, text = 'Click multiple spots on the screen', font = font, fill = 'red')
            canvas.create_text(mode.width/2, 170, text = 'where you want customers to show up', font = font, fill = 'red')
            canvas.create_text(mode.width/2, 190, text= 'Then press s to start the game', font = font, fill = 'pink')

class GameMode(Mode):
    
    def modeActivated(mode): 
        mode.initHamburg()
        mode.time = 0
    def initHamburg(mode):

        mode.timerDelay = 20

        mode.levelTwo = False
        mode.gameOver = False
        mode.mainplatex = mode.app.setUpMode.mainplatex
        mode.mainplatey = mode.app.setUpMode.mainplatey
        mode.circleplate = MainPlate(mode.mainplatex, mode.mainplatey, [])
        mode.isMovingOut = False 
        mode.startingx = mode.app.setUpMode.startingx
        mode.startingy = mode.app.setUpMode.startingy
        mode.score = 0
        mode.isHandingOut = False
        mode.people = []
        
        for i in range(mode.app.setUpMode.length):         

            mode.people.append(Customer(mode.startingx, mode.startingy))
        
     
        mode.seatCoords = mode.app.setUpMode.seatCoords
        mode.seatTaken = mode.app.setUpMode.seatTaken 
        
        mode.lastSeatTime = 0

        mode.clock = 0
        mode.time = 0
        mode.peopleWhoLeft = 0
        mode.background = Image.open('newback.png').resize((width, height), Image.ANTIALIAS)#mode.loadImage('largekitchen.png')
        
        mode.sprites = {}
        for dir in ["Left", "Right", "Up", "Down"]:
            if(dir == 'Down'):
                mode.url = 'walkfront.bmp'
            elif(dir == 'Up'):
                mode.url = 'walkback.bmp'
            elif(dir == 'Right'):
                mode.url = 'walkright.bmp'
            elif(dir == 'Left'):
                mode.url = 'walkleft.bmp'
            spritestrip = mode.loadImage(mode.url)
            mode.sprites[dir] = []
            for i in range(7):
                sprite = spritestrip.crop((51.5*i, 0, 51+51*i, 87))
                mode.sprites[dir].append(ImageTk.PhotoImage(sprite))
 
        mode.spriteCounter = 0
        mode.trashcan = TrashCan(mode.app.setUpMode.trashcanx, mode.app.setUpMode.trashcany)

        mode.x = 307
        mode.y = 313
        mode.direction = 'Down'
        
        #from https://clip.cookdiary.net/lettuce-clipart/lettuce-clipart-kangkong

        lettuce = Ingredient("Lettuce", 'lettucer.png',100000,10000)
        lettuce2 = lettuce.duplicate()
        lettuce2.move(mode.app.setUpMode.lettucex, mode.app.setUpMode.lettucey)
        
        #from https://physicsworld.com/a/reality-check/

        tomato = Ingredient("Tomato", 'tomato.png', 100000, 100000)
        tomato2 = tomato.duplicate()
        tomato2.move(mode.app.setUpMode.tomatox, mode.app.setUpMode.tomatoy)
        
        #from http://www.eatfunfoods.com/Products-Pre-Cooked_Hamburger_Beef_Patty_1_4_lb_10_lb_case.html
        patty = Ingredient("Patty",'rawpatty.png', 100000, 100000)
        patty = patty.duplicate()
        patty.move(mode.app.setUpMode.pattyx, mode.app.setUpMode.pattyy)
        #from https://www.humphreysfarm.com/productcart/pc/viewPrd.asp?idproduct=11593

        cheese = Ingredient("Cheese",'cheese slicer.png', 100000, 100000)
        cheese2 = cheese.duplicate()
        cheese2.move(mode.app.setUpMode.cheesex, mode.app.setUpMode.cheesey)
        #from https://www.lantmannen-unibake.com/Products/Easy-to-Eat/Burger-Buns/giant-hamburger-bun-sesam-seeds/
        bun = Ingredient("Bun", 'bunr.png', 100000, 100000)
        bun2 = bun.duplicate()
        bun2.move(mode.app.setUpMode.bunx, mode.app.setUpMode.buny)
        
        #from https://livejapan.com/en/article-a0000370/

        sushi = Ingredient("Sushi", 'sushi.png', 10000, 10000)
        sushi2 = sushi.duplicate()
        sushi2.move(mode.app.setUpMode.bunx, mode.app.setUpMode.buny)
        #from https://www.alamy.com/asian-noodle-soup-ramen-with-shrimp-vegetables-and-egg-in-black-bowl-on-gray-concrete-background-flat-lay-top-view-mockup-overhead-healthy-food-image333806059.html
        ramen = Ingredient("Ramen", 'ramen.png', 10000, 10000)
        ramen2 = ramen.duplicate()
        ramen2.move(mode.app.setUpMode.cheesex, mode.app.setUpMode.cheesey)
        #from https://www.spriters-resource.com/ds_dsi/cookingmama/sheet/27621/

        cake = Ingredient("Cake", 'cake.png', 100000, 10000)
        cake2 = cake.duplicate()
        cake2.move(mode.app.setUpMode.lettucex, mode.app.setUpMode.lettucey)
        #from https://www.alamy.com/stock-photo/baozi.html

        baozi = Ingredient("Baozi", 'baozi.png', 100000, 10000)
        baozi2 = baozi.duplicate()
        baozi2.move(mode.app.setUpMode.pattyx, mode.app.setUpMode.pattyy)
        #from https://twitter.com/bigbowlbeef

        rice = Ingredient("Rice", 'rice.png', 100000, 10000)
        rice2 = rice.duplicate()
        rice2.move(mode.app.setUpMode.tomatox, mode.app.setUpMode.tomatoy)
        
        mode.ingredientsList2 = [sushi2, ramen2, cake2, baozi2, rice2]

        mode.ingredientsList = [lettuce2, tomato2, patty, cheese2, bun2]
        
       

        mode.draggedIngredient = None
        mode.extraIngredients = []
        mode.plates = [Plate(mode.app.setUpMode.plate1x, mode.app.setUpMode.plate1y), Plate(mode.app.setUpMode.plate2x, mode.app.setUpMode.plate2y), Plate(mode.app.setUpMode.plate3x, mode.app.setUpMode.plate3y),
            Plate(mode.app.setUpMode.plate4x, mode.app.setUpMode.plate4y), Plate(mode.app.setUpMode.plate5x, mode.app.setUpMode.plate5y)]
 
        mode.pot = Pot(mode.app.setUpMode.potx, mode.app.setUpMode.poty)
    


    def seatCustomer(mode, customer):  
        for seat in range(len(mode.seatCoords)):
            
            if not mode.seatTaken[seat]: 
                customer.move(mode.seatCoords[seat][0], mode.seatCoords[seat][1])
                customer.isSeated = True
                customer.seat = seat
                mode.seatTaken[seat] = True
                return True
        return False


    def equal(mode, list1, list2):
        if(len(list1) != len(list2)):
            return False

        for i in range(len(list1)):
            if(list1[i].name != list2[i].name):
                return False
        for i in range(len(list2)):
            if(list2[i].url == 'rawpatty.png' or list2[i].url == 'burntpatty.png'):
                return False

        return True
    
    def getNumber(mode):
        
        number = random.randint(0, len(mode.app.setUpMode.doors)-1)
        #number = random.randint(0, 2)
        return number

    def timerFired(mode):
        
        if(mode.gameOver):
            return
        mode.pot.timerFired()
        if(mode.score >200):
            mode.app.setActiveMode(mode.app.winMode)
    
        mode.clock += 1
        
        if not mode.draggedIngredient is None:

            x1, y1, w1, h1 = mode.draggedIngredient.getPoints()
        
        x4, y4, w4, h4 = mode.pot.getPoints()

        if not mode.draggedIngredient is None:
            if(mode.rectanglesOverlap(x1, y1, w1, h1, x4, y4, w4, h4) and (mode.draggedIngredient.url == ('rawpatty.png'))):
                mode.draggedIngredient.move(mode.pot.cx, mode.pot.cy)
                mode.pot.hasBurger = True
                mode.draggedIngredient.isBurger = True
                
            else:
                mode.pot.hasBurger = False

        if(mode.pot.hasBurger):
            
            if(mode.clock%10 == 1):
                mode.pot.hamburgTime += 1

            if (not mode.draggedIngredient is None and mode.draggedIngredient.isBurger == True):
                mode.draggedIngredient.changeImage('patty.png')
                mode.draggedIngredient.url = 'patty.png'

            if(mode.pot.hamburgTime >7):
                if (not mode.draggedIngredient is None and mode.draggedIngredient.isBurger == True):
                    mode.draggedIngredient.changeImage('burntpatty.png')
                    mode.draggedIngredient.url = 'burntpatty.png'
                    mode.pot.hamburgTime = 0
                    mode.pot.hasBurger = False

        if(mode.peopleWhoLeft > 10):
            mode.gameOver = True

        for customer in range(len(mode.people)):
            if(mode.clock > 10 + mode.lastSeatTime):
                
                if not mode.people[customer].isSeated and not mode.people[customer].isMovingOut:
                    mode.seatCustomer(mode.people[customer])
                    mode.lastSeatTime = mode.clock
                    mode.people[customer].currentTime = 0

        i = 0
        while i< len(mode.people):
            if mode.people[i].isMovedOut(): 
                if(time.time() > mode.people[i].endTime):
                    mode.peopleWhoLeft += 1
                
                mode.people.remove(mode.people[i])

                i-=1
            i+=1
        

        startingx = mode.app.setUpMode.startingx
        startingy = mode.app.setUpMode.startingy
        i = 0
        while i < len(mode.people):
 
            if(time.time() > mode.people[i].endTime):
                
                if(mode.people[i].isMovingOut == False):
        
                    mode.people[i].isMovingOut = True

                    number = mode.getNumber()
                    door = mode.app.setUpMode.doors[number]

                  
                    mode.people[i].move(door.x, door.y)
                
                    mode.people.append(Customer(startingx, startingy))
 
                    
                    if(mode.people[i].isSeated):
                        mode.people[i].isSeated = False
                        mode.seatTaken[mode.people[i].seat] = False
                    
            x2, y2, w2, h2 = mode.circleplate.getPoints()
        
            if mode.equal(mode.people[i].b.getIngredientsList(), mode.circleplate.ingredients) and mode.rectanglesOverlap(x2, y2, w2, h2, mode.people[i].x-20, mode.people[i].y-20, mode.people[i].x +20, mode.people[i].y +20):
            
                if(mode.people[i].isMovingOut == False):
                    mode.people[i].isMovingOut = True
                    number = mode.getNumber()
                    door = mode.app.setUpMode.doors[number]
                    mode.people[i].move(door.x, door.y)
                    
                    mode.people.append(Customer(startingx, startingy))

                    mode.people[i].isSeated = False
                    mode.seatTaken[mode.people[i].seat] = False
                    mode.score += mode.people[i].duration - mode.people[i].currentTime
        
                mode.circleplate = MainPlate(mode.mainplatex, mode.mainplatey, [])
                mode.isHandingOut = False
            
            if mode.equal(mode.people[i].h.getIngredientsList(), mode.circleplate.ingredients) and mode.rectanglesOverlap(x2, y2, w2, h2, mode.people[i].x-20, mode.people[i].y-20, mode.people[i].x +20, mode.people[i].y +20):

                if(mode.people[i].isMovingOut == False): 
                    mode.people[i].isMovingOut = True

                    number = mode.getNumber()
                    door = mode.app.setUpMode.doors[number]

                    mode.people[i].move(door.x, door.y)

                    mode.people.append(Customer(startingx, startingy))
 
                    mode.people[i].isSeated = False
                    mode.seatTaken[mode.people[i].seat] = False
                    mode.score += mode.people[i].duration - mode.people[i].currentTime
                mode.circleplate = MainPlate(mode.mainplatex, mode.mainplatey, [])
                mode.isHandingOut = False            
            i+=1
           
        if(mode.rectanglesOverlap(x2, y2, w2, h2, mode.x, mode.y, 80, 80)):
            mode.isHandingOut = True
        if mode.isHandingOut: 
            if(mode.direction == 'Down') or (mode.direction == 'Right'):
                mode.circleplate.move(mode.x+30, mode.y+30)
            elif(mode.direction == 'Up'):
                    mode.circleplate.move(mode.x -30, mode.y -30)
            else: mode.circleplate.move(mode.x-50, mode.y)
    
        for i in range(len(mode.people)):
            mode.people[i].timerFired()
            mode.spriteCounter = (1 + mode.spriteCounter) % len(mode.sprites)    
        mode.pot.timerFired()
    
    def rectanglesOverlap(mode, x1, y1, w1, h1, x2, y2, w2, h2):
        
        if ((x1 <= x2 + w1 and x1 >= x2)and (y1 >= y2 and y1 <= y2 + h2)):
            return True
        if((x1 <= x2 + w1 and x1 >= x2) and (y1+ h1 >= y2 and y1+h1<= y2 + h2)):
            return True
        if((x1 + w1 <= x2 + w2 and x1 + w1 >= x2) and (y1 >= y2 and y1 <= y2 + h2)):
            return True
        if((x1 + w1 <= x2 + w2 and x1 + w1 >= x2) and (y1+ h1 >= y2 and y1+h1<= y2 +
        h2)):
            return True

        else: return False

               
    def redrawAll(mode, canvas):
        
        canvas.delete("all")
        mode.app.setUpMode.redrawAll(canvas)

        sprite = mode.sprites[mode.direction][mode.spriteCounter]
        canvas.create_image(mode.x,mode.y, image=sprite)
    
 
        mode.pot.drawImage(canvas)
        mode.trashcan.drawImage(canvas)
        for i in range(len(mode.plates)):
            mode.plates[i].drawImage(canvas)
     
        mode.circleplate.drawImage(canvas)
        font = 'Arial 26 bold'

        if(mode.score > 80):
            mode.ingredientsList = mode.ingredientsList2
            canvas.create_text(mode.width/2-140, 20, text='Level 2', font=font, fill = 'blue')
        else: canvas.create_text(mode.width/2-140, 20, text = 'Level 1', font = font, fill = 'purple')

    
        for i in range(len(mode.ingredientsList)):
            mode.ingredientsList[i].drawImage(canvas)
    
        for i in range(len(mode.extraIngredients)):
            mode.extraIngredients[i].drawImage(canvas)

        if(mode.score > 80):
            for i in range(len(mode.people)):
                mode.people[i].isTwo = True
 
        for i in range(len(mode.people)):
            mode.people[i].drawImage(canvas)

        font = 'Arial 22 bold'
        canvas.create_text(mode.width/2, 20, text=f'Score: {mode.score}', font=font, fill = 'blue')
        canvas.create_text(60, 20, text = f'Left: {mode.peopleWhoLeft}', font = font, fill = 'yellow')
        if (mode.gameOver):
            canvas.create_text(mode.width/2, mode.height/2, text='Game over!',
                            font='Arial 26 bold')
            canvas.create_text(mode.width/2, mode.height/2+40,
                            text='Press r to restart!',
                            font='Arial 26 bold')

    def keyPressed(mode, event):

        if(event.key == 'f'):
            
            mode.circleplate.move(mode.mainplatex, mode.mainplatey)
            mode.isHandingOut = False

        elif (event.key == 'Down'):

            mode.direction = 'Down'
            mode.y += 10
            mode.spriteCounter = 0
        
        elif (event.key == 'Left'):
            mode.direction = 'Left'
            mode.x -= 10
            mode.spriteCounter = 0
        elif (event.key == 'Right'):

            mode.direction = 'Right'
            mode.x += 10
            mode.spriteCounter = 0
        
        elif (event.key == 'Up'):
            mode.direction = 'Up'
            mode.y -= 10
            mode.spriteCounter = 0

        elif (event.key == 'r'):    
            mode.app.setUpMode.initrestart()
            mode.initHamburg()
            mode.app.setActiveMode(mode.app.splashScreenMode)

        elif mode.gameOver:
            return
       
    def mousePressed(mode, event):
        if mode.draggedIngredient:
            return
        
        for item in mode.extraIngredients[::-1]:
            if(item.getBounds(event.x, event.y)):
                mode.draggedIngredient = item
                return

        if(mode.score > 80):
            mode.ingredientsList = mode.ingredientsList2

        for item in mode.ingredientsList[::-1]:
            if(item.getBounds(event.x, event.y)):
                mode.draggedIngredient = item.duplicate()
                mode.extraIngredients.append(mode.draggedIngredient)
                return

        for item in mode.circleplate.ingredients[::-1]:
            if(item.getBounds(event.x, event.y)):
                mode.draggedIngredient = item 
                mode.circleplate.ingredients.remove(item)
                mode.extraIngredients.append(mode.draggedIngredient)
                return
 
    def mouseDragged(mode, event):
        x2, y2, w2, h2 = mode.circleplate.getPoints()
        
        if(mode.draggedIngredient):
            
            mode.draggedIngredient.move(event.x, event.y)
            x1, y1, w1, h1 = mode.draggedIngredient.getPoints()
            
            if(mode.rectanglesOverlap(x1, y1, w1, h1, x2-10, y2-10, w2+10, h2+10)):
                
                mode.draggedIngredient.move(mode.circleplate.cx, mode.circleplate.cy)
    def mouseReleased(mode, event):
        if mode.draggedIngredient is None:
            return

        x1, y1, w1, h1 = mode.draggedIngredient.getPoints()
        x3, y3, w3, h3 = mode.trashcan.getPoints()
        x2, y2, w2, h2 = mode.circleplate.getPoints()
        x4, y4, w4, h4 = mode.pot.getPoints()

        if(mode.rectanglesOverlap(x1, y1, w1, h1, x2, y2, w2, h2)):
        
            mode.circleplate.add(mode.draggedIngredient) 

            if(mode.draggedIngredient in mode.extraIngredients):
                mode.extraIngredients.remove(mode.draggedIngredient)

        if(mode.draggedIngredient in mode.extraIngredients):
            if(mode.rectanglesOverlap(x1, y1, w1, h1, x3, y3, w3, h3)):
                mode.extraIngredients.remove(mode.draggedIngredient)

        mode.draggedIngredient = None
        
class winMode(Mode):

    def appStarted(mode):
        mode.background = Image.open('cherry.png') #, Image.ANTIALIAS)
        mode.background = ImageTk.PhotoImage(mode.background)
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2 + 120, image = mode.background)

    def keyPressed(mode, event):
        if(event.key == 'r'):
            mode.app.setUpMode.initrestart()
            mode.app.gameMode.initHamburg()
            mode.app.setActiveMode(mode.app.splashScreenMode)
class MyModalApp(ModalApp):

    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.setUpMode = SetUpMode()
        app.instructionsMode = InstructionsMode()
        app.setActiveMode(app.splashScreenMode)
        app.winMode = winMode()
        app.timerDelay = 50

app = MyModalApp(width=width, height=height)
