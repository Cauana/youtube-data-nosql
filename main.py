from youtool import YouTube
from pymongo import MongoClient
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
import os

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
        title = item["snippet"]["title"]
        stats = item["statistics"]
        views = int(stats.get("viewCount", 0))
        comments = int(stats.get("commentCount", 0))
        videos_completos.append({
            "title": title,
            "view_count": views,
            "comment_count": comments
        })

print(f"✅ Estatísticas coletadas para {len(videos_completos)} vídeos.")

client = MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
col = db["videos_manodeyvin"]

for v in videos_completos:
    col.update_one(
        {"title": v["title"]},
        {"$set": v},
        upsert=True
    )

print("💾 Vídeos salvos/atualizados no MongoDB.")

top_visualizacoes = sorted(videos_completos, key=lambda x: x["view_count"], reverse=True)[:5]
top_comentarios = sorted(videos_completos, key=lambda x: x["comment_count"], reverse=True)[:5]

print("\n🏆 Top 5 Vídeos por Visualizações:")
for i, v in enumerate(top_visualizacoes, 1):
    print(f"{i}. {v['title']} - {v['view_count']} views")

print("\n📝 Top 5 Vídeos por Comentários:")
for i, v in enumerate(top_comentarios, 1):
    print(f"{i}. {v['title']} - {v['comment_count']} comentários")

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
