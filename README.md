## PorFin Simple Chatbot

#### Architecture

#### ConfigurationF
This project contains a chatbot using the following libraries

- Streamlit (https://streamlit.io/)
- Langchain (https://www.langchain.com/)
  - Qdrant (https://qdrant.tech/)
  - Huggingface (https://huggingface.co/)

### How to Use

#### Pre-requisite

- Docker installed
  It is suggested to use OrbStack (https://orbstack.dev/) a lighter tool to run Docker containers.

#### Running

Execute the following command inside `porfin` directory:

```shell
 docker-compose -f deployment/docker-compose.yml --project-directory . up --build
```

### Future works

#### 1. Save interactions to a database

Save interactions to database so the interactions can be used to enhance the chatbot for future interactions.

> Anonymize confidential information
