from langchain_core.messages import HumanMessage, SystemMessage, AIMessage,RemoveMessage
import uuid
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
from extracao_textos_links import LinksExtractor
from langchain_community.tools import TavilySearchResults

load_dotenv()

model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.2-11b-vision-preview",
        temperature=0.5,
    )

def summarize_messages(store, name="foo"):
    """
    Summarize the last two messages in the chat history.

    Args:
        store: The chat history store.
        name: The name of the chat history to summarize.

    Returns:
        The updated chat history store with the last two messages summarized and any messages older than 6000 characters removed.

    """
    
    prompt_summary = ChatPromptTemplate.from_messages(
                    [
                        SystemMessagePromptTemplate.from_template("""
                                                                Summarize the received information and the provided response.
                                                                Try to condense it into 300 characters. Write only the summary without adding extra messages or irrelevant information.
                                                                Use only words, avoiding punctuation or special formatting.
                                                                """),
                        
                        HumanMessagePromptTemplate.from_template("{input}")
                    ]
                )

    llm_chain_summary = prompt_summary | model | StrOutputParser()

    # Resumindo as duas últimas mensagens
    for i in range(-2, 0):  # Itera sobre as duas últimas mensagens
        mensagem = store[name].messages[i]
        if isinstance(mensagem, (HumanMessage, AIMessage)):
            summary = llm_chain_summary.invoke(input=mensagem)
            store[name].messages[i] = mensagem.__class__(content=summary, id=str(uuid.uuid4()))
    
    
    total_length = sum(len(msg.content) for msg in store[name].messages)
    
    if total_length >= 6000:
        # Remove as duas mensagens mais antigas 
        store[name].messages = store[name].messages[2:]
             
    return store

            
def search_and_incorporate(user_input):
    # Realizando a pesquisa
     
    """
    Performs a search based on the user input, filters the search results,
    extracts and cleans the text from the filtered URLs, and combines the
    cleaned text with the original user input to produce a final output.

    Args:
        user_input (str): The input query from the user.

    Returns:
        str: The combined string of the original user input and the cleaned
        text extracted from the filtered search results.
    """
    
    search_tool = TavilySearchResults(
    max_results=2,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False)
    
    pesquisa = search_tool.invoke({"query": user_input})

    links = []
    
    for numero in range(len(pesquisa)):
        links.append(pesquisa[numero]['url'])
        
    # Filtrando resultados para remover links do YouTube
    links_results = [result for result in links if "youtube.com" not in result]


    extractor = LinksExtractor()
    
    texto = []
    
    for link in links_results:
        texto.append(extractor.clean_text(link))
        
    if isinstance(texto, list):
        texto = "\n".join(texto)
    
    combined_input = user_input + texto
    
    return combined_input