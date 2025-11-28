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
                raw_data = json.load(f)

            # Detect format and normalize to internal structure
            self.data = self._normalize_format(raw_data)

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

    def _normalize_format(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize different JSON formats to internal structure

        Supports:
        1. Old format with 'configurations' key
        2. COLLECT export format (apply_export.json)
        3. Direct migration format (migration.json)

        Args:
            raw_data: Raw JSON data

        Returns:
            Normalized data with 'configurations' structure
        """
        # Format 1: Already has 'configurations' key (old format)
        if 'configurations' in raw_data:
            return raw_data

        # Format 2: COLLECT export format (has 'version', 'system', 'network', etc.)
        if 'version' in raw_data and 'system' in raw_data:
            return self._convert_collect_export(raw_data)

        # Format 3: Direct migration format (has direct keys like 'hostname', 'ipv4', etc.)
        if 'hostname' in raw_data or 'ipv4' in raw_data or 'netzlaufwerke' in raw_data:
            return self._convert_migration_format(raw_data)

        # Unknown format - return as is
        return raw_data

    def _convert_collect_export(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert COLLECT export format to internal format

        Args:
            data: COLLECT export data

        Returns:
            Normalized data structure
        """
        configurations = {}

        # System/Hostname
        if 'system' in data:
            system = data['system']
            if 'computername' in system:
                configurations['hostname'] = {
                    'value': system['computername'],
                    'description': 'Computername'
                }

            if 'benutzername' in system:
                configurations['username'] = {
                    'value': system['benutzername'],
                    'description': 'Benutzername'
                }

            if 'computer_domaene' in system or 'arbeitsgruppe' in system:
                configurations['domain'] = {
                    'value': system.get('computer_domaene', system.get('arbeitsgruppe', '')),
                    'description': 'Domäne/Arbeitsgruppe'
                }

            # Default applications
            if any(k in system for k in ['standard_browser', 'standard_pdf', 'standard_mail', 'standard_word']):
                configurations['default_apps'] = {
                    'browser': system.get('standard_browser', ''),
                    'pdf': system.get('standard_pdf', ''),
                    'mail': system.get('standard_mail', ''),
                    'word': system.get('standard_word', ''),
                    'description': 'Standard-Anwendungen'
                }

        # Network
        if 'network' in data and isinstance(data['network'], list) and len(data['network']) > 0:
            network_configs = {}
            for idx, iface in enumerate(data['network']):
                key = iface.get('name', f'Interface_{idx}')
                network_configs[key] = {
                    'interface': iface.get('name', ''),
                    'status': iface.get('status', ''),
                    'mac': iface.get('mac', ''),
                    'ip_address': iface.get('ipv4', ''),
                    'gateway': iface.get('gateway', ''),
                    'dns': iface.get('dns', ''),
                    'description': f"Netzwerkschnittstelle {iface.get('name', key)}"
                }
            configurations['network'] = network_configs

        # Browser bookmarks
        if 'browser' in data:
            browser = data['browser']
            if any(browser.get(k, False) for k in ['edge', 'chrome', 'firefox']):
                configurations['browser_favoriten'] = {
                    'edge': browser.get('edge', False),
                    'chrome': browser.get('chrome', False),
                    'firefox': browser.get('firefox', False),
                    'description': 'Browser-Favoriten'
                }

        # Email/MoBackup
        if 'email' in data:
            email = data['email']
            if email.get('outlook_installed', False):
                configurations['mobackup'] = {
                    'enabled': True,
                    'outlook_installed': True,
                    'description': 'MoBackup für Outlook'
                }

        return {
            'system_info': data.get('source', {}),
            'configurations': configurations
        }

    def _convert_migration_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert direct migration format to internal format

        Args:
            data: Migration format data

        Returns:
            Normalized data structure
        """
        configurations = {}

        # Hostname
        if 'hostname' in data:
            configurations['hostname'] = {
                'value': data['hostname'],
                'description': 'Hostname'
            }

        # Username
        if 'benutzername' in data:
            configurations['username'] = {
                'value': data['benutzername'],
                'description': 'Benutzername'
            }

        # Domain/Workgroup
        if 'domaene' in data or 'arbeitsgruppe' in data:
            configurations['domain'] = {
                'value': data.get('domaene', data.get('arbeitsgruppe', '')),
                'description': 'Domäne/Arbeitsgruppe'
            }

        # IPv4 Network
        if 'ipv4' in data:
            ipv4 = data['ipv4']
            configurations['ipv4_network'] = {
                'ip_address': ipv4.get('adresse', ''),
                'gateway': ipv4.get('gateway', ''),
                'dns': ipv4.get('dns', []),
                'description': 'IPv4-Netzwerkkonfiguration'
            }

        # Routes
        if 'routen_ipv4' in data and data['routen_ipv4']:
            configurations['ipv4_routes'] = {
                'routes': data['routen_ipv4'],
                'description': 'Ständige Routen IPv4'
            }

        # Network drives
        if 'netzlaufwerke' in data and data['netzlaufwerke']:
            drives = {}
            for idx, drive in enumerate(data['netzlaufwerke']):
                key = drive.get('laufwerk', f'Drive_{idx}')
                drives[key] = {
                    'letter': drive.get('laufwerk', ''),
                    'path': drive.get('pfad', ''),
                    'description': f"Netzlaufwerk {drive.get('laufwerk', key)}"
                }
            configurations['netzlaufwerke'] = drives

        # Default applications
        if any(k in data for k in ['standard_browser', 'standard_pdf', 'standard_mail', 'standard_word']):
            configurations['default_apps'] = {
                'browser': data.get('standard_browser', ''),
                'pdf': data.get('standard_pdf', ''),
                'mail': data.get('standard_mail', ''),
                'word': data.get('standard_word', ''),
                'description': 'Standard-Anwendungen'
            }

        # Browser bookmarks
        if 'browser_favoriten' in data:
            fav = data['browser_favoriten']
            configurations['browser_favoriten'] = {
                'edge_base64': fav.get('edge_bookmarks_base64', ''),
                'chrome_base64': fav.get('chrome_bookmarks_base64', ''),
                'firefox_base64': fav.get('firefox_places_base64', ''),
                'description': 'Browser-Favoriten'
            }

        return {
            'system_info': {
                'hostname': data.get('hostname', ''),
                'timestamp': data.get('timestamp', '')
            },
            'configurations': configurations
        }
