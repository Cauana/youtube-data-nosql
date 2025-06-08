<h1> 🎬 YouTube Data + Youtool + MongoDB </h1>

Este projeto tem como objetivo coletar e visualizar estatísticas de vídeos de um canal do YouTube, usando a biblioteca **youtool**, a **YouTube Data API** e o **MongoDB** para armazenar os dados.

---

<h2> 📌 Pré-requisitos </h2>

Antes de tudo, certifique-se de ter:

- Python 3.x instalado  
- MongoDB rodando localmente  
- Uma chave de API do YouTube -> https://console.cloud.google.com/. 

<h2> 1. Clone o repositório </h2>

git clone https://github.com/Cauana/youtube-data-nosql.git

cd youtube-data-nosql

<h2> 2. Instale as dependências </h2>

pip install -r requirements.txt

<h2> 3. Configure sua API Key do YouTube </h2>

Substitua o valor da variável api_key no código, na pasta .env:

***YOUTUBE_API_KEY= "SUA CHAVE API KEY AQUI"***

<h2> 4. Inicie o MongoDB </h2>

Certifique-se de que o serviço do MongoDB está rodando localmente.

<h2> 5. Execute o script principal </h2>

```sh
python main.py
```

<h2> 6. Use o menu interativo </h2> 

O programa irá mostrar um menu como este:

```
Opções
1 - Mostrar os videos com mais visualizações
2 - Mostrar os videos com mais comentários
3 - Gráfico videos com mais visualizações
4 - Gráfico videos com mais comentários
5 - Mostrar informações dos videos salvos 
6 - Gravar transcrição de um video 
7 - Sair
```

Escolha a opção desejada digitando o número correspondente.

- **1:** Lista os 5 vídeos mais visualizados.
- **2:** Lista os 5 vídeos com mais comentários.
- **3:** Gera um gráfico dos vídeos mais visualizados.
- **4:** Gera um gráfico dos vídeos com mais comentários.
- **5:** Mostra todos os vídeos salvos no banco.
- **6:** Baixa a transcrição de um vídeo (digite o ID do vídeo).
- **7:** Sai do programa.

<h2>  7. Saída </h2> 

- Gráficos são salvos como `top_visualizacoes.png` e `top_comentarios.png`.
- Transcrições são salvas na pasta `transcriptions/`.

**Dica:** Sempre que rodar o script, ele atualiza os dados do canal no MongoDB automaticamente.

![Demonstração do projeto](https://github.com/Cauana/youtube-data-nosql/blob/main/gif/aplicacao-funcionando.gif)
