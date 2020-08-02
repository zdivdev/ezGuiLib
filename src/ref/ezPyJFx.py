import os

from java.io import File, FileInputStream
from javafx.application import Application
from javafx.scene import Scene, Node
from javafx.scene.layout import VBox, HBox, Priority
from javafx.scene.input import Clipboard, ClipboardContent
from javafx.scene.image import Image, ImageView
from javafx.geometry import Insets, Orientation, Pos
from javafx.embed.swing import SwingFXUtils

#
# Control Table
#

_window__ctrl_table = {}

def GetControl(name):
    return _window__ctrl_table.get(name)

def GetNativeControl(name):
    if _window__ctrl_table.get(name): return _window__ctrl_table[name].ctrl;

def DumpControlTable():
    for k,v in _window__ctrl_table.items():
        print(k,v)
        
#
# Dialog
#

def FxAlertDialog(message, title=None, stage=None):
    from javafx.scene.control import Alert
    from javafx.scene.control.Alert import AlertType
    from javafx.stage import Modality
    alert = Alert(AlertType.INFORMATION)
    if stage: alert.initOwner(stage)
    if title: alert.setTitle(title)
    alert.setHeaderText("")
    alert.setContentText(message)
    alert.initModality(Modality.APPLICATION_MODAL)
    alert.showAndWait()

def FxYesNoDialog(message, title, stage=None):
    from javafx.scene.control import Alert
    from javafx.scene.control.Alert import AlertType
    from javafx.stage import Modality
    from javafx.scene.control import ButtonType
    alert = Alert(AlertType.CONFIRMATION)
    if stage: alert.initOwner(stage)
    if title: alert.setTitle(title)
    alert.setHeaderText("")
    alert.setContentText(message)
    alert.initModality(Modality.APPLICATION_MODAL)
    result = alert.showAndWait()
    if result.get() == ButtonType.OK:
        return True
    else:
        return False

def FxFileDialog(initialFile, save, stage=None):
    from javafx.stage import FileChooser
    from java.io import File
    dlg = FileChooser()
    if initialFile:
        f = File(initialFile)
        if f.exists():
            if f.isDirectory(): dlg.setInitialDirectory(f)
            if f.isFile():      dlg.setInitialFileName(f.getAbsolutePath());
    dlg.setTitle("Select File");
    if save: return dlg.showSaveDialog(stage);
    else:    return dlg.showOpenDialog(stage);

def FxFileOpenDialog(initialFile, stage=None):
    return FxFileDialog(initialFile, False, stage)

def FxFileSaveDialog(initialFile, stage=None):
    return FxFileDialog(initialFile, True, stage)

def FxDirectoryOpenDialog(initialDirectory, stage=None):
    from javafx.stage import DirectoryChooser
    from java.io import File
    dlg = DirectoryChooser()
    if initialDirectory:
        f = File(initialDirectory)
        if f.exists() and f.isDirectory():
            dlg.setInitialDirectory(f);
    dlg.setTitle("Select Folder");
    return dlg.showDialog(stage)
       
#
# Control
#

class FxControl():
    def Initialize(self,h):
        from javafx.scene.control import Tooltip
        if h.get('width') or h.get('height'):
            width = -1
            height = -1
            if h.get('width') : width  = h['width']
            if h.get('height'): height = h['height']
            self.ctrl.setPrefSize(width, height);
        if h.get('tooltip'): self.ctrl.setTooltip(Tooltip(h['tooltip']))           
        if h.get('menu'): self.ctrl.setContextMenu(FxContextMenu(h['menu']))
        if h.get('key'): _window__ctrl_table[h['key']] = self
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])                
        if h.get('icon'): self.SetIcon( h['icon'], h.get('size'), h.get('icon_top') )
            
    def SetBackground(self,color): # {D8BFD8}
        self.ctrl.setStyle("-fx-background-color: #" + color + ";")
    def SetFontSize(self,size):
        self.ctrl.setStyle("-fx-font-size: " + str(size) + ";")
    def SetIcon(self,icon,size=None,top=False):
        from javafx.scene.control import ContentDisplay;
        if os.path.isfile(icon):
            iv = ImageView(Image(FileInputStream(icon)))
            if size: iv.setFitHeight(size); iv.setFitWidth(size)
            self.ctrl.setGraphic(iv)
            if top: self.ctrl.setContentDisplay(ContentDisplay.TOP)

class FxLabel(FxControl):
    def __init__(self,h):
        from javafx.scene.control import Label
        self.ctrl = Label()
        self.Initialize(h)
        self.ctrl.setText(h.get('label'))
        if h.get('handler'): self.ctrl.setOnAction(h['handler'])
        #ctrl.setAlignment(Pos.CENTER);

