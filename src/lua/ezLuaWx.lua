package.cpath = package.cpath..";./?.dll;./?.so;../lib/?.so;"
require("wx")

--
-- Control Table
--
wxID_USER_Index = 1000

_window__ctrl_table = {}

function GetControl(key)
    return _window__ctrl_table[key]
end

function GetNativeControl(key)
    if _window__ctrl_table[key] then
        return _window__ctrl_table[key].ctrl
    end
    return ctrl
end

function DumpControlTable()
    for k,v in pairs(_window__ctrl_table) do
        print(k,v)
    end
end

function dump_ctrl_event()
    for k,v in pairs(__ctrl_event) do
        for k1, v1 in pairs(v) do
            print( k, k1expand, v1 )
        end
    end
end

--
-- Dialog
--


function Message(parent,caption,message)
    return wx.wxMessageBox( message, caption, wx.wxOK + wx.wxCENTRE, parent, -1, -1 )
end

function OpenFileDialog(parent,defaultDir,multiple,save)
    local style = 0
    if not save then style = wx.wxFD_OPEN + wx.wxFD_FILE_MUST_EXIST 
    else style = wx.xFD_SAVE + wx.wxFD_OVERWRITE_PROMPT end
    if multiple then style = style + wx.wxFD_MULTIPLE end
    if not defaultDir then defaultDir = "" end
    local dlg = wx.wxFileDialog(parent,"Choose a file",defaultDir,"","*.*",style)
    local rv = dlg:ShowModal()
    if rv == wx.wxID_OK then
        --[[
        if multiple == true then
            files = []
            for file in dlg.GetFilenames():
                files.append( os.path.join(dlg.GetDirectory(), file) )
            return files
        else:]]
        return dlg:GetDirectory() .. "\\" .. dlg:GetFilename()
    end
    return nil 
end

function SaveFileDialog(defaultDir)
    return OpenFileDialog(defaultDir, false, true)
end

--
-- Controls
--

function GetId()
    local id = wxID_USER_Index
    wxID_USER_Index = wxID_USER_Index + 1
    return id
end

function InitControl(obj,h)   

    obj.SetFgColor = function(r,g,b) obj.ctrl:SetForegroundColour( wx.wxColour( r, g, b ) ) end
    obj.SetBgColor = function(r,g,b) obj.ctrl:SetBackgroundColour( wx.wxColour( r, g, b ) ) end

    if h.bgcolor then obj.SetBgColor(h.bgcolor[1], h.bgcolor[2], h.bgcolor[3]) end
    if h.handler and obj.ev then obj.parent:Connect(obj.id, obj.ev, h.handler ) end
    if h.tooltip then obj.ctrl:SetToolTip(wx.wxToolTip(h.tooltip)) end
    if h.menu then
        local menu = EzMenu(obj.ctrl,h.menu)
        obj.ctrl:Connect(wx.wxEVT_RIGHT_DOWN, function(event) 
                obj.ctrl:PopupMenu(menu, event:GetPosition()) end ) 
    end
    if h.fontsize then
        obj.ctrl:SetFont( wx.wxFont( h.fontsize, wx.wxFONTFAMILY_DEFAULT, 
            wx.wxFONTSTYLE_NORMAL, wx.wxFONTWEIGHT_NORMAL, False, "" ) ) --fontname       
    end
    if h.filedrop then
        local dropTarget = wx.wxLuaFileDropTarget();
        dropTarget.OnDropFiles = function(self, x, y, filenames)
            return h.filedrop(filenames) -- 1..n, true, false
        end
        obj.ctrl:SetDropTarget(dropTarget)
    end
            
    obj.expand = 0 
    obj.border = 1 
    if h.layout then
        if h.layout.expand then obj.expand = h.layout.expand end
        if h.layout.border then obj.border = h.layout.border end
    end
end

function InitItemContainer(obj)
    obj.Clear  = function() return obj.ctrl:Clear() end
    obj.Append = function(value) return obj.ctrl:Append(value) end
    obj.Insert = function(value,index) return obj.ctrl:Insert(value,index) end
    obj.Delete = function(index) return obj.ctrl:Delete(index) end
    obj.Select = function(index) return obj.ctrl:Select(index) end
    obj.GetCount  = function() return obj.ctrl:GetCount() end
    obj.GetSelection  = function() return obj.ctrl:GetSelection() end
    obj.GetString = function(index) return obj.ctrl:GetString(index) end
