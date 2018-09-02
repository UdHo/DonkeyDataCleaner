#!/usr/bin/python3
import sys
import os
import json
import datetime
from tkinter import *
from PIL import ImageTk, Image


class DataCleaner:
    def __init__(self, path="."):
        self.path = path
        self.window = Tk()
        self.pastImages = []
        self.pastImagenames = []
        self.futureImages = []
        self.futureImagenames = []
        self.frame = Frame(self.window)
        self.panel = Label(self.window)
        self.angle = Label(self.window)
        self.bar = Canvas(self.window, width=200, height=30, bg='white')
        self.imagelist = list(sorted(list(
            filter(lambda x: x.find(".jpg") != -1, os.listdir(path))) , key = lambda x: int(x[:x.find("_")])))
        self.imageiter = iter(self.imagelist)
        self.panels = [self.panel]
        for i in range(10):
            self.loadImageInQueue(False)
        for i in range(len(self.futureImages)):
            self.panels.append(Label(self.frame))
        for i in self.panels:
            i.pack( side = LEFT )
        self.frame.pack()
        self.nextImage()
        #self.panel.pack()
        self.angle.pack()
        self.bar.pack()
        self.window.bind("<Key>", self.key)
        self.window.mainloop()


    def updateImages(self):
        c=0
        for panel in self.panels:
            if len(self.futureImages) > c:
                panel.config(image = self.futureImages[c])
            c+=1
         
        
    def nextImage(self):
        self.loadImageInQueue()
        self.imagename = self.futureImagenames[0]
        self.image = self.futureImages[0]
        self.imagenr = self.imagename[:self.imagename.find("_")] 
        #self.image = self.combineImages() 
        #self.panel.config(image = self.image)
        self.updateImages()
        self.updateAngle()

    def loadImageInQueue(self, shift = True):
        nextname = next(self.imageiter)
        while self.skipImage(nextname):
            nextname = next(self.imageiter)
        self.futureImages.append(self.loadImage(nextname))
        self.futureImagenames.append(nextname)
        if shift:
          self.futureImages.pop(0)
          self.futureImagenames.pop(0)

    def drawBar(self,angle):
        self.bar.delete("all")
        self.bar.create_rectangle(100 + int(angle*100),0,100,30,fill = "green")
        
    def loadImage(self, imageName):
        #self.imagename = imageName
        return ImageTk.PhotoImage(
            Image.open(self.path + "/" + imageName))
        #self.panel.config(image=self.image) 

    def updateAngle(self):
        self.jsonfile = self.path + "/" + "record_" + \
            self.imagenr + ".json"
        with open(self.jsonfile) as json_data:
            self.jsonData = json.load(json_data)
            self.angle.config(text=self.jsonData["user/angle"])
        self.drawBar(self.jsonData["user/angle"])
        
    def skipImage(self, filename):
        with open(self.path+ "/record_" +filename[:filename.find("_")]+".json") as json_data:
            data = json.load(json_data)
        return "status" in data
            
        
    def key(self, event):
        print("pressed", repr(event.char))
        c = event.char
        if c is " ":
            print("Keep")
            self.keep()
        elif c is "n" or c is "m" or c is "b":
            self.changeDirection(0.0)
        else:
            try:
                direction = int(c)
                if direction == 0:
                    direction = 10
                if direction <= 5:
                    direction = -1.2 + direction * 0.2
                else:
                    direction = (direction-5) * 0.2
                print("New direction", direction)
                self.changeDirection(direction)
            except ValueError:
                print("Delete")
                self.delete()
        self.writeJson()
        self.nextImage()

    def keep(self):
        f = open("keep.txt", "a+")
        f.write(self.imagename + "\n")
        f.close()
        self.jsonData["status"] = "keep"

    def delete(self):
        f = open("delete.txt", "a+")
        f.write(self.imagename + "\n")
        f.close()
        self.jsonData["status"] = "delete"

    def changeDirection(self, direction):
        f = open("change.txt", "a+")
        f.write(self.imagename + " " + str(direction) + "\n")
        f.close()
        self.jsonData["status"] = "changed"
        self.jsonData["oldAngle"] = self.jsonData["user/angle"]
        self.jsonData["user/angle"] = direction

    def writeJson(self):
        f = open(self.jsonfile, "w")
        print("New jsondata")
        self.jsonData["changetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json.dump(self.jsonData, f)
        f.close()

def main(argv):
    if len(argv) > 0:
        gui = DataCleaner(argv[0])
    else:
        gui = DataCleaner()


if __name__ == "__main__":
    main(sys.argv[1:])
