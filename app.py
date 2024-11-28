from flask import Flask, request, jsonify
import json
from enviar_mensagem import get_text_message_input, send_message
import time
from chat_bot import chat_bot, InMemoryHistory
from langchain_core.chat_history import BaseChatMessageHistory
from funcoes_auxiliares import summarize_messages

store = {}
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    
    
    """
    Retrieves a chat history by session ID, creating a new history if one does not exist.
    
    Args:
        session_id (str): The session ID of the chat history to retrieve.
    
    Returns:
        BaseChatMessageHistory: The retrieved chat history.
    """
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    store = summarize_messages(store)
    return store[session_id]

app = Flask(__name__)

@app.route('/', methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def handle_post(path=''):
    """
    Handles POST requests to the root URL or any sub-path of the Flask app.

    This function is called whenever a POST request is made to the root URL or
    any sub-path of the Flask app. The function checks if the request contains a
    'message' key in the payload and if it does, it extracts the phone number
    from the payload and the message text and uses the chat_bot function to
    generate a response. The response is then sent back to the user using the
    send_message function.

    The function also logs the received message and the phone number to the
    console.

    Returns:
        A JSON response with a message indicating that the message was received
        successfully.
    """
    print("-------------- New Request POST --------------")
    data = json.dumps(request.get_json(), indent=3)
    # Verificar se a mensagem está presente no payload
    if 'message' in data:
        # Obter o texto da mensagem
        
        if isinstance(data, str):
            data = json.loads(data)
        elif isinstance(data, bytes):  
            data = json.loads(data.decode("utf-8"))
            
        # Verificar o formato do payload e extrair o número de telefone
        if 'entry' in data and 'changes' in data['entry'][0] and 'value' in data['entry'][0]['changes'][0]:
            value = data['entry'][0]['changes'][0]['value']
            if 'contacts' in value:
                ## Obter o numero de telefone
                number_phone = value["contacts"][0]["wa_id"]
                
                ## Verificar se o numero de telefone tem o formato correto
                if len(number_phone) == 12:
                    number_phone = number_phone[:4] + '9' + number_phone[4:]
                ## Obter o texto da mensagem   
                message_text = value["messages"][0]["text"]["body"]
                
                time.sleep(5)
                
                ## Responder a mensagem
                resposta = chat_bot(message_text
                                    #, get_by_session_id
                                    )
                ## Formatar a resposta
                data = get_text_message_input(
                recipient=int(number_phone), text=resposta
                )
                ## Enviar a mensagem
                send_message(data)
                
                # Mova isso para depois de usar o store
                
                print("Mensagem recebida com sucesso.")
                print("Mensagem:", message_text)
                print("Número:", number_phone)
                
        else:
            pass

    return jsonify({"message": "Thank you for the message"})

if __name__ == '__main__':
    print(f"Example Facebook app listening at port 3000")
    app.run(port=3000)