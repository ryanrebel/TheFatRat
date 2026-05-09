import os
import shutil
import json
import tarfile
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime

class FileManager:
    """Manages file packaging and deployment"""
    
    def __init__(self):
        self.package_dir = Path("packages")
        self.deploy_dir = Path("deployment")
        self.logs = []
        self.package_dir.mkdir(exist_ok=True)
        self.deploy_dir.mkdir(exist_ok=True)
    
    def log(self, message):
        """Add message to logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
        return log_entry
    
    def create_package(self, deployment_target, package_format, config):
        """Create a deployment package"""
        try:
            self.log(f"Creating package for {deployment_target} in {package_format} format...")
            
            # Create temporary package directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_package = Path(f"temp_package_{timestamp}")
            temp_package.mkdir(exist_ok=True)
            
            # Gather installation files
            self.log("Gathering installation files...")
            self._gather_installation_files(temp_package, config)
            
            # Create package based on format
            package_path = None
            if package_format.upper() == "ZIP":
                package_path = self._create_zip_package(temp_package, timestamp)
            elif package_format.upper() == "TAR.GZ":
                package_path = self._create_targz_package(temp_package, timestamp)
            elif package_format.upper() == "7Z":
                package_path = self._create_7z_package(temp_package, timestamp)
            
            # Cleanup temporary directory
            shutil.rmtree(temp_package)
            
            self.log(f"✅ Package created successfully: {package_path}")
            return str(package_path)
        
        except Exception as e:
            self.log(f"❌ Package creation failed: {str(e)}")
            raise
    
    def _gather_installation_files(self, target_dir, config):
        """Gather all installation files into package directory"""
        try:
            # Create structure
            (target_dir / "tools").mkdir(exist_ok=True)
            (target_dir / "config").mkdir(exist_ok=True)
            (target_dir / "logs").mkdir(exist_ok=True)
            (target_dir / "scripts").mkdir(exist_ok=True)
            
            # Copy configuration
            self.log("Copying configuration files...")
            config_file = target_dir / "config" / "installation_config.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            # Create installation manifest
            manifest = {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "tools": {
                    "metasploit": config.get("enable_metasploit", False),
                    "backdoor_factory": config.get("enable_backdoor_factory", False),
                    "searchsploit": config.get("enable_searchsploit", False),
                    "apktool": config.get("enable_apktool", False),
                    "java": config.get("enable_java", False)
                },
                "install_path": config.get("install_path", "/data/local/tmp"),
                "deployment_target": config.get("deployment_target", "local_storage")
            }
            
            manifest_file = target_dir / "MANIFEST.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f, indent=4)
            
            self.log("✅ Files gathered successfully")
        
        except Exception as e:
            self.log(f"❌ Failed to gather files: {str(e)}")
            raise
    
    def _create_zip_package(self, source_dir, timestamp):
        """Create ZIP package"""
        try:
            self.log("Creating ZIP package...")
            package_name = f"thefatrat_android_{timestamp}.zip"
            package_path = self.package_dir / package_name
            
            shutil.make_archive(
                str(package_path).replace('.zip', ''),
                'zip',
                source_dir
            )
            
            # Get file size
            file_size = package_path.stat().st_size / (1024 * 1024)  # MB
            self.log(f"✅ ZIP package created: {package_path} ({file_size:.2f} MB)")
            return package_path
        
        except Exception as e:
            self.log(f"❌ ZIP creation failed: {str(e)}")
            raise
    
    def _create_targz_package(self, source_dir, timestamp):
        """Create TAR.GZ package"""
        try:
            self.log("Creating TAR.GZ package...")
            package_name = f"thefatrat_android_{timestamp}.tar.gz"
            package_path = self.package_dir / package_name
            
            with tarfile.open(package_path, "w:gz") as tar:
                tar.add(source_dir, arcname=".")
            
            # Get file size
            file_size = package_path.stat().st_size / (1024 * 1024)  # MB
            self.log(f"✅ TAR.GZ package created: {package_path} ({file_size:.2f} MB)")
            return package_path
        
        except Exception as e:
            self.log(f"❌ TAR.GZ creation failed: {str(e)}")
            raise
    
    def _create_7z_package(self, source_dir, timestamp):
        """Create 7Z package"""
        try:
            self.log("Creating 7Z package...")
            
            # Check if 7z is available
            result = subprocess.run(['which', '7z'], capture_output=True)
            if result.returncode != 0:
                self.log("⚠️ 7z not found, installing p7zip-full...")
                subprocess.run(['apt-get', 'install', '-y', 'p7zip-full'],
                             check=True, capture_output=True, timeout=300)
            
            package_name = f"thefatrat_android_{timestamp}.7z"
            package_path = self.package_dir / package_name
            
            subprocess.run([
                '7z', 'a', '-r', str(package_path), str(source_dir)
            ], check=True, capture_output=True)
            
            # Get file size
            file_size = package_path.stat().st_size / (1024 * 1024)  # MB
            self.log(f"✅ 7Z package created: {package_path} ({file_size:.2f} MB)")
            return package_path
        
        except Exception as e:
            self.log(f"❌ 7Z creation failed: {str(e)}")
            raise
    
    def deploy_package(self, deployment_target, config):
        """Deploy package to specified target"""
        try:
            self.log(f"Deploying package to {deployment_target}...")
            
            if deployment_target == "local_storage":
                return self._deploy_local_storage(config)
            elif deployment_target == "external_server":
                return self._deploy_external_server(config)
            elif deployment_target == "cloud_storage":
                return self._deploy_cloud_storage(config)
            else:
                raise ValueError(f"Unknown deployment target: {deployment_target}")
        
        except Exception as e:
            self.log(f"❌ Deployment failed: {str(e)}")
            raise
    
    def _deploy_local_storage(self, config):
        """Deploy to local device storage"""
        try:
            self.log("Deploying to local storage...")
            
            storage_path = Path("/sdcard/TheFatRat")
            storage_path.mkdir(parents=True, exist_ok=True)
            
            # Copy latest package to storage
            packages = list(self.package_dir.glob("thefatrat_android_*.zip")) + \
                      list(self.package_dir.glob("thefatrat_android_*.tar.gz")) + \
                      list(self.package_dir.glob("thefatrat_android_*.7z"))
            
            if packages:
                latest_package = max(packages, key=lambda x: x.stat().st_mtime)
                dest_path = storage_path / latest_package.name
                shutil.copy2(latest_package, dest_path)
                self.log(f"✅ Package deployed to {dest_path}")
                return {"success": True, "path": str(dest_path)}
            else:
                raise FileNotFoundError("No packages found to deploy")
        
        except Exception as e:
            self.log(f"❌ Local storage deployment failed: {str(e)}")
            raise
    
    def _deploy_external_server(self, config):
        """Deploy to external server (requires server config)"""
        try:
            self.log("Deploying to external server...")
            
            # Get latest package
            packages = list(self.package_dir.glob("thefatrat_android_*.*"))
            if not packages:
                raise FileNotFoundError("No packages found to deploy")
            
            latest_package = max(packages, key=lambda x: x.stat().st_mtime)
            
            # Create deployment info
            deployment_info = {
                "package_name": latest_package.name,
                "package_size_mb": latest_package.stat().st_size / (1024 * 1024),
                "deployment_time": datetime.now().isoformat(),
                "status": "ready_for_upload"
            }
            
            self.log(f"✅ Package ready for server deployment: {latest_package.name}")
            self.log(f"   Size: {deployment_info['package_size_mb']:.2f} MB")
            
            return {"success": True, "package": latest_package.name, "info": deployment_info}
        
        except Exception as e:
            self.log(f"❌ External server deployment failed: {str(e)}")
            raise
    
    def _deploy_cloud_storage(self, config):
        """Deploy to cloud storage (AWS S3, Google Drive, etc.)"""
        try:
            self.log("Preparing for cloud storage deployment...")
            
            # Get latest package
            packages = list(self.package_dir.glob("thefatrat_android_*.*"))
            if not packages:
                raise FileNotFoundError("No packages found to deploy")
            
            latest_package = max(packages, key=lambda x: x.stat().st_mtime)
            
            # Create deployment manifest
            deployment_manifest = {
                "package_name": latest_package.name,
                "package_size_bytes": latest_package.stat().st_size,
                "package_hash": self._calculate_hash(latest_package),
                "deployment_timestamp": datetime.now().isoformat(),
                "deployment_type": "cloud_storage",
                "status": "ready_for_upload"
            }
            
            manifest_file = self.deploy_dir / f"cloud_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(manifest_file, 'w') as f:
                json.dump(deployment_manifest, f, indent=4)
            
            self.log(f"✅ Cloud deployment manifest created: {manifest_file}")
            self.log(f"   Package: {latest_package.name}")
            self.log(f"   Size: {latest_package.stat().st_size / (1024 * 1024):.2f} MB")
            
            return {"success": True, "manifest": str(manifest_file), "package": latest_package.name}
        
        except Exception as e:
            self.log(f"❌ Cloud storage deployment failed: {str(e)}")
            raise
    
    def _calculate_hash(self, filepath):
        """Calculate SHA256 hash of file"""
        try:
            import hashlib
            sha256_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.log(f"⚠️ Hash calculation failed: {str(e)}")
            return "HASH_ERROR"
    
    def list_packages(self):
        """List all available packages"""
        try:
            packages = []
            for ext in ['*.zip', '*.tar.gz', '*.7z']:
                for pkg in self.package_dir.glob(ext):
                    packages.append({
                        "name": pkg.name,
                        "size_mb": pkg.stat().st_size / (1024 * 1024),
                        "created": datetime.fromtimestamp(pkg.stat().st_mtime).isoformat(),
                        "path": str(pkg)
                    })
            
            self.log(f"✅ Found {len(packages)} package(s)")
            return packages
        
        except Exception as e:
            self.log(f"❌ Failed to list packages: {str(e)}")
            return []
    
    def cleanup_old_packages(self, keep_count=5):
        """Remove old packages, keeping only the most recent"""
        try:
            self.log(f"Cleaning up old packages (keeping {keep_count} most recent)...")
            
            packages = []
            for ext in ['*.zip', '*.tar.gz', '*.7z']:
                packages.extend(self.package_dir.glob(ext))
            
            # Sort by creation time (newest first)
            packages.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove old ones
            removed_count = 0
            for old_package in packages[keep_count:]:
                old_package.unlink()
                removed_count += 1
                self.log(f"   Removed: {old_package.name}")
            
            self.log(f"✅ Cleanup complete: {removed_count} package(s) removed")
            return {"success": True, "removed": removed_count}
        
        except Exception as e:
            self.log(f"❌ Cleanup failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_logs(self):
        """Return all file manager logs"""
        return self.logs
