import re
import json
import xmlschema
from datetime import datetime
import logging
from jsonschema import validate, ValidationError as JSONValidationError

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ValidatorError(Exception):
    """Custom exception for validation errors."""
    pass

class Validator:
    """
    A comprehensive validator class to handle multiple types of data validation,
    including strings, JSON, XML, and date/time formats.
    """

    @staticmethod
    def validate_string(value, pattern=None, min_length=None, max_length=None):
        """
        Validate string length and pattern.
        
        Args:
            value (str): The string to validate.
            pattern (str): Optional regex pattern to match.
            min_length (int): Optional minimum length for the string.
            max_length (int): Optional maximum length for the string.
        
        Returns:
            bool: True if valid, otherwise raises ValidatorError.
        
        Raises:
            ValidatorError: If the string is not valid.
        """
        if not isinstance(value, str):
            raise ValidatorError("Input value must be a string.")
        
        if min_length is not None and len(value) < min_length:
            raise ValidatorError(f"String is shorter than minimum length {min_length}.")
        
        if max_length is not None and len(value) > max_length:
            raise ValidatorError(f"String is longer than maximum length {max_length}.")
        
        if pattern and not re.match(pattern, value):
            raise ValidatorError(f"String does not match the required pattern: {pattern}")
        
        return True

    @staticmethod
    def validate_json(data, schema=None):
        """
        Validate JSON data. Optionally validate against a schema.
        
        Args:
            data (dict or str): JSON data to validate.
            schema (dict, optional): JSON schema to validate against.
        
        Returns:
            bool: True if valid, otherwise raises ValidatorError.
        
        Raises:
            ValidatorError: If the JSON data is not valid.
        """
        try:
            if isinstance(data, str):
                data = json.loads(data)
            
            if schema:
                validate(instance=data, schema=schema)
            
            return True
        except json.JSONDecodeError as e:
            raise ValidatorError(f"Invalid JSON format: {e}")
        except JSONValidationError as e:
            raise ValidatorError(f"JSON schema validation failed: {e}")

    @staticmethod
    def validate_xml(xml_data, schema=None):
        """
        Validate XML data. Optionally validate against an XML schema.
        
        Args:
            xml_data (str): XML data to validate.
            schema (str, optional): Path to the XML schema (XSD file).
        
        Returns:
            bool: True if valid, otherwise raises ValidatorError.
        
        Raises:
            ValidatorError: If the XML data is not valid.
        """
        try:
            xmlschema_doc = None
            if schema:
                xmlschema_doc = xmlschema.XMLSchema(schema)
                xmlschema_doc.validate(xml_data)
            else:
                ET.fromstring(xml_data)  # Simple well-formed check
            
            return True
        except ET.ParseError as e:
            raise ValidatorError(f"Invalid XML format: {e}")
        except xmlschema.XMLSchemaValidationError as e:
            raise ValidatorError(f"XML schema validation failed: {e}")

    @staticmethod
    def validate_datetime(date_str, date_format="%Y-%m-%d %H:%M:%S"):
        """
        Validate a date string against a specific format.
        
        Args:
            date_str (str): Date string to validate.
            date_format (str): The expected date format (default is '%Y-%m-%d %H:%M:%S').
        
        Returns:
            bool: True if valid, otherwise raises ValidatorError.
        
        Raises:
            ValidatorError: If the date string is not valid.
        """
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError as e:
            raise ValidatorError(f"Date format validation failed: {e}")

    @staticmethod
    def validate_type(value, expected_type):
        """
        Validate that a value is of the expected type.
        
        Args:
            value: The value to validate.
            expected_type (type): The expected type (e.g., int, str, list).
        
        Returns:
            bool: True if valid, otherwise raises ValidatorError.
        
        Raises:
            ValidatorError: If the type does not match.
        """
        if not isinstance(value, expected_type):
            raise ValidatorError(f"Expected type {expected_type}, but got {type(value)}.")
        
        return True


if __name__ == "__main__":
    # Example usage
    try:
        print(Validator.validate_string("hello@example.com", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"))
        print(Validator.validate_json('{"name": "ChatGPT"}'))
        print(Validator.validate_xml('<root><child name="test"/></root>'))
        print(Validator.validate_datetime("2024-09-27 12:00:00"))
        print(Validator.validate_type(123, int))
    except ValidatorError as e:
        logging.error(f"Validation error: {e}")

