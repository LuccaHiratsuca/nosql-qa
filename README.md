# Question-Answering-System_over_NoSql

## Description:
This project is a Question-Answering System over NoSQL database. The system is designed to store questions and answers in a NoSQL database and retrieve the answers to the questions asked by the user.

## Flow of the System:
1. Ingestion of Excel data (with calculation of embeddings for each row) and storage in a NoSQL database (MongoDB).
2. Classification of the question (whether numeric, textual or mixed) via LLM.
3. For numeric questions, dynamic generation of an aggregation pipeline to perform precise operations directly in MongoDB.
4. For textual questions, similarity search using previously stored embeddings.
5. Combination of the results (numeric and/or textual) in a final prompt sent to LLM to return a precise answer.


## Requirements:
1. MongoDB Atlas Account
    - Create an account on MongoDB Atlas [here](https://account.mongodb.com/account/login).

