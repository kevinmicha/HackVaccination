import pandas as pd
from transformers import pipeline

# Load the CSV file
file_path = 'bluesky_posts_20241130_162013.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Initialize a quick lightweight model pipeline
model_name = "google/flan-t5-large"  # Lightweight and fast model
task_pipeline = pipeline("text2text-generation", model=model_name)

def process_with_llm(text, task):
    """
    Use a lightweight LLM to perform specific tasks: sentiment analysis, keyword extraction, or age estimation.
    """
    if task == "sentiment":
        prompt = f"Determine if the following text is POSITIVE, NEUTRAL or NEGATIVE towards vaccination. Respond with POSITIVE, NEUTRAL, or NEGATIVE.\n\nText: {text}"
    elif task == "keywords":
        prompt = f"Extract three distinct keywords from the following text. Respond with three words separated by commas.\n\nText: {text}"
    elif task == "age":
        prompt = f"Estimate the specific group age of the person who wrote the following text. Respond with a word between CHILD, YOUNG, MIDDLE-AGED, OLD or UNDEFINED.\n\nText: {text}"
    else:
        raise ValueError("Invalid task specified.")
    
    # Generate a response using the lightweight LLM
    result = task_pipeline(prompt, max_length=50, num_return_sequences=1)
    return result[0]['generated_text'].strip()

# Process the CSV
sentiments = []
keywords = []
ages = []

for _, row in data.iterrows():
    post_text = row['Post Text']
    print(post_text)
    # Sentiment analysis
    sentiment = process_with_llm(post_text, "sentiment")
    sentiments.append(sentiment)
    print(sentiment)
    
    # Keyword extraction
    extracted_keywords = process_with_llm(post_text, "keywords")
    keywords.append(extracted_keywords)
    print(extracted_keywords)
    
    # Age estimation
    estimated_age = process_with_llm(post_text, "age")
    ages.append(estimated_age)
    print(estimated_age)

# Add results to the DataFrame
data['Sentiment'] = sentiments
data['Keywords'] = keywords
data['Estimated Age'] = ages

# Save the updated CSV
output_file_path = 'updated_llm_tasks.csv'
data.to_csv(output_file_path, index=False)

print(f"Updated CSV saved to {output_file_path}")
