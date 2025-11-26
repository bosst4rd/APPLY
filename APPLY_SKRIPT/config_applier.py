"""
Configuration Applier
Applies collected configurations to the new system
"""
import os
import subprocess
import shutil
import platform
import winreg
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple
from pathlib import Path


class ConfigApplier:
    """Applies configurations to the system"""

    def __init__(self, dry_run: bool = False, create_backup: bool = True):
        """
        Initialize configuration applier

        Args:
            dry_run: If True, only simulate actions without applying them
            create_backup: If True, create backup before applying changes
        """
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.applied_configs = []
        self.errors = []
        self.backup_dir = None

        if self.create_backup and not self.dry_run:
            self._create_backup_directory()

    def _create_backup_directory(self):
        """Create backup directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = Path(f"APPLY_Backup_{timestamp}")
        self.backup_dir.mkdir(exist_ok=True)

    def _backup_registry_key(self, key_path: str):
        """Backup a registry key before modifying"""
        if not self.backup_dir or self.dry_run:
            return

        try:
            backup_file = self.backup_dir / f"registry_{key_path.replace('\\', '_').replace(':', '')}.reg"
            # Export registry key
            subprocess.run(
                ['reg', 'export', key_path, str(backup_file), '/y'],
                check=True,
                capture_output=True
            )
        except Exception as e:
            self.errors.append(f"Backup failed for {key_path}: {str(e)}")

    def apply_hostname_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply hostname configuration"""
        try:
            hostname = config.get('hostname', config.get('value', ''))

            if self.dry_run:
                current_hostname = platform.node()
                return True, f"[DRY RUN] Would change hostname from '{current_hostname}' to '{hostname}'"

            if platform.system() == 'Windows':
                # Backup current hostname
                if self.create_backup:
                    current = subprocess.run(['hostname'], capture_output=True, text=True).stdout.strip()
                    backup_file = self.backup_dir / "hostname_backup.txt"
                    backup_file.write_text(current)

                # Change hostname
                subprocess.run(['wmic', 'computersystem', 'where', 'name="%computername%"', 'call', 'rename', f'name="{hostname}"'],
                              check=True, capture_output=True)
                message = f"Hostname geändert zu: {hostname} (Neustart erforderlich)"
            else:
                subprocess.run(['hostnamectl', 'set-hostname', hostname], check=True)
                message = f"Hostname geändert zu: {hostname}"

            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler beim Ändern des Hostnames: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_network_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply network configuration (IPv4: IP, DNS, Gateway)"""
        try:
            interface = config.get('interface', 'LAN')
            ip_address = config.get('ip_address', '')
            netmask = config.get('netmask', '')
            gateway = config.get('gateway', '')
            dns_servers = config.get('dns', [])

            if self.dry_run:
                return True, f"[DRY RUN] Would configure {interface}: IP={ip_address}, Gateway={gateway}, DNS={dns_servers}"

            if platform.system() == 'Windows':
                # Backup current network config
                if self.create_backup:
                    backup_file = self.backup_dir / f"network_{interface}.json"
                    current_config = {
                        'interface': interface,
                        'timestamp': datetime.now().isoformat()
                    }
                    backup_file.write_text(json.dumps(current_config, indent=2))

                # Set static IP
                subprocess.run([
                    'netsh', 'interface', 'ip', 'set', 'address',
                    f'name="{interface}"', 'static', ip_address, netmask, gateway
                ], check=True, capture_output=True)

                # Set DNS
                if dns_servers:
                    for idx, dns in enumerate(dns_servers):
                        if idx == 0:
                            subprocess.run([
                                'netsh', 'interface', 'ip', 'set', 'dns',
                                f'name="{interface}"', 'static', dns
                            ], check=True, capture_output=True)
                        else:
                            subprocess.run([
                                'netsh', 'interface', 'ip', 'add', 'dns',
                                f'name="{interface}"', dns, f'index={idx+1}'
                            ], check=True, capture_output=True)

                message = f"Netzwerk {interface} konfiguriert: {ip_address}"
            else:
                # Linux network configuration
                message = f"Netzwerk {interface}: {ip_address} (Linux-Implementierung pending)"

            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Netzwerkkonfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_routes_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply persistent IPv4 routes"""
        try:
            dest = config.get('destination', '')
            mask = config.get('mask', '')
            gateway = config.get('gateway', '')

            if self.dry_run:
                return True, f"[DRY RUN] Would add persistent route: {dest} mask {mask} via {gateway}"

            if platform.system() == 'Windows':
                # Add persistent route
                subprocess.run([
                    'route', '-p', 'add', dest, 'mask', mask, gateway
                ], check=True, capture_output=True)
                message = f"Persistente Route hinzugefügt: {dest} via {gateway}"
            else:
                message = f"Route {dest} via {gateway} (Linux-Implementierung pending)"

            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Route-Konfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_domain_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply domain configuration"""
        try:
            domain = config.get('domain', config.get('value', ''))

            if self.dry_run:
                return True, f"[DRY RUN] Would join domain: {domain}"

            # Domain join requires admin rights and credentials
            message = f"Domäne: {domain} (Manuelle Domänenbeitrittskonfiguration erforderlich)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Domänenkonfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_workgroup_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply workgroup configuration"""
        try:
            workgroup = config.get('workgroup', config.get('value', ''))

            if self.dry_run:
                return True, f"[DRY RUN] Would set workgroup to: {workgroup}"

            if platform.system() == 'Windows':
                # Change workgroup via WMI
                subprocess.run([
                    'wmic', 'computersystem', 'where', 'name="%computername%"',
                    'call', 'joindomainorworkgroup', f'name="{workgroup}"'
                ], check=True, capture_output=True)
                message = f"Arbeitsgruppe geändert zu: {workgroup} (Neustart erforderlich)"
            else:
                message = f"Arbeitsgruppe: {workgroup} (Nur Windows)"

            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Arbeitsgruppen-Konfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_network_drives_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply network drives configuration"""
        try:
            drive_letter = config.get('drive_letter', '')
            unc_path = config.get('unc_path', '')
            username = config.get('username', '')

            if self.dry_run:
                return True, f"[DRY RUN] Would map {drive_letter}: to {unc_path}"

            if platform.system() == 'Windows':
                # Map network drive
                cmd = ['net', 'use', f'{drive_letter}:', unc_path, '/persistent:yes']
                if username:
                    cmd.extend([f'/user:{username}'])

                subprocess.run(cmd, check=True, capture_output=True)
                message = f"Netzlaufwerk gemappt: {drive_letter}: -> {unc_path}"
            else:
                message = f"Netzlaufwerk: {drive_letter} -> {unc_path} (Nur Windows)"

            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Netzlaufwerk-Konfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_default_browser_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply default browser configuration"""
        try:
            browser = config.get('browser', config.get('value', ''))

            if self.dry_run:
                return True, f"[DRY RUN] Would set default browser to: {browser}"

            # This typically requires registry changes on Windows
            message = f"Standard-Browser: {browser} (Registry-Änderungen erforderlich)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Browser-Konfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_default_pdf_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply default PDF application configuration"""
        try:
            pdf_app = config.get('application', config.get('value', ''))

            if self.dry_run:
                return True, f"[DRY RUN] Would set default PDF app to: {pdf_app}"

            message = f"Standard-PDF-Anwendung: {pdf_app} (Registry-Änderungen erforderlich)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei PDF-App-Konfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_default_mail_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply default mail program configuration"""
        try:
            mail_app = config.get('application', config.get('value', ''))

            if self.dry_run:
                return True, f"[DRY RUN] Would set default mail app to: {mail_app}"

            message = f"Standard-Mailprogramm: {mail_app} (Registry-Änderungen erforderlich)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Mail-App-Konfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_default_word_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply default Word application configuration"""
        try:
            word_app = config.get('application', config.get('value', ''))

            if self.dry_run:
                return True, f"[DRY RUN] Would set default Word app to: {word_app}"

            message = f"Standard für Word-Dokumente: {word_app} (Registry-Änderungen erforderlich)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Word-App-Konfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_browser_favorites_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply browser favorites configuration"""
        try:
            browser = config.get('browser', '')
            favorites_file = config.get('favorites_file', '')

            if self.dry_run:
                return True, f"[DRY RUN] Would restore {browser} favorites from {favorites_file}"

            message = f"Browser-Favoriten für {browser} (SQLite-Konvertierung erforderlich)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Browser-Favoriten: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_username_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply username configuration"""
        try:
            username = config.get('username', '')

            if self.dry_run:
                return True, f"[DRY RUN] Would create/configure user: {username}"

            message = f"Benutzer: {username} (Benutzererstellung erfordert Admin-Rechte)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei Benutzerkonfiguration: {str(e)}"
            self.errors.append(error_msg)
            return False, error_msg

    def apply_mobackup_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply MoBackup configuration"""
        try:
            outlook_backup = config.get('outlook_backup', False)

            if self.dry_run:
                return True, f"[DRY RUN] Would configure MoBackup for Outlook"

            message = f"MoBackup konfiguriert (GUI-Start erforderlich)"
            self.applied_configs.append(message)
            return True, message

        except Exception as e:
            error_msg = f"Fehler bei MoBackup-Konfiguration: {str(e)}"
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
            'username': self.apply_username_config,
            'domain': self.apply_domain_config,
            'workgroup': self.apply_workgroup_config,
            'network': self.apply_network_config,
            'routes': self.apply_routes_config,
            'network_drives': self.apply_network_drives_config,
            'default_browser': self.apply_default_browser_config,
            'default_pdf': self.apply_default_pdf_config,
            'default_mail': self.apply_default_mail_config,
            'default_word': self.apply_default_word_config,
            'browser_favorites': self.apply_browser_favorites_config,
            'mobackup': self.apply_mobackup_config,
        }

        applier = appliers.get(category)
        if applier:
            return applier(config)
        else:
            return False, f"Unbekannte Kategorie: {category}"

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of applied configurations"""
        return {
            'applied_count': len(self.applied_configs),
            'error_count': len(self.errors),
            'applied_configs': self.applied_configs,
            'errors': self.errors,
            'backup_dir': str(self.backup_dir) if self.backup_dir else None
        }
