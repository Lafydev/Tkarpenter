"""
* Copyright 2021 Lafydev 
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public
* License as published by the Free Software Foundation; either
* version 3 of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
* General Public License for more details.
*
* You should have received a copy of the GNU General Public
* License along with this program; if not,
* see http :// www . gnu . org /licences / .
"""
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from functools import partial
    
class Proprietes:
        
    def choixcouleur(self,i,events):
        col=colorchooser.askcolor("#cccccc",title="Palette")
        self.text[i].set(col[1])
        self.txtbg.configure(background=col[1])
        
    def __init__(self, root, widg, args, cancel="False"):
        self.root=root
        root.title('Widget ' +str(widg))
        self.top1=Toplevel(root)
        self.args=args
        
        #panedwindow : 2 frame verticaux ( libellés et valeurs)
        self.panOptions=PanedWindow(self.top1,orient=HORIZONTAL,width="200")
        self.panOptions.pack(padx="1m",pady="2m")
        
        self.panlibelles=Frame(self.panOptions,width="100m")
        self.panOptions.add(self.panlibelles)
        self.panlibelles.pack(side="left")
        
        self.panvaleurs=Frame(self.panOptions, width="100m")
        self.panOptions.add(self.panvaleurs)
        self.panvaleurs.pack()
        
        if args!=None: 
            i=0
            self.text={}
            for (option) in args:
                #ex: text="nom" borderwidth="3" relief="groove"
                sep=option.index("=")
                
                self.text[i]=StringVar()
                self.text[i].set(option[sep+1:].strip('"'))
                #print ("index " + str(i) +" " +str(self.text[i].get()))
                nomlabel = option[0:sep]
                #Label
                Label(self.panlibelles,text=nomlabel).pack(side="top",anchor="w", padx="1m",pady="2m")

                #Listbox pour les options finies 
                if (nomlabel =="relief") : 
                    cmbrelief=ttk.Combobox(self.panvaleurs)
                    cmbrelief['values']=["groove", "flat", "raised","ridge","sunken"]
                    cmbrelief.configure(textvariable=self.text[i])
                    #prem par defaut
                    if (str(self.text[i].get())==""):
                        cmbrelief.current(0) 

                    cmbrelief.pack(padx="1m",pady="2m")
                elif (nomlabel=="orient"):
                    cmborient=ttk.Combobox(self.panvaleurs)
                    cmborient['values']=["horizontal", "vertical"]
                    cmborient.configure(textvariable=self.text[i])
                    if (str(self.text[i].get())==""):
                        cmborient.current(0) 
                    cmborient.pack(padx="1m",pady="2m")
                elif (nomlabel=="justify"):
                    cmbjust=ttk.Combobox(self.panvaleurs)
                    cmbjust['values']=["left","right", "center"]
                    cmbjust.configure(textvariable=self.text[i])
                    if (str(self.text[i].get())==""):
                        cmbjust.current(0)
                    cmbjust.pack(padx="1m",pady="2m")
                elif (nomlabel=="selectmode"):
                    cmbsel=ttk.Combobox(self.panvaleurs)
                    cmbsel['values']=["single","browse", "multiple","extended"]
                    cmbsel.configure(textvariable=self.text[i])
                    if (str(self.text[i].get())==""):
                        cmbsel.current(0)
                    cmbsel.pack(padx="1m",pady="2m")
                elif (nomlabel=="state"):
                    #Pb: state boutons different state text
                    cmbstate=ttk.Combobox(self.panvaleurs)
                    if widg in ['Entry']:
                        cmbstate['values']=["normal", "readonly", "disabled"]
                    else:
                        cmbstate['values']=["normal","active", "disabled"]
                    cmbstate.configure(textvariable=self.text[i])
                    if (str(self.text[i].get())==""):
                        cmbstate.current(0)
                    cmbstate.pack(padx="1m",pady="2m")
                elif (nomlabel=="background"):
                     self.txtbg=Entry(self.panvaleurs,width=20, relief="sunken", bd=2,textvariable=self.text[i])
                     self.txtbg.bind("<Button-1>",partial(self.choixcouleur,i))
                     self.txtbg.pack( padx="1m", pady="2m")
                else:    
                    #Zone de texte
                    txt=Entry(self.panvaleurs,width=20, relief="sunken", bd=2, textvariable=self.text[i])
                    txt.pack( padx="1m", pady="2m")
                #dans tous les cas
                i=i+1
        #Bouton Annuler annule la création
        def cancel_callback():
            cancel.set("True")
            self.top1.destroy ()
                
        def ok_callback():
            #enregistrer le nouveau listeoptions
            newlisteoptions=[]
            i=0
            text = ""
            for (option) in args:
                (x,y)= option.split("=")
                text=str(self.text[i].get())
                newlisteoptions.append(x +"=" +'"'+text +'"')
                i=i+1
            self.args=newlisteoptions
            self.top1.destroy ()
                    
        btncancel=Button(self.top1,text="Cancel",underline=0,command=cancel_callback)
        btncancel.pack(side="right",padx=5,pady=5)

        #Bouton OK valide les options
        btnOK=Button(self.top1,text="OK",underline=0,command=ok_callback)
        btnOK.pack(side="right",padx=5,pady=5)
        
        self.top1.transient(self.root)  #pas de bouton reduire la fenetre
        self.top1.grab_status()    #récupere les interractions (evite interraction avec root )
        self.root.wait_window(self.top1) #attends que top1 ait fini pour agir sur root
        
if __name__=='__main__':
    root=Tk()
    #tests
    cancel = StringVar()
    def lancer():
        opt=Proprietes(root,"Label",{'text="test properties"', 'background="#cccccc"', 'pack="left"'},cancel=cancel)
        print ("cancel:"+str(cancel.get()))
        
        
    btn=Button(root,text="Run Options",command=lancer)
    btn.pack(padx=5,pady=5)
    root.mainloop()
    
