import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import filedialog as fd
import warnings
import tkinter.messagebox as ms
from evaluator import Evaluator
from datetime import datetime


class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.initStyle()
        self.df = self.load_df()
        self.mainWin(self.df)
        self.root.mainloop()
        

    def initStyle(self):
        self.style = ttk.Style()
        self.root.config(
            bg= "#5EABDF"
        )
        self.root.geometry("296x245")

    def mainWin(self, df):
        
        self.opt_var = tk.StringVar()

        self.lista_prov = ["Elija un proveedor"] + df["proveedor"].drop_duplicates().to_numpy().tolist()

        self.main_frame = ttk.Frame(self.root, padding=30)
        self.main_frame.pack()
                
        title_label = ttk.Label(self.main_frame, text="SISTEMA DE ANALISIS DE PROVEEDORES")
        title_label.grid(row=0, column=0, padx=10, pady=2)

        prov_opt = ttk.OptionMenu(self.main_frame, self.opt_var, self.lista_prov[0], *self.lista_prov)
        prov_opt.grid(row=4, column=0, padx=10, pady=2)

        button_OK = ttk.Button(self.main_frame, text="Aprovación de Proveedor", command=lambda: self.evalOK(self.df, self.opt_var.get()))
        button_OK.grid(row=5, column=0, padx=10, pady=2)
 
        button_evalProv = ttk.Button(self.main_frame, text="Evaluar Proveedor", command=lambda: self.manual_form(self.df, self.opt_var.get()))
        button_evalProv.grid(row=6, column=0, padx=10, pady=2)

        button_OK = ttk.Button(self.main_frame, text="Nuevo proveedor", command=lambda: self.new_prov(self.df))
        button_OK.grid(row=7, column=0, padx=10, pady=2)

        button_OK = ttk.Button(self.main_frame, text="Estado del proveedor", command=lambda: self.status_prov(self.opt_var.get()))
        button_OK.grid(row=8, column=0, padx=10, pady=2)

    def status_prov(self, name):
        status_prov_df = self.df.loc[self.df["proveedor"].str.contains(name)]

        mean_prov = status_prov_df["evaluación"].mean()
        
        print(mean_prov)
        print(status_prov_df)

        #------ GUI --------------------------
        new_status_prov_win = tk.Toplevel()
        new_status_prov_win.config(
        bg= "#5EABDF"
            )
        new_status_prov_win.geometry("400x200")
        new_status_prov_win.title("Status Supplier")

        status_frame = ttk.Frame(new_status_prov_win, padding=30)
        status_frame.columnconfigure(0, weight=3)
        status_frame.pack()



    def manual_form(self, df, name):

        if name != "" and name != "Elija un proveedor":
            
            specs = tk.IntVar()
            time = tk.IntVar()
            rta = tk.IntVar()
            compet_tec = tk.IntVar()
            certif = tk.IntVar()
            estado = tk.IntVar()
            docs = tk.IntVar()
            costo = tk.IntVar()
            
            self.resl = []

            def eval_chk():
                specs_chk = specs.get()
                time_chek = time.get()
                rta_chk = rta.get()
                compet_tec_chk = compet_tec.get()
                certif_chk = certif.get()
                estado_chk = estado.get()
                docs_chk = docs.get()
                costo_chk = costo.get()

                self.resl = [name, specs_chk, time_chek, rta_chk, compet_tec_chk, certif_chk, estado_chk, docs_chk, costo_chk]

            def submit():
                self.df = Evaluator.create_eval_chk(df, name, self.resl)
                self.export_df()
                print(self.df)
                form_win.destroy()

            form_win = tk.Toplevel()
            form_win.config(
                bg= "#5EABDF"
                    )
            form_win.geometry("553x710")
            form_win.title("Evaluation form")

            form_frame = ttk.Frame(form_win, padding=30)
            form_frame.columnconfigure(0, weight=3)

            form_frame.pack()

            new_prov_label = ttk.Label(form_frame, text=f"EVALUACIÓN MANUAL DE {name}")
            new_prov_label.grid(row=0, column=0, columnspan=6, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=1, column=0, columnspan=6, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento de las especificaciones")
            new_prov_label.grid(row=2, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=specs, value=0, command=eval_chk)
            new_chk.grid(row=3, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=specs, value=-5, command=eval_chk)
            new_chk.grid(row=3, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=specs, value=-10, command=eval_chk)
            new_chk.grid(row=3, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=specs, value=-20, command=eval_chk)
            new_chk.grid(row=3, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=specs, value=-30, command=eval_chk)
            new_chk.grid(row=3, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=specs, value=-40, command=eval_chk)
            new_chk.grid(row=3, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=4, column=0, columnspan=6, padx=10, pady=2)

            #------------------------------------------------------------------------------------------------------------------

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento de los tiempos de entrega")
            new_prov_label.grid(row=5, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=time, value=0, command=eval_chk)
            new_chk.grid(row=6, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=time, value=-5, command=eval_chk)
            new_chk.grid(row=6, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=time, value=-10, command=eval_chk)
            new_chk.grid(row=6, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=time, value=-20, command=eval_chk)
            new_chk.grid(row=6, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=time, value=-30, command=eval_chk)
            new_chk.grid(row=6, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=time, value=-40, command=eval_chk)
            new_chk.grid(row=6, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=7, column=0, columnspan=6, padx=10, pady=2)

            #------------------------------------------------------------------------------------------------------------------

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento de calidad de las respuestas")
            new_prov_label.grid(row=8, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=rta, value=0, command=eval_chk)
            new_chk.grid(row=9, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=rta, value=-5, command=eval_chk)
            new_chk.grid(row=9, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=rta, value=-10, command=eval_chk)
            new_chk.grid(row=9, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=rta, value=-20, command=eval_chk)
            new_chk.grid(row=9, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=rta, value=-30, command=eval_chk)
            new_chk.grid(row=9, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=rta, value=-40, command=eval_chk)
            new_chk.grid(row=9, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=10, column=0, columnspan=6, padx=10, pady=2)

            #------------------------------------------------------------------------------------------------------------------

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento en la predisposición para demostrar su competencia técnica")
            new_prov_label.grid(row=11, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=compet_tec, value=0, command=eval_chk)
            new_chk.grid(row=12, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=compet_tec, value=-5, command=eval_chk)
            new_chk.grid(row=12, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=compet_tec, value=-10, command=eval_chk)
            new_chk.grid(row=12, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=compet_tec, value=-20, command=eval_chk)
            new_chk.grid(row=12, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=compet_tec, value=-30, command=eval_chk)
            new_chk.grid(row=12, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=compet_tec, value=-40, command=eval_chk)
            new_chk.grid(row=12, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=13, column=0, columnspan=6, padx=10, pady=2)

            #------------------------------------------------------------------------------------------------------------------

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento de calidad de las respuestas")
            new_prov_label.grid(row=14, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=certif, value=0, command=eval_chk)
            new_chk.grid(row=15, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=certif, value=-5, command=eval_chk)
            new_chk.grid(row=15, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=certif, value=-10, command=eval_chk)
            new_chk.grid(row=15, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=certif, value=-20, command=eval_chk)
            new_chk.grid(row=15, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=certif, value=-30, command=eval_chk)
            new_chk.grid(row=15, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=certif, value=-40, command=eval_chk)
            new_chk.grid(row=15, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=16, column=0, columnspan=6, padx=10, pady=2)

            #------------------------------------------------------------------------------------------------------------------

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento en la estado del producto")
            new_prov_label.grid(row=17, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=estado, value=0, command=eval_chk)
            new_chk.grid(row=18, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=estado, value=-5, command=eval_chk)
            new_chk.grid(row=18, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=estado, value=-10, command=eval_chk)
            new_chk.grid(row=18, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=estado, value=-20, command=eval_chk)
            new_chk.grid(row=18, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=estado, value=-30, command=eval_chk)
            new_chk.grid(row=18, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=estado, value=-40, command=eval_chk)
            new_chk.grid(row=18, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=19, column=0, columnspan=6, padx=10, pady=2)

            #------------------------------------------------------------------------------------------------------------------

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento de la documentación general")
            new_prov_label.grid(row=20, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=docs, value=0, command=eval_chk)
            new_chk.grid(row=21, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=docs, value=-5, command=eval_chk)
            new_chk.grid(row=21, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=docs, value=-10, command=eval_chk)
            new_chk.grid(row=21, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=docs, value=-20, command=eval_chk)
            new_chk.grid(row=21, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=docs, value=-30, command=eval_chk)
            new_chk.grid(row=21, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=docs, value=-40, command=eval_chk)
            new_chk.grid(row=21, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=22, column=0, columnspan=6, padx=10, pady=2)

            #------------------------------------------------------------------------------------------------------------------

            new_prov_label = ttk.Label(form_frame, text=f"Nivel de incumpliemiento en el costo y presupuesto presentado")
            new_prov_label.grid(row=23, column=0, columnspan=6, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Cero", variable=costo, value=0, command=eval_chk)
            new_chk.grid(row=24, column=0, padx=10, pady=2)
            
            new_chk = ttk.Radiobutton(form_frame, text="Leve", variable=costo, value=-5, command=eval_chk)
            new_chk.grid(row=24, column=1, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Moderado", variable=costo, value=-10, command=eval_chk)
            new_chk.grid(row=24, column=2, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Grave", variable=costo, value=-20, command=eval_chk)
            new_chk.grid(row=24, column=3, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Muy Grave", variable=costo, value=-30, command=eval_chk)
            new_chk.grid(row=24, column=4, padx=10, pady=2)

            new_chk = ttk.Radiobutton(form_frame, text="Abyecto", variable=costo, value=-40, command=eval_chk)
            new_chk.grid(row=24, column=5, padx=10, pady=2)

            new_prov_label = ttk.Label(form_frame, text="")
            new_prov_label.grid(row=25, column=0, columnspan=6, padx=10, pady=2)

            submit_eval_btn = ttk.Button(form_frame, text="Submit", command=submit)
            submit_eval_btn.grid(row=26, column=0, columnspan=6, padx=10, pady=2)
            
            form_win.mainloop()
        
        else:
            ms.showerror(title="Error", message="Select Supplier!")
        
    def new_prov(self, df):
        new_prov_win = tk.Toplevel()
        new_prov_win.config(
        bg= "#5EABDF"
            )
        new_prov_win.geometry("400x200")
        new_prov_win.title("New Supplier")

        form_frame = ttk.Frame(new_prov_win, padding=30)
        form_frame.columnconfigure(0, weight=3)
        form_frame.pack()

        prov_name_var = tk.StringVar()

        def close_new():
            new_prov_win.destroy()

        def evaluation_OK(df):
            data_frame = Evaluator.eval_OK(df, prov_name_var.get())
            self.df = data_frame
            new_prov_win.destroy()
            self.export_df()
            print(self.df)
        
        def manual_evaluation(df):
            
            if prov_name_var.get() != "":
                new_prov_win.destroy()
                data_frame = self.manual_form(df, prov_name_var.get())
                self.df = data_frame
                print(self.df)
                            
            else:
                ms.showerror(title="Error", message="Write Supplier Name!") 

        new_prov_label = ttk.Label(form_frame, text="NUEVO PROVEEDOR")
        new_prov_label.grid(row=1, column=0, columnspan=2, padx=10, pady=2)

        new_prov_label = ttk.Label(form_frame, text="Nombre del Proveedor")
        new_prov_label.grid(row=2, column=0, padx=10, pady=2, sticky=tk.W)
            
        new_prov = ttk.Entry(form_frame, textvariable=prov_name_var, width=30)
        new_prov.grid(row=2, column=1, padx=10, pady=2)

        btn_evalOK = ttk.Button(form_frame, text="Aprovación de proveedor", command=lambda: evaluation_OK(df))
        btn_evalOK.grid(row=3, column=0, columnspan=2, padx=10, pady=2)

        btn_evalOK = ttk.Button(form_frame, text="Evaluación manual", command=lambda: manual_evaluation(df))
        btn_evalOK.grid(row=4, column=0, columnspan=2, padx=10, pady=2)

        btn_close = ttk.Button(form_frame, text="Cerrar", command=close_new)
        btn_close.grid(row=5, column=0, columnspan=2, padx=10, pady=2)

    def evalOK(self, df, name):
                
        if  df.loc[df["proveedor"].str.contains(name)].to_numpy().tolist() != []:
            self.df = Evaluator.eval_OK(df, name)
            self.export_df()
            print(self.df)

        elif df.loc[df["proveedor"].str.contains(name)].to_numpy().tolist() != "Elija un proveedor":
            ms.showerror(title="Error", message="Select Supplier!")

    def export_df(self):
        """
        Método que permite exportar a 2 archivos excel la base de datos. Según en el año en que se encuentre.
        De esta manera si por alguna razón se esta evaluando proveedores en el cambio de año, generará 2 archivos diferentes.

        El método guarda el archivo con el nombre del año en que se generó.
        """
        year_m_1_df = self.df.loc[self.df["fecha"].str.contains(str(datetime.today().year - 1), na=False)]
        year_df = self.df.loc[self.df["fecha"].str.contains(str(datetime.today().year), na=False)]

        excel = pd.ExcelWriter(f"{datetime.today().year}.xlsx")
        excel_m_1 = pd.ExcelWriter(f"{datetime.today().year - 1}.xlsx")
        
        year_df.to_excel(excel)
        year_m_1_df.to_excel(excel_m_1)
        
        excel.save()
        excel_m_1.save()
        

    def load_df(self):
        """
        Este método sirve apara abrir una ventana de dialogo para seleccionar el archivo del año correspondiente que se quiere evaluar.
        """
        url = fd.askopenfilename(initialdir="", title="Seleccione una BBDD", filetype=((".xlsx files", "*.xlsx"), ("todos los archivos", "*.*")))
        
        if url !="":
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                df = pd.read_excel(url, index_col = 0)
        
        return df

if __name__ == "__main__":
    Main()
