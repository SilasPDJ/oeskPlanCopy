import os


class Initial:
    main_path = os.path.dirname(os.path.realpath(__file__))
    main_path += '\with_titlePATH.txt'

    @classmethod
    def getset_folderspath(cls, folder_path_only=True):
        """Seleciona onde estão as pastas e planihas

        Returns:
            [type]: [description]
        """
        # filepath = os.path.realpath(__file__)
        # os.path.dirname(filepath)
        returned = False
        try:
            with open(cls.main_path) as f:
                returned = f.read()
        except FileNotFoundError:
            returned = cls._select_path_if_not_exists()

        if returned and folder_path_only:
            returned = os.path.dirname(returned)
        return returned

    def _select_path_if_not_exists(self, some_message="SELECIONE ONDE ESTÁ SUA PLANILHA.", savit=main_path):
        """[summary]
        Args:
            some_message (str, optional): []. Defaults to "SELECIONE ONDE ESTÃO SUAS PLANILHAS".
            savit (str, optional): customizable, where to save the info
        Returns:
            [type]: [description]
        """
        from tkinter import Tk, filedialog, messagebox

        # sh_management = SheetPathManager(file_with_name)
        way = None
        while way is None:
            way = filedialog.askopenfilename(title=some_message, filetypes=[
                                             ("Excel files", ".xlsx .xls .xlsm .csv")])
            if len(way) <= 0:
                way = None
                resp = messagebox.askokcancel(
                    'ATENÇÃO!', message='Favor, selecione uma pasta ou clique em CANCELAR.')
                if not resp:
                    return False
            else:
                wf = open(savit, 'w')
                wf.write(way)
                return way