class FxImageView(FxControl):
    def __init__(self,h,parent):
        if h.get('file'): self.ctrl = ImageView(Image(File(h['file']).toURI().toString()))
        else: self.ctrl = ImageView()
        self.ctrl.setPreserveRatio(True);
        if h.get('fitwidth'): self.ctrl.setFitWidth(h['fitwidth'])
        if h.get('fitheight'): self.ctrl.setFitHeight(h['fitheight'])
        if h.get('bindwidth'): self.ctrl.fitWidthProperty().bind(parent.widthProperty())
        if h.get('bindheight'): self.ctrl.fitHeightProperty().bind(parent.heightProperty())  
        self.Initialize(h)
        if h.get('handler'): self.ctrl.setOnAction(h['handler'])


class FxScrollImageView(FxControl):
    def __init__(self,h,parent):
        from javafx.scene.control import ScrollPane
        from javafx.scene.control.ScrollPane import ScrollBarPolicy        
        self.ctrl = ScrollPane()
        img = FxImageView(h,self.ctrl)
        box = FxHBox(1,1)
        box.addItem(img.ctrl,True)
        #scroll.setHmin(32)
        #scroll.setHmax(32)
        self.ctrl.setVbarPolicy(ScrollBarPolicy.AS_NEEDED)
        self.ctrl.setHbarPolicy(ScrollBarPolicy.ALWAYS)
        self.ctrl.setPannable(True)
        self.ctrl.setFitToHeight(True)
        self.ctrl.setContent(box.ctrl)
        
class FxButton(FxControl):
    def __init__(self,h):   
        from javafx.scene.control import Button
        self.ctrl = Button()
        self.Initialize(h)
        self.ctrl.setText(h.get('label'))
        if h.get('handler'): self.ctrl.setOnAction( h['handler'] )
        
class FxToggleButton(FxControl):
    def __init__(self,h):
        from javafx.scene.control import ToggleButton
        self.ctrl = ToggleButton()
        self.Initialize(h)
        self.ctrl.setText(h.get('label'))
        if h.get('handler'): self.ctrl.setOnAction( h['handler'] )
    def IsSelected(self):
        return self.ctrl.isSelected()
    def SetSelected(self,v):
        return self.ctrl.setSelected(v)
        
class FxCheckBox(FxControl):
    def __init__(self,h):
        from javafx.scene.control import CheckBox
        self.ctrl = CheckBox()
        self.Initialize(h)
        self.ctrl.setText(h.get('label'))
        if h.get('handler'): self.ctrl.setOnAction( h['handler'] )
    def IsSelected(self):
        return self.ctrl.isSelected()
    def SetSelected(self,v):
        return self.ctrl.setSelected(v)
        

class FxText(FxControl):
    def GetText(self): return self.ctrl.getText()
    def SetText(self,text): self.ctrl.setText(text)
    def Insert(self,index,text): self.ctrl.insertText(index,text)
    def Append(self,text): self.ctrl.appendText(text)
    def Clear(self): self.ctrl.clear()
    def Copy(self): self.ctrl.copy()
    def Paste(self): self.ctrl.paste()
        
class FxTextField(FxText):
    def __init__(self,h):
        from javafx.scene.control import TextField
        self.ctrl = TextField()
        self.Initialize(h)
        self.ctrl.setText(h.get('text'))
        if h.get('handler'): self.ctrl.setOnAction(h['handler'])
        SetFileDropHandler( self.ctrl, self.DropHandler )  
    def DropHandler(self,files):
        self.ctrl.setText( files.get(0).getPath() )
        
class FxTextArea(FxText):
    def __init__(self,h):
        from javafx.scene.control import TextArea
        self.ctrl = TextArea()
        self.Initialize(h)
        if h.get('handler'): self.ctrl.setOnAction(h['handler'])
        self.ctrl.setText(h.get('text'))

class FxChoiceBox(FxControl):
    def __init__(self,h):
        from javafx.beans.value import ChangeListener
        from javafx.beans.value import ObservableValue
        from javafx.scene.control import ChoiceBox
        self.ctrl = ChoiceBox()
        self.Initialize(h)
        if h.get('handler'): self.ctrl.setOnAction(h['handler'])
        if h.get('items'): self.ctrl.getItems().addAll( h['items'] );
        self.ctrl.getSelectionModel().selectFirst() 
    def Add(self,item):
        self.ctrl.getItems().add(item);
    def GetSelectedItem(self):
        return self.ctrl.getSelectionModel().getSelectedItem()
    def GetSelectedIndex(self):
        return self.ctrl.getSelectionModel().getSelectedIndex()

