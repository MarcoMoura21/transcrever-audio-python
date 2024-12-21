import subprocess
import whisper
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Função para transcrever o arquivo de áudio
def transcrever_arquivo(arquivo_audio):
    try:
        atualizar_status("Convertendo e transcrevendo o arquivo...")  # Atualiza o status para em andamento
        root.update()  # Atualiza a interface gráfica

        arquivo_convertido = arquivo_audio.rsplit(".", 1)[0] + ".wav"  # Cria o nome do arquivo .wav

        # Remove o arquivo convertido anterior, se existir
        if os.path.exists(arquivo_convertido):
            os.remove(arquivo_convertido)

        # Se o arquivo for .OGA ou .OPUS, converte para .WAV
        if arquivo_audio.endswith((".oga", ".opus")):
            comando = f"ffmpeg -i \"{arquivo_audio}\" \"{arquivo_convertido}\""
            subprocess.run(comando, shell=True)

        # Carregar o modelo Whisper
        modelo = whisper.load_model("large")

        # Usar o arquivo convertido para transcrição
        resposta = modelo.transcribe(arquivo_convertido)

        # Exibir a transcrição na interface
        transcricao_texto.config(state="normal")  # Permitir edição temporária
        transcricao_texto.delete("1.0", tk.END)   # Limpar texto anterior
        transcricao_texto.insert(tk.END, resposta['text'])  # Inserir o texto transcrito
        transcricao_texto.config(state="disabled")  # Bloquear edição novamente

        atualizar_status("Transcrição concluída com sucesso!")  # Atualiza o status para concluído

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo: {e}")
        atualizar_status("Erro durante a transcrição.")

# Função para abrir o seletor de arquivos e transcrever o áudio
def selecionar_audio():
    arquivo_audio = filedialog.askopenfilename(filetypes=[("Áudio", "*.oga;*.opus")])
    
    if arquivo_audio:  # Verifica se o usuário selecionou um arquivo
        atualizar_status(f"Arquivo selecionado: {os.path.basename(arquivo_audio)}")  # Atualiza o status do arquivo
        transcrever_arquivo(arquivo_audio)

# Função para atualizar o status na interface
def atualizar_status(mensagem):
    status_label.config(text=mensagem)

# Criar a interface gráfica com Tkinter
root = tk.Tk()
root.title("Transcrição de Áudio")

# Configuração da interface
root.geometry("600x450")

# Label para título
titulo = tk.Label(root, text="Transcrição de Áudio", font=("Arial", 16))
titulo.pack(pady=10)

# Área de texto para exibir a transcrição (Text Widget)
transcricao_texto = tk.Text(root, wrap="word", font=("Arial", 12), height=15, width=70)
transcricao_texto.pack(pady=10)
transcricao_texto.config(state="disabled")  # Configurar como read-only inicialmente

# Label para status
status_label = tk.Label(root, text="Selecione um arquivo para iniciar.", font=("Arial", 10), fg="blue")
status_label.pack(pady=5)

# Botão para selecionar o arquivo de áudio
botao_selecionar = tk.Button(root, text="Selecionar Áudio", command=selecionar_audio, font=("Arial", 12))
botao_selecionar.pack(pady=20)

# Iniciar a interface gráfica
root.mainloop()
