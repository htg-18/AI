import json
from webpage_links import extract_links, get_links_only
from ollama_client import call_ollama_model


def display_links(links):
    if not links:
        print("No links found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(links)} link(s) on the webpage:")
    print(f"{'='*80}\n")
    
    for i, link in enumerate(links, 1):
        print(f"{i}. Link Text: {link['text']}")
        print(f"   URL: {link['absolute_url']}")
        print()


def get_ollama_descriptions(links, model_name="gemma2:2b"):
    if not links:
        return None
    
    links_info = []
    for i, link in enumerate(links, 1):
        links_info.append({
            "index": i,
            "text": link['text'],
            "url": link['absolute_url']
        })
    
    prompt = f"""Please analyze the following links from a portfolio website and provide a description of what each link is and what it likely leads to. 

Return your response in JSON format with the following structure:
{{
    "links": [
        {{
            "index": 1,
            "url": "url_here",
            "link_text": "text_here",
            "description": "description of what this link is and where it leads",
            "category": "category like 'social_media', 'project', 'contact', 'navigation', etc."
        }}
    ]
}}

Here are the links to analyze:
{json.dumps(links_info, indent=2)}

Please provide your analysis in valid JSON format only."""
    
    print("\n" + "="*80)
    print("Calling Ollama to analyze links...")
    print("="*80 + "\n")
    
    response = call_ollama_model(model_name=model_name, prompt=prompt)
    
    return response


def extract_json_from_response(response):
    if not response:
        return None
    
    response = response.strip()
    
    if response.startswith("```json"):
        response = response[7:]
    elif response.startswith("```"):
        response = response[3:]
    
    if response.endswith("```"):
        response = response[:-3]
    
    response = response.strip()
    
    try:
        json_data = json.loads(response)
        return json_data
    except json.JSONDecodeError:
        print("Warning: Could not parse response as JSON. Returning raw response.")
        return {"raw_response": response}


def main():
    portfolio_url = "https://portfolio2-lac-psi.vercel.app/"
    
    print(f"Extracting links from: {portfolio_url}")
    print("="*80)
    
    links = extract_links(portfolio_url)
    
    if links is None:
        print("Failed to extract links from the webpage.")
        return
    
    display_links(links)
    
    ollama_response = get_ollama_descriptions(links)
    
    if ollama_response:
        print("\n" + "="*80)
        print("Ollama Response:")
        print("="*80 + "\n")
        
        # Try to parse and format JSON
        json_data = extract_json_from_response(ollama_response)
        
        if isinstance(json_data, dict) and "raw_response" not in json_data:
            # Pretty print the JSON
            print(json.dumps(json_data, indent=2))
        else:
            # Print raw response if JSON parsing failed
            print(ollama_response)
        
        # Optionally save to file
        try:
            with open("link_descriptions.json", "w", encoding="utf-8") as f:
                if isinstance(json_data, dict):
                    json.dump(json_data, f, indent=2)
                else:
                    json.dump({"response": ollama_response}, f, indent=2)
            print("\n✓ Saved descriptions to 'link_descriptions.json'")
        except Exception as e:
            print(f"\nWarning: Could not save to file: {e}")


if __name__ == "__main__":
    main()

