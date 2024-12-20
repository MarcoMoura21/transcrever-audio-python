import subprocess
import whisper
import os

# Caminho da pasta onde os áudios estão
pasta_audios = r"C:\Users\kiko\Downloads\Audio_Transcrever"

# Procura o primeiro arquivo .oga ou .opus na pasta
arquivo_audio = None
for arquivo in os.listdir(pasta_audios):
    if arquivo.endswith((".oga", ".opus")):
        arquivo_audio = os.path.join(pasta_audios, arquivo)
        break  # Vai parar no primeiro arquivo encontrado

# Se um arquivo de áudio foi encontrado
if arquivo_audio:
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

    # Imprimir a transcrição
    print(resposta)
else:
    print("Nenhum arquivo de áudio encontrado.")
