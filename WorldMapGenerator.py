#World Map Generator by mummiedanser

#imports
import random
import math
import time
from tkinter import *

#window setup
window=Tk()
window.title("World Map Generator")
window.configure(background="white")
window.resizable(False,False)

window.geometry("913x357")
disp=Canvas(window, width=613+300, height=357, bg="black",highlightthickness=0)

disp.grid(row=0, column=0, sticky=W)
disp.create_rectangle(614,307,863,50, outline="gray10", fill="gray10")
disp2=Canvas(window, width=513, height=257, bg="gray20",highlightthickness=0)
disp2_disp=disp.create_window(50, 50, anchor=NW, window=disp2)


def generatemap(xsize,ysize,stepsize,minheight,maxheight,height,rangefactor):
    xsize=2**xsize+1
    ysize=2**ysize+1
    stepsize=2**stepsize
    scale=1
    randrange=int(round(height/rangefactor))
    matrix=[[0 for x in range(xsize)] for y in range(ysize)]
    for x in range(0,xsize,stepsize):
        for y in range(0,ysize,stepsize):
            matrix[y][x]=random.randint(minheight,height)
    while stepsize>1:
        halfstepsize=int(stepsize/2)
        for x in range(xsize):
            for y in range(ysize):
                try:
                    if matrix[y+halfstepsize][x+halfstepsize]!=0 and matrix[y+halfstepsize][x-halfstepsize]!=0 and matrix[y-halfstepsize][x+halfstepsize]!=0 and matrix[y-halfstepsize][x-halfstepsize]!=0:
                        avg=(matrix[y+halfstepsize][x+halfstepsize]+matrix[y+halfstepsize][x-halfstepsize]+matrix[y-halfstepsize][x+halfstepsize]+matrix[y-halfstepsize][x-halfstepsize])/4
                        r=random.randint(-randrange,randrange)*scale
                        if matrix[y][x]==0:
                            matrix[y][x]=round(avg+r)
                        if matrix[y][x]<minheight:
                            matrix[y][x]=minheight
                        if matrix[y][x]>maxheight:
                            matrix[y][x]=maxheight
                except:
                    pass
        for x in range(xsize):
            for y in range(ysize):
                count=0
                value1=0
                value2=0
                value3=0
                value4=0
                try:
                    if matrix[y+halfstepsize][x]!=0:
                        count=count+1
                        value1=matrix[y+halfstepsize][x]
                except:
                    pass
                try:
                    if matrix[y-halfstepsize][x]!=0:
                        count=count+1
                        value2=matrix[y-halfstepsize][x]
                except:
                    pass
                try:
                    if matrix[y][x+halfstepsize]!=0:
                        count=count+1
                        value3=matrix[y][x+halfstepsize]
                except:
                    pass
                try:
                    if matrix[y][x-halfstepsize]!=0:
                        count=count+1
                        value4=matrix[y][x-halfstepsize]
                except:
                    pass
                if count>=3:
                    if count==3:
                        avg=(value1+value2+value3+value4)/3
                    if count==4:
                        avg=(value1+value2+value3+value4)/4
                    r=random.randint(-randrange,randrange)*scale
                    if matrix[y][x]==0:
                        matrix[y][x]=round(avg+r)
                    if matrix[y][x]<minheight:
                        matrix[y][x]=minheight
                    if matrix[y][x]>maxheight:
                        matrix[y][x]=maxheight
        stepsize/=2
        scale/=2
    return matrix

