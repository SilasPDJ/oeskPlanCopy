import tkinter as tk
from ttkwidgets import autocomplete as ttkac
import clipboard
from threading import Thread
from tkinter import filedialog
import pandas as pd
from sets import Initial


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
        filename = Initial.getset_folderspath(False)

        shname = "OESK"
        main_pandas = pd.read_excel(
            filename, sheet_name=shname or shname.lower())
        return main_pandas


class MainApplication(tk.Frame, Consultar):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Consultar().__init__()
        # lista_de_dados = self.GET_clien_DATA(self.get_clienid("Nome5"))

        self.parent = parent
        self.root = parent

        self.headers_plan = ttkac.AutocompleteEntryListbox(
            self.root, self.get_fieldnames())

        self.selected_client = ttkac.AutocompleteEntry(
            self.root, self.clients_list())

        bt_abre_pasta = self.button(
            'Abre e copia pasta de: ', self.abre_pasta, 'black', 'lightblue')
        bt_copia = self.button(
            'Copia Campo', lambda: self.get_copia(self.headers_plan.get()
                                                  ), 'black', 'lightblue')
        seleciona_planilha = self.button(
            'Seleciona planilha', self.select_path, 'black', 'lightblue')
        self.__pack(self.selected_client, bt_copia,
                    seleciona_planilha, self.headers_plan,)

        # self.__pack(self.selected_client, excel_col)
    # functions

    def select_path(self):
        # self.__read_pandas()

        self.main_file = self._select_path_if_not_exists()
        self.headers_plan.listbox.delete(0, 1000)  # deleta do 0 até o 1000...

        for val in self.get_fieldnames():
            self.headers_plan.listbox.insert('end', val or 123)

    def abre_pasta(self):
        import subprocess
        # folder = "\\".join(main_folder.split('/')[:-1])
        # folder = os.path.join(
        #     folder, COMPT[3:], COMPT, self.selected_client.get())
        # if not os.path.exists(folder):
        #     os.makedirs(folder)
        # subprocess.Popen(f'explorer "{folder}"')
        # clipboard.copy(folder)
        # self.selected_client

    def get_copia(self, campo: str):

        __vgot = campo
        self.__get_dataclipboard(__vgot)
        # getfieldnames()

    def __get_dataclipboard(self, campo: str):
        whoses_cnpj = self.selected_client.get()
        if whoses_cnpj == '':
            whoses_cnpj = 'Oesk Contabil'

        indcampo = self.get_fieldnames().index(campo)

        cnpjs = list(self.clients_list(indcampo))
        print(self.selected_client)
        input(cnpjs)
        whoses = list(self.get_clienid())
        whoindex = whoses.index(whoses_cnpj)
        clipboard.copy(cnpjs[whoindex])
        return cnpjs[whoindex]
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

    root.geometry('500x800')
    root.mainloop()