# StardewGPT 🐔

A Retrieval-Augmented Generation (RAG) pipeline using Llama 3.1 8B to answer questions any regarding the game Stardew Valley. The dataset used for this pipeline came from the [Stardew Valley Wiki](https://stardewvalleywiki.com/Stardew_Valley_Wiki) itself.

## Web App
This comes with a web app that is built using Chainlit. To start the it just type: ```chainlit run app.py```

## Dataset Generation 
To scrape the Stardew Valley Wiki use the wikiteam3 Python package and run: ```wikiteam3dumpgenerator  https://stardewvalleywiki.com/  --xml --curonly --namespaces 0```


## Libraries Used
- Llama-Index
- Ollama
- Chainlit 
- Chroma DB 


