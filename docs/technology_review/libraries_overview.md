# Technology Review

## Background

This project aims to create a tool to generate (i) a summary of the most popular reviews of a movie on Letterboxd to encapsulate not just the plot and themes but also the emotions elicited in viewers and (ii) a visualization demonstrating the top aspects mentioned in the reviews and their sentiment analysis.

To achieve this, we had to explore different generative AI and NLP technologies available.

## (i) Summarization:



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
