## PorFin Simple Chatbot

This simple chat uses a few-shot learning (prompting) approach to answer questions about a domain specific knowledge base. In this challenge, it is related to homeschooling. It was created a simple dataset with examples to be used during the interaction with some pre-trained LLM. The sample dataset has the following format:

```json
[
  {
    "input": "What is homeschooling?",
    "outpu": "Homeschooling is a method of education in which children are taught at home by their parents or other family members."
  }
]
```

And the model is instructed to just answer questions related to the topic.

To configure the chatbot, a `config.json` file must be placed at `src/data` and has the following format:

```json
{
  "chat_bot_title": "Title of the chatbot",
  "chat_bot_description": "Description of the chatbot",
  "llm_api_key": "api_key",
  "llm_model_name": "Groq llm model name",
  "llm_model_name_alternatives": ["list_of_all_available_models"],
  "vdb_collection": "examples_vectorstore",
  "vdb_api_url": "http://qdrad:6333",
  "system_instructions": "Instructions to the model",
  "examples_dataset_file": "json_file_with_examples",
  "embeddings_model_name": "huggingface_embedding_model_name"
}
```

This project was built using the following tools:

- Streamlit (https://streamlit.io/)
- Langchain (https://www.langchain.com/)
  - Qdrant (https://qdrant.tech/)
  - Huggingface (https://huggingface.co/)

When a user send a request, the chatbot will use the following steps:

1. Embed the user request into a vector using the embedding model.
2. Search for the most similar vectors in the vector store.
3. Use the most similar vectors to generate a prompt for the LLM.
4. Send the prompt to the LLM and get the response.
5. Return the response to the user.

### Replacing the domain specific examples

This chatbot can be easily customized to use a different dataset of examples. It can be done by only changing the configuration used. The main keys to change are:

- `chat_bot_title`: The title of the chatbot.
- `chat_bot_description`: The description of the chatbot.
- `examples_dataset_file`: The file with the examples to be used to create the few-shot prompt.
- `system_instructions`: The system instructions.

### Setting up

#### Pre-requisite

- Docker installed
  It is suggested to use OrbStack (https://orbstack.dev/) a lighter tool to run Docker containers.

#### Running

Execute the following command inside `porfin` directory:

```shell
 docker-compose -f deployment/docker-compose.yml --project-directory . up --build
```

When the container is running, open the browser at `http://localhost:8501` to interact with the chatbot.

### Future works

#### 1. Save interactions to a database

Save interactions to database so the interactions can be used to enhance the chatbot for future interactions. It is important to anonymize confidential information.

#### 2. Implement tests

Implement unit tests and ensure code coverage of at least 95%.

#### 3. Improve performance

- Implement caching to avoid re-computing embeddings for the same documents.

#### 4. Implement a REST API

Implement a REST API to allow the chatbot to be used by other applications.

#### 5. Implement a web interface

Implement a web interface to allow the chatbot to be used by users.
