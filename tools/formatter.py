import json
import xml.etree.ElementTree as ET
from datetime import datetime
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FormatterError(Exception):
    """Custom exception for formatter errors."""
    pass

class Formatter:
    """
    A comprehensive formatter class to handle multiple data formats,
    including string formatting, JSON, XML, and date/time formatting.
    """

    @staticmethod
    def format_string(value, case="capitalize"):
        """
        Format strings to various cases.
        
        Args:
            value (str): The string to format.
            case (str): The case to apply. Options: 'upper', 'lower', 'capitalize', 'title'.
        
        Returns:
            str: The formatted string.
        
        Raises:
            FormatterError: If the case is not recognized.
        """
        if not isinstance(value, str):
            raise FormatterError("Input value must be a string.")

        if case == "upper":
            return value.upper()
        elif case == "lower":
            return value.lower()
        elif case == "capitalize":
            return value.capitalize()
        elif case == "title":
            return value.title()
        else:
            raise FormatterError(f"Unsupported case option: {case}")

    @staticmethod
    def format_json(data, indent=4):
        """
        Pretty format a JSON string or object.
        
        Args:
            data (dict or str): JSON data to format.
            indent (int): Indentation level for pretty formatting.
        
        Returns:
            str: The formatted JSON string.
        
        Raises:
            FormatterError: If the input data is not valid JSON.
        """
        try:
            if isinstance(data, str):
                data = json.loads(data)
            return json.dumps(data, indent=indent, ensure_ascii=False)
        except json.JSONDecodeError as e:
            raise FormatterError(f"Invalid JSON data: {e}")

    @staticmethod
    def format_xml(xml_data, indent="  "):
        """
        Pretty format an XML string.
        
        Args:
            xml_data (str): The XML data as a string.
            indent (str): The indentation character(s) to use.
        
        Returns:
            str: The pretty-formatted XML string.
        
        Raises:
            FormatterError: If the input data is not valid XML.
        """
        try:
            root = ET.fromstring(xml_data)
            return Formatter._prettify_xml(root, indent)
        except ET.ParseError as e:
            raise FormatterError(f"Invalid XML data: {e}")

    @staticmethod
    def format_datetime(date_str, current_format, target_format="%Y-%m-%d %H:%M:%S"):
        """
        Convert a date string from one format to another.
        
        Args:
            date_str (str): Date string to format.
            current_format (str): The current format of the date string.
            target_format (str): The target format for the date string.
        
        Returns:
            str: The formatted date string.
        
        Raises:
            FormatterError: If the date conversion fails.
        """
        try:
            date_obj = datetime.strptime(date_str, current_format)
            return date_obj.strftime(target_format)
        except ValueError as e:
            raise FormatterError(f"Date formatting error: {e}")

    @staticmethod
    def _prettify_xml(elem, indent, level=0):
        """
        Private helper function to recursively format XML elements with indentation.
        
        Args:
            elem (ET.Element): The XML element to format.
            indent (str): The indentation string.
            level (int): The current indentation level.
        
        Returns:
            str: The pretty-formatted XML.
        """
        i = "\n" + level * indent
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + indent
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                Formatter._prettify_xml(child, indent, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
        return ET.tostring(elem, encoding='unicode')

    @staticmethod
    def format_code_style(code_str, style="pep8"):
        """
        Format code according to a specified style guide.
        
        Args:
            code_str (str): The code to format.
            style (str): The code style to apply. Currently supports 'pep8' (default).
        
        Returns:
            str: The formatted code.
        
        Raises:
            FormatterError: If the style is not supported.
        """
        if style == "pep8":
            # Importing autopep8 locally to avoid unnecessary overhead if not used
            try:
                import autopep8
                return autopep8.fix_code(code_str)
            except ImportError:
                raise FormatterError("autopep8 is not installed. Install it to use PEP8 formatting.")
        else:
            raise FormatterError(f"Unsupported code style: {style}")


if __name__ == "__main__":
    # Example usage
    try:
        print(Formatter.format_string("hello world", "upper"))
        print(Formatter.format_json('{"name": "ChatGPT", "version": 4}', indent=2))
        print(Formatter.format_xml('<root><child name="test"/></root>', indent="  "))
        print(Formatter.format_datetime("2024-09-27", "%Y-%m-%d", "%d/%m/%Y"))
    except FormatterError as e:
        logging.error(f"Formatting error: {e}")
