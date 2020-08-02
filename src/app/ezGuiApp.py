try:
    import clr
    clr.AddReference("PresentationFramework")
    clr.AddReference("PresentationCore");
    import ezPyWpfLib as ez    
except:
    import ezPyJFxLib as ez

def onExit(event):
    System.Windows.Application.Current.Shutdown();
def onAbout(event):
    ez.AlertDialog("Hello, world!", "My App");
def printText(text):
    ctrl = ez.GetControl('textarea')
    if ctrl:
        ctrl.AppendText(text + '\n')
        ctrl.ScrollToEnd()
def onChoice(event):
    ctrl = ez.GetControl('choice')
    if ctrl: printText("Selected: " + ctrl.GetSelectedItem() + "\n")
def onCheck(event):
    ctrl = ez.GetControl('check')
    if ctrl: printText("Checked: " + ctrl.GetValue().ToString() + "\n")
def onListBox(event):
    ctrl = ez.GetControl('listbox')
    if ctrl: printText("List Selected: " + ctrl.GetValue() + "\n")
def onListView(event): #event
    ctrl = ez.GetControl('listbox')
    listview = ez.GetControl('table')
    #row = listview.GetValue()
    #printText(row['col1'] + "," + row['col2'])
    rows = listview.GetSelectedItems()
    for row in rows:
        printText(row[0] + "," + row[1])
        
def onBrowse(event):
    ctrl = ez.GetControl('textfile')
    files = ez.FileOpenDialog()
    if files: ctrl.SetValue(files[0])
def onBrowseFolder(event):
    ctrl = ez.GetControl('textfile')
    folder = ez.DirectoryOpenDialog()
    if folder: ctrl.SetValue(folder)
def onToggle(event):
    ctrl = ez.GetControl('toggle')
    if ctrl: printText('Toggle: ' + str(ctrl.IsSelected()))
def onDatePicker(event):
    ctrl = ez.GetControl('datepicker')
    if ctrl: printText('Date: ' + str(ctrl.GetValue()))
def onSlider(event):
    ctrl = ez.GetControl('slider')
    if ctrl: printText('Slider: ' + str(ctrl.GetValue()))
def onTreeView(event):
    ctrl = ez.GetControl('tree')
    if ctrl: printText('Treeview: ' + str(ctrl.GetSelectedItemPath('/')))
def onRun(event):
    text = ez.GetControl('textfile')
    print(text.GetValue())
    if text:
        rv, out = ez.Execute(text.GetValue())
        textarea = ez.GetControl('textarea')
        textarea.SetValue(str(rv) + '\n' + out)

progress_value = 0

def threadHandler():
    import time
    label = ez.GetControl('status')
    prog = ez.GetControl('progress')    
    for i in range(100):
        ez.RunLater(label.ctrl, lambda : label.SetValue(str(i)))
        ez.RunLater(prog.ctrl, lambda : prog.SetValue(i))
        time.sleep(0.1)

def onFileDrop(files):
    print('onFileDrop',files)
    ctrl = ez.GetControl('textfile')
    ctrl.SetValue(files[0])

def onTableDrop(files):
    print('onFileDrop',files)
    ctrl = ez.GetControl('textfile')
    ctrl.SetValue(files[0])
    
def onCreated():
    ez.DumpControlTable()
    #SetFileDropHandler(GetControl('textfile').ctrl,onFileDrop)
    listview = ez.GetControl('table')
    listview.AddRow( [ "Anny" , "18" ] )
    listview.AddRow( [ "Bobby", "16" ] )
    listview.AddRow( [ "Candy", "14" ] )
    tree = ez.GetControl('tree')
    item = tree.AddRootItem("Item1")
    tree.AddItem("Item1-1",item)
    tree.AddItem("Item1-2",item)
    item = tree.AddRootItem("Item2")
    tree.AddItem("Item2-1",item)
    tree.AddItem("Item2-2",item)
    #ez.StartTimer(timerHandler,1000)
    ez.StartThread(threadHandler)
    #ez.StartTask(taskHandler)

def onClosing(event):
    if not ez.YesNoDialog("Do you want to quie ?","Quit"):
        event.args.Cancel = True

def onOK(event):
    win = MakeWindow()
    win.Popup()
    
app_mainmenu = [
    { 'name' : "File",
      'item' : [
            { 'name' : "Exit" , 'item' : onExit, 'image' : 'icon/exit.png', 'tooltip' : 'Exit Program' },
            { 'name' : "-" ,  },
            { 'name' : "About" , 'item' : onAbout, 'image' : 'exit.png' } ]
    }, { 'name' : "Help",
      'item' : [
            { 'name' : "About", 'item' : onAbout, 'check' : True, 'image' : 'new.png' } ]
    }]
