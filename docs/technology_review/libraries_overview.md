# **Technology Review**

## **Background**  

This project aims to develop a tool that:  
1. **Generates meaningful summaries** of the most popular Letterboxd movie reviews, capturing key themes, audience reactions, and emotions.  
2. **Creates a visualization** highlighting the most frequently mentioned aspects (e.g., cinematography, acting, direction) and their sentiment analysis.  
3. **Produces personalized roasts** of a Letterboxd user’s viewing habits based on their **ratings, most-watched genres, actors, and reviewing patterns**.  

To achieve these goals, different **Generative AI, NLP, and Web Scraping** techniques were explored, evaluating their **speed, accuracy, scalability, and integration feasibility**.

---

## **(i) Web Scraping for Data Extraction**  

Since **Letterboxd does not provide an official API**, web scraping is used to extract movie reviews and user profile data for analysis.  

### **1. BeautifulSoup for Movie Reviews (Summarization Feature)**  
To generate meaningful **summaries** of a movie’s **top reviews**, 300 of the most popular Letterboxd reviews are scraped from the movie's page.  

- **Technology Used:** `BeautifulSoup` (Python library for HTML parsing).  
- **Scraped Data:**  
  - **Movie title, director, year, genres, and synopsis**  
  - **Top 100 user reviews** (review text, user rating)  

- **How the Data is Used:**  
  - The **scraped reviews** are passed to **Gemini 1.5 Pro** for **summarization** and **aspect-based sentiment analysis**.  
  - The extracted **sentiment data** is then used to generate **visual insights** about audience reactions.  

---

### **2. BeautifulSoup for User Profiles (Roasting Feature)**  
For **personalized roasting**, multiple data sources from a user's **Letterboxd profile** are scraped and combined into a unified dataset.

- **Technology Used:** `BeautifulSoup` for scraping and `pandas` for data processing.  
- **Scraped Data Sources:**  
  - **User Reviews** (`letterboxd.com/{username}/films/reviews/`)  
    - Movies reviewed, ratings given, review text.  
  - **User Stats** (`letterboxd.com/{username}/stats/`)  
    - Most-watched genres, actors, directors, total watch hours, longest watch streaks.  
  - **Profile Activity Logs**  
    - Identifies trends in **rating behaviors**, **rewatch frequency**, and **genre obsession**.  

- **How the Data is Used:**  
  - **Data is merged** to **detect user patterns**, such as:  
    - **Genre fixation** ("You’ve watched 95 percent horror movies this year. Everything okay?").  
    - **Overrated favorites** ("Five rewatches of ‘Morbius’? That’s a commitment.").  
    - **Pretentious or extreme ratings** ("A 1-star for ‘The Godfather’? Let’s talk.").  
  - The **combined dataset** is passed to **Gemini 1.5 Pro**, which generates a **snarky AI-powered roast**.  

---

## **(ii) Summarization: Evaluating NLP Models for Movie Review Summaries**  

To generate concise and meaningful summaries of **Letterboxd movie reviews**, two different approaches were explored:  

### **1. Mistral 7B (via Hugging Face Transformers)**  
Mistral 7B is an **open-weight transformer model** optimized for efficiency and performance. It was implemented using the **Hugging Face `transformers` library** to generate summaries. However, it presented several drawbacks:  

- **Slow inference time**: Processing each review took **several seconds**, making it impractical for real-time summarization.  
- **Fine-tuning complexity**: Achieving **high-quality summaries** required **significant fine-tuning**, increasing development time and complexity.  
- **Infrastructure overhead**: Running Mistral **locally or on cloud infrastructure** required dedicated GPU resources.  

### **2. Google Gemini Pro (via Generative AI Python SDK)**  
Gemini Pro, a **cloud-based AI model by Google**, offered an alternative approach:  

- **Fast inference time**: **Near-instant response**, allowing real-time summary generation.  
- **High-quality output**: Fluent and coherent summaries with **minimal post-processing**.  
- **No fine-tuning required**: Well-optimized for **natural language generation** without requiring additional training.  
- **Scalability**: API-based access enabled effortless **scaling without infrastructure overhead**.  

| Feature               | Mistral 7B | Google Gemini Pro |
|-----------------------|-----------|------------------|
| **Author**           | Mistral AI | Google |
| **Summary**         | Open-source LLM | API-based generative AI for text processing |
| **Fine-tuning**     | Required for optimal results | Not required |
| **Inference Time**  | Too slow for real-time use | Nearly instant |
| **Output Quality**  | Required additional optimization | Fluent and coherent with minimal processing |
| **Error Handling**  | Predictable but required tuning | Required handling due to response variability |
| **Control**        | Full control over model and infrastructure | Dependent on Google's API policies |
| **Scalability**    | Infrastructure-dependent, complex to scale | Easy to scale with API-based access |

---

## **(iii) Aspect-Based Sentiment Analysis: Extracting Top Aspects from Reviews**  

To extract **key aspects** (e.g., cinematography, acting, music) and their **sentiment polarity**, three options were explored:  

| Feature                 | Hugging Face SetFit ABSA | Gemini 1.5 Pro |
|-------------------------|-------------------------|---------------|
| **Author**             | Hugging Face             | Google |
| **Summary**            | Few-shot learning ABSA model | API-based generative AI for text processing |
| **Fine-tuning**        | Required (small dataset) | Not required |
| **Inference Time**     | Too slow (~1 second per line) | Immediate |
| **Output Format**      | Dictionary               | String |
| **Error Handling**     | Predictable, fixed       | Requires structured prompt engineering |

- **Decision:** Selected **Gemini 1.5 Pro** for its **speed and accuracy**.  

---

## **(iv) Roasting Feature: Generating Personalized, AI-Powered Roasts**  

To generate **funny, engaging roasts** for Letterboxd users, two approaches were explored:  

| Feature                | Rule-Based Templates | Gemini 1.5 Pro |
|------------------------|---------------------|---------------|
| **Approach**          | Heuristic-based text | AI-generated freeform roast |
| **Creativity**        | Limited, predictable | High, dynamic |
| **Scalability**       | Manual expansion required | Easily scales with more inputs |
| **Personalization**   | Generic templates | User-specific, personalized roasts |
| **Error Handling**    | Minimal required | Requires structured prompt engineering |

- **Decision:** Selected **Gemini 1.5 Pro**, ensuring structured outputs through **prompt tuning and API constraints**.  

---

## **Conclusion: Selected Technologies**  

| Feature                 | Selected Technology |
|-------------------------|--------------------|
| **Web Scraping**        | BeautifulSoup |
| **Summarization**        | Google Gemini Pro |
| **Aspect-Based Sentiment** | Google Gemini 1.5 Pro |
| **Roasting Feature**     | Google Gemini 1.5 Pro |

These choices ensure:  
- **High-speed inference** for real-time processing.  
- **Minimal infrastructure requirements** (API-based).  
- **Scalability** without requiring fine-tuning.  