class FxComboBox(FxControl):
    def __init__(self,h):
        from javafx.beans.value import ChangeListener
        from javafx.beans.value import ObservableValue
        from javafx.scene.control import ComboBox
        self.ctrl = ComboBox()
        self.Initialize(h)
        if h.get('handler'): self.ctrl.setOnAction(h['handler'])
        if h.get('items'): self.ctrl.getItems().addAll( h['items'] )
        self.ctrl.getSelectionModel().selectFirst()    
    def Add(self,item):
        self.ctrl.getItems().add(item)
    def GetSelectedItem(self):
        return self.ctrl.getSelectionModel().getSelectedItem()
    def GetSelectedIndex(self):
        return self.ctrl.getSelectionModel().getSelectedIndex()

class FxListView(FxControl):
    def __init__(self,h):
        from javafx.beans.value import ChangeListener
        from javafx.beans.value import ObservableValue
        from javafx.scene.control import ListView
        self.ctrl = ListView()
        self.Initialize(h)
        if h.get('handler'): self.ctrl.getSelectionModel().selectedItemProperty().addListener(h['handler'])
        if h.get('items'): self.ctrl.getItems().addAll( h['items'] )
        self.ctrl.getSelectionModel().selectFirst() 
    def Add(self,item):
        self.ctrl.getItems().add(item)
    def GetSelectedItem(self):
        return self.ctrl.getSelectionModel().getSelectedItem()
    def GetSelectedIndex(self):
        return self.ctrl.getSelectionModel().getSelectedIndex()

        
class FxTableRow():
    def __init__(self,items=None):
        self.values = []
        if items:
            for item in items: self.AddItem(item)
    def AddItem(self,item):
        from javafx.beans.property import SimpleStringProperty
        self.values.append(SimpleStringProperty(item))

class FxTableView(FxControl):
    def __init__(self,h):
        from javafx.scene.control import TableView
        self.ctrl = TableView()
        self.Initialize(h)
        if h.get('columns'): self.SetColumn(h['columns'])
        if h.get('widths'): self.SetColumnWidth(h['widths']) 
        if h.get('rwidths'): self.SetColumnWidthPercent(h['rwidths']) 
        if h.get('aligns'): self.SetColumnAlign(h['aligns']) 
        if h.get('handler'): self.ctrl.getSelectionModel().selectedItemProperty().addListener(h['handler'])
    def SetColumn(self,labels):
        from javafx.scene.control import TableColumn
        for label in labels: self.AddColumn(label)
    def AddColumn(self,label):
        from javafx.scene.control import TableColumn
        index = self.ctrl.getColumns().size()
        column = TableColumn(label)
        column.setCellValueFactory(lambda row : row.getValue().values[index])
        self.ctrl.getColumns().add(column);
    def AddRow(self,row):
        self.ctrl.getItems().add(FxTableRow(row))
    def SetColumnWidth(self,widths):
        from javafx.scene.control import TableView
        self.ctrl.setColumnResizePolicy( TableView.UNCONSTRAINED_RESIZE_POLICY )
        for i in range(len(widths)):
            column = self.ctrl.getColumns().get(i)
            column.setPrefWidth( widths[i] )
    def SetColumnWidthPercent(self,widths):
        from javafx.scene.control import TableView
        self.ctrl.setColumnResizePolicy( TableView.CONSTRAINED_RESIZE_POLICY )
        for i in range(len(widths)):
            column = self.ctrl.getColumns().get(i)
            column.setMaxWidth( widths[i] * 100000 )
    def SetColumnAlign(self,aligns):
        for i in range(len(aligns)):
            column = self.ctrl.getColumns().get(i)
            if aligns[i] < 0: column.setStyle( "-fx-alignment: CENTER-LEFT;")
            elif aligns[i] == 0: column.setStyle( "-fx-alignment: CENTER;")
            elif aligns[i] > 0: column.setStyle( "-fx-alignment: CENTER-RIGHT;")
    def ClearSelection(self):
        self.ctrl.getSelectionModel().clearSelection()
    def SelectFirst(self):
        self.ctrl.getSelectionModel().selectFirst()
    def SelectLast(self):
        self.ctrl.getSelectionModel().selectLast();
    def EnableMultiSelection(self):
        from javafx.scene.control import SelectionMode
        self.ctrl.getSelectionModel().setSelectionMode(SelectionMode.MULTIPLE)
    def GetSelectedIndex(self):
        return self.ctrl.getSelectionModel().getSelectedIndex()
    def GetSelectedItem(self):
        index = self.ctrl.getSelectionModel().getSelectedIndex()
        return self.ctrl.getItems().get(index).values
    def GetSelectedItems(self):
        items = []
        for item in self.ctrl.getSelectionModel().getSelectedItems():
            items.append( item.values )
        return items;
    def RemoveSelectedItems(self):
        self.ctrl.getItems().removeAll(self.ctrl.getSelectionModel().getSelectedItems());

