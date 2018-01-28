#!/usr/bin/env python
#-*-coding:utf-8-*-

import threading
import sys
from gi.repository import Gtk, Gdk, WebKit2, GObject, GLib
import os 
from os import name
import urllib
import re
import time
import sqlite3

page_title = "HOME"
root = False

vt = sqlite3.connect("user/history.db")
im = vt.cursor()

vt2 = sqlite3.connect("user/user.db")
im2 = vt2.cursor()

class DialogExample(Gtk.Dialog):
    def __init__(self, parent, *args, **kwargs):
        super(DialogExample, self).__init__(*args, **kwargs)
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0) 

        self.set_default_size(500, 400)
    
        self.add_button("Kaydet", Gtk.ResponseType.OK)
        self.add_button("İptal", Gtk.ResponseType.CANCEL)

        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        stack.set_homogeneous(True)

        stackswitcher = Gtk.StackSwitcher()
        stackswitcher.set_stack(stack)   

        self.vbox2 = Gtk.VBox(False)
   
        self.label = Gtk.Label(label="Yazı ayarları")

        self.font = Gtk.FontButton(title="Yazım ayarları")

        self.label2 = Gtk.Label(label="Toolbar rengi")

        self.color = Gtk.ColorButton()

        self.label3 = Gtk.Label(label="Notebook aktif rengi")

        self.color2 = Gtk.ColorButton()

        self.label4 = Gtk.Label(label="Notebook rengi")

        self.color3 = Gtk.ColorButton()

        self.label5 = Gtk.Label(label="Entry Yazı rengi")

        self.color4 = Gtk.ColorButton()

        self.vbox2.pack_start(self.label, False, True, 0)
        self.vbox2.pack_start(self.font, False, True, 0)
        self.vbox2.pack_start(self.label2, False, True, 0)
        self.vbox2.pack_start(self.color, False, True, 0)
        self.vbox2.pack_start(self.label3, False, True, 0)
        self.vbox2.pack_start(self.color2, False, True, 0)
        self.vbox2.pack_start(self.label4, False, True, 0)
        self.vbox2.pack_start(self.color3, False, True, 0)
        self.vbox2.pack_start(self.label5, False, True, 0)
        self.vbox2.pack_start(self.color4, False, True, 0)
        self.vbox2.show()

        self.vbox3 = Gtk.VBox()

        self.entry = Gtk.Entry()
        self.entry.set_input_purpose(Gtk.InputPurpose.URL)
        self.entry.set_text("about:blank")

        self.entry2 = Gtk.Entry()
        self.entry2.set_input_purpose(Gtk.InputPurpose.URL)
        self.entry2.set_text("http://www.google.com.tr")
        
        self.label6 = Gtk.Label(label="Açılış sayfanızı ayarlayın:")
        self.label7 = Gtk.Label(label="Dilinizi Ayarlayın Not:Diliniz bilgisayarınızda kullanılan dile göre otamatik ayarlanmıştır:")
        self.label8 = Gtk.Label(label="Yeni sekmenizde açılacak url'yi ayarlayın:")
        self.label9 = Gtk.Label(label="Dosyaların kayıt yeri ")
        self.label10 = Gtk.Label(label="Gezgin açıldığında yapılacak eylemi belirtin")
 
        liststore = Gtk.ListStore(str)
	for item in ["Türkçe", "İngilizce"]:
            liststore.append([item])

	self.combobox = Gtk.ComboBox(model=liststore)
	if name == 'nt':
           self.language = os.environ['LANGUAGE']
           if self.language == "tr":
              self.combobox.set_active(0)
           else:
              self.combobox.set_active(1)
        if name == 'posix':
           self.language = os.environ['LANGUAGE']
           if self.language == "tr":
              self.combobox.set_active(0)
           else:
              self.combobox.set_active(1)

	self.cellrenderertext = Gtk.CellRendererText()
	self.combobox.pack_start(self.cellrenderertext, True)
	self.combobox.add_attribute(self.cellrenderertext, "text", 0)

        liststore2 = Gtk.ListStore(str)
	for item2 in ["Boş sayfayı aç", "Açılış sayfasını aç", "Son kullandığım sekmeleri aç --Not: Yanlızca birden fazla sekme açıkken gezgini kapattığınızda çalışır"]:
            liststore2.append([item2])

	self.combobox2 = Gtk.ComboBox(model=liststore2)
	self.combobox2.set_active(0)

	self.cellrenderertext2 = Gtk.CellRendererText()
	self.combobox2.pack_start(self.cellrenderertext2, True)
	self.combobox2.add_attribute(self.cellrenderertext2, "text", 0)

        self.entry3 = Gtk.Entry()
        if name == 'posix':   
           self.home_path = os.environ['HOME']
        if name == 'nt':
           self.home_path = os.environ['HOME']
        self.entry3.set_text(self.home_path)

        self.vbox3.pack_start(self.label6, False, True, 0)
        self.vbox3.pack_start(self.combobox2, False, True, 0)
        self.vbox3.pack_start(self.label8, False, True, 0)
        self.vbox3.pack_start(self.entry, False, True, 0)
        self.vbox3.pack_start(self.label7, False, True, 0)
        self.vbox3.pack_start(self.combobox, False, True, 0)
        self.vbox3.pack_start(self.label10, False, True, 0)        
        self.vbox3.pack_start(self.entry2, False, True, 0)
        self.vbox3.pack_start(self.label9, False, True, 0)
        self.vbox3.pack_start(self.entry3, False, True, 0)
        
        self.vbox3.show()

        self.vbox4 = Gtk.VBox()

        self.label11 = Gtk.Label(label="Özelleştirebilmek için yönetici olmalısınız")

        self.user_image = Gtk.Image()
        self.user_image.set_from_file("user/user.png")      
   
        self.label12 = Gtk.Label(label="Kullanıcının Adı")
	self.label13 = Gtk.Label(label="Kullanıcının Mail'i")
	self.label14 = Gtk.Label(label="Kullanıcının dil'i")
        self.label15 = Gtk.Label(label="Kullanıcının parolası")

        self.entry4 = Gtk.Entry()
        self.entry5 = Gtk.Entry()
        self.entry6 = Gtk.Entry()
	self.entry7 = Gtk.Entry()

        self.entry4.set_editable(False)
        self.entry5.set_editable(False)
        self.entry6.set_editable(False)
        self.entry7.set_editable(False)

	self.entry7.set_visibility(False)

        self.vbox4.pack_start(self.label11, False, True, 0)
        self.vbox4.pack_start(self.user_image, False, True, 0)
        self.vbox4.pack_start(self.label12, False, True, 0)
        self.vbox4.pack_start(self.entry4, False, True, 0)
        self.vbox4.pack_start(self.label13, False, True, 0)
        self.vbox4.pack_start(self.entry5, False, True, 0)
        self.vbox4.pack_start(self.label14, False, True, 0)
        self.vbox4.pack_start(self.entry6, False, True, 0)
        self.vbox4.pack_start(self.label15, False, True, 0)
        self.vbox4.pack_start(self.entry7, False, True, 0)
       
        self.vbox4.show()

        self.vbox5 = Gtk.VBox()

        self.label16 = Gtk.Label(label="Varsayılan arama motorunuzu belirleyin")
        self.label17 = Gtk.Label(label="Ayrıca adres çubuğuna arama motoru kısaltmaları koyarak'ta arama yapabilirsiniz\n")
        
        liststore3 = Gtk.ListStore(str)
	for item3 in ["Google", "Vikipedia", "Bing", "Youtube"]:
            liststore3.append([item3])

        self.combobox3 = Gtk.ComboBox(model=liststore3)
        self.combobox3.set_active(0)

	self.cellrenderertext3 = Gtk.CellRendererText()
	self.combobox3.pack_start(self.cellrenderertext3, True)
	self.combobox3.add_attribute(self.cellrenderertext3, "text", 0)

        self.g_label = Gtk.Label()
        self.g_label.set_text("Google     G:\n")
        self.v_label = Gtk.Label()
        self.v_label.set_text("Vikipedia     V:\n")
        self.b_label = Gtk.Label()
        self.b_label.set_text("Bing     B:\n")
        self.y_label = Gtk.Label()
        self.y_label.set_text("Youtube     Y:\n")

        self.label18 = Gtk.Label(label="Örnek\nG: hava durumu")

        self.vbox5.pack_start(self.label16, False, True, 0)
        self.vbox5.pack_start(self.combobox3, False, True, 0)
        self.vbox5.pack_start(self.label17, False, True, 0)
        self.vbox5.pack_start(self.g_label, False, True, 0)
        self.vbox5.pack_start(self.v_label, False, True, 0)
        self.vbox5.pack_start(self.b_label, False, True, 0)
        self.vbox5.pack_start(self.y_label, False, True, 0)
        self.vbox5.pack_start(self.label18, False, True, 0)


        self.vbox5.show()         

        stack.add_titled(self.vbox4, "Kullanıcı Ayarları", "Kullanıcı Ayarları")
        stack.add_titled(self.vbox2, "Görünüm Ayarları", "Görünüm Ayarları")
        stack.add_titled(self.vbox3, "Dil ve Web Ayarları", "Dil Ve Web Ayarları")
        stack.add_titled(self.vbox5, "Arama Motoru Ayarları", "Arama Motoru Ayarları")

        box = self.get_content_area()
        box.add(stackswitcher)
        box.add(stack)
        self.show_all()

        im2.execute("""SELECT * FROM web_informations""")

        data2 = im2.fetchall()

        self.data3 = data2[0] 

        self.a = self.data3[0]
        self.b = self.data3[1]
        self.c = self.data3[2]
        self.d = self.data3[3]
        self.e = self.data3[4]
        if len(self.a) > 0:
           self.entry.set_text(self.a)
        if len(self.b) > 0:
           self.entry2.set_text(self.b)
        if len(self.c) > 0:
           if self.c == "0":
              self.combobox.set_active(0)
           if self.c == "1":
              self.combobox.set_active(1)
        if len(self.d) > 0:
           if self.d == "0":
             self.combobox2.set_active(0)
           if self.d == "1":
             self.combobox2.set_active(1)
           else: 
             self.combobox2.set_active(2) 
        if len(self.e) > 0:
          self.entry3.set_text(self.e)   

