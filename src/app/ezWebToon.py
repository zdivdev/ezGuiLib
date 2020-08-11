import os
import zipfile
try:
    import ezPyWpfLib as ez    
except:
    import ezPyJFxLib as ez
'''
import clr
clr.AddReferenceToFileAndPath("ezPyWpfLib.dll")
import ezPyWpfLib as ez
'''

def refreshTree(basedir="webtoon"):
    tree = ez.GetControl('tree')
    dirs = os.listdir(basedir)
    for d in dirs:
        dpath = os.path.join(basedir,d)
        if os.path.isdir(dpath):
            item = tree.AddRootItem(d)
            files = os.listdir(dpath)
            for f in files:
                fpath = os.path.join(dpath,f)
                if os.path.isfile(fpath):
                    tree.AddItem(f,item)  
        elif zipfile.is_zipfile(dpath):
            item = tree.AddRootItem(d)
            with zipfile.ZipFile(dpath) as zf:
                for info in zf.infolist():
                    if not info.filename.endswith('/'):
                        #tree.AddItem(f,item)
                        tree.AddItem(info.filename.decode("cp949"),item)

def onTreeView(event):
    tree = ez.GetControl('tree')
    if tree.IsRootItem(tree.GetSelectedItem()):
        return
    path = tree.GetItemPath(tree.GetParentItem(tree.GetSelectedItem()))    
    if path and zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            with zf.open(tree.GetSelectedItemText().encode("cp949")) as f:
                web = ez.GetControl('web')
                web.Load(f.read())
    else:
        path = tree.GetSelectedItemPath()   
        if os.path.isfile(path) and path.endswith("html"):
            with open(path) as f:
                web = ez.GetControl('web')
                web.Load(f.read())   

def onCreated():
    ez.DumpControlTable()
    refreshTree()

def onClosing(event):
    if not ez.YesNoDialog("Do you want to quie ?","Quit"):
        event.args.Cancel = True

split1 = [[ { "name" : "TreeView", "label" : "WebToon", "key" : "tree", 'handler' : onTreeView, 'fontsize':14, "expand" : True },
          { "expand" : True }, ]]
split2 = [[ { "name" : "WebView", "key" : "web", "expand" : True, "toolbar" : False, "uri" : "http://google.co.kr" },   
        { "expand" : True }, ]]

app_content = [ # vbox  
    [ # hbox
        { "name" : "HSplit", "items" : [ split1, split2 ] , "first" : 0.4, "expand" : True, 'border' : False},
        { "expand" : True, 'border' : True  },
    ],          
]

def MakeWindow():
    win = ez.Window()
    win.SetTitle("WebToon Viewer")
    win.SetSize(640,400)
    win.SetContent(app_content)
    win.SetCreatedHandler(onCreated)  
    win.SetCloseHandler(onClosing)
    return win

if __name__ == "__main__":
    global appWin
    appWin = MakeWindow()
    appWin.Run()

