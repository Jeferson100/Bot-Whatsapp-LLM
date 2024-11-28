from langchain_groq import ChatGroq
#from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from funcoes_auxiliares import search_and_incorporate

load_dotenv()

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
        """In memory implementation of chat message history."""

        messages: List[BaseMessage] = Field(default_factory=list)

        def add_messages(self, messages: List[BaseMessage]) -> None:
                """Add a list of messages to the store"""
                self.messages.extend(messages)

        def clear(self) -> None:
                self.messages = []


def chat_bot(mensagem,
             # history
             ):
    
    """
    Generates a response from the chatbot for a given input message.

    Args:
        mensagem (str): The input message from the user.

    Returns:
        str: The chatbot's response based on movie recommendations.

    Behavior:
        - If the user greets, responds with a greeting.
        - If the user asks a question related to movies, provides two movie suggestions with a brief summary.
        - Uses internet search data to base responses.
        - Responds only if the user initiates contact.
        - Provides all responses in Portuguese.
    """
    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.2-11b-vision-preview",
        temperature=0.5,
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template("""
                                                      You are a chatbot specialized in movie recommendations for WhatsApp. Respond only to questions related to movie suggestions.

                                                        Behavior:
                                                        If the user greets you, greet them back; otherwise, respond only to the user's question.

                                                        Recommendations:
                                                        Always provide up to 5 movie suggestions with a brief summary of each. You receive internet search data about the subject requested by the user and should use this data to base your responses.
                                                        You are a chatbot specialized in movie recommendations for WhatsApp. Respond only to questions related to movie suggestions.
                                                        
                                                        
                                                        Restrictions:
                                                        Respond only if the user initiates contact. If the user neither greets nor asks a question, do not respond.
                                                        If the user asks where they can watch a movie, Just indicate where the movie is available without recommending another movie.

                                                        Final Note: Provide all responses in Portuguese.
                                                      """),
           # MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ]
    )
    
    llm_chain = prompt | model| StrOutputParser()
    

    pesquisa = search_and_incorporate(mensagem)
    
    combined_input = f"{mensagem}\n{pesquisa}"
    
    if len(combined_input) > 6999:
        combined_input = combined_input[:6500]
    
    resposta = llm_chain.invoke([{"role": "user", "content": combined_input}], 
                                         config={"configurable": {"session_id": "foo"}}
                                         )
    
    
    return resposta
    