class BrowserTab(Gtk.VBox):
    
    abc =  0

    def __init__(self, *args, **kwargs):
        super(BrowserTab, self).__init__(*args,**kwargs)

        GObject.threads_init()
        Gdk.threads_init()

        self.toolbar = Gtk.Toolbar()

        self.user2_image = Gtk.Image()
        self.user2_image.set_from_file("library/png/user.png")
        self.user2_button = Gtk.ToolButton()
        self.user2_button.set_icon_widget(self.user2_image)
        self.user2_button.connect("clicked", self.user2)
        self.toolbar.insert(self.user2_button, 0)

        self.home_image = Gtk.Image()
        self.home_image.set_from_file("library/png/home_image.png")
        self.home_button = Gtk.ToolButton()
        self.home_button.set_icon_widget(self.home_image)
        self.home_button.connect("clicked", self.home_page)
        self.toolbar.insert(self.home_button, 1)

        self.back_image = Gtk.Image()
        self.back_image.set_from_file("library/png/back_image.png")
        self.back_button = Gtk.ToolButton()
        self.back_button.set_icon_widget(self.back_image)
        self.back_button.connect("clicked", self.go_back)
        self.toolbar.insert(self.back_button, 2)

        self.forward_image = Gtk.Image()
        self.forward_image.set_from_file("library/png/forward_image.png")        
        self.forward_button = Gtk.ToolButton()
        self.forward_button.set_icon_widget(self.forward_image)        
        self.forward_button.connect("clicked", self.go_forward)
        self.toolbar.insert(self.forward_button, 3)        
        


        liststore = Gtk.ListStore(str)
        for item in ["www.google.com.tr", "www.facebook.com", "www.facebook.com.tr", "www.google.com", "www.youtube.com.tr", "www.hurriyet.com.tr", "www.milliyet.com.tr", "www.twitter.com", "www.sahibinden.com", "www.eksisozluk.com", "www.sabah.com.tr", "www.haber7.com", "www.mynet.com", "www.r10.net", "yandex.com.tr", "www.wikipedia.org", "www.instagram.com", "www.oyunskor.com", "www.sozcu.com.tr",
"www.ensonhaber.com","www.haberturk.com", 
"www.gittigidiyor.com", "www.internethaber.com", "www.donanimhaber.com", 
"www.n11.com.tr", "www.haberler.com", "www.hepsiburada.com", "www.garanti.com.tr", "www.sporx.com", "www.linkedin.com.tr",
"www.radikal.com.tr", "www.fanatik.com.tr", "www.uludagsozluk.com",
"www.gazetevatan.com", "www.hurriyetemlak.com", "www.ntv.com.tr",
"www.meb.gov.tr", "www.samanyolu.com", "www.wordpress.com",
"www.yahoo.com", "www.cumhuriyet.com.tr", "www.msn.com", 
"www.imdb.com", "www.cnnturk.com", "www.hdfilmfullizle.com.tr",
"www.tumblr.com", "www.shiftdelete.com", "www.dailymotion.com",
"www.ntvspor.net", "www.acun.com.tr", "www.izlesene.com.tr", 
"www.amazon.com.tr", "www.akakce.com", "www.fotomac.com.tr",
"www.tamindir.com"]:
             liststore.append([item])


        self.entrycompletion = Gtk.EntryCompletion()
        self.entrycompletion.set_model(liststore)
        self.entrycompletion.set_text_column(0)

        self.toolitem = Gtk.ToolItem()
        self.address_bar = Gtk.Entry()
        self.address_bar.connect("activate", self._load_url)
        self.address_bar.set_completion(self.entrycompletion)
        url2 = self.address_bar.get_text()
        self.address_bar.set_width_chars(95)
        self.address_bar_image = Gtk.Image()
        self.address_bar_image.set_from_file("library/png/go.png")
        self.address_bar_image2 = self.address_bar_image.get_pixbuf()
        self.address_bar.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, self.address_bar_image2)
        self.address_bar.connect("icon-press", self._load_url2)
        self.toolitem.add(self.address_bar)
        self.toolbar.insert(self.toolitem, 4)

        self.refresh_image = Gtk.Image()
        self.refresh_image.set_from_file("library/png/refresh_image.png")
        self.refresh_button = Gtk.ToolButton()
        self.refresh_button.set_icon_widget(self.refresh_image)
        self.refresh_button.connect("clicked", self.reload)
        self.toolbar.insert(self.refresh_button, 5) 
        
        self.stop_image = Gtk.Image()
        self.stop_image.set_from_file("library/png/stop_image.png") 
        self.stop_button = Gtk.ToolButton()
        self.stop_button.set_icon_widget(self.stop_image)
        self.stop_button.connect("clicked", self.stop_loading)
        self.toolbar.insert(self.stop_button, 6) 
        
        self.toolitem2 = Gtk.ToolItem()
        self.search_bar = Gtk.Entry()
        self.search_bar.connect("activate", self.search2)
        self.search_bar.set_width_chars(30)
        self.toolitem2.add(self.search_bar)
        self.toolbar.insert(self.toolitem2, 7)

        self.download_image = Gtk.Image()
        self.download_image.set_from_file("library/png/download_image.png")
        self.download_button = Gtk.ToolButton()
        self.download_button.set_icon_widget(self.download_image)
        self.toolbar.insert(self.download_button, 8) 

        self.preferences_menu_image = Gtk.Image()
        self.preferences_menu_image.set_from_file("library/png/settings_image.png")
        self.preferences_menu_button = Gtk.ToolButton()
        self.preferences_menu_button.set_icon_widget(self.preferences_menu_image)
        self.preferences_menu_button.connect("clicked", self.app)
        self.toolbar.insert(self.preferences_menu_button, 9)

        self.toolbar.show_all() 
        self.webview = WebKit2.WebView()
        self.websettings = self.webview.get_settings()
        self.find = self.webview.get_find_controller()
        sdf = self.webview.get_title()        

        self.webview.connect("load-changed", self.control)
        self.webview.connect("enter-fullscreen", self.enterfullscreen)
        self.webview.connect("leave-fullscreen", self.leavefullscreen)       
        self.webview.connect("notify::title", self.deneme1)
        self.webview.connect("notify::title", self.changed_url)
        self.webview.connect("load-failed", self.deneme3)     

        self.show()
 
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.add(self.webview)
 
        self.toolbar2 = Gtk.Toolbar()

        self.close_image = Gtk.Image()
        self.close_image.set_from_file("library/png/close_image.png") 
        self.close_find_entry = Gtk.ToolButton()
        self.close_find_entry.set_icon_widget(self.close_image)
        self.close_find_entry.connect("clicked", self.toolbar2_hide)
        self.toolbar2.insert(self.close_find_entry, 0)

        self.toolitem2 = Gtk.ToolItem()
        self.find_bar = Gtk.Entry()
        self.find_bar.connect("activate", self.find2)
        self.find_bar.set_width_chars(35)
        self.toolitem2.add(self.find_bar)
        self.toolbar2.insert(self.toolitem2, 1) 

        self.prev_image = Gtk.Image()
        self.prev_image.set_from_file("library/png/prev_image.png")
        self.prev_button = Gtk.ToolButton()
        self.prev_button.set_icon_widget(self.prev_image)
        self.prev_button.connect("clicked", self.find4)
        self.toolbar2.insert(self.prev_button, 2)

        self.next_image = Gtk.Image()
        self.next_image.set_from_file("library/png/next_image.png")
        self.next_button2 = Gtk.ToolButton()
        self.next_button2.set_icon_widget(self.next_image)
        self.next_button2.connect("clicked", self.find3)
        self.toolbar2.insert(self.next_button2, 3)  
        
        self.toolbar4 = Gtk.Toolbar()

        self.close_image2 = Gtk.Image()
        self.close_image2.set_from_file("library/png/close2_image.png") 
        self.close_find_entry2 = Gtk.ToolButton()
        self.close_find_entry2.set_icon_widget(self.close_image2)
        self.close_find_entry2.connect("clicked", self.toolbar4_hide)
        self.toolbar4.insert(self.close_find_entry2, 0)

        self.toolitem4 = Gtk.ToolItem()
        self.zoom_entry = Gtk.Entry()
        self.zoom_entry.connect("activate", self.zoom)
        self.zoom_entry.set_width_chars(15)
        zoom_level = self.webview.get_zoom_level()
        self.zoom_entry.set_text(str(zoom_level))
        self.toolitem4.add(self.zoom_entry)
        self.toolbar4.insert(self.toolitem4, 1)

        self.zoom_minus_image = Gtk.Image()
        self.zoom_minus_image.set_from_file("library/png/minus_image.png")
        self.minus_button = Gtk.ToolButton()
        self.minus_button.set_icon_widget(self.zoom_minus_image)
        self.minus_button.connect("clicked", self.zoom_out)
        self.toolbar4.insert(self.minus_button, 2) 
 
        self.zoom_plus_image = Gtk.Image()
        self.zoom_plus_image.set_from_file("library/png/plus_image.png")
        self.plus_button = Gtk.ToolButton()
        self.plus_button.set_icon_widget(self.zoom_plus_image)
        self.plus_button.connect("clicked", self.zoom_in)
        self.toolbar4.insert(self.plus_button, 3)
 
        self.zoom2 = Gtk.ToolButton()
        self.zoom2.set_label("Varsayılan görüntü")
        self.zoom2.connect("clicked", self.zoom3)
        self.toolbar4.insert(self.zoom2, 4)

        self.toolbar5 = Gtk.Toolbar()
        
        self.close_image4 = Gtk.Image()
        self.close_image4.set_from_file("library/png/close_image4.png") 
        self.close_button = Gtk.ToolButton()
        self.close_button.set_icon_widget(self.close_image4)
        self.close_button.connect("clicked", self.app2)
        self.toolbar5.insert(self.close_button, 0)

        self.new_window_image = Gtk.Image()
        self.new_window_image.set_from_file("library/png/new_window_image.png")
        self.new_window_button = Gtk.ToolButton()
        self.new_window_button.set_icon_widget(self.new_window_image)
        self.new_window_button.connect("clicked", self.new_window)
        self.toolbar5.insert(self.new_window_button, 1)

        self.print_image = Gtk.Image()
        self.print_image.set_from_file("library/png/print_image.png")
        self.print_button = Gtk.ToolButton()
        self.print_button.set_icon_widget(self.print_image)
        self.print_button.connect("clicked", self.deneme)
        self.toolbar5.insert(self.print_button, 2)

        self.history_image = Gtk.Image()
        self.history_image.set_from_file("library/png/history_image.png")
        self.history_button = Gtk.ToolButton()
        self.history_button.set_icon_widget(self.history_image)
        self.history_button.connect("clicked", self.history2)
        self.toolbar5.insert(self.history_button, 3)

        self.fullscreen_image = Gtk.Image()
        self.fullscreen_image.set_from_file("library/png/fullscreen_image.png")
        self.fullscreen_button = Gtk.ToolButton()
        self.fullscreen_button.set_icon_widget(self.fullscreen_image)
        self.fullscreen_button.connect("clicked", self.fullscreen2)
        self.toolbar5.insert(self.fullscreen_button, 4)

        self.unfullscreen_image = Gtk.Image()
        self.unfullscreen_image.set_from_file("library/png/unfullscreen_image.png")
        self.unfullscreen_button = Gtk.ToolButton()
        self.unfullscreen_button.set_icon_widget(self.unfullscreen_image)
        self.unfullscreen_button.connect("clicked", self.unfullscreen2)
        self.toolbar5.insert(self.unfullscreen_button, 5)
        
        self.find_image = Gtk.Image()
        self.find_image.set_from_file("library/png/find_image.png")
        self.find_button = Gtk.ToolButton()
        self.find_button.set_icon_widget(self.find_image)
        self.find_button.connect("clicked", self.find0)
        self.toolbar5.insert(self.find_button, 6)

        self.preferences_image = Gtk.Image()
        self.preferences_image.set_from_file("library/png/preferences_image.png")
        self.preferences_button = Gtk.ToolButton()
        self.preferences_button.set_icon_widget(self.preferences_image)
        self.preferences_button.connect("clicked", self.preferences)
        self.toolbar5.insert(self.preferences_button, 7)

        self.developer_image = Gtk.Image()
        self.developer_image.set_from_file("library/png/developer_image.png")
        self.developer_button = Gtk.ToolButton()
        self.developer_button.set_icon_widget(self.developer_image)
        self.developer_button.connect("clicked", self.developer)
        self.toolbar5.insert(self.developer_button, 8)
        
        self.pack_start(self.toolbar, False, False, 0)       
        self.pack_start(self.scrolled_window, True, True, 0)
        self.pack_start(self.toolbar4, False, False, 0)
        self.pack_start(self.toolbar2, False, False, 0)
        self.pack_start(self.toolbar5, False, False, 0)

        self.scrolled_window.show_all()

    def _load_url(self, widget):
        url = self.address_bar.get_text()
        try:
            url.index("://") 
        except:
            url = "http://"+url
        self.address_bar.set_text(url)
        self.webview.load_uri(url)

    def _load_url2(self, widget, icon_pos, event):
        url = self.address_bar.get_text()
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            try:
                url.index("://") 
            except:
                url = "http://"+url
        	self.address_bar.set_text(url)
        	self.webview.load_uri(url)

    def home_page(self, widget):
        dialog = DialogExample(self)
        a = dialog.entry2.get_text()
        print a
        self.webview.load_uri(a)
        dialog.destroy()

    def go_back(self, widget):
        self.webview.go_back()
    
    def go_forward(self, widget):
        self.webview.go_forward()

    def reload(self, widget):
        self.webview.reload()

    def stop_loading(self, widget):
        self.webview.stop_loading()

    def toolbar2_hide(self, widget):
        self.toolbar2.hide()
        self.find.search_finish()

    def toolbar4_hide(self, widget):
        self.toolbar4.hide()

    def zoom_out(self, widget):
        zoom_level = self.webview.get_zoom_level()
        zoom_level = int(zoom_level) - 1 
        self.webview.set_zoom_level(zoom_level)
        self.zoom_entry.set_text(str(zoom_level))

    def zoom_in(self, widget):
        zoom_level = self.webview.get_zoom_level()
        zoom_level = int(zoom_level) + 1 
        self.webview.set_zoom_level(zoom_level)
        self.zoom_entry.set_text(str(zoom_level))

    def find2(self, widget):
        a = self.find_bar.get_text()
        self.find.search(a, 8, 1000)

    def find3(self, widget):
        self.find.search_next()

    def find4(self, widget):
        self.find.search_previous()  

    def changed_url(self, widget, webview,):
          a = self.webview.get_uri()
          self.address_bar.set_text(a) 

    def zoom(self, widget):
        a = self.zoom_entry.get_text() 
        self.webview.set_zoom_level(float(a))

    def zoom3(self, widget):
        self.webview.set_zoom_level(float(1.0))
        self.zoom_entry.set_text("1.0")
                    
    def close3(self, widget):
        self.toolbar.hide()

    def deneme(self, widget):
        print "deneme"

    def deneme1(self, widget, webview):
        a = self.webview.get_title()
        dosya=open("çalıştır/title.txt", "w")
        dosya.write(a)

    def deneme3(self, widget, webview, url2, sdf):
        os.system('python hata/error.py')

    def app2(self, widget):
        self.toolbar5.hide()

    def app(self, widget):
        self.toolbar5.show_all()

    def new_window(self, widget):
        os.system('cd Masaüstü/gezgin2.0/')
        time.sleep(0.1)
        os.system('python gezgin2.py') 

    def search2(self, widget):
        a = self.search_bar.get_text()
        a = "https://www.google.com.tr/#q=" + a
        self.webview.load_uri(a)

    def history2(self, widget):
        os.system('python user/history.py')

    def fullscreen2(self, widget):
        browser = Browser()
        browser.header_bar.hide()

    def unfullscreen2(self, widget):
        browser = Browser()
        browser.header_bar.show()
   
    def enterfullscreen(self, widget, webview):
        self.toolbar.hide()
        self.toolbar2.hide()
        self.toolbar4.hide()
        self.toolbar5.hide()
    
    def leavefullscreen(self, widget, webview):
        self.toolbar.show() 

    def find0(self, widget):
        self.toolbar2.show()

    def developer(self, widget):
        developerwindow = Gtk.AboutDialog()
        developerwindow.set_program_name("Gezgin Web Browser")
        developerwindow.set_version(str(1.0))
	developerwindow.set_comments("Tamamen python ile geliştirilmiş hızlı güvenilir ve kişileştirilebilir WebBrowser")
	developerwindow.set_authors(["Samet Burgazoğlu"])
      
        image = Gtk.Image()
        image.set_from_file("gezgin.png") 
        image2 = image.get_pixbuf()
        developerwindow.set_logo(image2)

        developerwindow.run()
        developerwindow.destroy()

    def control(self, widget, webview):
        a = self.webview.is_loading()
        if a == True:
          self.stop_button.show()
          self.refresh_button.hide()          
        if a == False:       
          self.stop_button.hide()
          self.refresh_button.show()
          b = self.webview.get_title()
          c = self.webview.get_uri()
          d = time.strftime("%S/%M/%H/%d/%m/%Y")
          veriler = [(b, c, d)]
          for i in veriler:
              im.execute('''INSERT INTO history VALUES %s''' %(i,))
          vt.commit()

    def preferences(self, widget):
        dialog = DialogExample(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
           pass
        if response == Gtk.ResponseType.CANCEL:
           pass

        dialog.destroy()

    def user2(self, widget):
        dialog = Gtk.Dialog(title="Dialog")
	dialog.set_default_size(300, 200)

        self.vbox = Gtk.VBox()

        self.user3_image = Gtk.Image()
        self.user3_image.set_from_file("user/user.png")

        self.hbox = Gtk.HBox()

        self.name_label = Gtk.Label(label="Kullanıcı adı:")
        self.name_entry = Gtk.Entry()
             
        self.hbox.pack_start(self.name_label, False, True, 0)
        self.hbox.pack_start(self.name_entry, False, True, 0)

        self.hbox2 = Gtk.HBox()
 
        self.password_label = Gtk.Label(label="Kullanıcı şifresi:")
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)

        self.hbox2.pack_start(self.password_label, False, True, 0)
        self.hbox2.pack_start(self.password_entry, False, True, 0)

        self.label3 = Gtk.Label(label="Kullanıcı Adı veya parola yanlış")
        self.label3.show()

        self.vbox.pack_start(self.user3_image, False, True, 0)
        self.vbox.pack_start(self.hbox, False, True, 0)
        self.vbox.pack_start(self.hbox2, False, True, 0)
       
        self.vbox.show_all()
         
        box = dialog.get_content_area()
        box.add(self.vbox)

        dialog.add_button("Giriş Yap", Gtk.ResponseType.ACCEPT)

	response = dialog.run()

	if response == Gtk.ResponseType.ACCEPT:
       	 a = self.name_entry.get_text()
       	 b = self.password_entry.get_text()
         if a == "Admin" and b == "000000000":
            dialog.destroy()
         if len(b) < 5:
               print "parola en az 6 karekterli olmalıdır"
         if len(a) == 0:
               print "kullanıcı adı boş bırakılamaz"

