from openai import OpenAI
import os
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Initialize OpenAI client pointing to local Ollama instance
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama's OpenAI-compatible API endpoint
    api_key="ollama",  # Ollama doesn't require a real API key, but the client expects one
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
        # Create a chat completion request
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        # Extract and return the response
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error calling Ollama model: {e}")
        return None


# def stream_ollama_model(model_name: str = "gemma2:2b", prompt: str = "Hello, how are you?"):
#     """
#     Stream responses from a local Ollama model using OpenAI client.
    
#     Args:
#         model_name: Name of the Ollama model to use
#         prompt: The prompt to send to the model
    
#     Yields:
#         Chunks of the model's response as they are generated
#     """
#     try:
#         # Create a streaming chat completion request
#         stream = client.chat.completions.create(
#             model=model_name,
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7,
#             stream=True,
#         )
        
#         # Yield each chunk as it arrives
#         for chunk in stream:
#             if chunk.choices[0].delta.content is not None:
#                 yield chunk.choices[0].delta.content
    
#     except Exception as e:
#         print(f"Error streaming from Ollama model: {e}")
#         return None


if __name__ == "__main__":
    # Example usage
    print("Calling Ollama model (non-streaming)...")
    response = call_ollama_model(
        model_name="gemma2:2b",  # Using gemma:2b model
        prompt="Explain quantum computing in simple terms."
    )
    print(f"Response: {response}\n")
    
    # # Example usage with streaming
    # print("Calling Ollama model (streaming)...")
    # print("Response: ", end="", flush=True)
    # for chunk in stream_ollama_model(
    #     model_name="gemma2:2b",  # Using gemma:2b model
    #     prompt="Write a short poem about AI."
    # ):
    #     print(chunk, end="", flush=True)
    # print("\n")

