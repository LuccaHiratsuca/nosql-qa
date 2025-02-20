# NoSQL Tabular Data Question Answering System with Mongo DB

This repository contains a complete implementation of a hybrid question answering system over tabular data stored in a NoSQL database. The system is designed to efficiently and precisely answer queries on tabular datasets—regardless of whether the questions involve numerical calculations or textual retrieval—by combining the interpretative power of Large Language Models (LLMs) with the precise aggregation capabilities of NoSQL databases.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
  - [Challenges with SQL-Based Systems](#challenges-with-sql-based-systems)
  - [Our Hybrid Approach](#our-hybrid-approach)
- [System Architecture](#system-architecture)
  - [Data Ingestion](#data-ingestion)
  - [Query Processing](#query-processing)
- [API Endpoints](#api-endpoints)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Configuration](#configuration)

---

## Problem Statement

Modern applications increasingly rely on tabular data generated from diverse sources. Traditional SQL-based systems present several challenges when handling these datasets:

- **Scalability Issues:**  
  Relational databases require predefined schemas, making them inflexible when handling various tabular formats. Storing heterogeneous tabular data (with varying columns, data types, and structures) demands constant schema migrations, complicating scalability and maintenance.

- **Schema Rigidity:**  
  SQL databases enforce a strict schema. When tabular data from different sources or with evolving formats must be stored, the system either needs to normalize or transform the data—often leading to performance bottlenecks and increased development overhead.

- **Limited Numerical and Textual Integration:**  
  While SQL excels at structured numerical queries (aggregations, sums, averages), it may not handle natural language queries or unstructured text as flexibly. Moreover, LLMs, when directly applied to tabular data, may fail to perform precise arithmetic operations.

These limitations call for a system that can:
1. **Scale Efficiently:** Store various tabular data files in a NoSQL database that does not require a rigid schema.
2. **Handle Heterogeneous Data:** Adapt to different tabular formats without extensive preprocessing.
3. **Provide Accurate Answers:** Combine precise numerical calculations (using NoSQL aggregation functions) with the natural language understanding of LLMs to answer both numeric and textual queries.

---

## Solution Overview

Our solution leverages a **hybrid approach** that integrates a NoSQL database (MongoDB) with LLM capabilities to process and answer queries over tabular data.

### Challenges with SQL-Based Systems

- **Rigid Schemas:** SQL databases require a fixed schema, which complicates storing tabular data files that vary in structure.
- **Scalability Constraints:** Scaling SQL databases typically involves vertical scaling, which can be costly and limit performance when handling large, heterogeneous datasets.
- **Limited Flexibility in Querying:** While SQL is powerful for structured queries, converting natural language questions into complex SQL queries for numerical operations can be error-prone, and LLMs often struggle with exact arithmetic within textual outputs.

### Our Hybrid Approach

1. **Data Ingestion:**  
   - Tabular data files are processed using Python (via libraries like Pandas) and stored in MongoDB.
   - Each row is transformed into a document that preserves both the raw data (as a dictionary) and a textual representation.
   - An embedding is generated for each row (using OpenAI’s embedding model) to facilitate semantic similarity search.

2. **Query Processing:**  
   - **Question Classification:** An LLM classifies incoming questions as "numeric," "textual," or "mixed" based on whether they require precise calculations, text retrieval, or both.
   - **Numerical Queries:** For numeric aspects, the LLM generates a MongoDB aggregation pipeline that filters and groups data to compute exact results (e.g., sums, averages).
   - **Textual Queries:** For textual queries, a similarity search is performed over the stored embeddings to retrieve relevant context.
   - **Response Generation:** The system combines the numeric results and textual context into a final prompt and sends it to the LLM (e.g., GPT-3.5-turbo) to generate a concise and accurate answer.

3. **Automatic File Selection:**  
   The system automatically selects the most relevant file (i.e., the `excel_id`) based on the similarity between the question and the stored embeddings. This removes the need to manually pass an `excel_id` with each query.

---

## System Architecture

### Data Ingestion

- **Endpoint:** `/upload`
- **Process:**
  1. Accepts a file upload (tabular data file) and a `user_id`.
  2. Reads the file using Pandas.
  3. For each row:
     - Creates a text representation (e.g., `"Column1: value1 | Column2: value2 | ..."`)
     - Generates an embedding using OpenAI’s embedding model.
     - Stores the document in MongoDB with fields: `user_id`, `excel_id` (a unique identifier for the file), `row_text`, `data`, and `embedding`.

### Query Processing

- **Endpoint:** `/ask`
- **Process:**
  1. Receives a question along with a `user_id`.  
     The system automatically groups stored documents by `excel_id` and selects the file whose data best matches the question.
  2. Classifies the question as "numeric," "textual," or "mixed" using an LLM.
  3. **For Numeric/Mixed Queries:**  
     - Generates an aggregation pipeline via an LLM that translates the natural language question into a MongoDB query.
     - Executes the pipeline to get an exact numeric result.
  4. **For Textual/Mixed Queries:**  
     - Computes the embedding of the question and retrieves top relevant documents using cosine similarity.
  5. Combines both numeric and textual results into a final prompt and calls the LLM to generate a complete answer.
  6. Returns the answer along with the `excel_id` (i.e., the file used) for traceability.

---

## API Endpoints

### **Upload Endpoint**

```http
POST /upload
Content-Type: multipart/form-data
```

**Parameters:**
- `user_id` - form field, string: Identifier for the user
- `file` - form field, file: Tabular data file (e.g., CSV, Excel)

**Response:**
```json
{
  "message": "File processed and data stored successfully.",
  "excel_id": "unique-file-id"
}

```

### **Question Answering Endpoint**

```http
POST /ask
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "user123",
  "question": "What is the sum of the sales column for January?"
}
```

**Response:**
```json
{
  "answer": "The total sales for January is 12345.",
  "arquivo_utilizado": "unique-file-id",
  "prompt_used": "Final prompt sent to the LLM..."
}
```

---

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone ...
   cd no-sql-tabular-qa
    ```
2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Create a `.env` file in the root directory and add the following variables:
   ```env
    MONGO_URI=mongodb://localhost:27017
    DB_NAME=nosql_qa_db
    OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the Application:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

---

## Usage

1. **Upload Tabular Data:**
    Use the `/upload` endpoint to upload your tabular data files. These files will be processed and stored in the NoSQL database along with their embeddings.

2. **Asking Questions:**
    Use the `/ask` endpoint to send questions. The system will:

    - Classify the query (numeric, textual, or mixed).
    - Generate and execute an aggregation pipeline for numerical queries.
    - Retrieve relevant textual context for textual queries.
    - Combine the results and generate an answer using an LLM.

---

## Configuration

- **MongoDB Configuration:**  
  The MongoDB connection URI and database name can be configured using the `MONGO_URI` and `DB_NAME` environment variables.

- **OpenAI API Key:**
    To use the OpenAI embedding model, you need to provide an API key in the `OPENAI_API_KEY` environment variable.

- **Tabular Data:**
The system is designed to handle tabular data with arbitrary columns. During ingestion, each row is converted into a document that contains both the raw data and a textual representation for semantic searches.

---
