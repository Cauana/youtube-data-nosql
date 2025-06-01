from pathlib import Path
from youtool import YouTube
from pymongo import MongoClient
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
import os

def gravarTranscricaoVideo(idVideo):
    api_key = os.getenv("YOUTUBE_API_KEY")
    yt = YouTube([api_key], disable_ipv6=True)
    download_path = Path("transcriptions")
    if not download_path.exists():
        download_path.mkdir(parents=True)
    yt.videos_transcriptions([idVideo],language_code="pt",path=download_path)

def coletarArmazenarDadosCanal():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    canal_url = "https://www.youtube.com/@manodeyvin"

    yt = YouTube([api_key], disable_ipv6=True)

    channel_id = yt.channel_id_from_url(canal_url)
    playlist_id = "UU" + channel_id[2:]

    print("Coletando lista de vídeos do canal...")
    videos_basicos = list(yt.playlist_videos(playlist_id))
    print(f"{len(videos_basicos)} vídeos encontrados.")

    video_infos = [{"id": video["id"], "title": video["title"]} for video in videos_basicos]

    print("Buscando estatísticas detalhadas dos vídeos via API...")

    videos_completos = []
    batch_size = 50  

    for i in range(0, len(video_infos), batch_size):
        batch = video_infos[i:i+batch_size]
        ids_param = ",".join(video["id"] for video in batch)

        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={ids_param}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        for item in data.get("items", []):
            id  = item["id"]
            title = item["snippet"]["title"]
            stats = item["statistics"]
            views = int(stats.get("viewCount", 0))
            comments = int(stats.get("commentCount", 0))
            videos_completos.append({
                "id" : id,
                "title": title,
                "view_count": views,
                "comment_count": comments
            })

    print(f"✅ Estatísticas coletadas para {len(videos_completos)} vídeos.")

    for v in videos_completos:
        col.update_one(
            {"title": v["title"]},
            {"$set": v},
            upsert=True
        )

    print("💾 Vídeos salvos/atualizados no MongoDB.")


def mostrarVideosMaisVisualizacoes():

    videos_completos = col.find()

    top_visualizacoes = sorted(videos_completos, key=lambda x: x["view_count"], reverse=True)[:5]

    print("\n🏆 Top 5 Vídeos por Visualizações:")
    for i, v in enumerate(top_visualizacoes, 1):
        print(f"{i}. {v['title']} - {v['view_count']} views")


def mostrarVideos():

    videos_completos = col.find()

    print("\nTodos os Vídeos:")
    for i, v in enumerate(videos_completos, 1):
        print(f"{i}. {v['id']} {v['title']}")

def mostrarVideosMaisComentarios():

    videos_completos = col.find()

    top_comentarios = sorted(videos_completos, key=lambda x: x["comment_count"], reverse=True)[:5]

    print("\n📝 Top 5 Vídeos por Comentários:")
    for i, v in enumerate(top_comentarios, 1):
        print(f"{i}. {v['title']} - {v['comment_count']} comentários")

def mostrarGraficoMaisVisualizacoes():
    videos_completos = col.find()

    top_visualizacoes = sorted(videos_completos, key=lambda x: x["view_count"], reverse=True)[:5]
    plt.figure(figsize=(10, 6))
    plt.barh(
        [v['title'][:40] for v in top_visualizacoes],
        [v['view_count'] for v in top_visualizacoes],
        color='skyblue'
    )
    plt.xlabel("Visualizações")
    plt.title("Top 5 Vídeos Mais Vistos - @manodeyvin")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("top_visualizacoes.png")
    plt.show()

def mostrarGraficoMaisComentarios():
    videos_completos = col.find()

    top_comentarios = sorted(videos_completos, key=lambda x: x["comment_count"], reverse=True)[:5]
    plt.figure(figsize=(10, 6))
    plt.barh(
        [v['title'][:40] for v in top_comentarios],
        [v['comment_count'] for v in top_comentarios],
        color='lightgreen'
    )
    plt.xlabel("Comentários")
    plt.title("Top 5 Vídeos com Mais Comentários - @manodeyvin")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("top_comentarios.png")
    plt.show()


client = MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
col = db["videos_manodeyvin"]
coletarArmazenarDadosCanal()

while(True):
    print("Opções")
    print("1 - Mostrar os videos com mais visualizações")
    print("2 - Mostrar os videos com mais comentários")
    print("3 - Gráfico videos com mais visualizações")
    print("4 - Gráfico videos com mais comentários")
    print("5 - Mostrar informações dos videos salvos ")
    print("6 - Gravar transcrição de um video ")
    print("7 - Sair")

    opcao = input("Digite a opção desejada: ")
    if(opcao == '1'):
        mostrarVideosMaisVisualizacoes()
    elif(opcao == '2'):
        mostrarVideosMaisComentarios()
    elif(opcao == '3'):
        mostrarGraficoMaisVisualizacoes()
    elif(opcao == '4'):
        mostrarGraficoMaisComentarios()
    elif(opcao == '5'):
        mostrarVideos()
    elif(opcao == '6'):
        idVideo = input("Digite o id do video para gravar a transcrição: ")
        gravarTranscricaoVideo(idVideo)
    elif(opcao == '7'):
        break
    else:
        print("Opção não reconhecida")