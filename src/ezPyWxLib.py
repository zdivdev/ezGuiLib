import wx

'''
wxART_ERROR
wxART_QUESTION
wxART_WARNING
wxART_INFORMATION
wxART_ADD_BOOKMARK
wxART_DEL_BOOKMARK
wxART_HELP_SIDE_PANEL
wxART_HELP_SETTINGS
wxART_HELP_BOOK
wxART_HELP_FOLDER
wxART_HELP_PAGE
wxART_GO_BACK
wxART_GO_FORWARD
wxART_GO_UP
wxART_GO_DOWN
wxART_GO_TO_PARENT
wxART_GO_HOME
wxART_GOTO_FIRST (since 2.9.2)
wxART_GOTO_LAST (since 2.9.2)
wxART_PRINT
wxART_HELP
wxART_TIP
wxART_REPORT_VIEW
wxART_LIST_VIEW
wxART_NEW_DIR
wxART_FOLDER
wxART_FOLDER_OPEN
wxART_GO_DIR_UP
wxART_EXECUTABLE_FILE
wxART_NORMAL_FILE
wxART_TICK_MARK
wxART_CROSS_MARK
wxART_MISSING_IMAGE
wxART_NEW
wxART_FILE_OPEN
wxART_FILE_SAVE
wxART_FILE_SAVE_AS
wxART_DELETE
wxART_COPY
wxART_CUT
wxART_PASTE
wxART_UNDO
wxART_REDO
wxART_PLUS (since 2.9.2)
wxART_MINUS (since 2.9.2)
wxART_CLOSE
wxART_QUIT
wxART_FIND
wxART_FIND_AND_REPLACE
wxART_FULL_SCREEN (since 3.1.0)
wxART_EDIT (since 3.1.0)
wxART_HARDDISK
wxART_FLOPPY
wxART_CDROM
wxART_REMOVABLE
'''

ID_START = 1000
_window__ctrl_table = {}

#
# Common Function
#

def getId():
    global ID_START
    ID_START += 1
    return ID_START

def registerCtrl(name,ctrl):
    _window__ctrl_table[name] = ctrl

def GetControl(name):
    return _window__ctrl_table.get(name)

def GetNativeControl(name):
    if _window__ctrl_table.get(name): 
        return _window__ctrl_table[name].ctrl;
        
def encodeIcon(filename):
    from zlib import compress
    from base64 import b64encode
    with open(filename, "rb") as f:
        return b64encode(compress(f.read()))

def encodeIconToStr(filename):
    return encodeIcon(filename).decode('utf-8')
    
def decodeIcon(data):
    from base64 import b64decode
    from zlib import decompress
    return decompress(b64decode(data))

def getBitmap(data):
    from io import BytesIO
    stream = BytesIO(bytearray(decodeIcon(data))) # just bytes() for py3
    return wx.Bitmap(wx.Image(stream, wx.BITMAP_TYPE_ANY)) 

def getMenuBitmap(data, size=(16,16)):
    if data[0] == b'w'[0] and data[1] == b'x'[0]:
        return wx.ArtProvider.GetBitmap(data, wx.ART_MENU, size)
    else:
        return getBitmap(data)

def getToolbarBitmap(data, size=(32,32)):
    if data[0] == b'w'[0] and data[1] == b'x'[0]:
        return wx.ArtProvider.GetBitmap(data, wx.ART_TOOLBAR, size)
    else:
        return getBitmap(data)

def getButtonBitmap(data, size=(16,16)):
    if data[0] == b'w'[0] and data[1] == b'x'[0]:
        return wx.ArtProvider.GetBitmap(data, wx.ART_BUTTON, size)
    else:
        return getBitmap(data)

def wrapSizer(widget):
    sizer = wx.BoxSizer()
    sizer.Add( widget, 1, wx.EXPAND, 0 )
    sizer.Fit( widget )
    return sizer
            
#
# Controls
#


