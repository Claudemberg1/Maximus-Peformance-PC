import os
import sys
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import io
from PIL import Image, ImageTk, ImageSequence
import threading
import requests
import getpass
import socket
import ctypes

# --- INÍCIO DO CÓDIGO DE ATIVAÇÃO ---
#
# Este bloco de código é o portão de entrada para o seu programa.
# Ele será executado antes de tudo, verificando a licença do usuário.
#
# Garanta que você tenha a biblioteca 'requests' instalada:
# pip install requests
#

# A URL da sua API de validação do Google Apps Script
URL_VALIDACAO = "https://script.google.com/macros/s/AKfycbzQ0UV4Knx-e1VZZTXF7M-VO4ErVCe_Ihhb_Y_mBnDs057hW5SHtTfSnuSK2gVDNvKC/exec"

# Nome do arquivo que armazena o status da ativação
ARQUIVO_LICENCA = "licenca.dat"


def obter_id_pc():
    """Gera um identificador único para o PC do cliente."""
    try:
        pc_name = socket.gethostname()
        user_name = getpass.getuser()
        return f"{pc_name}-{user_name}"
    except Exception:
        return "desconhecido"


def verificar_licenca_online(chave_licenca):
    """Tenta validar a chave de licença online com sua API."""
    id_pc = obter_id_pc()
    payload = {'chave': chave_licenca, 'id_pc': id_pc}

    try:
        response = requests.post(URL_VALIDACAO, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'validado':
                with open(ARQUIVO_LICENCA, 'w') as f:
                    f.write(f"{chave_licenca}|{id_pc}")
                return True
            else:
                messagebox.showerror("Erro de Chave", data.get('mensagem'))
                return False
        else:
            messagebox.showerror("Erro de Servidor",
                                 f"Não foi possível conectar ao servidor de licenças. Código: {response.status_code}")
            return False

    except requests.exceptions.RequestException:
        messagebox.showerror("Erro de Conexão", "Erro de conexão. Verifique sua internet.")
        return False


def janela_ativacao():
    """Cria a janela de ativação para o cliente."""
    modal = tk.Tk()
    modal.title("Ativação Necessária")
    modal.geometry("450x280")
    modal.configure(bg="#1e1e1e")
    modal.attributes("-topmost", True)

    font_bold = font.Font(family="Helvetica", size=10, weight="bold")

    id_pc = obter_id_pc()

    label_id = tk.Label(modal, text="Seu ID do PC:",
                        font=font_bold, fg="#ffffff", bg="#1e1e1e")
    label_id.pack(pady=(10, 0))

    entry_id = tk.Entry(modal, width=50)
    entry_id.insert(0, id_pc)
    entry_id.config(state='readonly')
    entry_id.pack(pady=5)

    label_msg = tk.Label(modal, text="Insira sua chave de ativação:",
                         font=font_bold, fg="#ffffff", bg="#1e1e1e")
    label_msg.pack(pady=(20, 5))

    entry_key = tk.Entry(modal, width=50)
    entry_key.pack()

    def on_submit():
        chave_digitada = entry_key.get().strip()
        if verificar_licenca_online(chave_digitada):
            messagebox.showinfo("Sucesso!", "Software ativado. Reinicie o programa.")
            modal.destroy()
            sys.exit(0)

    btn_ativar = tk.Button(modal, text="Ativar", command=on_submit,
                           font=font_bold, bg="#4caf50", fg="white")
    btn_ativar.pack(pady=10)

    modal.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    modal.mainloop()


def verificar_licenca_local():
    """Verifica se a licença já está salva localmente."""
    if not os.path.exists(ARQUIVO_LICENCA):
        return False

    try:
        with open(ARQUIVO_LICENCA, 'r') as f:
            chave_salva, id_salvo = f.read().split('|')

        if id_salvo == obter_id_pc():
            return True
        else:
            os.remove(ARQUIVO_LICENCA)
            return False

    except Exception:
        return False


# Esta é a primeira coisa que seu programa fará, antes de tudo.
if not verificar_licenca_local():
    janela_ativacao()


# --- FIM DO CÓDIGO DE ATIVAÇÃO ---

# --- FUNÇÃO PARA PEGAR CAMINHO CORRETO NO PYINSTALLER ---
def resource_path(relative_path):
    """ Pega o caminho correto dos arquivos, mesmo no PyInstaller """
    try:
        base_path = sys._MEIPASS  # pasta temporária criada pelo PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- CARREGAR OS DADOS DO PDF E DO GIF NA MEMÓRIA NO INÍCIO DO PROGRAMA ---
# Isso garante que a referência aos arquivos não seja perdida.
try:
    with open(resource_path("loading.gif"), 'rb') as f:
        GIF_DATA = f.read()
except Exception as e:
    messagebox.showerror("Erro de Carregamento", f"Falha ao carregar o arquivo GIF: {e}")
    GIF_DATA = None

try:
    with open(resource_path("Maximus_PC_Performance_Manual.pdf"), 'rb') as f:
        PDF_DATA = f.read()
except Exception as e:
    messagebox.showerror("Erro de Carregamento", f"Falha ao carregar o arquivo PDF: {e}")
    PDF_DATA = None


def is_notebook():
    try:
        output = subprocess.check_output("wmic computersystem get PCSystemType", shell=True)
        return b"2" in output  # 2 = Notebook
    except:
        return False


IS_NOTEBOOK = is_notebook()


# ---------------- Função Finalização ---------------- #
def mostrar_finalizacao(msg):
    modal = tk.Toplevel(root)
    modal.title("Finalizado")
    modal.configure(bg="#1e1e1e")
    modal.geometry("400x200")
    modal.resizable(False, False)
    modal.attributes("-topmost", True)
    modal.grab_set()

    label_msg = tk.Label(modal, text=msg, font=("Helvetica", 11, "bold"),
                         fg="#ffffff", bg="#1e1e1e", wraplength=350, justify="center")
    label_msg.pack(pady=20)

    contador = tk.Label(modal, text="", font=("Helvetica", 10),
                        fg="#cccccc", bg="#1e1e1e")
    contador.pack(pady=10)

    def atualizar_contagem(segundos=10):
        if segundos > 0:
            contador.config(text=f"A janela será fechada em {segundos} segundos...")
            modal.after(1000, atualizar_contagem, segundos - 1)
        else:
            modal.destroy()

    atualizar_contagem()

    btn_ok = tk.Button(modal, text="OK", command=modal.destroy,
                       bg="#4caf50", fg="white", width=12, height=1, bd=0)
    btn_ok.pack(pady=10)


# ---------------- Funções principais ---------------- #
def limpar():
    temp_user = os.environ.get("TEMP")
    temp_windows = r"C:\Windows\Temp"

    for folder in [temp_user, temp_windows]:
        if folder and os.path.exists(folder):
            for root_dir, dirs, files in os.walk(folder):
                for f in files:
                    try:
                        os.remove(os.path.join(root_dir, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root_dir, d), ignore_errors=True)
                    except:
                        pass

    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1)
    except:
        pass

    prefetch = r"C:\Windows\Prefetch"
    if os.path.exists(prefetch):
        try:
            shutil.rmtree(prefetch, ignore_errors=True)
        except:
            pass

    updates = r"C:\Windows\SoftwareDistribution\Download"
    if os.path.exists(updates):
        shutil.rmtree(updates, ignore_errors=True)

    mostrar_finalizacao(
        "Limpeza concluída!\n"
        "Limpeza concluída! Arquivos desnecessários removidos, liberando espaço, RAM e deixando o sistema mais leve."
    )


