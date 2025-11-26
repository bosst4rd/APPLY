"""
COLLECT Data Parser
Parses configuration data collected by the COLLECT tool
"""
import json
import os
from typing import Dict, List, Any


class CollectParser:
    """Parser for COLLECT tool output files"""

    def __init__(self, collect_file_path: str):
        """
        Initialize parser with path to COLLECT output file

        Args:
            collect_file_path: Path to the JSON file containing collected configurations
        """
        self.collect_file_path = collect_file_path
        self.data = None

    def load(self) -> bool:
        """
        Load and parse the COLLECT data file

        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.collect_file_path):
                raise FileNotFoundError(f"File not found: {self.collect_file_path}")

            with open(self.collect_file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

            return True
        except Exception as e:
            print(f"Error loading COLLECT file: {e}")
            return False

    def get_categories(self) -> List[str]:
        """
        Get all configuration categories

        Returns:
            List of category names
        """
        if not self.data:
            return []
        return list(self.data.get('configurations', {}).keys())

    def get_category_items(self, category: str) -> Dict[str, Any]:
        """
        Get all items in a specific category

        Args:
            category: Category name

        Returns:
            Dictionary of items in the category
        """
        if not self.data:
            return {}
        return self.data.get('configurations', {}).get(category, {})

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information from the COLLECT data

        Returns:
            Dictionary containing system information
        """
        if not self.data:
            return {}
        return self.data.get('system_info', {})

    def get_all_data(self) -> Dict[str, Any]:
        """
        Get all parsed data

        Returns:
            Complete data dictionary
        """
        return self.data or {}
