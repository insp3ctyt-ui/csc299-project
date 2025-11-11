import os
from openai import OpenAI

def main():
    """
    Main function to run the OpenAI summarization experiment.
    This function is called when you run `uv run tasks4`.
    """
    
    # 1. Initialize the OpenAI client.
    # It automatically looks for the OPENAI_API_KEY environment variable.
    try:
        client = OpenAI()
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        print("Please make sure the 'openai' package is installed (`uv add openai`)")
        return

    # 2. Check if the API key is set
    if not client.api_key:
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        print("Please set it in your terminal before running:")
        print("  (macOS/Linux): export OPENAI_API_KEY='your_key_here'")
        print("  (Windows CMD): set OPENAI_API_KEY=your_key_here")
        return

    # 3. Define the sample paragraph-length descriptions
    task_descriptions = [
        "Create a new feature for the user dashboard that allows them to "
        "upload a CSV file of their monthly sales data. The system must "
        "parse this file, validate all columns (Date, Amount, ProductID), "
        "and then update the central sales database, flagging any rows "
        "that had errors during import.",
        
        "Refactor the existing authentication module to support "
        "third-party OAuth 2.0 providers, starting with Google and GitHub. "
        "This involves updating the user model to store provider tokens, "
        "creating new API endpoints for the OAuth callback, and ensuring "
        "the frontend can handle the new login flow seamlessly."
    ]
    
    # 4. Define the system prompt (the instructions for the AI)
    system_prompt = (
        "You are an expert summarizer. Summarize the following task "
        "description into a short, concise phrase of 5-10 words."
    )

    print("--- Starting Task Summarization Experiment ---")

    # 5. Loop through each description and get a summary
    for i, description in enumerate(task_descriptions):
        print(f"\n[Task {i+1}]")
        print(f"Original: {description}")
        
        try:
            # 6. Send the request to the OpenAI API
            completion = client.chat.completions.create(
                # Use the cheapest, fastest model suitable for this
                model="gpt-5-nano", 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": description}
                ],
                temperature=0.5, # Lower temp for more focused summaries
            )
            
            # 7. Extract and print the summary
            summary = completion.choices[0].message.content
            print(f"Summary: {summary}")

        except Exception as e:
            print(f"An error occurred while contacting the OpenAI API: {e}")
    
    print("\n--- Experiment Complete ---")

if __name__ == "__main__":
    main()