class Browser(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)        

        self.set_title("Gezgin Web Browser 1.0")

        self.maximize()

        self.fullscreen()

        self.set_name('browser')

        self.set_hide_titlebar_when_maximized(True)

        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_title("Gezgin Web Browser")
        self.header_bar.set_show_close_button(True)

        self.close_tab_image = Gtk.Image()
        self.close_tab_image.set_from_file("library/png/close_tab.png")
        self.close_tab_button = Gtk.ToolButton()
        self.close_tab_button.set_icon_widget(self.close_tab_image)
        self.close_tab_button.connect("clicked", self._close_current_tab2)
        self.header_bar.add(self.close_tab_button)

        self.add_tab_image = Gtk.Image()
        self.add_tab_image.set_from_file("library/png/add_tab.png")
        self.add_tab_button = Gtk.ToolButton()
        self.add_tab_button.set_icon_widget(self.add_tab_image)
        self.add_tab_button.connect("clicked", self._open_new_tab2)
        self.header_bar.add(self.add_tab_button)

        self.header_bar.show_all()

        self.notebook = Gtk.Notebook()
	
        self.notebook.set_scrollable(True)
        self.notebook.set_show_tabs(True)
        self.notebook.set_show_border(True)
         
        self.tabs = []
	
        self.set_size_request(400,400)

        self.hbox2 = Gtk.HBox()
        self.label = Gtk.Label(label="Yeni sekme")
 
        self.close_image3 = Gtk.Image()
        self.close_image3.set_from_file("library/png/close_image.png")
        self.close_button = Gtk.Button()
        self.close_button.set_image(self.close_image3)
        
        self.hbox2.pack_start(self.label, False, True, 0)
        self.hbox2.pack_start(self.close_button, False, True, 0)

        self.hbox2.show_all()

        self.tabs.append((self._create_tab(), Gtk.Label("Yeni sekme")))
        self.notebook.append_page(*self.tabs[0])

        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self._key_pressed)
        self.notebook.connect("switch-page", self._tab_changed)
 
        self.notebook.show()
        self.show()
 
        self.vbox = Gtk.VBox()
        self.vbox.pack_start(self.header_bar, False, True, 0)
        self.vbox.pack_start(self.notebook, True, True, 0)
        
        self.vbox.show()        

        self.add(self.vbox)
        

        style_provider = Gtk.CssProvider()

        css = '''
        #browser {
             background-color: #204A87;
             border-radius: 10px;
             border-color: #32F740;
        }
        #browser GtkEntry {
              background: #000;
              color: #007BFF;
        }
        #browser GtkNotebook {
              background: #000;
              color: #EEEEEC;
        }
        #browser GtkNotebook tab:active{
              background: #204A87;
        }
        #browser GtkToolbar {
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

    def _tab_changed(self, notebook, current_page, index):
        if not index:
            return
        dosya=open("çalıştır/title.txt")
        title = dosya.readline()
        if title:
            self.set_title(title)
 
    def _title_changed(self, webview, title):
        current_page = self.notebook.get_current_page()
 
        counter = 0
        for tab, label in self.tabs:
            if tab.webview is webview:
                dosya=open("çalıştır/title.txt")
                title2 = dosya.readline()
                label.set_text(str(title2))
                if counter == current_page:
                    self._tab_changed(None, None, counter)
                break
            counter += 1
 
    def _create_tab(self):
        tab = BrowserTab()
        dialog = DialogExample(self)
        a = dialog.entry2.get_text()
        dialog.destroy()
        tab.webview.load_uri(a)
        tab.webview.connect("notify::title", self._title_changed)
        return tab

    def _create_tab2(self):
        tab = BrowserTab()
        tab.webview.connect("notify::title", self._title_changed)
        dialog = DialogExample(self)
        a = dialog.entry.get_text()
        dialog.destroy()
        if a == "about:blank":
           tab.address_bar.set_text("about:blank")
        else:
           tab.webview.load_uri(a) 
        return tab

    def _reload_tab(self):
        self.tabs[self.notebook.get_current_page()][0].webview.reload()
 
    def _close_current_tab(self):
        if self.notebook.get_n_pages() == 1:
            return
        page = self.notebook.get_current_page()
        current_tab = self.tabs.pop(page)
        self.notebook.remove(current_tab[0])
 
    def _open_new_tab(self):
        current_page = self.notebook.get_current_page()
        page_tuple = (self._create_tab2(), Gtk.Label("Yeni sekme"))
        self.tabs.insert(current_page+1, page_tuple)
        self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page+1)
        self.notebook.set_current_page(current_page+1)      

    def _close_current_tab2(self, widget):
        if self.notebook.get_n_pages() == 1:
            return
        page = self.notebook.get_current_page()
        current_tab = self.tabs.pop(page)
        self.notebook.remove(current_tab[0])
 
    def _open_new_tab2(self, widget):
        current_page = self.notebook.get_current_page()
        page_tuple = (self._create_tab2(), Gtk.Label("Yeni sekme"))
        self.tabs.insert(current_page+1, page_tuple)
        self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page+1)
        self.notebook.set_current_page(current_page+1)        
 
    def _focus_url_bar(self):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].url_bar.grab_focus()

    def _zoom_bar(self):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].toolbar4.show_all()
 
    def _raise_find_dialog(self):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].toolbar2.show_all()
        self.tabs[current_page][0].find_bar.grab_focus()

    def _url_bar(self):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].toolbar.show_all()
    
    def _key_pressed(self, widget, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        mapping = {Gdk.KEY_r: self._reload_tab,
                   Gdk.KEY_w: self._close_current_tab,
                   Gdk.KEY_t: self._open_new_tab,
                   Gdk.KEY_l: self._focus_url_bar,
                   Gdk.KEY_b: self._zoom_bar,
                   Gdk.KEY_f: self._raise_find_dialog,
                   Gdk.KEY_g: self._url_bar,
                   Gdk.KEY_q: Gtk.main_quit}
 
        if event.state & modifiers == Gdk.ModifierType.CONTROL_MASK \
          and event.keyval in mapping:
            mapping[event.keyval]()
        
 
if __name__ == "__main__":
    Gtk.init(sys.argv)

    browser = Browser()
 
    Gtk.main()
