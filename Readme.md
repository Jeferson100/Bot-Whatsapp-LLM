# Chat Bot LLM no WhatsApp

## Descrição

Este projeto implementa um chatbot para recomendações de filmes para WhatsApp utilizando Large Language Models (LLM). O bot é capaz de processar mensagens naturalmente e fornecer respostas contextualizadas usando a API do WhatsApp Business.
O projeto utiliza as seguintes Tecnologias: 🚀

- **[LangChain](https://www.langchain.com/)** Framework para construção de modelos baseados em LLMs.

- **[Groq](https://groq.com/)** Biblioteca para criação de Modelos LLM

- **[Crawl4ai](https://github.com/unclecode/crawl4ai)** Biblioteca para extracao de textos e links de paginas web

- **[Tavily](https://docs.tavily.com/docs/integrations/langchain)** Biblioteca para busca e incorporação de resultados online

- **[Ngrok](https://ngrok.com/)** Para criar um endpoint para receber as mensagens do whatsapp

- **[FastAPI](https://fastapi.tiangolo.com/)** Framework para desenvolvimento de APIs


## Requisitos

- 1. Crie uma conta no [Meta developer](https://developers.facebook.com/).

- 2. Primeiro configure o whatsapp para receber mensagens, [tutorial aqui](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started#set-up-developer-assets)

- 2. 1 - Aqui um primeiro exemplo da integração de python com o whatsapp [exemplo aqui](https://developers.facebook.com/blog/post/2022/10/24/sending-messages-with-whatsapp-in-your-python-applications/).

- 3. Crie e configure o webhook (endpoint) com Ngrok para receber as mensagens, [tutorial aqui](https://ngrok.com/docs/integrations/whatsapp/webhooks/)

## Codigos do projeto

O projeto conta com os seguintes arquivos:

### Extracao_textos_links

O arquivo [extracao_textos_links](extracao_textos_links.py) contém uma classe Python chamada `LinksExtractor` que utiliza o [crawl4ai](https://github.com/unclecode/crawl4ai) para extrair, processar e limpar texto de URLs fornecidas. Ele é útil para obter o conteúdo em formato markdown de uma página web, remover links e limpar o texto extraído para uso em modelos LLMs.

**Observação importante:**

O pacote crawl4ai não funciona em notebooks, ocorrendo um erro. 

#### Exemplo de Uso

```python

from extracao_textos_links import LinksExtractor

# Inicialize o extrator
extractor = LinksExtractor()

# URL alvo
url = "https://www.eu-startups.com/directory/"

# Extraia e limpe o texto
texto_limpo = extractor.clean_text(url)

print(texto_limpo)

```

### Enviar_mensagem

O arquivo [enviar_mensagem](enviar_mensagem.py) fornece uma implementação em Python para enviar mensagens de texto via **API do WhatsApp Business**, utilizando o **Facebook Graph API**. Ele inclui funcionalidades para configurar as credenciais necessárias, criar mensagens no formato JSON, e enviar mensagens a destinatários específicos.


#### Exemplo de Uso

Certifique-se de ter as seguintes variáveis configuradas no arquivo `.env`:

- `ACCESS_TOKEN`
- `RECIPIENT_WAID`
- `PHONE_NUMBER_ID`
- `VERSION`
- `APP_ID`
- `APP_SECRET`

##### Código Exemplo

```python
from whatsapp_api import get_text_message_input, send_message

# Mensagem e destinatário
mensagem = "Olá! Esta é uma mensagem de teste."

destinatario = os.getenv("RECIPIENT_WAID")

# Gera o payload
data = get_text_message_input(destinatario, mensagem)

# Envia a mensagem
response = send_message(data)

# Verifica a resposta
print(response.status_code)
print(response.json())
```

### Funções Auxiliares

Este arquivo [funcoes_auxiliares](funcoes_auxiliares.py) implementa funcionalidades de **resumo de mensagens** e **integração com ferramentas de busca** utilizando o framework **LangChain**. O código permite condensar históricos de mensagens e incorporar informações externas a partir de pesquisas na web, otimizando fluxos de conversação e tomada de decisões.


#### Resumo de Mensagens (`summarize_messages`)
- **Descrição**: 
  - Resume as duas últimas mensagens em um histórico de conversação.
  - Condensa o conteúdo em até 300 caracteres, utilizando um modelo de linguagem configurado com **LangChain**.
  - Remove mensagens antigas para manter o histórico abaixo de 6000 caracteres.

```python
from funcoes_auxiliares import summarize_messages, search_and_incorporate

# Resumindo mensagens
store = {"foo": {"messages": [HumanMessage(content="Qual a previsão do tempo hoje?"), AIMessage(content="O tempo estará ensolarado.")]}}

store_resumido = summarize_messages(store, name="foo")
print(store_resumido)
```	
---

#### Busca e Incorporação de Resultados (`search_and_incorporate`)
- **Descrição**:
  - Realiza buscas online com base na entrada do usuário utilizando o **TavilySearchResults**.
  - Filtra URLs irrelevantes, como links do YouTube.
  - Extrai e limpa o texto dos resultados utilizando a classe `LinksExtractor`.
  - Combina o texto limpo com a entrada original do usuário para gerar uma nova entrada aprimorada.

```python
from funcoes_auxiliares import search_and_incorporate

# Incorporando informações da web
user_input = "Quais são as últimas notícias sobre IA?"
resultado = search_and_incorporate(user_input)
print(resultado)
```

### Chat_bot
O arquivo [chat_bot](chat_bot.py) implementa um **chatbot de recomendações de filmes** projetado para interagir com os usuários no WhatsApp. Baseado em **LangChain** e **Groq AI**, o modelo LLM utilizado é o **llama-3.2-11b-vision-preview**, esse modelo tem uma capacidade de linguagem avançada para oferecer sugestões personalizadas de filmes com base em consultas do usuário.

```python
from chat_bot import chat_bot

mensagem_usuario = "Recomende alguns filmes de ação."
resposta = chat_bot(mensagem_usuario)

print(resposta)
```


### app

O arquivo [app][app.py] implementa uma **API Flask** para um chatbot integrado ao WhatsApp. O chatbot utiliza **LangChain** para gerar respostas contextuais e personalizadas, enquanto a API gerencia o recebimento de mensagens, processamento e envio de respostas.

Exemplo de Funcionamento 📖

#### Fluxo de Mensagens

1. O usuário envia uma mensagem pelo WhatsApp.
2. O webhook da NGROK recebe a mensagem e a envia para a API.
3. A API:
   - Extrai o texto da mensagem e o número de telefone.
   - Gera uma resposta usando o `chat_bot`.
   - Envia a resposta de volta ao usuário no WhatsApp.

## Execução Do Projeto

- Crie um ambiente virtual com o comando:

```bash	
python -m venv venv
source venv/bin/activate
```	

- Instale as dependências do projeto com o comando:

```bash
pip install -r requirements.txt
```

- Execute o seu dominio no ngrok com o comando:

```bash
ngrok http --url= seu dominio no ngrok: 3000
```

- Execute o projeto com o comando:

```bash	
python app.py
```

## Contribua para o Projeto

- Sinta-se a vontade para contribuir com o projeto, abra uma issue ou envie um pull request.

# Licenca

Este projeto esta licenciado sob a licenca MIT



