import os
try:
    import ezPyWpfLib as ez    
except:
    import ezPyJFxLib as ez

def refreshTree(basedir="webtoon"):
    tree = ez.GetControl('tree')
    dirs = os.listdir(basedir)
    for d in dirs:
        dpath = os.path.join(basedir,d)
        if not os.path.isdir(dpath):
            continue
        item = tree.AddRootItem(d)
        files = os.listdir(dpath)
        for f in files:
            fpath = os.path.join(dpath,f)
            if os.path.isfile(fpath):
                tree.AddItem(f,item)
    
def onTreeView(event):
    tree = ez.GetControl('tree')
    path = tree.GetSelectedItemPath()   
    if os.path.isfile(path):
        with open(path) as f:
            web = ez.GetControl('web')
            web.Load(f.read())

def onCreated():
    ez.DumpControlTable()
    refreshTree()

def onClosing(event):
    if not ez.YesNoDialog("Do you want to quie ?","Quit"):
        event.args.Cancel = True

split1 = [[ { "name" : "TreeView", "label" : "WebToon", "key" : "tree", 'handler' : onTreeView,"expand" : True },
          { "expand" : True }, ]]
split2 = [[ { "name" : "WebView", "key" : "web", "expand" : True, "toolbar" : False, "uri" : "http://google.co.kr" },   
        { "expand" : True }, ]]

app_content = [ # vbox  
    [ # hbox
        { "name" : "HSplit", "items" : [ split1, split2 ] , "first" : 0.2, "expand" : True, 'border' : False},
        { "expand" : True, 'border' : True  },
    ],          
]

def MakeWindow():
    win = ez.Window()
    win.SetTitle("WebToon Viewer")
    #win.SetIcon("./Lenna.png")
    win.SetSize(640,400)
    win.SetContent(app_content)
    win.SetCreatedHandler(onCreated)  
    win.SetCloseHandler(onClosing)
    return win

if __name__ == "__main__":
    global appWin
    appWin = MakeWindow()
    appWin.Run()