class FxTreeView(FxControl):
    def __init__(self,h):
        from javafx.scene.control import TreeView
        from javafx.scene.control import TreeItem
        self.root = TreeItem(h['name'])
        self.ctrl = TreeView(self.root)
        self.Initialize(h)
        if h.get('handler'): self.ctrl.getSelectionModel().selectedItemProperty().addListener(h['handler'])
    def AddRootItem(self,label):
        return self.AddItem(label)
    def AddItem(self,label,parent=None):
        from javafx.scene.control import TreeItem
        item = TreeItem(label)
        if parent: parent.getChildren().add(item)
        else: self.root.getChildren().add(item)
        return item
    def GetSelectedIndex(self):
        return self.ctrl.getSelectionModel().getSelectedIndex()
    def GetSelectedItem(self):
        return self.ctrl.getSelectionModel().getSelectedItem()
    def GetSelectedItemText(self):
        return self.ctrl.getSelectionModel().getSelectedItem().getValue()
    def GetSelectedItemPath(self,delim=""):
        item = self.ctrl.getSelectionModel().getSelectedItem()
        return self.GetItemPath(item)
    def GetItemPath(self,item,delim=""):
        item = self.ctrl.getSelectionModel().getSelectedItem()
        path = item.getValue()
        while item.getParent():
            item = item.getParent()
            path = item.getValue() + delim + path
        return path
    def GetParentItem(self,item):
        return item.getParent()
    def GetItemValue(self,item):
        return item.getValue()

class FxProgressBar(FxControl):
    def __init__(self,h):   
        from javafx.scene.control import ProgressBar
        self.ctrl = ProgressBar()
        self.Initialize(h)
        if h.get('handler'): self.ctrl.setOnAction(h['handler'])
    def GetValue(self):
        return self.ctrl.getProgress()
    def SetValue(self,v):
        self.ctrl.setProgress(v)


#
# Container
#

class FxBox():
    def getItem(self,index): return self.ctrl.getChildren().get(index)
    def addItem(self,item,expand=False): 
        self.ctrl.getChildren().add(item)
        if expand == True: self.setExpand(item)
    def alignLeft(self): self.setAlignLeft()
    def alignRight(self): self.setAlignRight()
    def addSeparator(self):
        from javafx.scene.control import Separator
        sep = Separator()
        sep.setOrientation(self.separatorOrientation)
        self.ctrl.getChildren().add( sep )

class FxVBox(FxBox):
    def __init__(self,gap=0,pad=0):
        self.ctrl = VBox( gap )
        self.setExpand = lambda x : VBox.setVgrow(x, Priority.ALWAYS)
        self.setAlignLeft = lambda : self.ctrl.setAlignment(Pos.CENTER_LEFT)
        self.setAlignRight = lambda : self.ctrl.setAlignment(Pos.CENTER_RIGHT)
        self.separatorOrientation = Orientation.HORIZONTAL
        self.ctrl.setAlignment(Pos.CENTER)
        self.ctrl.setSpacing( gap )
        self.ctrl.setPadding( Insets( pad, pad, pad, pad ) )

class FxHBox(FxBox):
    def __init__(self,gap=0,pad=0):
        self.ctrl = HBox( gap )
        self.setExpand = lambda x : HBox.setHgrow(x, Priority.ALWAYS)
        self.setAlignLeft = lambda : self.ctrl.setAlignment(Pos.CENTER_LEFT)
        self.setAlignRight = lambda : self.ctrl.setAlignment(Pos.CENTER_RIGHT)
        self.separatorOrientation = Orientation.VERTICAL
        self.ctrl.setAlignment(Pos.CENTER)
        self.ctrl.setSpacing( gap )
        self.ctrl.setPadding( Insets( pad, pad, pad, pad ) )

class FxBorderPane():
    def __init__(self):
        from javafx.scene.layout import BorderPane
        from javafx.geometry import Insets
        self.ctrl = BorderPane()
        self.ctrl.setPadding(Insets(0, 0, 0, 0))
    def setTop(self,item):    self.ctrl.setTop(item)
    def setBottom(self,item): self.ctrl.setBottom(item)
    def setLeft(self,item):   self.ctrl.setLeft(item)
    def setRight(self,item):  self.ctrl.setRight(item)
    def setCenter(self,item): self.ctrl.setCenter(item)

