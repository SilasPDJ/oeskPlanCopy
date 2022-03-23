import tkinter as tk
from ttkwidgets import autocomplete as ttkac
import clipboard
from threading import Thread
from tkinter import filedialog
import pandas as pd
from sets import Initial
# ESSA VERSÃO POSSO ATUALIZAR ELA PARA O PROGRAMA OESK
# CONSULTAR = BACKEND


class Consultar(Initial):

    def get_fieldnames(self):

        fieldnames = list(self.__read_pandas().to_dict().keys())
        return fieldnames

    @staticmethod
    def any_to_str(*args):
        for v in args:
            yield "".join(str(v))

    def clients_list(self, get_campo=0) -> list:
        def __lsdv(dta): return list(dta.values())
        df = self.__read_pandas()
        return list(__lsdv(df.to_dict())[get_campo].values())

    def GET_clien_DATA(self, clid):
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

    def __read_pandas(self):
        filename = Initial().getset_folderspath(False)

        shname = "OESK"
        main_pandas = pd.read_excel(
            filename, sheet_name=shname or shname.lower(), dtype=str)
        return main_pandas


class MainApplication(tk.Frame, Consultar):

    def __init__(self, parent, *args, **kwargs):
        # ---- init
        super().__init__(*args, **kwargs)
        Consultar().__init__()
        LABELS = []
        self.parent = parent
        self.root = parent

        # ---- lambda methods
        def increment_header_tip(tip, fg="#000"): LABELS.append(
            tk.Label(root, text=tip, font=("Currier", 12), fg=fg))

        def copia_command(e=None): return self.__get_dataclipboard(
            self.headers_plan.get())

        increment_header_tip(
            "PRESSIONE F2 PARA COPIAR O CAMPO SELECIONADO", "#ff523d")

        # gui ----------
        self.headers_plan = ttkac.AutocompleteEntryListbox(
            self.root, self.get_fieldnames())

        self.selected_client = ttkac.AutocompleteEntryListbox(
            self.root, self.clients_list())
        bt_copia = self.button(
            'Copia Campo', copia_command, 'black', 'lightblue')
        seleciona_planilha = self.button(
            'Seleciona planilha', self.select_path, 'black', 'lightblue')
        self.__pack(*LABELS, self.selected_client, bt_copia,
                    seleciona_planilha, self.headers_plan,)
        # self.__pack(self.selected_client, excel_col)

        # ---- create shortcuts
        root.bind("<F2>", copia_command)
        self.headers_plan.listbox.selection_set(0)
        self.selected_client.listbox.selection_set(0)

    # functions

    def select_path(self):
        import sys
        from os import execl
        # self.__read_pandas()
        self.main_file = self._select_path_if_not_exists()
        python = sys.executable
        execl(python, python, * sys.argv)

    def __get_dataclipboard(self, campo: str):
        self.mask_cnpjcpf = True

        indcampo = self.get_fieldnames().index(campo)
        selected_list_values = list(
            self.any_to_str(*self.clients_list(indcampo)))

        whoindex = self.get_clienid(self.selected_client.get())
        resultado = str(selected_list_values[whoindex])

        if self.mask_cnpjcpf and (campo.upper() == 'CNPJ' or campo.upper() == 'CPF'):
            if len(resultado) == 11:
                resultado = "%s%s%s.%s%s%s.%s%s%s-%s%s" % tuple(resultado)
            else:
                input(len(resultado))
                resultado = "%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s" % tuple(
                    resultado)

        clipboard.copy(resultado)
        return resultado
    # Elements and placements

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

    root.geometry('530x560')
    root.mainloop()
