'''
  Author: Nathan Peterson
  Date: 10-23-2017
'''

import random

def collage():
  setMediaPath()

  #Load Images
  canvasFile = getMediaPath('landscape_canvas.jpg')
  file0 = getMediaPath('0.png')
  file1 = getMediaPath('1.png')
  
  #Create Canvas Image
  canvas = makePicture(canvasFile)
  
  #Get Width / Height of Canvas
  canvasWidth = getWidth(canvas) -1
  canvasHeight = getHeight(canvas) -1
  
  #Switch background to black
  setBackgroundBlack(canvas)
  
  #Generate a Random Collage of 0 and 1
  generateCollage(file0, file1, canvas, canvasWidth, canvasHeight)

  #Sign the Image
  sign(canvas, canvasWidth, canvasHeight)
  
  #Save Image to current Path
  saveCollage(canvas)
  
  #Show the Collage
  show(canvas)

#Function to generate a random RGBA color
def randomColorGenerator():
  red = random.randint(0,255)
  green = random.randint(0,255)
  blue = random.randint(0,255)
  alpha = random.random()
  return red, green, blue, alpha

#Set a random Background Color to image
#Distort boolean: False: Solid Color || True: Each Pixel different Color 
def setRandomBackgroundColor(image, distort):
  backgroundColor = randomColorGenerator()
  for px in getPixels(image):
    if(getRed(px) == 0 and getBlue(px) == 0 and getGreen(px) == 0):
      continue
    elif(distort == 1):
      backgroundColor = randomColorGenerator()
    newColor = makeColor(backgroundColor[0], backgroundColor[1], backgroundColor[2])
    setColor(px, newColor)
  return image

#Set a random Text Color to image
#Distort boolean: False: Solid Color || True: Each Pixel different Color 
def setRandomTextColor(image, distort):
  textColor = randomColorGenerator()
  for px in getPixels(image):
    if(getRed(px) != 0 and getBlue(px) != 0 and getGreen(px) != 0):
      continue
    elif(distort == 1):
      textColor = randomColorGenerator()
    newColor = makeColor(textColor[0], textColor[1], textColor[2])
    setColor(px, newColor)
  return image

#Function that Randomly Assigns which color function to use
def alterImageColor(image):
  number = random.randint(0,11)
  #Only Set background to distorted
  if(number == 2):
    newImage = setRandomBackgroundColor(image, 1)
    newImage = setRandomTextColor(image, 0)
  #Only set Text to distorted
  elif(number == 7): 
    newImage = setRandomBackgroundColor(image, 0)         
    newImage = setRandomTextColor(image, 1)
  #Do not change colors from orginal
  elif(number == 1):
    newImage = image
  #Everything else set to different background/text color
  else:
    newImage = setRandomBackgroundColor(image, 0)         
    newImage = setRandomTextColor(image, 0)    
  return newImage 

#Randomly generate a 0 or 1 image
def OneOrZeroPicture(file0, file1):
  binary = random.randint(0,1)
  if(binary == 0):
    return  makePicture(file0)
  elif(binary == 1):
    return  makePicture(file1)

#Add the current image to the canvas
def addToCanvas(image, canvas, i, j, canvasWidth, canvasHeight):
  #Split X axis in 10
  targetX = (canvasWidth)/10 * j
  for sourceX in range(0,(canvasWidth/10) -1):
  
    #Split Y axis in 6
    targetY = (canvasHeight)/6 * i
    for sourceY in range(0, getHeight(image)-1):
    
      #Get Color of current image
      color = getColor(getPixel(image, sourceX, sourceY))
      #Place Pixel color onto canvas at a specific pixel
      setColor(getPixel(canvas, targetX, targetY), color)
      targetY = targetY + 1
      
    #Ensure Count stays below length -1
    if(targetX < getWidth(canvas)-1):
        targetX = targetX + 1

#Set image to Grey Scale
def greyScale(image):
  for px in getPixels(image):
    r = getRed(px) * 0.299
    g = getGreen(px) * 0.587
    b = getBlue(px) * 0.114
    lum = r+g+b
    setColor(px, makeColor(lum, lum, lum))

