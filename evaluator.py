import tkinter as tk
from tkinter import ttk
from turtle import rt, width
import pandas as pd
from tkinter import filedialog as fd
import warnings
import tkinter.messagebox as ms
from datetime import datetime

class Evaluator:

    def create_eval_chk(df, name, eval_chk):
        
        answer = ms.askyesno(title="Confirm Evaluation", message=f"Would you like to confirm the {name} evaluation?")
                
        if answer:
            evaluation_list = eval_chk
            df_manual_eval = pd.DataFrame([evaluation_list + [datetime.today().strftime("%d/%m/%Y")]], columns=[
            "proveedor",
            "cumplimiento_especificaciones",
            "tiempo_de_entrega",
            "calidad_de_respuesta_ante_consultas",
            "predisposicion_competencia_tecnica",
            "certificados",
            "estado_del_producto",
            "estado_de_la_documentacion_general",
            "evaluación",
            "fecha"
            ])

        df = df.append(df_manual_eval, ignore_index=True)
        
        return df

    def eval_OK(df, prov, win=None):
        
        if prov != "":
            answer = ms.askyesno(title="Confirm Evaluation", message=f"Would you like to confirm the {prov} automatic evaluation?")
                
            if answer:
                df_new_prov = pd.DataFrame([[
                    prov,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    100,
                    datetime.today().strftime("%d/%m/%Y")
                ]], columns=[
                    "proveedor",
                    "cumplimiento_especificaciones",
                    "tiempo_de_entrega",
                    "calidad_de_respuesta_ante_consultas",
                    "predisposicion_competencia_tecnica",
                    "certificados",
                    "estado_del_producto",
                    "estado_de_la_documentacion_general",
                    "evaluación",
                    "fecha"
                    ])

                df = df.append(df_new_prov, ignore_index=True)

                return df
        else:
            ms.showerror(title="Error", message="Write Supplier Name!")