app_tool = [[
        { "name" : "Button", "label" : "Click", "image" : "./icon/exit.png", 'size' : 16  },
    ],[
        { "name" : "ChoiceBox", "items" : [ "apple", "grape" ], 'key' : 'choicetool', 'handler' : onChoice },
        { "name" : "ComboBox", "items" : [ "apple", "grape" ] },
        { "name" : "Label", "label" : "Address:", "menu" : app_mainmenu },
        { "name" : "TextField", "key" : "textfile", 'width' : 40 },
        { "name" : "Button", 'handler' : onBrowse, "label" : "Browse", "tooltip" : "About this program" },
        { "name" : "ToggleButton", "label" : "Toggle", 'key' : 'toggle', 'handler' : onToggle },
    ]]
    
app_status = [
        { "name" : "ProgressBar", 'key' : 'progress' },
        { "name" : "Slider", 'key' : 'slider', 'handler' : onSlider },
        { "name" : "Label", "label" : "Ready", 'key' : 'status' },
        { "name" : "Button", "label" : "Click" },
        { "name" : "Spacer" },
    ]
    
tab1 = [[ { "name" : "WebView", "key" : "webview", "expand" : True, "toolbar" : True, "uri" : "http://google.co.kr" },
        { 'expand' : True } ]]
tab2 = [[ { "name" : "ListBox", "items" : [ "apple", "grape" ], 'expand' : True, 'key' : 'listbox', 'handler' : onListBox },
        { 'expand' : True } ]]
tab3 = [[ { "name" : "TableView", "columns" : [ "Name", "Age" ], 'widths' : [ 100, 200 ], 'expand' : True, 'key' : 'table', 'handler' : onListView, 'menu' : app_mainmenu, 'drop' : onTableDrop },
        { 'expand' : True } ]]
tab4 = [[ { "name" : "TreeView", "key" : "tree", 'handler' : onTreeView,"expand" : True },
          { "expand" : True }, ]]
tab5 = [[ { "name" : "ImageView", 'file' : "./Lenna.png", "stretch" : "uniform", "scroll" : True, "expand" : True, 'bindwidth' : True, 'bindheight' : True,  },
          { "expand" : True }, ]]
split1 = [[
        { "name" : "TabPane", "labels" : [ "Web", "List", "Table", "Tree", "Image" ], "items" : [ tab1, tab2, tab3, tab4, tab5 ], "expand" : True },
        { "expand" : True }, ]]
split2 = [[ { "name" : "TextArea", 'key' : 'textarea', "expand" : True, 'toolbar' : True },
            { "expand" : True }, ]]

app_content = [ # vbox
    [ # hbox
        { "name" : "GroupBox" , 'label': "Tool2", 'item' : [[
            { "name" : "Label", "label" : "Address:", "menu" : app_mainmenu },
            { "name" : "TextField", "key" : "textfile", "expand" : True, "menu" : app_mainmenu },
            { "name" : "Button", 'handler' : onBrowse, "label" : "File", "tooltip" : "About this program" },
            { "name" : "Button", 'handler' : onBrowseFolder, "label" : "Folder", "tooltip" : "About this program" },
            { "name" : "Button", 'handler' : onRun, "label" : "Run", "tooltip" : "Execute Command" },
        ]], 'expand' : True }
    ],
    [ # hbox
        { "name" : "ChoiceBox", "items" : [ "apple", "grape" ], 'key' : 'choice', 'handler' : onChoice },
        { "name" : "ComboBox", "items" : [ "apple", "grape" ] },
        { "name" : "CheckBox", "label" : "Click Me", 'key' : 'check', 'handler' : onCheck },
        { "name" : "ToggleButton", "label" : "Toggle", 'key' : 'toggle', 'handler' : onToggle },
        { "name" : "DatePicker", "label" : "Toggle", 'key' : 'datepicker', 'handler' : onDatePicker },
        { "name" : "Spacer",  },
        { 'group' : "Tools" },
    ],     
    [ # hbox
        { "name" : "HSplit", "items" : [ split1, split2 ] , "first" : 0.5, "expand" : True, 'border' : False},
        { "expand" : True, 'border' : True  },
    ],     
    [ # hbox
        { "name" : "Spacer",  },
        { "name" : "Button", "label" : "OK", 'width' : 64, 'height' : 24, 'handler' : onOK },
    ],     
]

def MakeWindow():
    win = ez.Window()
    win.SetTitle("ezGuiApp")
    win.SetIcon("./Lenna.png")
    win.SetSize(640,400)
    win.SetMenuBar(app_mainmenu)
    win.SetToolBar(app_tool)
    win.SetStatusBar(app_status)
    win.SetContent(app_content)
    win.SetCreatedHandler(onCreated)  
    win.SetCloseHandler(onClosing)
    win.SetFileDropHandler(onFileDrop)
    return win

if __name__ == "__main__":
    global appWin
    appWin = MakeWindow()
    appWin.Run()

