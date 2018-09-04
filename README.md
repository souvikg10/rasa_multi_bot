# Rasa chatbot example
This is an example bilingual rasa chatbot implementation that can be connected to your Facebook page using chatfuel.

## Proof of Concept
The project is a quick implementation to demonstrate a desired architecture of Rasa components using the latest tensforflow embeddings
in French and English

Feel free to make the project your own. 

## How to start

Requirements 
- Docker

### 1
```
docker-compose up --build

```

### 2
You will have two servers up 
at localhost:5005 - serving the english model
at localhost:5006 - serviing the french model

### 3
Redis tracker is running at port 6379
