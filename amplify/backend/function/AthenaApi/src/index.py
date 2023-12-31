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


def query_gpt(api_key_openai, api_key_pinecone, index_name, embed_model_name, query):
    # Setup OpenAI GPT API
    openai.api_key = api_key_openai

    # Setup Pinecone
    pinecone.init(api_key=api_key_pinecone, environment='gcp-starter')
    index = pinecone.Index(index_name)

    # Initialize ChatOpenAI model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key_openai)

    # Setup the conversation memory buffer
    buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

    # Define the prompt template
    system_msg_template = SystemMessagePromptTemplate.from_template(
        template="""Answer the question as truthfully as possible using the provided context,
        and if the answer is not contained within the text below, say 'I don't know'""")
    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
    prompt_template = ChatPromptTemplate.from_messages(
        [system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

    # Initialize the conversation chain
    conversation = ConversationChain(memory=buffer_memory, prompt=prompt_template, llm=llm, verbose=True)


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
        contexts) + "\n\n-----\n\n" + query

    # Define the primer
    primer = "You're owl of Athena, Be friendly and supportive to help others learning"

    # Query GPT-4
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": augmented_query}
        ]
    )

    return res

def handler(event, context):
  print('received event:')
  print(event)
  res = query_gpt(api_key_openai="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",
            api_key_pinecone="09a611bc-0e25-4710-9f6d-1386849bd03e",
            index_name="articles",
            embed_model_name="text-embedding-ada-002",
            query="What is the best way to learn a new language?")
  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps({'res':res})
  }