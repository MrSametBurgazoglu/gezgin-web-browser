#!/usr/bin/env python
#-*-coding:utf-8-*-

from gi.repository import Gtk, Gdk
import sys
import os
import sqlite3

class History(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(History, self).__init__(*args, **kwargs)        

        self.set_title("history")
        self.set_name('history')
        self.set_size_request(600,1000)
        self.move(1366,200)
        
        self.connect("destroy", Gtk.main_quit)
        self.show()   

        style_provider = Gtk.CssProvider()

        css = '''
        #history {
             background-color: #204A87;
        }
        #history GtkEntry {
              background: #000;
              color: #204A87;
        }
        #history GtkNotebook {
              background: #204A87;
              color: #EEEEEC;
        }      
        '''
        
        style_provider.load_from_data(css)
      
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), 
            style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )     

        vt = sqlite3.connect("history.db")
        im = vt.cursor()
        im.execute("""SELECT * FROM history""")

        data = im.fetchall()
        f = len(data)

        liststore = Gtk.ListStore(str, str, str)    

        sayi = 0

        for i in range(f):
         a = data[sayi]
         b = a[0] 
         c = a[1]
         d = a[2]
         liststore.append([b, c, d])
         sayi += 1            

	self.treeview = Gtk.TreeView(model=liststore)
	self.treeviewcolumn = Gtk.TreeViewColumn("Başlık")
	self.treeview.append_column(self.treeviewcolumn)
	self.cellrenderertext = Gtk.CellRendererText()
	self.treeviewcolumn.pack_start(self.cellrenderertext, False)
	self.treeviewcolumn.add_attribute(self.cellrenderertext, "text", 0)
	self.treeviewcolumn = Gtk.TreeViewColumn("Adres")
	self.treeview.append_column(self.treeviewcolumn)
	self.cellrenderertext = Gtk.CellRendererText()
	self.treeviewcolumn.pack_start(self.cellrenderertext, False)
	self.treeviewcolumn.add_attribute(self.cellrenderertext, "text", 1)
	self.treeviewcolumn = Gtk.TreeViewColumn("Zaman")
	self.treeview.append_column(self.treeviewcolumn)
	self.cellrenderertext = Gtk.CellRendererText()
	self.treeviewcolumn.pack_start(self.cellrenderertext, True)
	self.treeviewcolumn.add_attribute(self.cellrenderertext, "text", 2)


        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.add(self.treeview)
 
        self.add(self.scrolled)
        self.show_all()

if __name__ == "__main__":
    Gtk.init(sys.argv)

    history = History()
 
    Gtk.main()