def landscapecalculator(heightmap,heatmap,humiditymap,xsize,ysize):
    xsize=2**xsize+1
    ysize=2**ysize+1
    matrix=[["" for x in range(xsize)] for y in range(ysize)]
    for x in range(xsize):
        for y in range(ysize):
            if heightmap[y][x]<30:
                matrix[y][x]="Ocean"
            elif heightmap[y][x]>=30 and heightmap[y][x]<50:
                if heatmap[y][x]==1:
                    matrix[y][x]="Ice Floe"
                elif heatmap[y][x]==7:
                    matrix[y][x]="Tropical Sea"
                else:
                    matrix[y][x]="Sea"
            elif heightmap[y][x]>=90 and heightmap[y][x]<94:
                matrix[y][x]="Mountain"
            elif heightmap[y][x]>=94 and heightmap[y][x]<98:
                matrix[y][x]="High Mountain"
            elif heightmap[y][x]>=98:
                matrix[y][x]="Mountain Peak"
            else:
                if heatmap[y][x]==1:
                    matrix[y][x]="Polar"
                elif heatmap[y][x]==2:
                    matrix[y][x]="Tundra"
                elif humiditymap[y][x]<=2:
                    if heatmap[y][x]>=5:
                        matrix[y][x]="Hot Desert"
                    elif heatmap[y][x]==4:
                        matrix[y][x]="Cool Desert"
                    elif heatmap[y][x]==3:
                        matrix[y][x]="Cold Parkland"
                elif humiditymap[y][x]==3 or humiditymap[y][x]==4:
                    if heatmap[y][x]>=6:
                        matrix[y][x]="Savanna"
                    elif heatmap[y][x]==3 or heatmap[y][x]==4:
                        matrix[y][x]="Steppe"
                    elif heatmap[y][x]==5:
                        matrix[y][x]="Chaparral"
                elif humiditymap[y][x]==5 or humiditymap[y][x]==6:
                    if heatmap[y][x]==3:
                        matrix[y][x]="Grassland"
                    elif heatmap[y][x]==4:
                        matrix[y][x]="Grassland"
                    elif heatmap[y][x]==5:
                        matrix[y][x]="Grassland"
                    elif heatmap[y][x]==6:
                        matrix[y][x]="Tropical Seasonal Forest"
                    elif heatmap[y][x]==7:
                        matrix[y][x]="Tropical Rainforest"
                
                elif humiditymap[y][x]==7 or humiditymap[y][x]==8:
                    if heatmap[y][x]==3:
                        matrix[y][x]="Coniferous Forest"
                    elif heatmap[y][x]==4:
                        matrix[y][x]="Mixed Forest"
                    elif heatmap[y][x]==5:
                        matrix[y][x]="Deciduous Forest"
                    elif heatmap[y][x]>=6:
                        matrix[y][x]="Tropical Rainforest"
    return matrix       
                    
def img_landscape(landscapemap,heightmap,xsize,ysize):
    xsize=2**xsize+1
    ysize=2**ysize+1
    landscapeimage=PhotoImage(width=xsize, height=ysize)
    for x in range(xsize):
        for y in range(ysize):
            darkening=1
            if heightmap[y][x]>=55 and heightmap[y][x]<70:
                darkening=0.8
            if heightmap[y][x]>=70 and heightmap[y][x]<80:
                darkening=0.6
            if heightmap[y][x]>=80 and heightmap[y][x]<90:
                darkening=0.5

            
            if landscapemap[y][x]=="Ocean":
                color=(26,142,194)
            elif landscapemap[y][x]=="Sea":
                color=(58,177,225)
            elif landscapemap[y][x]=="Tropical Sea":
                color=(58,200,225)
            elif landscapemap[y][x]=="Ice Floe":
                color=(210,237,241)
            elif landscapemap[y][x]=="Mountain":
                color=(140,160,176)
            elif landscapemap[y][x]=="High Mountain":
                color=(108,129,151)
            elif landscapemap[y][x]=="Mountain Peak":
                color=(212,216,225)

            elif landscapemap[y][x]=="Polar":
                color=(242,242,247)
            elif landscapemap[y][x]=="Tundra":
                color=(135,165,165)
            elif landscapemap[y][x]=="Cold Parkland":
                color=(125,126,103)
            elif landscapemap[y][x]=="Coniferous Forest":
                color=(25,78,78)
            elif landscapemap[y][x]=="Mixed Forest":
                color=(22,139,98)
            elif landscapemap[y][x]=="Steppe":
                color=(67,139,65)
            elif landscapemap[y][x]=="Cool Desert":
                color=(155,182,84)
            elif landscapemap[y][x]=="Deciduous Forest":
                color=(25,199,104)
            elif landscapemap[y][x]=="Chaparral":
                color=(70,199,65)
            elif landscapemap[y][x]=="Hot Desert":
                color=(204,255,62)
            elif landscapemap[y][x]=="Savanna":
                color=(131,255,62)
            elif landscapemap[y][x]=="Tropical Seasonal Forest":
                color=(72,255,61)
            elif landscapemap[y][x]=="Tropical Rainforest":
                color=(31,167,51)
            elif landscapemap[y][x]=="Grassland":
                color=(160,224,128)

            color=tuple(round(v*darkening) for v in color)
            hexcolor='#%02x%02x%02x' % color
            landscapeimage.put(hexcolor,(x,y))
    return landscapeimage

