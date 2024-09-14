
# Todo:
# 1. Remember context of the conversation - https://github.com/felipearosr/RAG-LlamaIndex/blob/main/1.Streaming%20-%20Memory%20-%20Sources/main.py - tried this already
# 2. Modify the prompt -ok 
# 3. Rerun index - ok
# 4. Update llama index package -ok 
# 4. Chainlit deco -ok
# 5. deploy

import os 
import chainlit as cl 

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from llama_index.core import VectorStoreIndex


from llama_index.core import PromptTemplate

try:
    db=chromadb.PersistentClient(path="./chroma_db")
    collection=db.get_collection("stardew_wiki")
    vector_store = ChromaVectorStore(collection)
    embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
    index = VectorStoreIndex.from_vector_store(vector_store,embed_model=embed_model)
except:
    print("Error loading the index")




@cl.set_starters
async def set_starters():
    return[
        cl.Starter(
            label="Ask about a villager's birthday",
            message="When is Maru's birthday?",
            icon="/public/starter_icons/birthday.svg"
        ),
        cl.Starter(
            label=" Community Center bundles inclusions?",
            message="What crops are in the summer bundle?",
            icon="/public/starter_icons/crop.svg"
        ),
        cl.Starter(
            label="A Village's favorite gift",
            message="What is Penny's favorite gift?",
            icon="/public/starter_icons/gift.svg"
        ),
        cl.Starter(
            label="How to obtain certain items",
            message="What is the sword you get from prismatic shard?",
            icon="/public/starter_icons/sword.svg"
        ),
    ]

@cl.on_chat_start
async def start():    
    
    # llm=Ollama(model="llama3", request_timeout=60.0)
    llm=Ollama(model="llama3.1:latest", request_timeout=120.0)
    retriever=index.as_retriever(verbose=True)

    
    query_engine=index.as_query_engine(llm=llm,similarity_top_k=3,streaming=True)

    qa_prompt_tmpl_str = """\
    Context information is below.
    ---------------------
    {context_str}
    ---------------------
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know.\
    Use three sentences maximum and keep the answer concise. \
    Only answer questions related to the video game Stardew Valley.\
    If the question is not related to the video game Stardew Valley, just say you do not know.\

    Reminders:
    1. Birthday of Characters in Stardew Valley is formatted by Season and Day number. Example: |birthday  =  {{Season|Fall}} 21.

    Question: {query_str}
    Answer: \
    """



    qa_prompt_tmpl = PromptTemplate(
        qa_prompt_tmpl_str,
        # function_mappings={"few_shot_examples": few_shot_examples_fn},
    )


    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
    )


    cl.user_session.set("query_engine", query_engine)

    # await cl.Message(
    #     author="Assistant", content="Hello! I am your assistant. You can ask me anything about Stardew Valley. How can I help you today?"
    # ).send()

@cl.on_message
async def main(message: cl.Message):
    query_engine=cl.user_session.get("query_engine")

    
    msg=cl.Message(content="",author="Assistant")

    # user_message=message.content


    res = await cl.make_async(query_engine.query)(message.content)

    for token in res.response_gen:
        await msg.stream_token(token)
    await msg.send()