class WxVBox():
    def __init__(self,parent=None,label=None,orient=wx.VERTICAL,proportion=0):
        if label is None: self.ctrl = wx.BoxSizer( orient )
        else: self.ctrl = wx.StaticBoxSizer( wx.StaticBox( parent, wx.ID_ANY, label ), orient )
    def addItem(self,child,proportion=0,expand=True,border=5,align=0):
        flags = align
        flags |= wx.EXPAND if expand == True else 0
        flags |= wx.ALL if border > 0 else 0
        self.ctrl.Add( child, proportion, flags, border )
    def addSpacer(self,proportion=1):
        self.ctrl.Add( ( 0, 0), proportion, wx.EXPAND|wx.ALL, 5 )

class WxHBox(WxVBox):
    def __init__(self,parent=None,label=None,orient=wx.HORIZONTAL,proportion=0):
        super().__init__(parent,label,orient,proportion)

class WxControl():
    def DefaultAction(self,h):
        if h.get('tooltip'): self.ctrl.SetToolTip(wx.ToolTip(h.get('tooltip')))
        if h.get('key'): registerCtrl( h.get('key'), self )    
    def getLabel(self): #button
        return self.ctrl.GetLabel()
    def setLabel(self,value): #button
        self.ctrl.SetLabel(value)
    def getValue(self):
        return self.ctrl.GetValue()
    def setValue(self,value):
        self.ctrl.SetValue(value)
    def clearValue(self):
        self.ctrl.SetValue('')
    def appendValue(self,value):
        self.ctrl.Append(value)
    def deleteValue(self,value):
        if type(value) is str:
            n = self.ctrl.FindString(value)
            if n != wx.NOT_FOUND:
                self.ctrl.Delete(n)
        elif type(value) is int:
                self.ctrl.Delete(value)
    def removeValue(self,value):
        self.deleteValue(value)
    def setFgColor(self,value):
        self.ctrl.SetForegroundColour(value)
        self.ctrl.Refresh()
    def setBgColor(self,value):
        self.ctrl.SetBackgroundColour(value)
        self.ctrl.Refresh()
    def castValue(self,value):
        return value

class WxButton(WxControl):
    def __init__(self,parent,h):
        id = getId()
        self.ctrl = wx.Button( parent, id, h.get('label'), wx.DefaultPosition, wx.DefaultSize, 0 )
        if h.get('handler'): self.ctrl.Bind( wx.EVT_BUTTON, h.get('handler'), id=id )
        self.DefaultAction(h)

class WxLabel(WxControl):
    def __init__(self,parent,h):
        flags = wx.ALIGN_CENTER 
        flags |= wx.ALIGN_CENTER_VERTICAL
        if h.get('align') == 'left': flags = wx.ALIGN_LEFT
        if h.get('align') == 'right': flags = wx.ALIGN_RIGHT
        self.ctrl = wx.StaticText( parent, wx.ID_ANY, h.get('label'), wx.DefaultPosition, wx.DefaultSize, 0|flags )        
        self.DefaultAction(h)

class WxTextArea(WxControl):
    def __init__(self,parent,h):
        '''
        flags |= wx.TE_MULTILINE if self.multiline is True else 0
        flags |= wx.TE_PASSWORD if self.password is True else 0
        flags |= wx.TE_READONLY if self.readonly is True else 0
        flags |= wx.TE_DONTWRAP if self.wrap is False else 0
        '''
        id = getId()
        flags = wx.TE_MULTILINE | wx.TE_DONTWRAP
        self.ctrl = wx.TextCtrl( parent, id, "", wx.DefaultPosition, wx.DefaultSize, 0|flags )
        #self.ctrl.Bind( wx.EVT_TEXT, self.handler, id=id )
        #self.ctrl.Bind( wx.EVT_CHAR, self.handler )
        drop_target = FileDrop(self)
        self.ctrl.SetDropTarget(drop_target)
        self.DefaultAction(h)
    def drop_handle(self,filenames):
        for filename in filenames:
            self.ctrl.AppendText( filename )
            if self.multiline is False:
                break
            self.ctrl.AppendText( '\n' )
    def appendValue(self,value):
        self.ctrl.AppendText(value)