def img_height(heightmap,xsize,ysize):          
    xsize=2**xsize+1
    ysize=2**ysize+1
    heightimage=PhotoImage(width=xsize, height=ysize)
    for x in range(xsize):
        for y in range(ysize):
            color1=(240,220,130)#height=1
            color2=(138,51,36)#height=100
            color=(round((color1[0]*(100-heightmap[y][x])+color2[0]*(heightmap[y][x]-1))/99),round((color1[1]*(100-heightmap[y][x])+color2[1]*(heightmap[y][x]-1))/99),round((color1[2]*(100-heightmap[y][x])+color2[2]*(heightmap[y][x]-1))/99))
            hexcolor='#%02x%02x%02x' % color
            heightimage.put(hexcolor,(x,y))
    return heightimage

def img_heat(heatmap,xsize,ysize):          
    xsize=2**xsize+1
    ysize=2**ysize+1
    heatimage=PhotoImage(width=xsize, height=ysize)
    for x in range(xsize):
        for y in range(ysize):
            color1=(0,35,149)#heat=1
            color2=(237,41,57)#heat=7
            color=(round((color1[0]*(7-heatmap[y][x])+color2[0]*(heatmap[y][x]-1))/6),round((color1[1]*(7-heatmap[y][x])+color2[1]*(heatmap[y][x]-1))/6),round((color1[2]*(7-heatmap[y][x])+color2[2]*(heatmap[y][x]-1))/6))
            hexcolor='#%02x%02x%02x' % color
            heatimage.put(hexcolor,(x,y))
    return heatimage

def img_humidity(humiditymap,xsize,ysize):          
    xsize=2**xsize+1
    ysize=2**ysize+1
    humidityimage=PhotoImage(width=xsize, height=ysize)
    for x in range(xsize):
        for y in range(ysize):
            color1=(81,40,136)#humidity=1
            color2=(11,218,81)#humidity=8
            color=(round((color1[0]*(8-humiditymap[y][x])+color2[0]*(humiditymap[y][x]-1))/7),round((color1[1]*(8-humiditymap[y][x])+color2[1]*(humiditymap[y][x]-1))/7),round((color1[2]*(8-humiditymap[y][x])+color2[2]*(humiditymap[y][x]-1))/7))
            hexcolor='#%02x%02x%02x' % color
            humidityimage.put(hexcolor,(x,y))
    return humidityimage

def generateworldmap():
    global maptype,heightimage,heatimage,humidityimage,landscapeimage,heightmap,heatmap,humiditymap,landscapemap,biomemap
    button1.config(text="Generating...", state="disabled")
    displaytype(0,xsize,ysize)
    text5.config(text="-")
    text7.config(text="-")
    text8.config(text="-")
    text10.config(text="-")
    text12.config(text="-")
    text14.config(text="-")
    disp.update()
    random.seed(input1.get())
    start_time=time.time()
    print("Generating world map...",2**xsize+1,"x",2**ysize+1)
    heightmap=generatemap(xsize,ysize,5,1,100,100,4)
    heatmap=generatemap(xsize,ysize,8,1,7,7,1)
    humiditymap=generatemap(xsize,ysize,8,1,8,8,1)
    landscapemap=landscapecalculator(heightmap,heatmap,humiditymap,xsize,ysize)
    heightimage=img_height(heightmap,xsize,ysize)
    heatimage=img_heat(heatmap,xsize,ysize)
    humidityimage=img_humidity(humiditymap,xsize,ysize)
    landscapeimage=img_landscape(landscapemap,heightmap,xsize,ysize)
    print("World map generated and images created. Took",round(time.time()-start_time,3),"seconds total.")
    displaytype(1,xsize,ysize)
    button1.config(text="Generate", state="normal")
    disp.update()

def randomseed():
    input1.delete(0,END)
    input1.insert(1,random.randint(100000000000,999999999999))
    
def displaytype(n,xsize,ysize):
    global maptype
    maptype=n
    disp2.delete("all")
    if n==1:
        disp2.create_image(0,0,image=landscapeimage, anchor=NW, state="normal")
    elif n==2:
        disp2.create_image(0,0,image=heightimage, anchor=NW, state="normal")
    elif n==3:
        disp2.create_image(0,0,image=heatimage, anchor=NW, state="normal")
    elif n==4:
        disp2.create_image(0,0,image=humidityimage, anchor=NW, state="normal")

