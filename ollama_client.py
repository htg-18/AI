from openai import OpenAI
import os

client = OpenAI(
    base_url="http://localhost:11434/v1",  
    api_key="ollama", 
)

def call_ollama_model(model_name: str = "gemma2:2b", prompt: str = "Hello, how are you?"):
    """
    Call a local Ollama model using OpenAI client.
    
    Args:
        model_name: Name of the Ollama model to use (e.g., "llama2", "mistral", "codellama")
        prompt: The prompt to send to the model
    
    Returns:
        The model's response text
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error calling Ollama model: {e}")
        return None

if __name__ == "__main__":
    print("Calling Ollama model (non-streaming)...")
    response = call_ollama_model(
        model_name="gemma2:2b",  
        prompt="Explain quantum computing in simple terms."
    )
    print(f"Response: {response}\n")
    