def update():
    try:
        subprocess.run("wuauclt /detectnow", shell=True)
        subprocess.run("wuauclt /updatenow", shell=True)
        mostrar_finalizacao("Windows Update iniciado!\nGanho: Sistema atualizado, estabilidade melhorada.")
    except:
        messagebox.showerror("Erro", "Falha ao atualizar Windows!")


def winget_upgrade():
    try:
        subprocess.run("winget upgrade --all --silent --accept-source-agreements --accept-package-agreements",
                       shell=True)
        mostrar_finalizacao("Programas atualizados via Winget!\nGanho: Todos softwares na versão mais recente.")
    except:
        messagebox.showerror("Erro", "Falha ao atualizar programas!")


def otimizar():
    if not IS_NOTEBOOK:
        subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True)
        subprocess.run("powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True)
    subprocess.run(
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 26 /f',
        shell=True)
    subprocess.run(
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f',
        shell=True)
    mostrar_finalizacao("Sistema otimizado!\nGanho: + Velocidade, CPU mais responsiva, menor consumo de recursos.")


def modo_gamer():
    subprocess.run("taskkill /f /im OneDrive.exe", shell=True)
    subprocess.run(
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\OneDrive" /v DisableFileSyncNGSC /t REG_DWORD /d 1 /f',
        shell=True)
    servicos = ["XblAuthManager", "XblGameSave", "XboxNetApiSvc", "XboxGipSvc", "DiagTrack", "dmwappushservice"]
    for s in servicos:
        subprocess.run(f"sc stop {s}", shell=True)
        subprocess.run(f"sc config {s} start= disabled", shell=True)
    subprocess.run(
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d 0xffffffff /f',
        shell=True)
    subprocess.run(
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f',
        shell=True)
    subprocess.run(
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 6 /f',
        shell=True)
    mostrar_finalizacao("Modo Gamer Extremo ativado!\nGanho: Prioridade máxima para jogos, menor lag, melhor FPS.")


def restaurar():
    subprocess.run('reg delete "HKLM\\Software\\Policies\\Microsoft\\Windows\\OneDrive" /v DisableFileSyncNGSC /f',
                   shell=True)
    subprocess.run(f'start %SystemRoot%\\System32\\OneDriveSetup.exe /configure', shell=True)
    servicos = ["XblAuthManager", "XblGameSave", "XboxNetApiSvc", "XboxGipSvc", "DiagTrack", "dmwappushservice"]
    for s in servicos:
        subprocess.run(f"sc config {s} start= demand", shell=True)
    subprocess.run(
        'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v NetworkThrottlingIndex /f',
        shell=True)
    subprocess.run(
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d 2 /f',
        shell=True)
    subprocess.run(
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 2 /f',
        shell=True)
    mostrar_finalizacao("Configurações restauradas!\nGanho: Sistema normalizado, estabilidade restaurada.")


def executar_tudo():
    limpar()
    update()
    winget_upgrade()
    otimizar()
    mostrar_finalizacao("Todas as otimizações concluídas!\nGanho: Sistema totalmente otimizado, máximo desempenho.")


def abrir_pdf():
    if PDF_DATA:
        try:
            temp_pdf_path = os.path.join(os.environ['TEMP'], "Maximus_PC_Performance_Manual.pdf")
            with open(temp_pdf_path, 'wb') as f:
                f.write(PDF_DATA)
            os.startfile(temp_pdf_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF: {e}")
    else:
        messagebox.showerror("Erro", "PDF não encontrado!")


# ---------------- Modal com GIF ---------------- #
def mostrar_gif(func):
    def wrapper():
        if not GIF_DATA:
            messagebox.showerror("Erro", "O GIF de carregamento não foi encontrado. Por favor, reinstale o software.")
            return

        modal = tk.Toplevel(root)
        modal.title("Aguarde")
        modal.configure(bg="#1e1e1e")
        modal.resizable(False, False)

        width, height = 400, 250
        x, y = 500, 10
        modal.geometry(f"{width}x{height}+{x}+{y}")

        modal.transient(root)
        modal.attributes("-topmost", True)
        modal.grab_set()

        tk.Label(modal,
                 text="Por favor, estamos configurando.\nNão aperte em nada e clique em 'Sim' em tudo que aparecer.\nTempo de espera, de 1 à 15 minutos dependendo do seu PC...",
                 font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#1e1e1e").pack(pady=10)

        try:
            gif_stream = io.BytesIO(GIF_DATA)
            img = Image.open(gif_stream)
            frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(img)]
            lbl_img = tk.Label(modal, bg="#1e1e1e")
            lbl_img.pack()

            def anim(ind=0):
                if not modal.winfo_exists():
                    return
                frame = frames[ind]
                lbl_img.configure(image=frame)
                ind = (ind + 1) % len(frames)
                modal.after(100, anim, ind)

            anim()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar GIF: {e}")
            modal.destroy()
            return

        def run_func():
            try:
                func()
            finally:
                if modal.winfo_exists():
                    root.after(0, modal.destroy)

        threading.Thread(target=run_func, daemon=True).start()

    return wrapper


root = tk.Tk()
root.title("Maximus PC Performance")
root.configure(bg="#1e1e1e")
root.resizable(True, True)

title_font = font.Font(family="Helvetica", size=20, weight="bold")
btn_font = font.Font(family="Helvetica", size=10, weight="bold")
desc_font = font.Font(family="Helvetica", size=8, slant="italic")

tk.Label(root, text="MAXIMUS PC PERFORMANCE", font=title_font, bg="#1e1e1e", fg="#ffffff").pack(pady=10)

buttons_info = [
    ("Limpar arquivos temporários", limpar, "#4caf50", "+ Espaço + RAM"),
    ("Atualizar Windows e Drivers", update, "#2196f3", "Sistema atualizado, estabilidade"),
    ("Atualizar Programas (Winget)", winget_upgrade, "#00bcd4", "Softwares atualizados"),
    ("Otimizar desempenho do sistema", otimizar, "#ff9800", "Mais velocidade, CPU responsiva"),
    ("Executar tudo", executar_tudo, "#9c27b0", "Sistema totalmente otimizado"),
    ("Modo Gamer Extremo", modo_gamer, "#f44336", "Prioridade máxima para jogos, ganho de FPS"),
    ("Restaurar configurações padrão", restaurar, "#607d8b", "Estabilidade restaurada"),
    ("Abrir PDF do Manual", abrir_pdf, "#795548", "Guia completo de uso")
]


def on_enter(e, btn, color):
    btn['bg'] = "#ffffff"
    btn['fg'] = color


def on_leave(e, btn, color):
    btn['bg'] = color
    btn['fg'] = "#ffffff"


for text, func, color, desc in buttons_info:
    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack(pady=5, padx=10, fill='both', expand=True)
    btn = tk.Button(frame, text=text, command=mostrar_gif(func), font=btn_font, bg=color, fg="#ffffff",
                    activebackground="#ffffff", activeforeground=color, width=40, height=2, bd=0, relief="raised")
    btn.pack(fill='both', expand=True)
    lbl = tk.Label(frame, text=desc, font=desc_font, fg="#cccccc", bg="#1e1e1e")
    lbl.pack(pady=2)
    btn.bind("<Enter>", lambda e, b=btn, c=color: on_enter(e, b, c))
    btn.bind("<Leave>", lambda e, b=btn, c=color: on_leave(e, b, c))

footer = tk.Frame(root, bg="#1e1e1e")
footer.pack(side="bottom", fill="x", pady=10)

btn_sair = tk.Button(footer, text="Sair", command=root.destroy, font=btn_font, bg="#9e9e9e", fg="#ffffff",
                     activebackground="#ffffff", activeforeground="#9e9e9e", width=20, height=2, bd=0, relief="raised")
btn_sair.pack()

tk.Label(root, text="Seguro para PC & Notebook | Admin necessário",
         font=("Helvetica", 10), bg="#1e1e1e", fg="#aaaaaa").pack(side="bottom", pady=5)

root.mainloop()