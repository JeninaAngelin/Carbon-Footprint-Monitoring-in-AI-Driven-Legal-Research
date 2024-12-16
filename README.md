# AI's Carbon Footprint caused by Information Retrieval System: A Case Study

This project was presented at the **15th ICEEE 2024 Online International Annual Conference**, held on November 21st and 22nd, 2024, at Obuda University, Budapest, Hungary. The presentation highlighted the system’s innovative integration of AI-based legal research and its commitment to sustainability by minimizing carbon footprints.

## Project Overview

The Legal Information Retrieval System is designed to improve legal research efficiency by enabling the retrieval of relevant case summaries and legal documents. The system focuses on sustainability by tracking and optimizing energy consumption throughout its operations. Using natural language processing (NLP), semantic similarity engines, and energy monitoring tools, it provides legal professionals and researchers with accurate, environmentally-conscious tools for document retrieval.

To ensure sustainability, the system analyzes the following aspects:

- **Energy Consumption**: Tracks electricity usage (kWh) for various tasks, including data preprocessing, embedding collection, model training, and document retrieval.
- **Carbon Emissions**: Calculates CO₂ emissions generated during computational tasks to assess environmental impact.
- **Optimization Potential**: Identifies high-impact stages in the workflow (e.g., model training and inference) where energy and resource efficiency can be improved.
- **Efficiency Metrics**: Monitors GPU and CPU utilization to optimize performance while minimizing waste.
- **Algorithmic Efficiency**: Evaluates and implements energy-efficient algorithms to reduce computational overhead.
- **Sustainability Insights**: Provides actionable recommendations for using renewable energy sources, optimizing code, and adopting green AI practices.

---

## Features

### 1. **Data Ingestion and Preprocessing**
- Load and process legal case files from sources such as the Australian Federal Courts website.
- Apply XML parsing, tokenization, stemming, and vectorization (e.g., TF-IDF) to prepare documents for analysis.

### 2. **Document Similarity and Retrieval**
- Utilize pretrained models from libraries like Transformers to compute embeddings for legal documents.
- Deploy a semantic similarity engine to compare input queries with database documents and rank results based on relevance.

### 3. **Energy Monitoring and Optimization**
- Track energy usage (kWh) and carbon emissions (kg CO₂) for tasks like preprocessing, embedding collection, model training, and retrieval.
- Identify and implement optimizations at high-impact stages, such as XML parsing and document retrieval.

### 4. **Sustainability Insights**
- Highlight the environmental impact of the retrieval process by integrating tools like CodeCarbon and gpustat to measure energy efficiency.
- Provide actionable insights for developers to adopt energy-efficient algorithms and minimize the ecological footprint of AI-driven systems.

---

## Methodology

### **Data Preprocessing**
- Clean and tokenize legal documents.
- Convert text into numerical embeddings for semantic analysis.

### **Model Training**
- Fine-tune pretrained language models using embeddings of XML-parsed legal documents.
- Evaluate energy usage during training with a focus on GPU and CPU consumption.

### **Document Retrieval**
- Rank and retrieve relevant legal documents based on similarity scores.
- Optimize inference processes to reduce energy usage while maintaining accuracy.

### **Computational Resource Analysis**
- Calculate energy metrics such as kWh and CO₂ emissions for each operational stage.
- Use Python libraries like Carbon Tracker and pynvml to assess and minimize resource utilization.

---

## Environmental Impact and Carbon Footprint Results

The project meticulously tracked energy consumption and carbon emissions at various stages of development. The results are summarized in the table below:

| **Stage**               | **Energy Consumption (kWh)** | **Carbon Emissions (kg CO₂)** | **Optimization Potential**       |
|--------------------------|-----------------------------|-------------------------------|-----------------------------------|
| **XML Cleaning**         | 0.12                       | 0.054                         | High                             |
| **Embedding Collection** | 0.35                       | 0.157                         | Moderate                         |
| **Model Training**       | 1.24                       | 0.558                         | High (most energy-intensive)     |
| **Document Retrieval**   | 0.18                       | 0.081                         | Significant                      |

This table highlights the stages with the greatest environmental impact and identifies opportunities for optimization. The total training hours amounted to **2 hours and 46 minutes**, with the final output achieving accurate retrieval of top-k related legal cases based on semantic similarity. These findings underscore the importance of energy-efficient practices in AI systems, particularly during model training and deployment.

---

## Key Findings

1. Training and retrieval processes consumed measurable energy, highlighting the importance of optimizing algorithms and hardware.
2. By implementing optimizations, energy usage for retrieval tasks was reduced without sacrificing performance.
3. Sustainable computing practices, including the use of renewable energy sources and energy-efficient algorithms, are critical for minimizing environmental impact.

---

# Tools Used

### **Natural Language Processing (NLP) Tools**

- **NLTK**: Employed for stemming and stopword removal to clean and prepare text data.
- **Hugging Face Transformers**: Utilized for implementing pretrained models (e.g., BERT, RoBERTa) to compute embeddings and perform semantic similarity analysis.
- **CodeCarbon**: Tracks energy consumption (kWh) and calculates the corresponding carbon emissions (kg CO₂) for different computational tasks.
- **gpustat**: Monitors GPU utilization and power consumption in real-time during model training and inference.
- **Carbon Tracker**: Measures energy usage and carbon emissions of machine learning models, helping identify energy-intensive stages.
- **lxml**: Efficient XML parsing library used to extract and clean legal document data.
- **PyTorch**: An alternative deep learning framework used for custom model implementations and optimization.
- **Energy-Efficient Algorithms**: Implements optimized algorithms for retrieval tasks to reduce computation without sacrificing accuracy.

By leveraging these tools, the system maintains a balance between high performance and sustainability, ensuring accurate results while minimizing environmental impact.

---

## Conclusion

The Legal Information Retrieval System not only enhances legal research but also serves as a model for sustainable AI development. By integrating energy monitoring and optimization tools, the system addresses the dual goals of accuracy and environmental responsibility. Future advancements can focus on further reducing energy consumption through innovative architectures and real-time carbon tracking mechanisms.

<!-- ## Technologies Used

- **Frontend**: React.js, HTML5, CSS3
- **Backend**: Node.js, Express.js
- **Database**: MongoDB
- **NLP Tools**: spaCy, NLTK
- **Search Engine**: Elasticsearch

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/legal-info-retrieval.git
   cd legal-info-retrieval

2. Install dependencies:

   ```bash
   npm install

Set up the database and environment variables as per the config.example.js file.

3. Start the application:

   ```bash
   npm start -->
