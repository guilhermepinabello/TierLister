import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import ImageGrab,ImageTk,Image
from sys import exit
import ctypes
import os

myappid = 'madebypina' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

version = "2.1"
main = tk.Tk("Tierlister")
tiers=["S","A","B","C","D","F","",""]
# default tierColors = [["#2f2938","white"] for i in range(8)]
tierColors = [["#ff7f7e","black"],["#ffbf7f","black"],["#ffdf80","black"],["#feff7f","black"],["#beff7f","black"],["#7eff80","black"],["#7fffff","black"],["#7fbfff","black"],]
title="Tier List"
tierList={}
freshSave = True
freshSave = False
def CreateImageReferences(name):
    imageReference = Image.open(f"images/{name}.png")
    imageReference = imageReference.resize((25,25), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(imageReference)

imageReferences = []
for i in ["openfoldericon","saveicon","uploadicon"]:
    imageReferences.append(CreateImageReferences(i))
windowIcon = tk.PhotoImage(file="TierListerIcon.png")

def SaveListScreenshot():
    x,y = main.winfo_rootx(),main.winfo_rooty()
    box = (x, y, x+ main.winfo_width(), y + main.winfo_height())
    width = 1000
    height = 650
    main.geometry(f"{width}x{height}+100+25")
    screenshot = ImageGrab.grab(bbox=box)
    screenshot.save(f"Tierlists/{title}.png")
    screenshot.show(title=title)

def OpenSavedList():
    global title,tiers,tierList,tierColors
    savedListFolder = os.path.join(os.getcwd(), 'saves')
    listPath = filedialog.askopenfilename(title="Select a Tier List",initialdir=savedListFolder,filetypes=(("Text files", "*.txt"),))

    if listPath:
        file = open(listPath, 'r')
        fileRead = file.readlines()
        if fileRead[0].strip() == "TierLister List":
            tierList = {}
            title = fileRead[1].strip()
            tiers = (fileRead[2].strip()).split("|")
            #tiers = tiers + ["" for i in range(8-len(tiers))]
            tierColors = [i.split("¢") for i in (fileRead[3].strip()).split("|")]
            for n,line in enumerate(fileRead[4:]):
                tier = (line.strip()).split("|")
                if tier == ['']:
                    tierList[tiers[n]] = []
                else:
                    tierList[tiers[n]] = tier.copy()
        file.close()
    
    Clear()                
def SaveListFile():
    global freshSave
    freshSave = True
    listPath = os.path.join(os.getcwd(), 'saves', f'{title}.txt')
    with open(listPath, 'w') as file:
        content = "\n".join([
            "TierLister List",
            title,
            "|".join([i for i in tiers if i.strip() != ""]),
            "|".join([f"{i[0]}¢{i[1]}" for i in tierColors]),
        ] + ["|".join(tierList[i]) for i in tiers]) + "\n"
        file.write(content)

def RaiseWarning(action):
    if not freshSave:
        Question = messagebox.askokcancel(title="Unsaved changes", message="Unsaved changes will be lost. Click OK to continue.")      
        if not Question:
            return
    action()
        
    
def QuitApplication():
    main.destroy()
    exit()

def StartWindow():
    main.title("Tierlister")
    main.resizable(False,False)
    main.config(bg="#1f1b24")
    width = 500
    height = 300
    main.geometry(f"{width}x{height}")

    

    title = tk.Label(main, text="Tierlister", font=("", 40), fg="#ffffff",bg="#1f1b24")
    title.place(relx=0.5,rely=0.125,anchor="center")

    credit = tk.Label(main, text=f"Made by Pina - version {version}", font=("", 10), fg="#ffffff",bg="#1f1b24")
    credit.place(relx=0.5,rely=0.925,anchor="center")

    b1 = tk.Button(main, text="Create New Tierlist",font=("",15),bg="#2f2938",bd=0,fg="white", command=SetupWindow)
    b1.place(relx=0.5,rely=0.4,anchor="center")
    
    b2 = tk.Button(main, text="Open",font=("",15),bg="#2f2938",bd=0,fg="white", command=OpenSavedList)
    b2.place(relx=0.5,rely=0.55,anchor="center")

    b3 = tk.Button(main, text="Quit",font=("",15),bg="#2f2938",bd=0,fg="white", command=QuitApplication)
    b3.place(relx=0.5,rely=0.7,anchor="center")

itemSelect=None
def NewItem():
    global itemSelect, finalVote
    if itemSelect != None and itemSelect.winfo_exists():
        itemSelect.lift()
        return
    itemSelect = tk.Toplevel(main)
    itemSelect.title("Tierlister - New Item")
    itemSelect.resizable(False,False)
    itemSelect.iconphoto(False,windowIcon)
    width = 500
    height = 315
    itemSelect.geometry(f"{width}x{height}")

    def CheckValidExit(*args):
        itemString = e1.get("1.0", "end-1c")   
        if len(itemString) > 100:
            e1.delete("1.0", tk.END)
            e1.insert("1.0", itemString[:100])
            itemString = e1.get("1.0", "end-1c")  
        l2.config(text=f"Char:{len(itemString)}/100")
        if (itemString).strip() == "" or finalVote == None:
            b1["state"] = "disabled"
        else:
            b1["state"] = "normal"
    votes = []
    finalVote = None
    def AddVote(vote):
        global finalVote
        votes.append(vote)
        
        finalVote = int(int(sum(votes)/len(votes)+0.49))

        voteCounters[vote].config(text=str(int(voteCounters[vote]["text"])+1))
 
        l3.config(text=f"Final Vote: {tiers[finalVote]}")
        delb["state"] = "normal"
        #print("ADD",sum(votes),len(votes),votes,finalVote)
        CheckValidExit()

    def ClearVotes():
        global finalVote
        finalVote = None
        votes.clear()
        for i in voteCounters:
            i.config(text="0")
        l3.config(text="Final Vote: Not Selected")
        delb["state"] = "disabled"
        #print("CLEAR",sum(votes),len(votes),votes,finalVote)
    
    def QuitNewItem():
        global freshSave
        freshSave = False
        tierList[tiers[finalVote]].append(e1.get("1.0", "end-1c"))
        Clear()
    fl = tk.Frame(itemSelect, bg="#1f1b24", height=height,width=width/2, highlightbackground="#2f2938",highlightthickness=3)
    fr = tk.Frame(itemSelect, bg="#1f1b24", height=height,width=width/2, highlightbackground="#2f2938",highlightthickness=3)
    
    fl.grid_propagate(False)
    fr.grid_propagate(False)

    fl.grid(row=0, column=0, sticky="W")
    fr.grid(row=0, column=1, sticky="W")
    
    l1 = tk.Label(fl, text = "Item Name:", font=("", 10), fg="#ffffff",bg="#1f1b24")
    l1.place(x=20,y=10)

    l2 = tk.Label(fl, text = "Char: 0/100", font=("", 7), fg="#ffffff",bg="#1f1b24")
    l2.place(x=25,y=130)

    l3 = tk.Label(fl, text = "Final Vote: Not Selected", font=("", 10), fg="#ffffff",bg="#1f1b24")
    l3.place(relx=0.5,y=175,anchor="center")

    b1 = tk.Button(fl, text="Create New",bg="#2f2938",bd=0,fg="white",command=QuitNewItem, state="disabled")
    b1.place(relx=0.5,rely=0.9,anchor="center")

    delb = tk.Button(fl, text="Clear Votes",bg="#2f2938",bd=0,fg="white",command=ClearVotes, state="disabled")
    delb.place(relx=0.5,rely=0.7,anchor="center")
    
    e1 = tk.Text(fl,bg="#2f2938",bd=1,fg="white",wrap="word")
    e1.place(relx=0.5,rely=0.125,anchor="n",relheight=0.3,relwidth=0.8)
    e1.bind("<KeyPress>", CheckValidExit)
    e1.bind("<KeyRelease>", CheckValidExit)

    
        
    selectTierButtons=[]
    voteCounters=[]
    for n,i in enumerate(tiers):       
        selectTierButtons.append(tk.Button(fr, text = i, font=("", 10), fg=tierColors[n][1],bg=tierColors[n][0],command=lambda m=n: AddVote(m)))
        voteCounters.append(tk.Label(fr, text = "0", font=("", 8), fg="#ffffff",bg="#1f1b24"))
        selectTierButtons[n].grid(row = n, column = 0, sticky = "W", pady = 5, padx=10)
        voteCounters[n].grid(row = n, column = 1, sticky = "W", pady = 5, padx=10)
    

    

   
def TierListWindow():
    main.title("Tierlister")
    main.resizable(False,False)
    width = 1000
    height = 650
    main.geometry(f"{width}x{height}+100+50")

    head = tk.Frame(main, bg="#1f1b24", height=75, highlightbackground="#797979",highlightthickness=3)
    head.pack_propagate(False)
    head.place(relwidth=1,relheight=3/26)

    if len(title)>20:
        titleSize = 20
    else:
        titleSize = 30
    headText = tk.Label(head, text = title, font=("", titleSize), fg="#ffffff",bg="#1f1b24",width=75)
    headText.pack(anchor="center",pady=15)

    table = tk.Frame(main, bg="#1f1b24")
    table.grid_propagate(False)
    table.place(rely=3/26,relwidth=1,relheight=23/26)

    newButton = tk.Button(head, text="New List",font=("",15),bg="#2f2938",bd=0,fg="white",wraplength=165, command=lambda: RaiseWarning(SetupWindow))
    newButton.place(rely=0.5,relx=0.94,anchor="center")

    itemButton = tk.Button(head, text="+ New Item",font=("",15),bg="#2f2938",bd=0,fg="white",wraplength=165, command=NewItem)
    itemButton.place(rely=0.5,relx=0.83,anchor="center")

    saveButton = tk.Button(head, image=imageReferences[2],font=("",15),bg="#2f2938",bd=0,fg="white",wraplength=165, command=lambda: main.after(1,SaveListScreenshot),width=40,height=40)
    saveButton.place(rely=0.5,relx=0.035,anchor="center")

    saveFileButton = tk.Button(head, image=imageReferences[1],font=("",15),bg="#2f2938",bd=0,fg="white",wraplength=165, command=SaveListFile,width=40,height=40)
    saveFileButton.place(rely=0.5,relx=0.085,anchor="center")

    loadFileButton = tk.Button(head, image=imageReferences[0],font=("",15),bg="#2f2938",bd=0,fg="white",wraplength=165, command=lambda: RaiseWarning(OpenSavedList),width=40,height=40)
    loadFileButton.place(rely=0.5,relx=0.135,anchor="center")

    
    tierNameFrames=[]
    tierItemsFrames=[]

    for n,i in enumerate(tiers):
        if len(i) <= 5:
            tierFontSize = 30
        else:
            tierFontSize = 15
        
        tierNameFrames.append(tk.Frame(table, bg="#1f1b24", height=(height-75)/len(tiers),width=180,highlightbackground="#797979",highlightthickness=2))
        tierNameFrames[n].grid(row=n, column=0, sticky="W")
        tk.Label(tierNameFrames[n], text=i,font=("",tierFontSize),bg=tierColors[n][0],bd=0,fg=tierColors[n][1],wraplength=165).place(relheight=1,relwidth=1)
        tierItemsFrames.append(tk.Frame(table, bg="#1f1b24", height=(height-75)/len(tiers),highlightbackground="#797979",highlightthickness=2,width=width-180))     
        tierItemsFrames[n].grid_propagate(False)
        tierItemsFrames[n].grid(row=n, column=1, sticky="W")
        
        
    

    def DeleteItem(item,tier):
        global freshSave
        freshSave = False
        tierList[tier].pop(item)
        Clear()
    for n1,i1 in enumerate(tiers):  
        for n2,i2 in enumerate(tierList[i1]):
            itemFrame = tk.Frame(tierItemsFrames[n1], bg="#1f1b24", height=(height-75)/len(tiers),width=(width-180)//len(tierList[i1]),highlightbackground="#797979",highlightthickness=0)
            itemFrame.grid(row=0, column=n2, sticky="W")
            #print(i2)
            itemFontSize = int(22 - (2.34*len(i2)/100)*len(tierList[i1]))
            if itemFontSize < 8:
                itemFontSize = 8
            '''itemText = tk.Text(itemFrame,bg=tierColors[n1][0],bd=1,fg=tierColors[n1][1],font=("",itemFontSize),relief="sunken",wrap="word",)
            itemText.tag_configure("center",justify=tk.CENTER)
            itemText.insert("1.0", i2, "center")
            itemText.config(state="disabled")'''
            itemText = tk.Label(itemFrame,bg=tierColors[n1][0],bd=1,fg=tierColors[n1][1],font=("",itemFontSize),relief="sunken", text=i2,wraplength=(width-180)//len(tierList[i1])-8)
            itemText.place(relx=0.5,rely=0.5,relheight=1,relwidth=1,anchor="center")           
            tk.Button(itemFrame, text="X",font=("",7),bg="#1f1b24",bd=1,fg="white", command=lambda item=n2,tier=i1: DeleteItem(item,tier)).place(relx=1,rely=0,anchor="ne") 

    
    #main.after(1000, SaveListScreenshot)

def Clear(refresh=TierListWindow):
    for widget in main.winfo_children():
        widget.destroy()
    refresh()

def SetupWindow():
    main.title("Tierlister - Setup")
    main.resizable(False,False)
    width = 500
    height = 300
    main.geometry(f"{width}x{height}")

    def QuitSetup():
        global title, tierList
        title = title_Var.get()
        for i in tiers:
            tierList[i] = []
        Clear()
        

    def CheckValidExit(*args):
        global tiers
        gapTiers = [tiersList[i].get() for i in range(8)]
        fullTiers = [i for i in gapTiers if i.strip() != ""]
        takeOutTiers = gapTiers[0:len(fullTiers)]

        if "" in takeOutTiers or len(fullTiers) <2 or (title_Var.get().strip()) == "":
            b1["state"] = "disabled"

        else:
            tiers = fullTiers.copy()
            b1["state"] = "normal"
        
    def ChooseColor(tierIndex):
    
        colorCode = colorchooser.askcolor(title="TierLister - Choose Tier Color",initialcolor=tierColors[tierIndex][0])
        
        if colorCode[1]:
            colorCodeRGB = colorCode[0]
            brightness = (0.3*colorCodeRGB[0] + 0.587*colorCodeRGB[1] + 0.114*colorCodeRGB[2])/255
            if brightness > 0.5:
                textColor = "black" #"#797979"
            else:
                textColor = "white"
            tierColors[tierIndex][0] = colorCode[1]
            tierColors[tierIndex][1] = textColor
            Clear(SetupWindow)

    fl = tk.Frame(main, bg="#1f1b24", height=height,width=width/2, highlightbackground="#2f2938",highlightthickness=3)
    fr = tk.Frame(main, bg="#1f1b24", height=height,width=width/2, highlightbackground="#2f2938",highlightthickness=3)
    
    fl.grid_propagate(False)
    fr.grid_propagate(False)

    fl.grid(row=0, column=0, sticky="W")
    fr.grid(row=0, column=1, sticky="W")
    
    l1 = tk.Label(fl, text = "List title:", font=("", 10), fg="#ffffff",bg="#1f1b24")
    l1.grid(row = 0, column = 0, sticky = "W", pady = 5, padx=10)

    title_Var = tk.StringVar()
    
    e1 = tk.Entry(fl,bg="#2f2938",bd=0,fg="white",textvariable=title_Var)
    e1.insert(0,"Tier List")

    e1.grid(row = 0, column = 1, sticky = "W", pady = 5, padx=0)
    title_Var.trace("w", CheckValidExit)

    b1 = tk.Button(fl, text="Create New",bg="#2f2938",bd=0,fg="white", command=QuitSetup)

    b1.grid(row = 1, column = 1, sticky = "N", pady = 225, padx=0)

    tiersList = [tk.StringVar(value=x) for x in tiers]
    for i in range(8-len(tiersList)):
        tiersList.append(tk.StringVar(value=""))
    for n,i in enumerate(tiersList):       
        tk.Label(fr, text = f"Tier {n+1}", font=("", 10), fg="#ffffff",bg="#1f1b24").grid(row = n, column = 0, sticky = "W", pady = 5, padx=10)
        tk.Entry(fr,bg="#2f2938",bd=0,fg="white",textvariable=i).grid(row = n, column = 1, sticky = "W", pady = 5, padx=10)
        tk.Button(fr,bg=tierColors[n][0],bd=1,highlightcolor="#797979",height=1,width=1, command=lambda N=n:ChooseColor(N)).grid(row = n, column = 2, sticky = "W", pady = 5, padx=10)
        i.trace("w", CheckValidExit)
    CheckValidExit()
StartWindow()
#SetupWindow()
#TierListWindow()

main.iconphoto(False,windowIcon)
main.mainloop()
