# Legiscan: AI-Powered Contract Compliance Checker

Legiscan is an AI-powered tool designed to streamline contract compliance analysis. Leveraging advanced machine learning techniques, it generates detailed compliance reports, highlighting strengths, shortcomings, and providing a compliance score for uploaded contracts.

## Key Features

- **AI-Driven Analysis**: Uses Gemini LLM to generate embeddings and perform similarity searches on stored contract data.
- **Comprehensive Reporting**: Provides a compliance score out of 100, highlights strengths and weaknesses, and explains the evaluation process.
- **Efficient Storage**: Stores embeddings, summaries, and metadata of 100+ contracts in Dockerized PostgreSQL for fast and reliable retrieval.
- **User-Friendly Interface**: Built with Streamlit, offering an intuitive experience for uploading contracts (PDF or TXT) and viewing detailed reports.
- **Cosine Similarity**: Utilized for similarity searches to compare uploaded contracts with existing data.

## Technology Stack

- **Frontend**: Streamlit
- **Machine Learning**: Gemini LLM for embeddings and analysis
- **Backend**: Dockerized PostgreSQL
- **Similarity Search**: Cosine similarity algorithm
- **Programming Language**: Python

## How It Works

1. **Upload a Contract**: Users can upload contracts in PDF or TXT format.
2. **AI Analysis**: Legiscan runs a similarity search on stored embeddings to analyze the uploaded contract.
3. **Detailed Report**: The tool generates a report with:
   - A compliance score out of 100
   - Strengths and weaknesses of the contract
   - An explanation of the analysis process

## Installation

Follow these steps to set up Legiscan on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/legiscan.git
   cd legiscan
   ```

2. **Set Up the Environment**:
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run Docker**:
   - Ensure Docker is installed and running on your machine.
   - Start the PostgreSQL container:
     ```bash
     docker-compose up
     ```

4. **Start the Application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the App**:
   - Open your browser and go to `http://localhost:8501`.

## Usage

- Upload a contract in PDF or TXT format.
- Wait for the analysis to complete.
- Download the detailed compliance report.

## Contribution

We welcome contributions! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


