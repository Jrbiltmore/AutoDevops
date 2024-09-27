import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReviewModelError(Exception):
    """Custom exception for review model errors."""
    pass

class ReviewModel:
    """
    A model for sentiment analysis on user reviews, based on BERT.
    
    This model can classify reviews into sentiments (positive, negative, neutral) or more 
    complex multi-class categorization, depending on how it is fine-tuned.
    """

    def __init__(self, model_name='bert-base-uncased', num_labels=3, device=None):
        """
        Initialize the review model.
        
        Args:
            model_name (str): Pre-trained BERT model name or path.
            num_labels (int): The number of classification labels (default is 3 for sentiment analysis).
            device (str): Device to run the model on ('cpu' or 'cuda').
        """
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_name = model_name
        self.num_labels = num_labels

        # Load pre-trained model and tokenizer
        try:
            self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
            self.model = BertForSequenceClassification.from_pretrained(self.model_name, num_labels=self.num_labels).to(self.device)
            logging.info(f"Model '{self.model_name}' with {self.num_labels} labels loaded successfully on {self.device}.")
        except Exception as e:
            raise ReviewModelError(f"Failed to load model: {e}")

    def classify_review(self, review_text):
        """
        Classify the sentiment of a user review.
        
        Args:
            review_text (str): The review text to classify.
        
        Returns:
            dict: A dictionary with sentiment label and probability.
        
        Raises:
            ReviewModelError: If the classification fails.
        """
        try:
            # Preprocess the input review
            inputs = self.tokenizer.encode_plus(
                review_text,
                return_tensors="pt",
                max_length=512,
                padding=True,
                truncation=True
            )
            input_ids = inputs['input_ids'].to(self.device)
            attention_mask = inputs['attention_mask'].to(self.device)

            # Run the model
            with torch.no_grad():
                outputs = self.model(input_ids, attention_mask=attention_mask)

            logits = outputs.logits
            probs = F.softmax(logits, dim=1)
            confidence, predicted_label = torch.max(probs, dim=1)

            # Return the result as a dictionary
            label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
            return {
                'label': label_map[predicted_label.item()],
                'confidence': confidence.item()
            }

        except Exception as e:
            raise ReviewModelError(f"Review classification failed: {e}")

    def adjust_model_params(self, num_labels=None):
        """
        Adjust the number of labels for the classification task.
        
        Args:
            num_labels (int): The new number of labels for classification.
        
        Returns:
            None
        
        Raises:
            ReviewModelError: If adjusting the parameters fails.
        """
        if num_labels:
            self.num_labels = num_labels
            try:
                self.model = BertForSequenceClassification.from_pretrained(self.model_name, num_labels=self.num_labels).to(self.device)
                logging.info(f"Model adjusted to {self.num_labels} labels.")
            except Exception as e:
                raise ReviewModelError(f"Failed to adjust model parameters: {e}")

    def save_model(self, path):
        """
        Save the model weights and tokenizer to a given path.
        
        Args:
            path (str): The directory path where the model will be saved.
        
        Raises:
            ReviewModelError: If the model save operation fails.
        """
        try:
            self.model.save_pretrained(path)
            self.tokenizer.save_pretrained(path)
            logging.info(f"Model saved successfully to {path}.")
        except Exception as e:
            raise ReviewModelError(f"Failed to save model: {e}")

    def load_model(self, path):
        """
        Load a model from a given path.
        
        Args:
            path (str): The directory path from where the model will be loaded.
        
        Raises:
            ReviewModelError: If the model load operation fails.
        """
        try:
            self.tokenizer = BertTokenizer.from_pretrained(path)
            self.model = BertForSequenceClassification.from_pretrained(path, num_labels=self.num_labels).to(self.device)
            logging.info(f"Model loaded successfully from {path}.")
        except Exception as e:
            raise ReviewModelError(f"Failed to load model: {e}")


if __name__ == "__main__":
    # Example usage
    try:
        review_text = "This product was excellent! I had a great experience."
        review_model = ReviewModel()
        result = review_model.classify_review(review_text)
        print(f"Sentiment: {result['label']}, Confidence: {result['confidence']:.2f}")
    except ReviewModelError as e:
        logging.error(f"ReviewModel error: {e}")
