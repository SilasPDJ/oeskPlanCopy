import tkinter as tk
from turtle import width
from ttkwidgets import autocomplete as ttkac
from ttkwidgets import UpperStringEntry
import clipboard
from threading import Thread
from tkinter import filedialog
import pandas as pd
from sets import Initial
from subprocess import Popen
import sys
import os
# ESSA VERSÃO POSSO ATUALIZAR ELA PARA O PROGRAMA OESK
# CONSULTAR = BACKEND


class Consultar(Initial):

    @staticmethod
    def any_to_str(*args):
        for v in args:
            yield "".join(str(v))

    def get_fieldnames(self) -> list:
        fieldnames = list(self.__read_pandas().to_dict().keys())
        return fieldnames

    def clients_list(self, get_campo=0) -> list:
        def __lsdv(dta): return list(dta.values())
        df = self.__read_pandas()
        dados = list(__lsdv(df.to_dict())[get_campo].values())
        return dados

    def ___GET_clien_DATA(self, clid):
        # GET VALUES FROM SPECIFC CLIENT
        def __lsdv(dta): return list(dta.values())
        # list of dict values = lsdv meaning
        df = self.__read_pandas()
        for v in __lsdv(df.to_dict()):
            return list(v.values())[clid]

    def get_clienid(self, client_name):
        """
        get data from client_name...
        """
        df = self.__read_pandas()
        clientid = False

        for cloop in list(df.to_dict().values())[:1]:  # somente nome...
            clientid = list(cloop.values()).index(
                client_name)  # procura o index

            return clientid

    def __read_pandas(self, upper=True):
        filename = Initial().getset_folderspath(False)

        shname = "OESK"
        df = main_pandas = pd.read_excel(
            filename, sheet_name=shname or shname.lower(), dtype=str)
        if upper is not None:  # then normal cased
            if upper is False:  # then lower cased
                main_pandas = main_pandas.apply(
                    lambda x: x.astype(str).str.lower())
            else:  # then upper cased
                main_pandas = main_pandas.apply(
                    lambda x: x.astype(str).str.upper())
            main_pandas.columns = main_pandas.columns.str.upper()
            # apply to be upper case
        return main_pandas

    def select_path(self, e=None):
        # self.__read_pandas()
        self.main_file = self._select_path_if_not_exists()
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def show_database(self, e=None):
        path = Initial().getset_folderspath(False).replace('/', '\\')
        return Popen(f'explorer /select,"{path}"')


