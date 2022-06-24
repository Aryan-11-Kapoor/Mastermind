#-------------------------------------  Tkinter module for gui model of game--------------------------------------------------------------------

import tkinter
import random
import time

root=tkinter.Tk()

frame=tkinter.Frame(root)
canvas=tkinter.Canvas(frame, width=400, height= 600, highlightthickness=0, highlightbackground="black", relief=tkinter.FLAT, bg='#aaaaff', bd=0)

colors=['white','green','red','maroon1','gold','dark orange','blue']
position=0
speed=2

#-----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------- User defined function required for implementation of game--------------------------------------------------

def useraction():                                      #Function to select colors and position at start of game
    canvas.bind('<Right>',lambda _: selectpos(1))
    canvas.bind('<Left>',lambda _: selectpos(-1))
    canvas.bind('<Up>',lambda _:switchcolor(1))
    canvas.bind('<Down>',lambda _:switchcolor(-1))
    canvas.bind('<Return>',lambda _:switchrow())
    canvas.unbind('<space>')

def userinaction():                                    #Function to avoid call of function id
    canvas.unbind("<Right>")
    canvas.unbind("<Left>")
    canvas.unbind("<Up>")
    canvas.unbind("<Down>")
    canvas.unbind("<Return>")

def createcode():                                      #Function to generate secret code
    select=[x for x in range(len(colors))]
    code=[]
    for i in range(codelength):
        codeindex=random.randint(0,len(select)-1)
        code.append(select[codeindex])
        select.pop(codeindex)
    return code

def initiaterow():                                     #Function to select colors in a row
    global selectcolors,top,bottom
    selectcolors=[x for x in range(len(colors))]
    top=0
    bottom=0

def initiategame():                                    #Function to check response with secret code that is game starts!!
    global row,pos,pickcolor,codedcolor
    canvas.itemconfig(board[row][pos],width=0)
    for i in range(guesses):
        for j in range(codelength):
            canvas.itemconfig(board[i][j],fill='#8888dd')
            if i < guesses-1:
                canvas.itemconfig(response[i][j],fill='#8888dd')
    pickcolor=[[-1 for i in range(codelength)] for j in range(guesses)]
    row=0
    pos=0
    canvas.itemconfig(board[row][pos],width=1)
    useraction()
    codedcolor=createcode()
    initiaterow()

def select(colorposition):                            #Function to show colors available for selection
    canvas.itemconfig(colorposition, width=4)

def deselect(colorposition):                          #Function to deselect a color
    canvas.itemconfig(colorposition,width=0)

def setcolor(colorposition,color):                    #Function to fill selected color
    canvas.itemconfig(colorposition,fill=color)

def selectpos(increment):                             #Function to select position
    global pos
    canvas.itemconfig(board[row][pos],width=0)
    pos+=increment
    if pos<0:
        pos=codelength-1
    if pos>=codelength:
        pos=0
    canvas.itemconfig(board[row][pos],width=1)

def switchcolor(increment):                           #Function to switch through different available colours
    pickcolor[row][pos]+=increment
    if pickcolor[row][pos] > len(colors)-1:
        pickcolor[row][pos]=0
    if pickcolor[row][pos] < 0:
        pickcolor[row][pos]=len(colors)-1
    canvas.itemconfig(board[row][pos],fill=colors[pickcolor[row][pos]])

def switchrow():                                      #Function to switch to next row
    global row, top, bottom, pickcolor
    for i in range(codelength):
        if pickcolor[row][i]==-1:
            print("Colors are not set {},{}:".format(row,i))
            return False
        for j in range(codelength):
            if(j==i and codedcolor[j]==pickcolor[row][i]):
                top+=1
            if(j!=i and codedcolor[j]==pickcolor[row][i]):
                bottom+=1
    if top<codelength and row<guesses-2:
        print("top:{}, bottom:{}".format(top,bottom))
        for i in range(top):
            canvas.itemconfig(response[row][i],fill="black")
        for i in range(bottom):
            canvas.itemconfig(response[row][i+top],fill="white")
        canvas.itemconfig(board[row][pos],width=0)
        row+=1
        canvas.itemconfig(board[row][pos],width=1)
        initiaterow()
        return False
    else:
        print("Row{} top{} and bottom{}".format(row,top,bottom))
        output=True
        if row==guesses-2:
            output=False
        for i in range(top):
            canvas.itemconfig(response[row][i],fill="black")
        for i in range(bottom):
            canvas.itemconfig(response[row][i+top],fill="white")
        for i in range(codelength):
            canvas.itemconfig(board[guesses-1][i],fill=colors[codedcolor[i]])
        userinaction()
        canvas.bind("<space>",lambda _:intitiategame())
        return output

#-----------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------- Main Program ------------------------------------------------------------------------------------

print("Instructions to play the game: ")
print("1. Use up and down arrow keys to navigate through different colors.")
print("2. Use right and left arrow keys to navigate through different positions of a row.")
print("3. Use enter key to submit a response of one row.")
print("\n")
print("Clues given:")
print("1. Black color at the right row next to given response indicates there is a correct color at a correct position.")
print("2. White color at the right row next to given response indicates there is a correct color but not at correct position.")
print("\n")
print("Be cautious as to fill all colors in a row before submitting a response.")

guesses=9
codelength=4
colorsize=40
colorpadding=50

row=0
pos=0
selectColors=[]
pickcolor=[[-1 for i in range(codelength)]for j in range(guesses)]

codedcolor=createcode()

board=[]
response=[]
for i in range(guesses):
    newrow=[]
    newresponse=[]
    for j in range(codelength):
        x=colorpadding*j+5
        y=600-colorpadding*i-colorsize-5
        newrow.append(canvas.create_oval(x,y,x+colorsize,y+colorsize,fill='#8888dd',outline='black',width=0))
        if i<guesses-1:
            x=colorpadding/2*j+255
            y+=colorsize/8
            newresponse.append(canvas.create_oval(x+colorsize/4,y+colorsize/4,x+colorsize/2,y+colorsize/2,fill='#8888dd',outline='black',width=0))
    board.append(newrow)
    if i<guesses-1:
        response.append(newresponse)
initiategame()
canvas.itemconfig(board[row][pos],width=1)

frame.pack()
canvas.pack()
root.title("Mastermind Game")

canvas.focus_set()
useraction()
canvas.bind("<space>",lambda _:initiategame())

root.mainloop()

#-----------------------------------------------------------------------------------------------------------------------------------------------
#Reference:
#Here #aaaaff refers to pale blue color
#Here #8888dd refers to magenta blue color. These are hexadecimal codes of respective colors.