# Technology Review

## Background

This project aims to create a tool to generate (i) a summary of the most popular reviews of a movie on Letterboxd to encapsulate not just the plot and themes but also the emotions elicited in viewers and (ii) a visualization demonstrating the top aspects mentioned in the reviews and their sentiment analysis.

To achieve this, we had to explore different generative AI and NLP technologies available.

## (i) Summarization:

To generate a meaningful summary of the most popular reviews of a movie, we explored two different approaches: Mistral 7B and Google Gemini Pro.

### Mistral 7B (via Hugging Face Transformers)
Mistral 7B is an open-weight transformer model optimized for efficiency and performance. We used the Hugging Face transformers library to generate summaries, but the inference time was too slow, taking several seconds per review, which made it impractical for real-time processing. While the model allowed full control over fine-tuning and customization, achieving high-quality summaries required extensive optimization. Maintaining the necessary infrastructure for efficient inference also increased complexity. These factors made Mistral 7B unsuitable for our needs.

### Google Generative AI Python SDK (for Gemini Pro)
Google Gemini Pro is a generative AI model optimized for natural language processing. We used its Python SDK to generate summaries with a structured prompt that guided the model to focus on key themes, emotions, and audience reactions. This approach produced fluent, coherent summaries with minimal post-processing. The inference time was nearly instant, making it efficient for handling large volumes of reviews. While the response format varied at times, careful prompt engineering and targeted error handling ensured consistent outputs. Given its speed, high-quality summaries, and low infrastructure overhead, Gemini Pro was the best choice for our needs.

| Feature               | Mistral 7B | Google Gemini Pro |
|-----------------------|-----------|------------------|
| **Author**           | Mistral AI | Google          |
| **Summary**         | Open-source LLM | API-based generative AI for text processing |
| **Fine-tuning**     | Required for optimal results | Not required |
| **Inference Time**  | Too slow for real-time use | Nearly instant |
| **Output Quality**  | Required additional optimization | Fluent and coherent with minimal processing |
| **Error Handling**  | Predictable but required tuning | Required handling due to response variability |
| **Control**        | Full control over model and infrastructure | Dependent on Google's API policies |
| **Scalability**    | Infrastructure-dependent, complex to scale | Easy to scale with API-based access |


## (ii) Top Aspects Visualization

To extract the top aspects from a list of reviews, we explored three options:

### Finetuning Hugging Face SetFit ABSA model using few-shot learning
We used Hugging Face’s SetFit library that takes individual sentences as input and outputs extracted aspects along with their predicted sentiment (positive/neutral/negative). This library was suited for few-shot learning, so we created a manually labelled training data set of ~ 50 lines (extracted from actual reviews) with their relevant aspects and sentiments to finetune the model to extract cinematic aspects from movie reviews.

While the prediction accuracy seemed promising on a small manually created testing set, the inference time was too long - ~ 1 second per sentence, which is impractical when processing hundreds of reviews for quick results.

### Google Generative AI Python SDK (for Gemini Pro)
This approach mostly required intensive prompt engineering, followed by some text processing to extract data from the response provided by gemini. This method easily overcame the issue of long inference time, however, it needs much more rigorous error handling due to the unpredictable nature of gemini responses.

### Google Generative AI Python SDK (for Gemini 1.5 Pro)
This approach was the same as the previous one, but this model is specially fine-tuned for text processing compared to multimodal processing, which is why we received much more nuanced and impressive results with this generative AI model. This is the option we finally picked.

|                                | Hugging Face SetFit ABSA model | Gemini 1.5 Pro |
|--------------------------------|--------------------------------|---------------|
| **Author**                     | Hugging Face                   | Google        |
| **Summary**                    | A library for few-shot text classification and aspect-based sentiment analysis. | Python SDK for interacting with Google's Gemini models, enabling text generation and understanding through API calls. |
| **Fine tuning**                 | Few shot learning              | Not required/feasible on a small training set. |
| **Inference time**              | Too long ~ 1 second per line   | Immediate     |
| **Output format**               | Dictionary                     | String       |
| **Error handling**              | Predictable, fixed             | Unpredictable due to variance in gemini responses |

### The main challenges with Gemini 1.5 Pro are:
- No control over the model changes its usage policies.
- Unpredictable response format, which makes error handling more difficult.