class MainApplication(tk.Frame, Consultar):
    default_font = ("Currier", 12)

    def __init__(self, parent, *args, **kwargs):
        # ---- init
        super().__init__(*args, **kwargs)
        Consultar().__init__()
        LABELS = []
        self.parent = parent
        self.root = parent

        # ---- lambda methods
        def increment_header_tip(tip, fg="#000", bg="#FFF"): LABELS.append(
            tk.Label(root, text=tip, font=self.default_font, fg=fg, bg=bg))

        def copia_command(e=None): return self.__get_dataclipboard(
            self.headers_plan.get())

        increment_header_tip("Planilhas estão dentro da pasta selecionada")
        increment_header_tip(
            "O nome da planilha usada pelo sistema é OESK")
        increment_header_tip(
            "PRESSIONE F4 PARA COPIAR O CAMPO SELECIONADO", "#006400", "#ffff00")
        increment_header_tip("PRESSIONE F2 p/ exibir a base de dados")
        increment_header_tip(
            "PRESSIONE F5 PARA TROCAR A BASE DE DADOS", "#ff523d")
        # gui ----------
        self.outputwb_formated = tk.BooleanVar()

        self.headers_plan = ttkac.AutocompleteEntryListbox(
            self.root, self.get_fieldnames())

        self.selected_client = ttkac.AutocompleteEntryListbox(
            self.root, self.clients_list())

        bt_copia = self.button(
            'Copia Campo', copia_command, 'black', 'lightblue')
        seleciona_planilha = self.button(
            'Seleciona planilha', self.select_path, 'black', 'lightblue')
        self.__pack(*LABELS, self.headers_plan)
        self.__pack(self.radiobutton4format(), x=50, y=2,
                    fill=tk.Y)  # centralizou com fill Y
        self.__pack(bt_copia,
                    seleciona_planilha, self.selected_client,)
        # self.__pack(self.selected_client, excel_col)

        # ---- create bind methods
        self.selected_client.entry.bind(
            "<KeyPress>", lambda event, arg=self.selected_client: self.__entrywrite(event, arg))
        self.headers_plan.entry.bind(
            "<KeyPress>", lambda event, arg=self.headers_plan: self.__entrywrite(event, arg))

        # ---- create shortcuts
        self.root.bind("<F4>", copia_command)
        self.root.bind("<F5>", self.select_path)
        self.root.bind("<F2>", self.show_database)
        self.set_initials()
        bt_copia.focus()

    def set_initials(self):
        self.headers_plan.listbox.selection_set(0)
        self.selected_client.listbox.selection_set(0)

        cli = self.selected_client.listbox.get(0)
        self.selected_client.entry.insert('end', cli)

        hd = self.headers_plan.listbox.get(1)
        self.headers_plan.entry.insert('end', hd)

    # functions
    def __get_dataclipboard(self, campo: str):

        indcampo = self.get_fieldnames().index(campo)
        selected_list_values = list(
            self.any_to_str(*self.clients_list(indcampo)))

        whoindex = self.get_clienid(self.selected_client.get())
        returned = str(selected_list_values[whoindex])

        can_format = self.outputwb_formated.get()
        if ('CNPJ' in campo.upper() or 'CPF' in campo.upper()):
            returned = "".join(n for n in returned if n.isnumeric())
            if can_format:
                if len(returned) == 11:
                    returned = "%s%s%s.%s%s%s.%s%s%s-%s%s" % tuple(returned)
                else:
                    returned = "%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s" % tuple(
                        returned)

        clipboard.copy(returned)
        return returned

    def __entrywrite(self, e, elem):
        # TODO: se for tudo lower, check se foi digitado upper...
        if e.char.islower():
            elem._listbox_keypress(e)

    # Elements and placements

    def radiobutton4format(self) -> tuple:
        # com frame
        height, width = 10, 20
        frame = tk.Frame(self.root, bg="green")

        rb1 = tk.Radiobutton(frame, text="COM formatação",
                             variable=self.outputwb_formated, value=True, font=self.default_font)
        rb2 = tk.Radiobutton(frame, text="SEM formatação",
                             variable=self.outputwb_formated, value=False, font=self.default_font)

        rb2.grid(row=0)
        rb1.grid(row=0, column=1)

        return frame

    @ staticmethod
    def __pack(*els, x=50, y=10, fill='x', side=tk.TOP, expand=0):
        try:
            x1, x2 = x
        except TypeError:
            x1, x2 = x, x

        try:
            y1, y2 = y
        except TypeError:
            y1, y2 = y, y
        for el in els:
            el.pack(padx=(x1, x2), pady=(
                y1, y2), fill=fill, side=side, expand=expand)

    @ staticmethod
    def change_state(*args, change_to=None):
        """
        :param args: elements [buttons]
        :param change_to: Change state to [normal, disabled, ...], if None changes to opposite, 0 -> disabled, 1 -> normal
        :return:
        """
        for bt in args:
            bt_state = bt['state']
            if change_to is None:
                if bt_state == 'normal':
                    bt['state'] = 'disabled'
                else:
                    bt['state'] = 'normal'
            else:
                if str(change_to).lower().strip() == 'disabled' or str(change_to).lower().strip() == 'normal':
                    pass
                elif not isinstance(change_to, int):
                    print(f'{bt} em estado NORMLA')
                    change_to = 'normal'
                else:
                    change_to = 'disabled' if change_to == 0 else 'normal'

                bt['state'] = change_to

    def button(self, text, command=None, fg='#fff', bg='#000',):
        bt = tk.Button(self, text=text, command=lambda: self.start(
            command), fg=fg, bg=bg)
        return bt
        # threading...

    def refresh(self):
        self.root.update()
        self.root.after(1000, self.refresh)

    def start(self, stuff):
        self.refresh()
        Thread(target=stuff).start()
    # threading


if __name__ == "__main__":
    root = tk.Tk()
    root.title = 'Autoesk'

    b = MainApplication(root)
    b.pack(side="top", fill="both", expand=True)

    root.geometry('530x800')
    root.mainloop()