class WxTextField(WxControl):
    def __init__(self,parent,h):
        id = getId()
        flags = 0
        self.ctrl = wx.TextCtrl( parent, id, "", wx.DefaultPosition, wx.DefaultSize, 0|flags )
        self.ctrl.Bind( wx.EVT_CHAR, h.get('handler') )
        drop_target = FileDrop(self)
        self.ctrl.SetDropTarget(drop_target)
        self.DefaultAction(h)
    def drop_handle(self,filenames):
        for filename in filenames:
            self.ctrl.AppendText( filename )
            break
    def appendValue(self,value):
        self.ctrl.AppendText(value)
       
def makeLayout(content,parent):
    vbox = WxVBox(parent)
    for v in content:
        hbox = WxHBox(parent)
        expand = True
        for h in v:
            name = h.get('name')
            if not name:
                if h.get('expand'): expand = h['expand']
                continue
            if name == '<>' or name == 'Spacer':
                hbox.addSpacer()
                continue                
            elif name == 'Button': f = WxButton(parent,h)
            elif name == 'Label': f = WxLabel(parent,h)
            elif name == 'TextArea': f = WxTextArea(parent,h)
            elif name == 'TextField': f = WxTextField(parent,h)
            else: continue
            prop = 1 if h.get('expand') else 0
            hbox.addItem(f.ctrl,proportion=prop)
        prop = 1 if h.get('expand') else 0
        vbox.addItem(hbox.ctrl,proportion=prop,expand=expand)
    return vbox.ctrl

class WxPanel():
    def __init__(self,layout,parent=None):
        self.ctrl = wx.Panel( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.sizer = makeLayout(layout,self.ctrl)
        self.ctrl.SetSizer( self.sizer )
        self.ctrl.Layout()
 
#
# Windows Function
#

def getHandler(handler):
    def eventHandler(event):
        handler(event)
        event.Skip()
    return eventHandler
    
def runLater(handler):
    wx.CallAfter(handler)

def runThread(handler):
    import threading
    thread = threading.Thread(target=handler)
    thread.start()

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self, x, y, filenames):
        self.window.OnDropFile(filenames)
        return True

class Timer():
    def __init__(self,parent,handler):
        self.timer = wx.Timer(parent)
        parent.Bind( wx.EVT_TIMER, handler, self.timer )
    def start(self,msec):
        self.timer.Start(msec)
    def stop(self):
        self.timer.Stop()
        
