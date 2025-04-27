from openai import OpenAI
import json
import os

# Initialize the OpenAI client with NVIDIA API
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "USE YOUR API"
)

# Path to the conversation memory file
MEMORY_FILE = "amigo_memory.json"

def sanitize_text(text):
    """Sanitize text by handling special characters"""
    # Replace special characters with safe alternatives
    text = text.replace('\\', '\\\\')  # Escape backslashes
    text = text.replace('*', '×')      # Replace asterisk with multiplication sign
    text = text.replace('/', '∕')      # Replace forward slash with division sign
    return text

def load_memory():
    """Load conversation memory from file"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"conversations": []}
    else:
        return {"conversations": []}

def save_memory(memory):
    """Save conversation memory to file"""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def get_ai_response(query, use_memory=True):
    """
    Get a response from the AI model with optional memory integration
    
    Args:
        query (str): The user's query
        use_memory (bool): Whether to use conversation memory
        
    Returns:
        str: The AI's response
    """
    # Sanitize the input query
    sanitized_query = sanitize_text(query)
    
    # Initialize messages with system prompt
    messages = [
        {"role": "system", "content": "You are Amigo, a helpful voice assistant. Keep your responses clear and concise."}
    ]
    
    # Add conversation memory if enabled
    if use_memory:
        memory = load_memory()
        # Add up to the last 10 conversation exchanges to provide context
        for conv in memory["conversations"][-10:]:
            messages.append({"role": "user", "content": sanitize_text(conv["user"])})
            messages.append({"role": "assistant", "content": sanitize_text(conv["assistant"])})
    
    # Add the current query
    messages.append({"role": "user", "content": sanitized_query})
    
    # Get response from the model
    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=messages,
            temperature=0.7,
            top_p=1,
            max_tokens=512,
            stream=False
        )
        
        response = completion.choices[0].message.content
        
        # Save to memory if enabled
        if use_memory:
            memory = load_memory()
            memory["conversations"].append({
                "user": query,  # Store original query without sanitization
                "assistant": response
            })
            # Keep only the last 50 conversations
            if len(memory["conversations"]) > 50:
                memory["conversations"] = memory["conversations"][-50:]
            save_memory(memory)
        
        return response
    
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return "I'm having trouble connecting to my AI services right now. Can I help you with something else?"