end

function EzLabel(parent,h)
    local obj = { }
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxStaticText( parent, obj.id, h.label,
                wx.wxDefaultPosition, wx.wxDefaultSize,
                wx.wxALIGN_CENTER + wx.wxALIGN_CENTER_VERTICAL )
    InitControl(obj,h)
    return obj
end

function EzButton(parent,h)
    local obj = { }
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxButton( parent, obj.id, h.label, wx.wxDefaultPosition,wx.wxDefaultSize,0)
    obj.ev   = wx.wxEVT_COMMAND_BUTTON_CLICKED
    InitControl(obj,h)
    return obj
end

function EzToggleButton(parent,h)
    local obj = { }
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxToggleButton( parent, obj.id, h.label, wx.wxDefaultPosition,wx.wxDefaultSize)
    obj.ev   = wx.wxEVT_COMMAND_TOGGLEBUTTON_CLICKED
    obj.GetValue  = function()  return obj.ctrl:GetValue() end
    obj.SetValue  = function(v) return obj.ctrl:SetValue(v) end
    obj.SetLabel  = function(v) return obj.ctrl:SetLabel(v) end
    InitControl(obj,h)
    return obj
end

function EzCheckBox(parent,h)
    local obj = { }
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxCheckBox( parent, obj.id, h.label, wx.wxDefaultPosition,wx.wxDefaultSize)
    obj.ev   = wx.wxEVT_COMMAND_CHECKBOX_CLICKED
    obj.SetLabel  = function(v) return obj.ctrl:SetLabel(v) end
    obj.GetValue  = function()  return obj.ctrl:IsChecked() end
    obj.SetValue  = function(v) return obj.ctrl:SetValue(v) end
    obj.IsChecked = function()  return obj.ctrl:IsChecked() end        
    InitControl(obj,h)
    return obj
end


function EzTextCtrl(parent,h)
    local obj = { }
    local style = 0 
    if h.multiline then style = style + wx.wxTE_MULTILINE + wx.wxTE_DONTWRAP
    else style = style + wx.wxTE_PROCESS_ENTER end
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxTextCtrl( parent, obj.id, h.label,
                wx.wxDefaultPosition,wx.wxDefaultSize, style)
    obj.ev   = nil
    obj.Clear   = function() obj.ctrl:Clear() end
    obj.Append = function(data) obj.ctrl:AppendText(data) end       
    obj.AppendText = function(data) obj.ctrl:AppendText(data) end
    obj.GetValue = function()  return obj.ctrl:GetValue() end
    obj.SetValue = function(v)  obj.ctrl:SetValue(v) end
    InitControl(obj,h)
    return obj
end

function EzFilePickerCtrl(parent,h)
    local obj = { }
    local style = wx.wxFLP_DEFAULT_STYLE 
    if h.save then style = style + wx.wxFLP_SAVE + wx.wxFLP_OVERWRITE_PROMPT 
    else style = style + wx.wxFLP_OPEN end 
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxFilePickerCtrl( parent, obj.id, h.label, "File Open", "*.*",
                wx.wxDefaultPosition,wx.wxDefaultSize, style)
    obj.ev   = nil
    obj.GetValue = function()  return obj.ctrl:GetPath() end
    obj.SetValue = function(v) return obj.ctrl:SetPath(v) end       
    InitControl(obj,h)
    return obj
end

function EzDirPickerCtrl(parent,h)
    local obj = { }
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxDirPickerCtrl( parent, obj.id, h.label, "Directory Open",
                wx.wxDefaultPosition,wx.wxDefaultSize)
    obj.ev   = nil
    obj.GetValue = function()  return obj.ctrl:GetPath() end
    obj.SetValue = function(v) return obj.ctrl:SetPath(v) end       
    InitControl(obj,h)
    return obj
end


function EzStyledText(parent,h)
    local obj = {}
    obj.id = GetId()
    obj.ctrl = wxstc.wxStyledTextCtrl(parent, obj.id, 
                wx.wxDefaultPosition, wx.wxDefaultSize, 0, "wxStyledTextCtrl" ) 
    InitControl(obj,h)  
    
    obj.enableLineNumber = function()
            obj.ctrl:SetMargins(0, 0)
            obj.ctrl:SetMarginType(1, wxstc.wxSTC_MARGIN_NUMBER)
            obj.ctrl:SetMarginMask(2, wxstc.wxSTC_MASK_FOLDERS)
            obj.ctrl:SetMarginSensitive(2, True)
            obj.ctrl:SetMarginWidth(1, 32) -- 2,25
            obj.ctrl:SetMarginWidth(2, 16) -- 2,25  
        end
    obj.enableLineNumber();
    obj.AppendText = function(v) obj.ctrl:AppendText(v) end
    return obj
