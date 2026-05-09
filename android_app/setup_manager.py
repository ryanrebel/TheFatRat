import subprocess
import os
import json
from pathlib import Path
from datetime import datetime
import shutil

class SetupManager:
    """Manages TheFatRat installation and setup process"""
    
    def __init__(self):
        self.install_path = "/data/local/tmp"
        self.logs = []
        self.installed_components = []
        self.setup_script_path = None
        
    def log(self, message):
        """Add message to logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
        return log_entry
    
    def check_root_access(self):
        """Check if device has root access"""
        try:
            result = subprocess.run(['su', '-c', 'whoami'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                self.log("✅ Root access verified")
                return True
            else:
                self.log("❌ Root access denied")
                return False
        except Exception as e:
            self.log(f"⚠️ Root check failed: {str(e)}")
            return False
    
    def check_internet_connection(self):
        """Check if device has internet connection"""
        try:
            result = subprocess.run(['ping', '-c', '1', '8.8.8.8'],
                                  capture_output=True,
                                  timeout=5)
            if result.returncode == 0:
                self.log("✅ Internet connection verified")
                return True
            else:
                self.log("❌ No internet connection")
                return False
        except Exception as e:
            self.log(f"⚠️ Internet check failed: {str(e)}")
            return False
    
    def check_python_version(self):
        """Check Python version compatibility"""
        try:
            result = subprocess.run(['python3', '--version'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            version = result.stdout.strip()
            self.log(f"✅ Python version: {version}")
            return True
        except Exception as e:
            self.log(f"❌ Python check failed: {str(e)}")
            return False
    
    def setup_environment(self, config):
        """Setup installation environment"""
        try:
            self.log("Setting up installation environment...")
            self.install_path = config.get("install_path", "/data/local/tmp")
            
            # Create installation directories
            Path(self.install_path).mkdir(parents=True, exist_ok=True)
            Path(f"{self.install_path}/logs").mkdir(parents=True, exist_ok=True)
            Path(f"{self.install_path}/tools").mkdir(parents=True, exist_ok=True)
            Path(f"{self.install_path}/config").mkdir(parents=True, exist_ok=True)
            
            self.log(f"✅ Installation environment ready at {self.install_path}")
            return {"success": True}
        except Exception as e:
            error_msg = f"❌ Environment setup failed: {str(e)}"
            self.log(error_msg)
            return {"success": False, "error": str(e)}
    
    def install_java(self):
        """Install Java JDK"""
        try:
            self.log("Installing Java JDK...")
            
            # Check if already installed
            result = subprocess.run(['which', 'java'],
                                  capture_output=True,
                                  timeout=5)
            if result.returncode == 0:
                self.log("✅ Java already installed")
                self.installed_components.append("Java JDK")
                return {"success": True}
            
            # Install Java
            subprocess.run(['apt-get', 'update'], check=True, capture_output=True, timeout=300)
            subprocess.run(['apt-get', 'install', '-y', 'default-jdk', 'default-jre'],
                         check=True, capture_output=True, timeout=600)
            
            self.log("✅ Java JDK installed successfully")
            self.installed_components.append("Java JDK")
            return {"success": True}
        except Exception as e:
            error_msg = f"❌ Java installation failed: {str(e)}"
            self.log(error_msg)
            return {"success": False, "error": str(e)}
    
    def install_metasploit(self):
        """Install Metasploit Framework"""
        try:
            self.log("Installing Metasploit Framework...")
            
            # Check if already installed
            result = subprocess.run(['which', 'msfconsole'],
                                  capture_output=True,
                                  timeout=5)
            if result.returncode == 0:
                self.log("✅ Metasploit already installed")
                self.installed_components.append("Metasploit Framework")
                return {"success": True}
            
            # Install Metasploit
            subprocess.run(['apt-get', 'update'], check=True, capture_output=True, timeout=300)
            subprocess.run(['apt-get', 'install', '-y', 'metasploit-framework'],
                         check=True, capture_output=True, timeout=600)
            
            self.log("✅ Metasploit Framework installed successfully")
            self.installed_components.append("Metasploit Framework")
            return {"success": True}
        except Exception as e:
            error_msg = f"❌ Metasploit installation failed: {str(e)}"
            self.log(error_msg)
            return {"success": False, "error": str(e)}
    
    def install_backdoor_factory(self):
        """Install Backdoor Factory"""
        try:
            self.log("Installing Backdoor Factory...")
            
            # Check if already installed
            result = subprocess.run(['which', 'backdoor-factory'],
                                  capture_output=True,
                                  timeout=5)
            if result.returncode == 0:
                self.log("✅ Backdoor Factory already installed")
                self.installed_components.append("Backdoor Factory")
                return {"success": True}
            
            # Install Backdoor Factory
            subprocess.run(['apt-get', 'update'], check=True, capture_output=True, timeout=300)
            subprocess.run(['apt-get', 'install', '-y', 'backdoor-factory'],
                         check=True, capture_output=True, timeout=600)
            
            self.log("✅ Backdoor Factory installed successfully")
            self.installed_components.append("Backdoor Factory")
            return {"success": True}
        except Exception as e:
            error_msg = f"❌ Backdoor Factory installation failed: {str(e)}"
            self.log(error_msg)
            return {"success": False, "error": str(e)}
    
    def install_searchsploit(self):
        """Install Searchsploit (ExploitDB)"""
        try:
            self.log("Installing Searchsploit...")
            
            # Check if already installed
            result = subprocess.run(['which', 'searchsploit'],
                                  capture_output=True,
                                  timeout=5)
            if result.returncode == 0:
                self.log("✅ Searchsploit already installed")
                self.installed_components.append("Searchsploit")
                return {"success": True}
            
            # Install Searchsploit
            subprocess.run(['apt-get', 'update'], check=True, capture_output=True, timeout=300)
            subprocess.run(['apt-get', 'install', '-y', 'exploitdb'],
                         check=True, capture_output=True, timeout=600)
            
            self.log("✅ Searchsploit installed successfully")
            self.installed_components.append("Searchsploit")
            return {"success": True}
        except Exception as e:
            error_msg = f"❌ Searchsploit installation failed: {str(e)}"
            self.log(error_msg)
            return {"success": False, "error": str(e)}
    
    def install_apktool(self):
        """Install APKTool"""
        try:
            self.log("Installing APKTool...")
            
            # Check if already installed
            result = subprocess.run(['which', 'apktool'],
                                  capture_output=True,
                                  timeout=5)
            if result.returncode == 0:
                self.log("✅ APKTool already installed")
                self.installed_components.append("APKTool")
                return {"success": True}
            
            # Install APKTool
            subprocess.run(['apt-get', 'update'], check=True, capture_output=True, timeout=300)
            subprocess.run(['apt-get', 'install', '-y', 'apktool'],
                         check=True, capture_output=True, timeout=600)
            
            self.log("✅ APKTool installed successfully")
            self.installed_components.append("APKTool")
            return {"success": True}
        except Exception as e:
            error_msg = f"❌ APKTool installation failed: {str(e)}"
            self.log(error_msg)
            return {"success": False, "error": str(e)}
    
    def install_component(self, component_name, config):
        """Install a specific component"""
        component_map = {
            "Metasploit Framework": self.install_metasploit,
            "Backdoor Factory": self.install_backdoor_factory,
            "Searchsploit": self.install_searchsploit,
            "APKTool": self.install_apktool,
            "Java JDK": self.install_java
        }
        
        if component_name in component_map:
            return component_map[component_name]()
        else:
            return {"success": False, "error": f"Unknown component: {component_name}"}
    
    def run_setup_checks(self):
        """Run pre-installation checks"""
        self.log("Running pre-installation checks...")
        
        checks = {
            "Root Access": self.check_root_access(),
            "Internet Connection": self.check_internet_connection(),
            "Python Version": self.check_python_version()
        }
        
        self.log("\n=== Pre-Installation Checks ===")
        for check_name, result in checks.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"{check_name}: {status}")
        
        return all(checks.values())
    
    def start_installation(self, config):
        """Start full installation process"""
        try:
            self.log("=== TheFatRat Installation Started ===")
            self.log(f"Timestamp: {datetime.now()}")
            
            # Run pre-checks
            if not self.run_setup_checks():
                self.log("⚠️ Pre-installation checks failed. Continuing anyway...")
            
            # Setup environment
            env_result = self.setup_environment(config)
            if not env_result['success']:
                return {"success": False, "error": "Environment setup failed"}
            
            # Install components based on config
            if config.get("enable_java"):
                self.install_java()
            
            if config.get("enable_metasploit"):
                self.install_metasploit()
            
            if config.get("enable_backdoor_factory"):
                self.install_backdoor_factory()
            
            if config.get("enable_searchsploit"):
                self.install_searchsploit()
            
            if config.get("enable_apktool"):
                self.install_apktool()
            
            self.log(f"\n=== Installation Complete ===")
            self.log(f"Total Components Installed: {len(self.installed_components)}")
            self.log(f"Timestamp: {datetime.now()}")
            
            return {
                "success": True,
                "installed_components": self.installed_components,
                "logs": self.logs
            }
        except Exception as e:
            error_msg = f"❌ Installation failed: {str(e)}"
            self.log(error_msg)
            return {"success": False, "error": str(e), "logs": self.logs}
    
    def get_logs(self):
        """Return all installation logs"""
        return self.logs
    
    def save_logs(self, filepath):
        """Save logs to file"""
        try:
            with open(filepath, 'w') as f:
                f.write("\n".join(self.logs))
            self.log(f"✅ Logs saved to {filepath}")
            return True
        except Exception as e:
            self.log(f"❌ Failed to save logs: {str(e)}")
            return False