class FxTabPane():
    def __init__(self,h):
        from javafx.scene.control import TabPane
        self.ctrl = TabPane()
        labels = h.get('labels')
        items = h.get('items')
        if labels and items:
            for i in range(0,len(items)):
                self.addItem( labels[i], FxLayout(items[i],self.ctrl))        
    def addItem(self, title, item):
        from javafx.scene.control import Tab
        tab = Tab()
        tab.setText(title)
        tab.setClosable(False)
        tab.setContent(item)
        self.ctrl.getTabs().add(tab)
       

class FxSplitPane(object):
    def addItem(self,item): self.ctrl.getItems().add(item)
    def addItems(self,layout):
        items = layout.get('items')
        if items:
            for item in items:
                self.addItem(FxLayout(item,self.ctrl))
        
class FxVSplitPane(FxSplitPane):
    def __init__(self,h):
        from javafx.scene.control import SplitPane
        self.ctrl = SplitPane()
        if h.get('first'):
            self.ctrl.setDividerPositions(h['first'], 1-h['first']);
        self.ctrl.setOrientation(Orientation.VERTICAL);
        self.addItems(h)

class FxHSplitPane(FxSplitPane):
    def __init__(self,h):
        from javafx.scene.control import SplitPane
        self.ctrl = SplitPane()
        if h.get('first'):
            self.ctrl.setDividerPositions(h['first'], 1-h['first']);
        self.ctrl.setOrientation(Orientation.HORIZONTAL);
        self.addItems(h)

#
# Window
#

def RunLater(handler):
    from javafx.application import Platform
    Platform.runLater(handler)

def Exec():
    from java.lang import Runtime
    from java.io import BufferedReader
    from java.io import InputStreamReader

    process = Runtime.getRuntime().exec(cmd)
    inp = BufferedReader(InputStreamReader(process.getInputStream(),"euc-kr"))
    out = ""
    line = inp.readLine()
    while line:
        out = out + line
        line = inp.readLine()

def Execute(cmd):
    '''
    import os
    os.system(cmd)
    '''
    import subprocess
    try:
        out = subprocess.check_output(cmd)
        return 0,out
    except:
        return -1,""
    
def StartThread(handler,args):
    import threading
    thread = threading.Thread(target=handler,args=args)
    thread.daemon = True
    thread.start()

def DragOver(event):
    from javafx.scene.input import TransferMode
    if event.getDragboard().hasFiles():
        event.acceptTransferModes(TransferMode.COPY_OR_MOVE)
    event.consume()

def DragDropped(handler):
    from javafx.scene.input import DragEvent
    from javafx.scene.input import Dragboard
    def _DragDropped(event): #closure
        db = event.getDragboard()
        if db.hasFiles():
            handler( db.getFiles() ) # List<File>
            event.setDropCompleted(True)
        else:
            event.setDropCompleted(False)
        event.consume()
    return _DragDropped

def SetFileDropHandler(ctrl,handler):  
    ctrl.setOnDragOver( DragOver )
    ctrl.setOnDragDropped( DragDropped(handler) )
 
def FxMenu(name,menu_table):
    from javafx.scene.control import Menu
    from javafx.scene.control import ContextMenu
    from javafx.scene.control import MenuItem
    from javafx.scene.control import SeparatorMenuItem
    if not name: menu = ContextMenu()
    else: menu = Menu(name)
    for m in menu_table:
        if not m.get('name') or m['name'] == '-':
            menu.getItems().add(SeparatorMenuItem());
        if not m.get('item'): continue # Disabled
        if type(m['item']) == list:
            menu.getItems().add(FxMenu(m['name'],m['item']))
        else:
            item = MenuItem(m['name'])
            item.setOnAction(m['item'])
            menu.getItems().add(item);
    return menu

def FxContextMenu(menu_table):
    return FxMenu(None,menu_table)
    
def FxMenuBar(menubar_table):
    from javafx.scene.control import MenuBar
    menubar = MenuBar()
    for m in menubar_table:
        if m.get('name'):
            menubar.getMenus().add(FxMenu(m['name'],m['item']))
        else:
            if m.get('fontsize'):
                menubar.setStyle("-fx-font: " + m['fontsize'] + " arial;")  
    return menubar