#Mirror the image
def mirror(image):
  for y in range (0,getHeight(image)):
    for x in range (0, getWidth(image)/2):
      #Get Left and Right most Pixel
      left=getPixel(image, x, y)
      right=getPixel(image, getWidth(image)-x-1,y)
      color1=getColor(left)
      color2=getColor(right)
      
      #Swap the colors
      setColor(right, color1)
      setColor(left, color2)

#Flip image upside down
def flip(image):
  for y in range (0,getHeight(image)/2):
    for x in range (0, getWidth(image)):
      #Get the top and bottom most pixel
      up=getPixel(image, x, y)
      down=getPixel(image, x,getHeight(image)-y-1)
      color1=getColor(up)
      color2=getColor(down)
      
      #Swap the colors
      setColor(down, color1)
      setColor(up, color2)

#Create a negative of the picture
def negative(image):
  for px in getPixels(image):
    r = 255 - getRed(px)
    g = 255 - getGreen(px)
    b = 255 - getBlue(px)
    setColor(px, makeColor(r, g, b))

#Change background of canvas to Black
def setBackgroundBlack(canvas):
  for px in getPixels(canvas):
    setColor(px,  makeColor(0, 0, 0))

#Function to Randomly Select One of the Manipulations or a Combination of them
def randomManipulation(image):
  number = random.randint(0,20)
  if(number == 1 or number ==14):
    flip(image)
  elif(number == 2 or number == 12):
    mirror(image)
  elif(number == 3 or number == 15 or number == 9 or number == 8):
    mirror(image)
    flip(image)
  elif(number == 4):
    negative(image)
  elif(number == 5):
    greyScale(image)
  elif(number == 6):
    mirror(image)
    flip(image)
    greyScale(image)
  elif(number == 7): 
    flip(image)
    greyScale(image)

#Funtion to generate the collage Using an Multi-dimenstional array [4][10]
def generateCollage(file0, file1, canvas, canvasWidth, canvasHeight):
  for i in range(0,5):
    for j in range(0,10):
      #First image is default image for 0
      if(i == 0 and j == 0):
        image =  makePicture(file0)
        
      #Second Image is default image for 1
      elif(i == 0 and j ==1):
        image =  makePicture(file1)
        
      #Set Row 1 Col 1/2 to negative of default to see what happens
      elif(i == 1 and (j == 0 or j == 1)):
        if(j == 0):
          image =  makePicture(file0)
          negative(image)
        if(j == 1):
          image =  makePicture(file1)
          negative(image)
      #Else select at random
      else:
        #Set a random Color
        image = alterImageColor(OneOrZeroPicture(file0, file1))
        
        #Set a random Manipulation
        randomManipulation(image)
        
      #Add the image to canvas
      addToCanvas(image, canvas, i, j, canvasWidth, canvasHeight)

#Sign the canvas witha Chromakey like signature
def sign(canvas, canvasWidth, canvasHeight):
  print "Signing"
  
  #Load and Create Signature image
  signatureFile = getMediaPath('signature.png')
  signature = makePicture(signatureFile)
  
  #Starting point at where to place signature
  start =  canvasHeight/6 * 5
  targetY = 0
  targetX = 0
  for sourceX in range(0, getWidth(signature)):
    for sourceY in range(0, getHeight(signature)):
      #If the current px is not white than grab color and coordinates of px
      if(getRed(getPixel(signature, sourceX, sourceY)) != 255 and getBlue(getPixel(signature, sourceX, sourceY)) != 255 and getGreen(getPixel(signature, sourceX, sourceY)) != 255):
       #Set coordinates of px
       targetX = sourceX
       targetY = start + sourceY
       
       #Get color of signature
       color = getColor(getPixel(signature, sourceX, sourceY))
       
       #Apply Signature to canvas
       setColor(getPixel(canvas, targetX, targetY), color)

#Save the Collage to File Path by generating a random file name for image using large random number generator
def saveCollage(image):
  name = "canvas" + str(random.randint(0, 9999999999)) + ".png"
  writePictureTo(image, getMediaPath(name))

#Call Collage and Generate Image
collage()