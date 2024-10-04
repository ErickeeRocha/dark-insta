import os
import time
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
from instagrapi import Client

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
USERNAME = os.getenv('LOGIN')
PASSWORD = os.getenv('SENHA')

LEGENDA_FIXA = """Painel para iniciantes do 7️⃣ na bio! 🐀
.
.
.
.
#marketingdigital #marketingdigitalbrasil
#dropshipping #dropshippingbrasil #dropshippingnacional #ecommerce
#negociosonline #trafegopago
#empreendedorismodigital #rendaextra
#rendaextraemcasa #dinheiro
#dinheiroextra #dinheiroonline #shopify"""

def postar_videos_thread(pasta_videos):
    try:
        client = Client()
        client.login(USERNAME, PASSWORD)

        videos = [f for f in os.listdir(pasta_videos) if f.endswith('.mp4')]
        
        if not videos:
            raise FileNotFoundError("Nenhum vídeo encontrado na pasta selecionada.")

        horarios_postagem = [f"{hour:02d}:00" for hour in range(6, 24)]  # De 06:00 a 23:00
        videos_postados = 0
        
        for horario_postagem in horarios_postagem:
            if videos_postados >= 10:
                break

            horario_obj = datetime.strptime(horario_postagem, "%H:%M")
            agora = datetime.now()
            proxima_postagem = agora.replace(hour=horario_obj.hour, minute=horario_obj.minute, second=0, microsecond=0)

            if proxima_postagem < agora:
                proxima_postagem += timedelta(days=1)

            tempo_espera = (proxima_postagem - agora).total_seconds()

            print(f"Aguardando até {horario_postagem} para postar o vídeo {videos[videos_postados]}...")
            time.sleep(tempo_espera)

            video_path = os.path.join(pasta_videos, videos[videos_postados])
            client.video_upload(video_path, caption=LEGENDA_FIXA)
            print(f"Vídeo {videos[videos_postados]} postado com sucesso!")

            # Excluir o vídeo após a postagem
            os.remove(video_path)
            print(f"Vídeo {videos[videos_postados]} foi excluído com sucesso.")
            videos_postados += 1

        print("Postagens concluídas.")
    except Exception as e:
        print(f"Erro: {str(e)}")

def main():
    pasta_videos = input("Digite o caminho da pasta com os vídeos: ")
    if os.path.exists(pasta_videos):
        # Inicia o processo de postagem em um thread separado
        threading.Thread(target=postar_videos_thread, args=(pasta_videos,)).start()
    else:
        print("A pasta selecionada não existe.")

if __name__ == "__main__":
    main()