end

function EzChoiceBox(parent,h)
    local obj = { }
    if not h.items then h.items = {} end
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxChoice( parent, obj.id, wx.wxDefaultPosition,wx.wxDefaultSize,
                            h.items, 0, wx.wxDefaultValidator)
    obj.ev   = wx.wxEVT_COMMAND_CHOICE_SELECTED
    if h.value then obj.ctrl:SetSelection(h.value) end
    obj.GetValue = function() return obj.ctrl:GetSelection() end
    obj.SetValue = function(v) return obj.ctrl:SetValue(v) end
    obj.GetText  = function() return obj.ctrl:GetString(obj.ctrl:GetSelection()) end    
    InitControl(obj,h)
    InitItemContainer(obj)
    return obj
end

function EzComboBox(parent,h)
    local obj = { }
    if not h.items then h.items = {} end
    if not h.value then h.value = "" end
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxComboBox( parent, obj.id, h.value,
                wx.wxDefaultPosition,wx.wxDefaultSize,
                h.items, 0, wx.wxDefaultValidator)
    obj.ev   = wx.wxEVT_COMMAND_COMBOBOX_SELECTED
    obj.GetValue = function()  return obj.ctrl:GetValue() end
    obj.SetValue = function(v) return obj.ctrl:SetValue(v) end
    obj.GetText  = function()  return obj.ctrl:GetValue() end
    InitControl(obj,h)
    InitItemContainer(obj)
    return obj
end

function EzListBox(parent,h)
    local obj = { }
    if not h.items then h.items = {} end
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxListBox( parent, obj.id, 
                wx.wxDefaultPosition,wx.wxDefaultSize,
                h.items, 0, wx.wxDefaultValidator)
    obj.ev   = wx.wxEVT_COMMAND_LISTBOX_SELECTED
    obj.IsSelected = function(i) return obj.ctrl:IsSelected(i) end
    InitControl(obj,h)
    InitItemContainer(obj)
    return obj
end

function EzCheckListBox(parent,h)
    local obj = { }
    if not h.items then h.items = {} end
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxCheckListBox( parent, obj.id, 
                wx.wxDefaultPosition,wx.wxDefaultSize,
                h.items, 0, wx.wxDefaultValidator)
    obj.ev   = wx.wxEVT_COMMAND_CHECKLISTBOX_TOGGLED
    obj.IsSelected = function(i) return obj.ctrl:IsSelected(i) end
    obj.IsChecked  = function(i) return obj.ctrl:IsChecked(i) end
    InitControl(obj,h)
    InitItemContainer(obj)
    return obj
end
 
function EzRadioBox(parent,h)
    local obj = { }
    if not h.items then h.items = {} end
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxRadioBox( parent, obj.id, h.label,
                wx.wxDefaultPosition,wx.wxDefaultSize,
                h.items, 0, wx.wxRA_SPECIFY_ROWS, wx.wxDefaultValidator)
    obj.ev   = wx.wxEVT_COMMAND_RADIOBOX_SELECTED
    if h.value then obj.ctrl:SetSelection(h.value) end    
    obj.GetValue = function() return obj.ctrl:GetSelection() end
    obj.SetValue = function(v) return obj.ctrl:SetValue(v) end
    obj.GetText  = function() return obj.ctrl:GetString(obj.ctrl:GetSelection()) end    
    InitControl(obj,h)
    InitItemContainer(obj)
    return obj
end

