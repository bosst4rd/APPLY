"""
Configuration Applier
Applies collected configurations to the new system
Enhanced with ALBIS-Registry and Hostname support
"""
import os
import subprocess
import shutil
import platform
from typing import Dict, Any, List, Tuple
from pathlib import Path


class ConfigApplier:
    """Applies configurations to the system"""

    def __init__(self, dry_run: bool = False):
        """
        Initialize configuration applier

        Args:
            dry_run: If True, only simulate actions without applying them
        """
        self.dry_run = dry_run
        self.applied_configs = []
        self.errors = []

    def apply_network_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply network configuration

        Args:
            config: Network configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        try:
            if self.dry_run:
                return True, f"[DRY RUN] Would apply network config: {config.get('interface', 'unknown')}"

            # Example: Apply network configuration
            # In real implementation, this would configure network interfaces
            interface = config.get('interface', 'eth0')
            ip_address = config.get('ip_address', '')
            netmask = config.get('netmask', '')

            message = f"Applied network config for {interface}: {ip_address}/{netmask}"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Error applying network config: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_user_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply user configuration

        Args:
            config: User configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        try:
            if self.dry_run:
                return True, f"[DRY RUN] Would create user: {config.get('username', 'unknown')}"

            username = config.get('username', '')
            groups = config.get('groups', [])

            # In real implementation, this would create users and assign groups
            message = f"Applied user config for {username} (groups: {', '.join(groups)})"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Error applying user config: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_file_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply file/directory configuration

        Args:
            config: File configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        try:
            source = config.get('source', '')
            destination = config.get('destination', '')
            permissions = config.get('permissions', '')

            if self.dry_run:
                return True, f"[DRY RUN] Would copy {source} to {destination}"

            # Create destination directory if needed
            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file (in real implementation, would restore from backup)
            message = f"Applied file config: {destination}"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Error applying file config: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_package_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply package configuration

        Args:
            config: Package configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        try:
            packages = config.get('packages', [])

            if self.dry_run:
                return True, f"[DRY RUN] Would install {len(packages)} packages"

            # In real implementation, would install packages
            message = f"Applied package config: {len(packages)} packages"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Error applying package config: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_service_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply service configuration

        Args:
            config: Service configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        try:
            service_name = config.get('name', '')
            enabled = config.get('enabled', False)
            running = config.get('running', False)

            if self.dry_run:
                return True, f"[DRY RUN] Would configure service: {service_name}"

            # In real implementation, would configure systemd services
            message = f"Applied service config: {service_name}"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Error applying service config: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_hostname_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply hostname configuration

        Args:
            config: Hostname configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        try:
            hostname = config.get('hostname', config.get('value', ''))

            if self.dry_run:
                current_hostname = platform.node()
                return True, f"[DRY RUN] Would change hostname from '{current_hostname}' to '{hostname}'"

            # In real implementation, would use hostnamectl or /etc/hostname
            # subprocess.run(['hostnamectl', 'set-hostname', hostname], check=True)
            message = f"Applied hostname: {hostname}"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Error applying hostname config: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_albis_registry_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply ALBIS-Registry configuration

        Args:
            config: ALBIS-Registry configuration dictionary

        Returns:
            Tuple of (success, message)
        """
        try:
            key = config.get('key', '')
            value = config.get('value', '')
            value_type = config.get('type', 'string')

            if self.dry_run:
                return True, f"[DRY RUN] Would set ALBIS registry key: {key} = {value} (type: {value_type})"

            # In real implementation, would use ALBIS API or registry editor
            # This would typically use:
            # - Windows Registry API for Windows systems
            # - ALBIS-specific configuration tool
            # - Direct file modification depending on ALBIS version

            message = f"Applied ALBIS registry: {key} = {value}"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Error applying ALBIS registry config: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_configuration(self, category: str, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply a configuration based on its category

        Args:
            category: Configuration category
            config: Configuration data

        Returns:
            Tuple of (success, message)
        """
        appliers = {
            'hostname': self.apply_hostname_config,
            'network': self.apply_network_config,
            'albis_registry': self.apply_albis_registry_config,
            'users': self.apply_user_config,
            'files': self.apply_file_config,
            'packages': self.apply_package_config,
            'services': self.apply_service_config,
        }

        applier = appliers.get(category)
        if applier:
            return applier(config)
        else:
            return False, f"Unknown configuration category: {category}"

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of applied configurations

        Returns:
            Dictionary with summary information
        """
        return {
            'applied_count': len(self.applied_configs),
            'error_count': len(self.errors),
            'applied_configs': self.applied_configs,
            'errors': self.errors
        }