def FxToolBar(toolbar_table):
    from javafx.scene.control import Separator
    from javafx.scene.control import ToolBar      
    ctrl = ToolBar();
    for h in toolbar_table:
        if not h.get('name') or h['name'] == '-':
            ctrl.getItems().add(Separator())
            continue
        name = h['name'] 
        if   name == 'Label': f = FxLabel(h)
        elif name == 'Button': f = FxButton(h)
        elif name == 'CheckBox': f = FxCheckBox(h)
        elif name == 'ChoiceBox': f = FxChoiceBox(h)
        elif name == 'ComboBox': f = FxComboBox(h)
        elif name == 'ProgressBar': f = FxProgressBar(h)
        elif name == 'ToggleButton': f = FxToggleButton(h)
        elif name == 'TextField': f = FxTextField(h)
        else: continue  
        ctrl.getItems().add(f.ctrl);
    return ctrl

def FxStatusBar(statusbar_table):
    from javafx.scene.control import Separator     
    from javafx.scene.layout import Region     
    hbox = FxHBox(1,1);
    for h in statusbar_table:
        if not h.get('name'): continue
        if h['name'] == '--' or h['name'] == '--': hbox.addItem(Separator()); continue
        if h['name'] == '<>':
            space = Region(); HBox.setHgrow(space, Priority.ALWAYS)
            hbox.addItem(space)
            continue
        name = h['name'] 
        if   name == 'Label': f = FxLabel(h)
        elif name == 'Button': f = FxButton(h)
        elif name == 'CheckBox': f = FxCheckBox(h)
        elif name == 'ChoiceBox': f = FxChoiceBox(h)
        elif name == 'ComboBox': f = FxComboBox(h)
        elif name == 'ProgressBar': f = FxProgressBar(h)
        elif name == 'ToggleButton': f = FxToggleButton(h)
        elif name == 'TextField': f = FxTextField(h)
        else: continue  
        hbox.addItem(f.ctrl);
    return hbox.ctrl

def FxLayout(content,parent):
    from javafx.scene.control import Tooltip
    vbox = FxVBox(1,1)
    for v in content:
        hbox = FxHBox(1,1)
        expand = False
        for h in v:
            name = h.get('name')
            if not name:
                if h.get('expand'): expand = h['expand']
                continue
            if   name == 'Label': f = FxLabel(h)
            elif name == 'ImageView': f = FxImageView(h,parent)
            elif name == 'ScrollImageView': f = FxScrollImageView(h,parent)
            elif name == 'Button': f = FxButton(h)
            elif name == 'ToggleButton': f = FxToggleButton(h)
            elif name == 'CheckBox': f = FxCheckBox(h)
            elif name == 'TextField': f = FxTextField(h)
            elif name == 'TextArea': f = FxTextArea(h)
            elif name == 'ChoiceBox': f = FxChoiceBox(h)
            elif name == 'ComboBox': f = FxComboBox(h)
            elif name == 'ListBox': f = FxListView(h)
            elif name == 'TreeView': f = FxTreeView(h)
            elif name == 'Table': f = FxTableView(h)
            elif name == 'ProgressBar': f = FxProgressBar(h)
            elif name == 'TabPane': f = FxTabPane(h)
            elif name == 'HSplit': f = FxHSplitPane(h)
            elif name == 'VSplit': f = FxVSplitPane(h)
            else: continue
            hbox.addItem(f.ctrl,expand=h.get('expand'))
        vbox.addItem(hbox.ctrl,expand=expand)
    return vbox.ctrl

def ClipboardClear():
    Clipboard.getSystemClipboard().clear();
def GetClipboardText():
    if Clipboard.getSystemClipboard().hasString():
        return Clipboard.getSystemClipboard().getString()
def GetClipboardHtmlText():
    if Clipboard.getSystemClipboard().hasHtml():
        return Clipboard.getSystemClipboard().getHtml()
def GetClipboardFiles():
    if Clipboard.getSystemClipboard().hasFiles():
        return Clipboard.getSystemClipboard().getFiles()
def GetClipboardImage():
    return SwingFXUtils.fromFXImage( Clipboard.getSystemClipboard().getImage()  )

def putClipboardText(text):
    content = ClipboardContent()
    content.putString(text);
    Clipboard.getSystemClipboard().setContent(content)
def putClipboardHtmlText(text):
    content = ClipboardContent()
    content.putString(text)
    content.putHtml(text)
    Clipboard.getSystemClipboard().setContent(content)
def putClipboardFiles(files):
    content = ClipboardContent()
    content.putFiles(files)
    Clipboard.getSystemClipboard().setContent(content)
