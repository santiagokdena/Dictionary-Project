import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import sqlite3
con = sqlite3.connect("dic")
cur = con.cursor()

class Datos():
    def __init__(self,ventana):
        self.ventana=ventana #at
        self.ventana.title('Diccionario')
        self.ventana.geometry('400x200')
        self.ventana.eval('tk::PlaceWindow . center')
        self.framemenu=tk.Frame(self.ventana) #at
        self.framemenu.pack()
        #labels
        tk.Label(self.framemenu,text="Palabra en ingles:").grid(column=0,row=0,padx=5,pady=5,sticky=tk.W+tk.E)
        tk.Label(self.framemenu,text="Palabra en español:").grid(column=0,row=1,padx=5,pady=5,sticky=tk.W+tk.E)
        #entradas
        self.w=tk.Entry(self.framemenu,width=30) #at (word)
        self.w.grid(column=1,row=0,padx=5,pady=5,sticky=tk.W+tk.E) 
        self.w.focus() #el m focus() permite que el cursor se quede en esta entrada
        self.p=tk.Entry(self.framemenu,width=30) #at (palabra)
        self.p.grid(column=1,row=1,padx=5,pady=5,sticky=tk.W+tk.E) 
        #botones
        tk.Button(self.framemenu, text='Cambiar',command=lambda:self.editar()).grid(row=0,column=2,padx=5,pady=5)
        tk.Button(self.framemenu, text='Eliminar',command=lambda:self.delete()).grid(row=1,column=2,padx=5,pady=5)
        self.crear_guardar=tk.Button(self.framemenu, text='Crear',command=lambda:self.agregar())
        self.crear_guardar.grid(column=0,row=2,pady=5,padx=5,sticky=tk.W+tk.E)
        tk.Button(self.framemenu,text='Buscar',command=lambda:self.buscar()).grid(row=2,column=1,pady=5,padx=5,sticky=tk.W+tk.E)
        
        #marco
        tk.LabelFrame(self.framemenu).grid(row=3,column=0,columnspan=2)
        #tabla y scroll
        self.tabla=ttk.Treeview(self.framemenu,columns=('c1','c2')) #at
        self.sc=tk.Scrollbar(self.framemenu)
        self.sc.config(command=self.tabla.yview)
        self.tabla.config(yscrollcommand=self.sc.set)
        #boton de tabla
        self.bt=tk.Button(self.framemenu,text='Mostrar tabla',command=lambda:switch_tabla())  #at
        self.bt.grid(row=4,column=0,columnspan=2,sticky=tk.E+tk.W)
        def switch_tabla():   
            if  self.bt['text']=='Mostrar tabla':
                
                #ajusta el boton
                self.bt.grid(row=5,column=0,columnspan=2,sticky=tk.E+tk.W)
                self.bt.config(text='Ocultar tabla')
                #ajusta la tabla y scroll
                self.tabla.grid(column=0,row=4,columnspan=2)
                self.sc.grid(column=2,row=4,sticky='nsew')
                #headers
                self.head=[True,True,True]
                self.tabla.heading("#0",text="Word",anchor=tk.CENTER,command=lambda:ordenar('ping',0)) #el 1 argumento es la columna
                self.tabla.heading("c1",text="Palabra",anchor=tk.CENTER,command=lambda:ordenar('pesp',1))
                self.tabla.heading("c2",text="Fecha de Creación",anchor=tk.CENTER,command=lambda:ordenar('fecha',2))
                
                self.actualizar_tabla()
                #evento dobleclick 
                #en los eventos no se pone ()
                self.tabla.bind("<Double-Button-1>",doubleclick) #(1) click derecho (Double-Button) selecciona el registro especifico
                
                #ajusta el tamaño de la ventana
                self.ventana.geometry('670x400')
            else:
                self.tabla.destroy()
                self.sc.destroy()
                #ajusta el boton
                self.bt.config(text='Mostrar tabla')
                self.bt.grid(row=4,column=0,columnspan=2,sticky=tk.E+tk.W)
                #crea la tabla y scroll sin agregarla
                self.tabla=ttk.Treeview(self.framemenu,columns=('c1','c2')) 
                self.sc=tk.Scrollbar(self.framemenu)
                #ajustes tabla,scroll
                self.sc.config(command=self.tabla.yview)
                self.tabla.config(yscrollcommand=self.sc.set)
                #ajusta el tamaño de la ventana
                self.ventana.geometry('400x200')
        def doubleclick(event):
            self.w.delete(0,tk.END)
            self.p.delete(0,tk.END)
            self.w.insert(0,self.tabla.item(self.tabla.selection())['text']) #inserta la seleccion en los entrys
            clave=self.tabla.item(self.tabla.selection())['values'][0] #values contiene una tupla con el indice 0 indicando la palabra
            self.p.insert(0,clave)
        def ordenar(tipo,ind):
            if self.head[ind]:
                s=" ORDER BY "+tipo+" DESC"
                self.head[ind]=False
            else:
                s=""
                self.head[ind]=True
            self.actualizar_tabla(s)
    def is_in(self):
       cur.execute("SELECT * FROM Palabras WHERE ping='"+self.w.get()+"' and pesp='"+self.p.get()+"'") #and
       rows= cur.fetchone()
       if rows is None:
           return False
       else:
           return True
    def agregar(self):
        if self.verificar_ent():
            if not self.is_in():
                cur.execute("INSERT INTO Palabras (ping,pesp,fecha) VALUES (?,?,datetime('now','localtime'))",(self.w.get(),self.p.get()))
                con.commit()
                mb.showinfo('Mensaje','Palabras guardadas satisfactoriamente')
            else:
                mb.showerror('Error','La palabra o palabras digitadas ya existen')
            self.w.delete(0,tk.END)
            self.p.delete(0,tk.END)
            self.actualizar_tabla()
            self.w.focus()
    def delete(self):
        if self.verificar_ent():
            if self.is_in():
                cur.execute("DELETE FROM Palabras Where ping='"+self.w.get()+"' or pesp='"+self.p.get()+"'")
                con.commit()
                mb.showinfo('Mensaje','Palabras eliminadas satisfactoriamente')
            else:
                mb.showerror('Error','La palabra o palabras digitadas no existen')
            self.w.delete(0,tk.END)
            self.p.delete(0,tk.END)
            self.w.focus() #el cursor apunta a w
            self.actualizar_tabla()
    def verificar_ent(self):
        if len(self.w.get())==0 or len(self.p.get())==0:
            mb.showerror('Error','Usted no ha digitado palabras en ninguno de los dos campos')
            return False
        return True
    def editar(self):
        cur.execute("SELECT * FROM Palabras WHERE ping='"+self.w.get()+"' and pesp='"+self.p.get()+"'")
        row=cur.fetchone()
        if row is not None:
            self.w_antigua=str(self.w.get())
            self.crear_guardar['text']='Guardar'
            self.crear_guardar['command']=lambda:self.guardar()
        else:
            mb.showerror('Error','La palabra o palabras digitadas no existen')
    def guardar(self):
        cur.execute("UPDATE Palabras SET ping='"+self.w.get()+"',pesp='"+self.p.get()+"' WHERE ping='"+self.w_antigua+"'")
        con.commit()
        self.actualizar_tabla()
        self.crear_guardar['text']='Crear'
        self.crear_guardar['command']=lambda:self.agregar()
    def actualizar_tabla(self,cadena=""):
        s="SELECT ping,pesp,fecha FROM Palabras "+cadena
        registros=self.tabla.get_children() 
        for registro in registros: #elimina los registros anteriores
            self.tabla.delete(registro)
        for (word,palabra,date) in cur.execute(s): #carga las palabras de la bd  
            print(word,palabra,date)
            self.tabla.insert('',0,text=word,values=(palabra,date)) #the string is pass it as a tuple...
    def buscar(self):
        cadena=" WHERE 1=1"
        if len(self.w.get())>0:
            cadena+=" AND ping LIKE '%"+self.w.get()+"%'"
        if len(self.p.get())>0:
            cadena+=" AND pesp LIKE '%"+self.p.get()+"%'"
        self.actualizar_tabla(cadena)
#segun el usuario vaya buscando, que el Treeview se actualice con segun las claves de busqueda

root = tk.Tk()   
Datos(root)
root.mainloop()
cur.close()
         
