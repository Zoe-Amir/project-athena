import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import pinecone
import openai


def query_gpt(api_key_openai, api_key_pinecone, index_name, embed_model_name, query, history="\{\}"):
    # Setup OpenAI GPT API
    openai.api_key = api_key_openai

    # Setup Pinecone
    pinecone.init(api_key=api_key_pinecone, environment='gcp-starter')
    index = pinecone.Index(index_name)

    # Accept user input and generate response
    res = openai.Embedding.create(
        input=[query],
        engine=embed_model_name
    )

    # Retrieve from Pinecone
    xq = res['data'][0]['embedding']
    res = index.query(xq, top_k=5, include_metadata=True)
    contexts = [item['metadata']['text'] for item in res['matches']]

    # Augment the query with relevant contexts
    augmented_query = f"""\n\n---\n\ncontext='The bot (Owl) will have to be ...'""".join(
        contexts) + "\n\n-----\n\nliterature(Article/Book/PDF)=" + history+"\n\n----\n\n" + query

    # Define the primer
    primer = "You're owl of Athena, Be friendly and supportive to help others learning. You can be referred as the literature enclosed as well. e.g. you will be asked to personify the literature as yourself"

    # Query GPT-4
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": augmented_query}
        ]
    )

    return res['choices'][0]


def handler(event, context):
  print('received event:')
  print(event)
  query='Hi there! How are you?'
  history="\{\}"
  if event and event['question'] is not None:
     query=event['question']
  if event and event["context"] is not None:
     history=event["context"]
  res = query_gpt(api_key_openai="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",
                  api_key_pinecone="09a611bc-0e25-4710-9f6d-1386849bd03e",
                  index_name="articles",
                  embed_model_name="text-embedding-ada-002",
                  query=query, history=history)
  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': res
  }