def putClipboardImage(image):
    content = ClipboardContent()
    content.putImage(SwingFXUtils.toFXImage(image, null))
    Clipboard.getSystemClipboard().setContent(content)

class FxWindowVars():
    def __init__(self):
        self.ctrl = None
        self.stage = None
        self.createdHandler = None
        self.closeHandler = None
        self.title = None
        self.icon = None
        self.width = 800
        self.height = 600
        self.menu = None
        self.tool = None
        self.status = None
        self.content = None

__vars = FxWindowVars()

class Window(Application):
    def __init__(self):
        print('FxWindow.__init__()');

    def start(self, stage):
        print('FxWindow.start()');
        from javafx.application import Platform
        __vars.ctrl  = _window__ctrl_table
        __vars.stage = stage
        if __vars.title: __vars.stage.setTitle(__vars.title)
        if __vars.icon: __vars.stage.getIcons().add(Image(FileInputStream(__vars.icon)))   
        if __vars.closeHandler: __vars.stage.setOnCloseRequest(__vars.closeHandler)
        Platform.setImplicitExit(True)
        vbox = FxVBox()
        if __vars.menu: vbox.addItem(FxMenuBar(__vars.menu))
        for m in __vars.tool: vbox.addItem(FxToolBar(m))
        pane = FxBorderPane()
        if __vars.content: pane.setCenter(FxLayout(__vars.content,pane.ctrl))
        pane.setTop(vbox.ctrl)
        pane.setBottom(FxStatusBar(__vars.status))
        __vars.scene = Scene(pane.ctrl, __vars.width, __vars.height)
        __vars.stage.setScene(__vars.scene)
        if __vars.createdHandler: __vars.createdHandler()
        __vars.stage.show()      
    def Run(self): print('Run()'); self.launch(self.class, [])
    def GetStage(self): return __vars.stage     
    def SetTitle(self,title): print('SetTitle()'); __vars.title = title
    def SetSize(self,width,height): __vars.width = width;  __vars.height = height    
    def SetIcon(self,icon): __vars.icon = icon
    def SetCreatedHandler(self,handler): __vars.createdHandler = handler
    def SetCloseHandler(self,handler): __vars.closeHandler = handler
    def Close(self): __vars.stage.close()
    def SetMenuBar(self,menu): __vars.menu = menu
    def SetToolBar(self,tool): __vars.tool = tool
    def SetStatusBar(self,status): __vars.status = status
    def SetContent(self,content): __vars.content = content
    def Alert(self, title, message): FxAlertDialog(title,message,__vars.stage)
    def YesNo(self, title, message, stage=None): return FxYesNoDialog(title,message,__vars.stage)
    def FileOpenDialog(self, initialFile): return FxFileOpenDialog(initialFile, __vars.stage)
    def FileSaveDialog(self, initialFile): return FxFileSaveDialog(initialFile, __vars.stage)

#
# Application
#
 

def onAbout(event):
    v = FxYesNoDialog("Global", "Dialog")
    if v: Alert("Result", "Yes")
    else: Alert("Result", "No")
def onBrowse(event):
    f = FxFileOpenDialog(None)
    ctrl = GetControl('text')
    if ctrl and f: ctrl.SetText(f.getPath())
def onExit(event):
    from javafx.application import Platform
    Platform.exit()
    #from java.lang import System
    #System.exit(0)
    #self.Close()
def onClose(event):
    global appWin
    v = FxYesNoDialog("Alert", "Do you want to quit ?", appWin.GetStage())
    if not v: event.consume()
def onChoice(event):
    c = GetControl('choice')
    t = GetControl('texttool')
    if c and t: t.SetText( c.GetSelectedItem() )
def onCombo(event):
    c = GetControl('combo')
    t = GetControl('texttool')
    if c and t: t.SetText( c.GetSelectedItem() )
def onListBox(event):
    c = GetControl('listbox')
    t = GetControl('texttool')
    if c and t: t.SetText( c.GetSelectedItem() )
def onTreeView(event):
    c = GetControl('tree')
    t = GetControl('texttool')
    print(c.GetSelectedItem())
    if c and t: t.SetText( c.GetSelectedItemPath("-") )
def onTableView(event):
    c = GetControl('table')
    for item in c.GetSelectedItems():
        print(item)
def onToggle(newvalue):
    print("toggle")
def onCheck(newvalue):
    print("toggle")
def threadHandler():
    import time
    p = GetControl('progress')
    for i in range(100):
        RunLater(lambda : p.SetValue(1.0*i/100))
        time.sleep(0.1)