class Window():  
    def __init__(self,title="",width=800,height=600):
        self.app = wx.App()
        self.app.locale = wx.Locale(wx.Locale.GetSystemLanguage())
        self.frame = wx.Frame(None, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( width,height ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.ctrl = self.frame
        self.createdHandler = None
        self.closeHandler = None
        self.icon = None
        self.menu = None
        self.tool = None
        self.status = None
        self.content = None
        self.frame.Center();
        self.frame.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
    def Run(self):
        self.frame.Show()
        self.app.MainLoop()
   
    def SetTitle(self,label):
        pass
        
    def SetIcon(self,filename):
        pass
        
    def SetSize(self,width,height):
        pass
        
    def makeMenu(self, value):
        menu = wx.Menu()
        for k, v in value.items():
            if k[0] == '-':
                menu.AppendSeparator()
            else:
                if type(v) is dict:
                    submenu = self.makeMenu(v)
                    menu.AppendSubMenu(submenu, k)
                else:
                    if type(v) is list:
                        handler = v[0]
                        icon = v[1]
                    else:
                        handler = v
                        icon = None
                    item = wx.MenuItem( menu, getId(), k, wx.EmptyString, wx.ITEM_NORMAL )
                    if icon is not None: item.SetBitmap(getMenuBitmap(icon))
                    if handler is None: item.Enable( False )
                    else: self.frame.Bind(wx.EVT_MENU, getHandler(handler), item)
                    menu.Append(item)
        return menu
        
    def SetMenuBar(self,menu_table):
        self.menubar = wx.MenuBar(0)
        for key, value in menu_table.items():
            if type(value) is dict:
                menu = self.makeMenu(value)
                self.menubar.Append( menu, key )
        self.frame.SetMenuBar(self.menubar)

    def SetToolBar(self,tool_table): #icon, text, handler 
        flags = wx.TB_FLAT|wx.TB_HORIZONTAL
        if len(tool_table[0]) >= 3:
            flags |= wx.TB_TEXT
        self.toolbar = self.frame.CreateToolBar( flags, wx.ID_ANY )
        for value in tool_table:
            if value[0] is None:
                self.toolbar.AddSeparator()
            else:
                text = handler = tooltip = None
                if len(value) >= 2:
                    handler = value[1]
                if len(value) >= 3:
                    text = value[2]
                if len(value) >= 4:
                    tooltip = value[3]
                icon = getToolbarBitmap(value[0])
                id = getId()
                if text is not None:
                    tool = self.toolbar.AddTool( id, text, icon, wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
                else:
                    tool = self.toolbar.AddSimpleTool( id, icon, wx.EmptyString, wx.EmptyString, None )
                if tooltip is not None:
                    self.toolbar.SetToolShortHelp(id, tooltip);
                if handler is None:
                    tool.Enable( False )
                else:
                    self.toolbar.Bind( wx.EVT_TOOL, getHandler(handler), id = id )
        self.toolbar.Realize()

        
    def SetStatusBar(self,status_table):
        self.statusbar = self.frame.CreateStatusBar( len(status_table), wx.STB_SIZEGRIP, wx.ID_ANY )
        widths = []
        for i in range(len(status_table)):
            self.statusbar.SetStatusText( status_table[i][0], i)
            widths.append(status_table[i][1])
        self.statusbar.SetStatusWidths(widths)

    def setStatusText(self,text,index=0): 
        if self.statusbar:
            if index < self.statusbar.GetFieldsCount():
                self.statusbar.SetStatusText(text,index)
        
    def SetContent(self,content_table):
        self.panel = WxPanel(content_table,self.frame)
        self.frame.SetSizer( wrapSizer(self.panel.ctrl) )
        self.frame.Layout()
        
    def SetCreatedHandler(self,onCreated):
        self.frame.Bind(wx.EVT_SHOW, getHandler(onCreated))
        
    def SetCloseHandler(self,onClosing):
        self.frame.Bind(wx.EVT_CLOSE, getHandler(onClosing))
        
    def SetFileDropHandler(self, onFileDrop):
        pass

#
# Application
#

def onCreated(event):
    print("onCreated()")

def onClosing(event):
    print("onClosing()")
    
def onFileDrop(event):
    print("onFileDrop")

def onAbout(event):
    print("onAbout")
    
def onExit(event):
    print("onExit")
        
menu_table = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

status_table = [
    ["Ready", -6],   # width will have space with proportion 6 
    ["Status", -4],  # width will have space with proportion 4
    ["Code:1", 20]   # fixed width
]

tool_table =  [ #icon, text, handler
    [wx.ART_QUIT, onExit, "Exit", "Close Window" ],
    [None],                             # Tool separator
    [wx.ART_FLOPPY, None, "Save", ],    # Disabled toolbar item
]

layout_table = [ # vbox
    [ # hbox
        { "name" : "Label", "label" : "Address:", "menu" : menu_table, 'expand' : False },
        { "name" : "TextField", "key" : "textfile", "expand" : True, "menu" : menu_table },
        { "name" : "Button", 'handler' : onExit, "label" : "File", "tooltip" : "About this program" },
    ], [ # hbox
        { "name" : "TextArea", "key" : "text", "expand" : True, "menu" : menu_table },
    ],    
]

def MakeWindow():
    win = Window()
    win.SetTitle("ezGuiApp")
    win.SetIcon("./Lenna.png")
    win.SetSize(640,400)
    win.SetMenuBar(menu_table)
    win.SetToolBar(tool_table)
    win.SetStatusBar(status_table)
    win.SetContent(layout_table)
    win.SetCreatedHandler(onCreated)  
    win.SetCloseHandler(onClosing)
    win.SetFileDropHandler(onFileDrop)
    return win
            
if __name__ == "__main__":
    global appWin
    appWin = MakeWindow()
    appWin.Run()


