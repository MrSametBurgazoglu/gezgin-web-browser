#!/usr/bin/env python
#-*-coding:utf-8-*-

import pygtk
pygtk.require20()
import gtk
import gobject

class IlkPencere(object):
    def __init__(self):
        gobject.threads_init()
        self.pencere = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.pencere.connect("delete_event", gtk.main_quit)
        self.pencere.set_position(gtk.WIN_POS_CENTER) 
        self.pencere.set_title("Gezgin Hata")
        self.pencere.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#204A87"))
        self.pencere.set_border_width(15)
        self.pencere.resize(500, 100)
        self.pencere.set_position(gtk.WIN_POS_CENTER)

        self.label = gtk.Label("Gezgin Web Tarayıcı bir sorunla karşılaştı\nBu sorunun şunlardan kaynaklanıyor olabilir")
        self.label2 = gtk.Label("Bilgisayarınızın internet bağlantısı olmayabilir")    
        self.label3 = gtk.Label("Site çalışmıyor veya tadilatta olabilir")
        self.label4 = gtk.Label("Bilgisayarınızın antivirisü veya firewall'ı çalışmıyor olabilir")
        
        self.label.set_markup("<span foreground='white'>Gezgin Web Tarayıcı bir sorunla karşılaştı\nBu sorunun şunlardan kaynaklanıyor olabilir</span>")
        self.label2.set_markup("<span foreground='white'>Bilgisayarınızın internet bağlantısı olmayabilir</span>")
        self.label3.set_markup("<span foreground='white'>Site çalışmıyor veya tadilatta olabilir</span>")
        self.label4.set_markup("<span foreground='white'>Bilgisayarınızın antivirisü veya firewall'ı çalışmıyor olabilir</span>")


        self.vbox = gtk.VBox(False, 0)
        self.vbox.pack_start(self.label, False, True, 0)
        self.vbox.pack_start(self.label2, False, True, 0)
        self.vbox.pack_start(self.label3, False, True, 0)
        self.vbox.pack_start(self.label4, False, True, 0)


     
        self.pencere.add(self.vbox)
        self.pencere.show_all()      
 
    def main(self):
        gtk.main()

ilk = IlkPencere()
ilk.main()