def getorigin(eventorigin):
    global ycoord,xcoord,biomemap,heightmap,heatmap,humiditymap,landscapemap
    ycoord=eventorigin.y
    xcoord=eventorigin.x
    text5.config(text=xcoord)
    text7.config(text=ycoord)
    text8.config(text=landscapemap[ycoord][xcoord])
    text10.config(text=heightmap[ycoord][xcoord])
    text12.config(text=heatmap[ycoord][xcoord])
    text14.config(text=humiditymap[ycoord][xcoord])


disp2.bind("<Button 1>",getorigin)
xcoord=0
ycoord=0
xsize=9
ysize=8
    
input1=Entry(window, bg="white", fg="black", font="none 16", width=12)
input1.insert(1,random.randint(100000000000,999999999999))
input1_disp=disp.create_window(713, 60, anchor=NW, window=input1)

text1=Label(window, text="Seed:", bg="gray20", fg="white", font="none 20 bold", width=6)
text1_disp=disp.create_window(623, 60, anchor=NW, window=text1)

text2=Label(window, text="Display:", bg="gray20", fg="white", font="none 20 bold", width=6)
text2_disp=disp.create_window(623, 130, anchor=NW, window=text2)

text3=Label(window, text="Tile Info:", bg="gray20", fg="white", font="none 20 bold", width=8)
text3_disp=disp.create_window(723, 130, anchor=NW, window=text3)

text4=Label(window, text="x:", bg="gray20", fg="white", font="none 12", width=1)
text4_disp=disp.create_window(723, 165, anchor=NW, window=text4)

text5=Label(window, text="-", bg="gray20", fg="white", font="none 12", width=2)
text5_disp=disp.create_window(737, 165, anchor=NW, window=text5)

text6=Label(window, text="y:", bg="gray20", fg="white", font="none 12", width=1)
text6_disp=disp.create_window(773, 165, anchor=NW, window=text6)

text7=Label(window, text="-", bg="gray20", fg="white", font="none 12", width=2)
text7_disp=disp.create_window(787, 165, anchor=NW, window=text7)

text8=Label(window, text="-", bg="gray20", fg="white", font="none 10", width=18)
text8_disp=disp.create_window(723, 195, anchor=NW, window=text8)

text9=Label(window, text="Height:", bg="gray20", fg="white", font="none 10", width=6)
text9_disp=disp.create_window(723, 216, anchor=NW, window=text9)

text10=Label(window, text="-", bg="gray20", fg="white", font="none 10", width=2)
text10_disp=disp.create_window(771, 216, anchor=NW, window=text10)

text11=Label(window, text="Heat:", bg="gray20", fg="white", font="none 10", width=6)
text11_disp=disp.create_window(723, 237, anchor=NW, window=text11)

text12=Label(window, text="-", bg="gray20", fg="white", font="none 10", width=2)
text12_disp=disp.create_window(771, 237, anchor=NW, window=text12)

text13=Label(window, text="Humidity:", bg="gray20", fg="white", font="none 10", width=6)
text13_disp=disp.create_window(723, 258, anchor=NW, window=text13)

text14=Label(window, text="-", bg="gray20", fg="white", font="none 10", width=2)
text14_disp=disp.create_window(771, 258, anchor=NW, window=text14)


button1=Button(window, text="Generate", font="none 16", width=8, command=generateworldmap)
button1_disp=disp.create_window(623, 95, anchor=NW, window=button1)

button2=Button(window, text="Random Seed", font="none 16", width=10, command=randomseed)
button2_disp=disp.create_window(723, 95, anchor=NW, window=button2)

button3=Button(window, text="Landscape", font="none 16", width=8, command=lambda:displaytype(1,xsize,ysize))
button3_disp=disp.create_window(623, 165, anchor=NW, window=button3)
button4=Button(window, text="Height", font="none 16", width=8, command=lambda:displaytype(2,xsize,ysize))
button4_disp=disp.create_window(623, 190, anchor=NW, window=button4)
button5=Button(window, text="Heat", font="none 16", width=8, command=lambda:displaytype(3,xsize,ysize))
button5_disp=disp.create_window(623, 215, anchor=NW, window=button5)
button6=Button(window, text="Humidity", font="none 16", width=8, command=lambda:displaytype(4,xsize,ysize))
button6_disp=disp.create_window(623, 240, anchor=NW, window=button6)
button7=Button(window, text="Nothing", font="none 16", width=8, command=lambda:displaytype(0,xsize,ysize))
button7_disp=disp.create_window(623, 265, anchor=NW, window=button7)