def onCreated():
    table = GetControl('table')
    table.EnableMultiSelection()
    table.AddRow(["Tom", "and", "Doe"])
    table.AddRow(["Jane", "and", "Deer"])
    tree = GetControl('tree')
    item = tree.AddRootItem("Item1")
    tree.AddItem("Item1-1",item)
    tree.AddItem("Item1-2",item)
    item = tree.AddRootItem("Item2")
    tree.AddItem("Item2-1",item)
    tree.AddItem("Item2-2",item)
    StartThread(threadHandler,None)
    #ControlTable()      
def onRun(event):
    text = GetControl('text')
    print(text.GetText())
    if text:
        rv, out = Execute(text.GetText())
        textarea = GetControl('textarea')
        textarea.SetText(str(rv) + '\n' + out)

app_mainmenu = [
    { 'name' : "File",
      'item' : [
            { 'name' : "Exit" , 'item' : onExit, 'icon' : 'exit' },
            { 'name' : "-" },
            { 'name' : "About", 'item' : onAbout, 'icon' : 'help' } ]
    }, { 'name' : "Help",
      'item' : [
            { 'name' : "About", 'item' : onAbout, 'icon' : 'help' } ]
    }]
    
app_tool = [[
        { "name" : "Label", "label" : "Address:", "menu" : app_mainmenu },
        { "name" : "ChoiceBox", "key" : "choice", 'handler' : onChoice, 'items' : ["apple","orange"] },
        { "name" : "ComboBox", "key" : "combo", 'handler' : onCombo, 'items' : ["apple","orange"] },
        { "name" : "TextField", "key" : "texttool", "width" : 100 },
        { "name" : "ToggleButton", "label" : "Toggle", "handler" : onToggle, "tooltip" : "Toggle", 'icon' : 'icon/folder512.png', 'size' : 16  },
        { "name" : "CheckBox", "label" : "Check", "handler" : onCheck, "tooltip" : "Check", 'icon' : 'icon/folder512.png', 'size' : 16  },
    ],[
        { "name" : "Button",  "label" : "Exit", "handler" : onExit, "tooltip" : "Quit", 'icon' : 'icon/folder512.png', 'size' : 16, 'icon_top' : True  },
    ]]
    
app_status = [
        { "name" : "ProgressBar", 'key' : 'progress' },
        { "name" : "<>"},
    ]
    
tab1 = [[ { "name" : "TreeView", "key" : "tree", 'handler' : onTreeView,"expand" : True },
          { "expand" : True }, ]]
tab2 = [[ { "name" : "ListBox", "key" : "listbox", 'handler' : onListBox, 'items' : ["apple","orange"], 'expand' : True },
          { "expand" : True }, ]]
tab3 = [[ { "name" : "ScrollImageView", 'file' : "./icon/Lenna.png", 'bindwidth' : True, 'bindheight' : True, 'expand' : True },
          { "expand" : True }, ]]
tab4 = [[ { "name" : "Table", 'key':'table', 'columns' : ['First','Mid','Last'], 'rwidths' : [100,50,100], 'aligns':[1,0,-1], 'handler':onTableView, 'expand' : True },
          { "expand" : True }, ]]
split1 = [[
        { "name" : "TabPane", "labels" : [ "Tree", "List", "Image", "Table" ], "items" : [ tab1, tab2, tab3, tab4 ], "expand" : True },
        { "expand" : True }, ]]
split2 = [[ { "name" : "TextArea", 'key' : 'textarea', "expand" : True },
            { "expand" : True }, ]] 
app_content = [ # vbox
    [ # hbox
        { "name" : "Label", "label" : "Address:", "menu" : app_mainmenu },
        { "name" : "TextField", "key" : "text", "expand" : True, "menu" : app_mainmenu },
        { "name" : "Button",  "label" : "Browse", "tooltip" : "Open File", "handler" : onBrowse  },
        { "name" : "Button",  "label" : "Run", "handler" : onRun, "menu" : app_mainmenu  },
    ],  
    [ # hbox
        { "name" : "HSplit", "items" : [ split1, split2 ] , "first" : 0.5, "expand" : True},
        { "expand" : True },
    ],                
]

if __name__ == "__main__":
    global appWin
    appWin = Window()
    appWin.SetTitle("ezPyJFX")
    appWin.SetSize(640,400)
    #appWin.SetIcon("./icon/Lenna.png")
    appWin.SetMenuBar(app_mainmenu)
    appWin.SetToolBar(app_tool)
    appWin.SetStatusBar(app_status)
    appWin.SetContent(app_content)
    appWin.SetCreatedHandler(onCreated)  
    appWin.SetCloseHandler(onClose)
    appWin.Run()
    