--wx.wxLC_REPORT + wx.wxLC_SORT_ASCENDING + wx.wxLC_SORT_DESCENDING 
function EzTableView(parent,h)
    local obj = { }
    if not h.items then h.items = {} end
    obj.parent = parent
    obj.id   = GetId()
    obj.ctrl = wx.wxListCtrl( parent, obj.id, 
                wx.wxDefaultPosition,wx.wxDefaultSize,
                  wx.wxLC_REPORT + wx.wxBORDER_SUNKEN )
    obj.ev   = wx.wxEVT_COMMAND_LIST_ITEM_SELECTED
    h.filedrop = function(self, x, y, filenames)
        for i = 1, #filenames do
            obj.ctrl:InsertItem(obj.ctrl:GetItemCount()+1, filenames[i])    
        end
        return true
    end
    InitControl(obj,h)

    --list:SetImageList(listImageList, wx.wxIMAGE_LIST_SMALL)
    obj.col = 0
    obj.row = 0
    
    obj.Clear = function() obj.ctrl:DeleteAllItems() end
    obj.Set = function( row, col, label )
        obj.ctrl:SetItem( row, col, label)
    end
    obj.GetSelectedItems = function()
        local items = { }
        local item = -1
        while true do
            item = obj.ctrl:GetNextItem(item, wx.wxLIST_NEXT_ALL, wx.wxLIST_STATE_SELECTED)
            if item == -1 then  
                break 
            end
            items[#items+1] = item
        end
        return items
    end
    obj.AddColumn = function( label, size )
        obj.ctrl:InsertColumn(obj.col, label)
        obj.ctrl:SetColumnWidth(obj.col, size)
        obj.col = obj.col + 1
    end
    obj.AddColumns = function( labels, widths )
        if labels then 
            for col = 1, #labels do
                obj.ctrl:InsertColumn( col-1, labels[col])
                obj.col = obj.col + 1
            end
            if widths then 
                for col = 1, #widths do obj.ctrl:SetColumnWidth(col-1, widths[col]) end
            end
        end
    end    
    obj.AddRow = function( row )
        obj.ctrl:InsertItem( obj.row, row[1] )
        for col = 2, #row do
            obj.ctrl:SetItem( obj.row, col-1, row[col])
        end
        obj.row = obj.row + 1
    end

    obj.ctrl:Connect( wx.wxEVT_COMMAND_LIST_COL_CLICK, function(event)
        obj.ctrl.SortItems( function(a,b,c)
            if a > b then return 1 end
            if a < b then return -1 end
            return 0 
        end, obj.ctrl )
        event:Skip()
    end )
        
    return obj
end

--
-- Containers
--


function EzBoxSizer(orient)
    local sizer = { }
    if orient == nil then orient = wx.wxVERTICAL end
    sizer.ctrl = wx.wxBoxSizer( orient )
    sizer.Add = function(child) 
        local expand = 0
        local border = 0
        local flags = wx.wxALIGN_CENTER + wx.wxEXPAND + wx.wxALL 
        if child.border then border = child.border end 
        if child.expand then expand = child.expand end
        sizer.ctrl:Add( child.ctrl, expand, flags, border )
    end
    sizer.AddSpacer = function(size) 
        if size == nil then size = 5 end
        sizer.ctrl:Add( 0, 0, 1, wx.wxEXPAND, size )
    end
    return sizer
end

function EzVBox()
    return EzBoxSizer(wx.wxVERTICAL)
end
      
function EzHBox()
    return EzBoxSizer(wx.wxHORIZONTAL)
end

function EzHStaticBox(parent,name) 
    local hsbox = { }
    local box = wx.wxStaticBox( parent, wx.wxID_ANY, name)
    hsbox.ctrl = wx.wxStaticBoxSizer( box, wx.wxHORIZONTAL )
    hsbox.Add = function(child) 
        hsbox.ctrl:Add( child.ctrl, 1, wx.wxEXPAND + wx.wxALL + wx.wxGROW, 1 )
    end    
    return hsbox
end

function EzPanel(parent,content)
    local panel = { }
    panel.ctrl = wx.wxPanel( parent, wx.wxID_ANY, wx.wxDefaultPosition, wx.wxDefaultSize, wx.wxTAB_TRAVERSAL )
    panel.ctrl:SetSizer( Layout( panel.ctrl,content).ctrl )
    panel.ctrl:Layout()
    return panel
end

function EzBoxPanel(parent,content)
    local vbox = EzVBox()
    local panel = EzPanel(parent,content)
    panel.expand = 1
    vbox.Add(panel)
    vbox.expand = 1
    return vbox
end

function EzTabPane(parent,content)
    local note = { }
    note.ctrl = wx.wxNotebook( parent, wx.wxID_ANY, wx.wxDefaultPosition, wx.wxDefaultSize, 0 )
    if content ~= nil and content.children ~= nil then
        for i = 1, #content.children do
            local panel = Panel( note.ctrl, content.children[i] )
            local title = tostring(i)
            if content.title ~= nil and content.title[i] ~= nil then
                title = content.title[i]
            end
            note.ctrl:AddPage( panel.ctrl, title, False ) 
        end
    end
    return note
end

function EzSplitterWindow(parent,content,direction)
    local swin = { }
    swin.ctrl = wx.wxSplitterWindow( parent, wx.wxID_ANY, wx.wxDefaultPosition, wx.wxDefaultSize, 0 --[[wx.wxSP_3D]] )
    local left_panel = EzPanel( swin.ctrl, content.children[1] )
    local right_panel = EzPanel( swin.ctrl, content.children[2] )
    if direction == 'horizontal' then
        swin.ctrl:SplitHorizontally( left_panel.ctrl, right_panel.ctrl, 0 )
    else
        swin.ctrl:SplitVertically( left_panel.ctrl, right_panel.ctrl, 0 )
    end
    return swin
end

function EzVSplitWindow(parent,content)
    return EzSplitterWindow(parent,content,'vertical')
end

function EzHSplitWindow(parent,content)
    return EzSplitterWindow(parent,content,'horizontal')
end

--
-- Window
--


function GetMenuBitmap(name,size)
 if name == "exit" then
  return wx.wxArtProvider.GetBitmap(wx.wxART_QUIT, wx.wxART_MENU, wx.wxSize(size, size))
 end
 if name == "help" then
  return wx.wxArtProvider.GetBitmap(wx.wxART_HELP, wx.wxART_MENU, wx.wxSize(size, size))
 end
end

function GetToolBitmap(name,size)
 if name == "exit" then
  return wx.wxArtProvider.GetBitmap(wx.wxART_QUIT, wx.wxART_TOOLBAR, wx.wxSize(size, size))
 end
 if name == "help" then
  return wx.wxArtProvider.GetBitmap(wx.wxART_HELP, wx.wxART_TOOLBAR, wx.wxSize(size, size))
 end
end

function GetBitmap(xpm_table)
     return wx.wxBitmap(xpm_table)
end
    
function GetBitmapFile( filename )
    if os.isfile( filename ) then
        return wx.wxBitmap( filename, wx.wxBITMAP_TYPE_ANY )
    else
        return nil
    end
end

function GetIcon(name)
     local icon = wx.wxIcon()
     if type(name) == "string" then
        icon:CopyFromBitmap(wx.wxBitmap(name))
     end
     return icon
end

function EzMenu(parent,menu_table)
    local menu = wx.wxMenu()
    for i, m in ipairs(menu_table) do
        if type(m.Name) == "string" then 
            if type(m.Value) == "table" then
                local submenu = EzMenu( parent, m.Value )
                menu:Append( submenu, m.Name ) 
            end  
            if type(m.Value) == "function" then
                local id = GetId()
                local item = wx.wxMenuItem( menu, id, m.Name, "", wx.wxITEM_NORMAL )
                if m.Icon ~= nil then
                    item:SetBitmap(GetMenuBitmap(m.Icon,16))
                end
                menu:Append( item )
                parent:Connect(id, wx.wxEVT_COMMAND_MENU_SELECTED, m.Value)
            end
        end  
    end    
    return menu
end

function EzMenuBar(parent,menubar_table)
    local menubar = wx.wxMenuBar( 0 )
    for i, m in ipairs(menubar_table) do
        local menu
        if type(m.Name) == "string" then 
            local item
            if type(m.Value) == "table" then
                menu = EzMenu( parent, m.Value )
                menubar:Append( menu, m.Name ) 
            end
            if type(m.Value) == "function" then
                local id = GetId()
                item = wx.wxMenuItem( menubar, id, m.Name, "", wx.wxITEM_NORMAL )
                menubar:Append( item )
                parent:Connect(id, wx.wxEVT_COMMAND_MENU_SELECTED, m.Value)
            end
        end   
    end
    return menubar
end

function EzToolBar(parent,toolbar_table)
    local flags = wx.wxTB_FLAT + wx.wxTB_HORIZONTAL + wx.wxTB_TEXT
    local toolbar = parent:CreateToolBar( flags, wx.wxID_ANY )
    for i, m in ipairs(toolbar_table) do
        local tool
        local icon
        local tooltip
        local name = m.Name
        if m.Name ~= nil and m.Name == '-' then
            toolbar:AddSeparator()
        else
            if m.Icon == nil then icon = wx.NullBitmap else icon = GetToolBitmap(m.Icon,32) end
            if m_ToolTip == nil then tooltip = "" else tooltip = m.ToolTip end
            if m.Name == nil then
                flags = flags + wx.wxTB_TEXT
                name = ""
            end
            local id = GetId()
            tool = toolbar:AddTool(id, name, icon, tooltip, wx.wxITEM_NORMAL)
            if m.ToolTip ~= nil then toolbar:SetToolShortHelp( id, m.ToolTip) end
            if m.Value == nil then tool:Enable( false ) else 
                toolbar:Connect( id, wx.wxEVT_COMMAND_TOOL_CLICKED, m.Value )
            end
        end
    end
    toolbar:Realize()
 
--[[
    local toolbar = wx.wxToolBar(parent, ID_TOOLBAR, wx.wxDefaultPosition, wx.wxDefaultSize)
    for i, m in ipairs(toolbar_table) do
  local tool = toolbar:AddTool(wx.wxID_ANY, m.Name, m.Icon, m.ToolTip, wx.wxITEM_NORMAL)
    end
    return toolbar
 ]]
end

function EzStatusBar(parent,count)
    return parent:CreateStatusBar( count, 0, wxID_STATUS )
end

function Layout(parent,content) 
    local vbox = EzVBox()
    for i, v in ipairs(content) do
        local hbox = EzHBox()
        if type(v) == "table" then
            for j, h in pairs(v) do
                if type(h) == "table" then
                    local ctrl;
                    if     h.name == "StaticText" then ctrl = EzLabel(parent,h)
                    elseif h.name == "Button" then ctrl = EzButton(parent,h)
                    elseif h.name == "ToggleButton" then ctrl = EzToggleButton(parent,h)
                    elseif h.name == "CheckBox" then ctrl = EzCheckBox(parent,h)
                    elseif h.name == "Choice" then ctrl = EzChoiceBox(parent,h)
                    elseif h.name == "ComboBox" then ctrl = EzComboBox(parent,h)
                    elseif h.name == "ListBox" then ctrl = EzListBox(parent,h)
                    elseif h.name == "CheckListBox" then ctrl = EzCheckListBox(parent,h)
                    elseif h.name == "RadioBox" then ctrl = EzRadioBox(parent,h)
                    elseif h.name == "TextField" then ctrl = EzTextCtrl(parent,h)
                    elseif h.name == "TextArea" then h.multiline = true; ctrl = EzTextCtrl(parent,h)
                    elseif h.name == "FilePicker" then ctrl = EzFilePickerCtrl(parent,h)
                    elseif h.name == "DirPicker" then ctrl = EzDirPickerCtrl(parent,h)
                    elseif h.name == "StyledText" then ctrl = EzStyledText(parent,h)
                    elseif h.name == "Table" then ctrl = EzTableView(parent,h)
                    elseif h.name == "Panel" then ctrl = EzPanel(parent,h)
                    elseif h.name == "TabPane" then ctrl = EzTabPane(parent,h)
                    elseif h.name == "HSplit" then ctrl = EzVSplitWindow(parent,h)
                    elseif h.name == "VSplit" then ctrl = EzHSplitWindow(parent,h)
                    elseif h.name == "Spacer" then hbox.AddSpacer(0)
                    elseif h.name == nil then for k1,v1 in pairs(h) do hbox[k1] = v1 end
                    end
                    if ctrl ~= nil then
                        if h.layout ~= nil then
                            for k1,v1 in pairs(h.layout) do ctrl[k1] = v1 end                
                        end
                        for k1,v1 in pairs(h) do ctrl[k1] = v1 end                
                        if ctrl.key ~= nil then _window__ctrl_table[ctrl.key] = ctrl end
                        hbox.Add(ctrl)
                    end
                else
                    --TODO: Error Meeesage
                end
            end

        else
            --TODO: Error Meeesage
        end  
        vbox.Add(hbox)
    end  
    return vbox
end

function Window(title,icon,layout, width, height, fontsize ) 
    
    window = {} 
    if fontsize then __font_size = fontsize end
    window.ctrl = _window__ctrl_table
    window.frame = wx.wxFrame (wx.NULL, wx.wxID_ANY, title, wx.wxDefaultPosition, wx.wxSize( width, height ), wx.wxDEFAULT_FRAME_STYLE+wx.wxTAB_TRAVERSAL )
    
    window.frame:SetSizeHints( wx.wxDefaultSize, wx.wxDefaultSize )
    window.Show = function() window.frame:Show() end
    
    window.SetMenuBar = function(menu) window.frame:SetMenuBar( EzMenuBar( window.frame, menu) ) end
    window.SetToolBar = function(tool) EzToolBar( window.frame, tool ) end    
    window.SetStatusBar = function(count) 
        window.StatusBar = window.frame:CreateStatusBar( count, 0, wx.wxID_ANY )
    end
    window.SetStatusText = function(text,index) window.StatusBar:SetStatusText(text,index) end

    window.SetContent = function(content) 
        --window.frame:SetSizer( Layout( window.frame, content ).ctrl )
        window.frame:SetSizer( EzBoxPanel( window.frame, content ).ctrl )
        window.frame:Layout() --TODO: not necessary
        window.frame:Centre( wx.wxBOTH ) --TODO: not necessary
    end
    
    window.SetTimer = function(handler) 
        window.frame:Connect( wx.wxEVT_TIMER, handler )
        window.Timer = wx.wxTimer(window.frame, wxID_USER_Index) 
        wxID_USER_Index = wxID_USER_Index + 1
    end
    window.StartTimer = function(msec) window.Timer:Start(msec) end
    window.StopTimer = function() window.Timer:Stop() end  
    
    window.GetCtrl = function(name) 
        return _window__ctrl_table[name];
    end

    window.SetIcon = function(name)
        window.frame:SetIcon(GetIcon(name))
    end

    window.Run = function() 
        wx.wxLocale(wx.wxLocale:GetSystemLanguage()) -- TODO
        wx.wxGetApp():MainLoop()
    end
    
    if icon ~= nil then window.SetIcon(icon) end
    
    if layout ~= nil then
        if layout.menubar   ~= nil then window.SetMenuBar(layout.menubar) end
        if layout.toolbar   ~= nil then window.SetToolBar(layout.toolbar) end
        if layout.statusbar ~= nil then window.SetStatusBar(layout.statusbar) end
        if layout.content   ~= nil then window.SetContent(layout.content) end
    end
    return window
end

--
-- Aplication
--
 

function fnExit()
    --appWin.frame.Close()
    os.exit(0)
end

function fnAbout()
    Message( appWin.frame, "About ezWxLua", "ezWxLua V0.0.1" )
end

function fnOpen() 
    local path = OpenFileDialog( appWin.frame )
    print(path)
    if path ~= nil then
        appWin.ctrl.text.Clear()
        appWin.ctrl.text.AppendText(path)
    end
end

function fnToggle() 
    local ctrl = GetControl('toggle')
    if ctrl.GetValue() then
        ctrl.SetLabel('On')
    else
        ctrl.SetLabel('Off')
    end
end

function fnCheckBox() 
    local wxCtrl = GetControl('checkbox')
    if wxCtrl.GetValue() then
        wxCtrl.SetLabel('CheckOn')
    else
        wxCtrl.SetLabel('CheckOff')
    end
end


function fnStart() 
    appWin.StartTimer(0)
end

fnTimer_index = 0
function fnTimer()
    appWin.ctrl.list.AddRow( {
        string.format("Time:%d", fnTimer_index),
        string.format("Diff:%d", fnTimer_index),
    } )
    
    appWin.SetStatusText( string.format("Timer: %d", fnTimer_index), 0 )
    fnTimer_index = fnTimer_index + 1
    if fnTimer_index > 300 then
        appWin.StopTimer()
    end
end

function fnChoice()
    Message( appWin.frame, "About Choice", GetControl('choice').GetText() )
end

function fnComboBox()
    Message( appWin.frame, "About ComboBox", GetControl('combobox').GetText())
end

function fnListBox()
    local ctrl = GetControl('listbox')
    local count = ctrl.GetCount()
    local value = ""
    for i = 1, count do
        if ctrl.IsSelected(i-1) then
            value = value .. " " .. ctrl.GetString(i-1)
        end
    end
    Message( appWin.frame, "About ListBox", value)
end

function fnListCtrl()
    local ctrl = GetCtrl('list')
    local items = ctrl.GetSelectedItems()
    local value = ""
    for i = 1, #items do
        value = value .. " " .. items[i]
    end
    Message( appWin.frame, "About ListCtrl", value)
end

function fnCheckListBox()
    local ctrl = GetControl('checklist')
    local count = ctrl.GetCount()
    local value = ""
    for i = 1, count do
        if ctrl.IsChecked(i-1) then
            value = value .. " " .. ctrl.GetString(i-1)
        end
    end
    Message( appWin.frame, "About ListBox", value)
end

function fnRadioBox()
    local ctrl = GetControl('radiobox')
    Message( appWin.frame, "About RadioBox", tostring(ctrl.GetSelection()) .. " " .. ctrl.GetText())
end

function fnFileDrop(filenames)
    local ctrl = GetControl('text')
    ctrl.SetValue(filenames[1]) 
end

function fnCopyFilePath()
    local fpick = GetControl('filepick')
    local stc = GetControl('stc')
    stc.AppendText( fpick.GetValue() )
end

function fnCopyDirPath()
    local fpick = GetControl('dirpick')
    local stc = GetControl('stc')
    stc.AppendText( fpick.GetValue() )
end

function main()
    local menu = { 
        { Name = "File", Value = {
                { Name = "Exit" , Value = fnExit, Icon='exit' } 
            }
        },
        { Name = "Help", Value = {
                { Name = "About", Value = fnAbout, Icon='help' }
            }
        } 
    }    
    local tool = {
        { Name = "Exit", Value = fnExit, Icon='exit', ToolTip="Quit Program" },
        { Name = "-" },
        { Name = nil, Value = fnAbout, Icon='help', ToolTip="About this Program" },
    }
    local main_layout = { expand=1, border=1 } 
    local list_menu = {
        { Name = "Exit" , Value = fnExit, Icon='exit' }
    }
    local listctrl_menu = {
        { Name = "Show Selected Items" , Value = fnListCtrl }
    }    
    local left = { -- vbox
            { -- hbox
                { name="Table", key="list", menu=listctrl_menu, layout=main_layout },
                { expand=1}
            },
            { expand=1 }
        }
    local right = { --vbox
            { -- hbox
                { name="StyledText", key="stc", layout=main_layout },
                { expand=1 }
            },
            { expand=1}
        }
    local content = { -- vbox
        { -- hbox
            { name="StaticText", label="  File  ",  },
            { name="TextField", key="text", label="Text", layout=main_layout, bgcolor={140,240,140}, filedrop=fnFileDrop },
            { name="Button", label="Open", handler=fnOpen,   },
            { name="ToggleButton", key='toggle', label="On", handler=fnToggle,   },
            { name="CheckBox", key='checkbox', label="CheckOn", handler=fnCheckBox,   },
        },
        { -- hbox
            { name="StaticText", label="  File  ",  },
            { name='FilePicker', key='filepick', label="C:\\a.txt", layout=main_layout },
            { name="Button", label="Copy", handler=fnCopyFilePath,   },
        },        
        { -- hbox
            { name="StaticText", label="  Folder  ",  },
            { name='DirPicker', key='dirpick', label="", layout=main_layout },
            { name="Button", label="Copy", handler=fnCopyDirPath,   },
        },        
        { -- hbox
            { name='Choice', key='choice', items={'apple','grape'}, value=1, handler=fnChoice },
            { name='ComboBox', key='combobox', items={'apple','grape'}, value="apple", handler=fnComboBox },
        },        
        { -- hbox
            { name='ListBox', key='listbox', items={'apple','grape'}, menu=list_menu, handler=fnListBox },
            { name='CheckListBox', key='checklist', items={'apple','grape'}, menu=list_menu, handler=fnCheckListBox },
            { name='RadioBox', key='radiobox', label='RadioBox', items={'apple','grape'}, value=1, menu=list_menu, handler=fnRadioBox },
        },
        { -- hbox
            { name="HSplit", key="split", children={left, right}, layout=main_layout },
            { expand=1 }
        },
        { -- hbox
            { name="Spacer",  },
            { name="Button", label="Start", tooltip="Make dummy list data", handler=fnStart,   },
        },
    }
    local layout = {
        menubar = menu,
        toolbar = tool,
        statusbar = 2,
        content = content,
    }

    appWin = Window("ezWxLua",exit_xpm,layout,800,600,10)
    appWin.SetTimer(fnTimer)
    appWin.ctrl.list.AddColumns( { "Time", "Diff" }, { 150, 150 } )
    appWin.Show()
    appWin.Run()
end

main() 
