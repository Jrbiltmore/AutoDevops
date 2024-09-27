import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChatModelError(Exception):
    """Custom exception for chat model errors."""
    pass

class ChatModel:
    """
    A Chatbot model based on GPT-2 for generating conversational responses.
    
    This model can handle multi-turn conversations by maintaining context 
    and dynamically generating responses based on input queries.
    """

    def __init__(self, model_name='gpt2', max_length=512, device=None):
        """
        Initialize the chat model.
        
        Args:
            model_name (str): Pre-trained model name or path.
            max_length (int): Maximum length of responses.
            device (str): Device to run the model on ('cpu' or 'cuda').
        """
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_name = model_name
        self.max_length = max_length

        # Load pre-trained model and tokenizer
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
            self.model = GPT2LMHeadModel.from_pretrained(self.model_name).to(self.device)
            logging.info(f"Model '{self.model_name}' loaded successfully on {self.device}.")
        except Exception as e:
            raise ChatModelError(f"Failed to load model: {e}")

    def generate_response(self, conversation_history, user_input, max_length=None):
        """
        Generate a response based on the conversation history and user input.
        
        Args:
            conversation_history (str): The conversation context as a string.
            user_input (str): The new user input.
            max_length (int): Maximum length for the generated response.
        
        Returns:
            str: The generated response.
        
        Raises:
            ChatModelError: If the response generation fails.
        """
        try:
            # Prepare input for the model by appending user input to conversation history
            input_text = f"{conversation_history} {self.tokenizer.eos_token} {user_input} {self.tokenizer.eos_token}"
            input_ids = self.tokenizer.encode(input_text, return_tensors='pt').to(self.device)

            # Generate response
            response_ids = self.model.generate(
                input_ids,
                max_length=max_length or self.max_length,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7
            )

            # Decode the response and return it
            response_text = self.tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
            return response_text.strip()

        except Exception as e:
            raise ChatModelError(f"Response generation failed: {e}")

    def clear_conversation(self):
        """
        Clear the conversation history.
        """
        return self.tokenizer.eos_token

    def adjust_parameters(self, max_length=None, temperature=None, top_k=None, top_p=None):
        """
        Adjust parameters for response generation.
        
        Args:
            max_length (int): Maximum length of responses.
            temperature (float): Sampling temperature.
            top_k (int): Top-K sampling.
            top_p (float): Top-p (nucleus) sampling.
        
        Returns:
            dict: Updated parameters.
        """
        if max_length:
            self.max_length = max_length
        parameters = {
            'max_length': self.max_length,
            'temperature': temperature or 0.7,
            'top_k': top_k or 50,
            'top_p': top_p or 0.95
        }
        logging.info(f"Parameters adjusted: {parameters}")
        return parameters

    def save_model(self, path):
        """
        Save the model weights and tokenizer to a given path.
        
        Args:
            path (str): The directory path where the model will be saved.
        
        Raises:
            ChatModelError: If the model save operation fails.
        """
        try:
            self.model.save_pretrained(path)
            self.tokenizer.save_pretrained(path)
            logging.info(f"Model saved successfully to {path}.")
        except Exception as e:
            raise ChatModelError(f"Failed to save model: {e}")

    def load_model(self, path):
        """
        Load a model from a given path.
        
        Args:
            path (str): The directory path from where the model will be loaded.
        
        Raises:
            ChatModelError: If the model load operation fails.
        """
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(path)
            self.model = GPT2LMHeadModel.from_pretrained(path).to(self.device)
            logging.info(f"Model loaded successfully from {path}.")
        except Exception as e:
            raise ChatModelError(f"Failed to load model: {e}")

if __name__ == "__main__":
    # Example usage
    conversation_history = "User: Hello, how are you?"
    user_input = "What's the weather like today?"
    
    try:
        chat_model = ChatModel()
        response = chat_model.generate_response(conversation_history, user_input)
        print(f"Chatbot: {response}")
    except ChatModelError as e:
        logging.error(f"ChatModel error: {e}")
