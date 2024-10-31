import pandas as pd
import os
import warnings
import locale

warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_TIME, '') #'pt_BR.UTF-8' 'en_US.UTF-8' 'pt_BR'
# try:
#     locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
# except locale.Error:
#     # Tenta configurar um locale alternativo ou padrão do sistema
#     locale.setlocale(locale.LC_TIME, 'pt_BR' if locale.getlocale()[0] else '')


#usuario = os.getlogin()
#diretorio = f'C:\\Users\\{usuario}\\OneDrive - NTT DATA EMEAL\\Escritorio\\PEM_NPEM DEC-FEC\\'


# # Leitura das bases
# base_dec = pd.read_excel(f'{diretorio}\\DEC-FEC Conjuntos.xlsx', sheet_name='DEC')
# base_fec = pd.read_excel(f'{diretorio}\\DEC-FEC Conjuntos.xlsx', sheet_name='FEC')
# base_dec_polo_enel = pd.read_excel(f'{diretorio}\\DEC-FEC Polos.xlsx', sheet_name='DEC')
# base_fec_polo_enel = pd.read_excel(f'{diretorio}\\DEC-FEC Polos.xlsx', sheet_name='FEC')
# def ler_arquivos(dir):
#     base_clientes = pd.read_csv(dir, sep='|', on_bad_lines='skip')
#     base_conjuntos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
#     base_meta_aneel_conjuntos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
#     base_meta_dec_aneel_polos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
#     base_meta_fec_aneel_polos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
#     return base_clientes, base_conjuntos, base_meta_aneel_conjuntos, base_meta_dec_aneel_polos, base_meta_fec_aneel_polos
# base_clientes = ler_arquivos(f'{diretorio}Clientes 2024.txt')
# base_clientes = base_clientes[0]
# base_conjuntos = ler_arquivos(f'{diretorio}Conjuntos.txt')
# base_conjuntos = base_conjuntos[0]
# base_meta_aneel_conjuntos = ler_arquivos(f'{diretorio}Meta Aneel Conjuntos 2024.txt')
# base_meta_aneel_conjuntos = base_meta_aneel_conjuntos[0]
# base_meta_dec_aneel_polos = ler_arquivos(f'{diretorio}Meta Aneel DEC Polos Enel 2024.txt')
# base_meta_dec_aneel_polos = base_meta_dec_aneel_polos[0]
# base_meta_fec_aneel_polos = ler_arquivos(f'{diretorio}Meta Aneel FEC Polos Enel 2024.txt')
# base_meta_fec_aneel_polos = base_meta_fec_aneel_polos[0]




# Leitura das bases
base_dec = pd.read_excel(f'DEC-FEC Conjuntos.xlsx', sheet_name='DEC')
base_fec = pd.read_excel(f'DEC-FEC Conjuntos.xlsx', sheet_name='FEC')
base_dec_polo_enel = pd.read_excel(f'DEC-FEC Polos.xlsx', sheet_name='DEC')
base_fec_polo_enel = pd.read_excel(f'DEC-FEC Polos.xlsx', sheet_name='FEC')
def ler_arquivos(dir):
    base_clientes = pd.read_csv(dir, sep='|', on_bad_lines='skip')
    base_conjuntos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
    base_meta_aneel_conjuntos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
    base_meta_dec_aneel_polos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
    base_meta_fec_aneel_polos = pd.read_csv(dir, sep='|', on_bad_lines='skip')
    return base_clientes, base_conjuntos, base_meta_aneel_conjuntos, base_meta_dec_aneel_polos, base_meta_fec_aneel_polos
base_clientes = ler_arquivos(f'Clientes 2024.txt')
base_clientes = base_clientes[0]
base_conjuntos = ler_arquivos(f'Conjuntos.txt')
base_conjuntos = base_conjuntos[0]
base_meta_aneel_conjuntos = ler_arquivos(f'Meta Aneel Conjuntos 2024.txt')
base_meta_aneel_conjuntos = base_meta_aneel_conjuntos[0]
base_meta_dec_aneel_polos = ler_arquivos(f'Meta Aneel DEC Polos Enel 2024.txt')
base_meta_dec_aneel_polos = base_meta_dec_aneel_polos[0]
base_meta_fec_aneel_polos = ler_arquivos(f'Meta Aneel FEC Polos Enel 2024.txt')
base_meta_fec_aneel_polos = base_meta_fec_aneel_polos[0]