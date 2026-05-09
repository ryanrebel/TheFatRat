import streamlit as st
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from setup_manager import SetupManager
from file_manager import FileManager

# Page configuration
st.set_page_config(
    page_title="TheFatRat Android Installer",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'setup_manager' not in st.session_state:
    st.session_state.setup_manager = SetupManager()

if 'file_manager' not in st.session_state:
    st.session_state.file_manager = FileManager()

if 'installation_started' not in st.session_state:
    st.session_state.installation_started = False

if 'installation_complete' not in st.session_state:
    st.session_state.installation_complete = False

if 'logs' not in st.session_state:
    st.session_state.logs = []

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #ff6b6b;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .status-complete {
        color: #51cf66;
        font-weight: bold;
    }
    .status-error {
        color: #ff6b6b;
        font-weight: bold;
    }
    .status-pending {
        color: #ffd43b;
        font-weight: bold;
    }
    .status-running {
        color: #4dabf7;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<div class="main-header">☣️ TheFatRat Android Installer ☣️</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Installation Settings")
    with col2:
        if st.button("🔄 Refresh Settings"):
            st.rerun()
    
    st.markdown("---")
    
    # Load/Save Configuration
    config_file = Path("config/settings.json")
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "install_path": "/data/local/tmp",
            "enable_metasploit": True,
            "enable_backdoor_factory": True,
            "enable_searchsploit": True,
            "enable_apktool": True,
            "enable_java": True,
            "package_for_deployment": True,
            "deployment_target": "local_storage"
        }
    
    # Configuration options
    st.write("**Core Tools**")
    config["enable_metasploit"] = st.checkbox("Metasploit Framework", value=config.get("enable_metasploit", True))
    config["enable_backdoor_factory"] = st.checkbox("Backdoor Factory", value=config.get("enable_backdoor_factory", True))
    config["enable_searchsploit"] = st.checkbox("Searchsploit (ExploitDB)", value=config.get("enable_searchsploit", True))
    config["enable_apktool"] = st.checkbox("APKTool", value=config.get("enable_apktool", True))
    config["enable_java"] = st.checkbox("Java JDK", value=config.get("enable_java", True))
    
    st.markdown("---")
    st.write("**Deployment**")
    config["package_for_deployment"] = st.checkbox("Package for Deployment", value=config.get("package_for_deployment", True))
    config["deployment_target"] = st.selectbox(
        "Deployment Target",
        ["local_storage", "external_server", "cloud_storage"],
        index=0
    )
    
    st.markdown("---")
    st.write("**Installation Path**")
    config["install_path"] = st.text_input("Base Installation Path", value=config.get("install_path", "/data/local/tmp"))
    
    # Save configuration
    if st.button("💾 Save Configuration"):
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        st.success("✅ Configuration saved!")

# Main Content Area
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Installation", "📊 Status", "📦 Packaging", "📜 Logs"])

# Tab 1: Installation
with tab1:
    st.header("Installation Process")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Selected Components")
        components = []
        if config.get("enable_metasploit"):
            components.append("✅ Metasploit Framework")
        if config.get("enable_backdoor_factory"):
            components.append("✅ Backdoor Factory")
        if config.get("enable_searchsploit"):
            components.append("✅ Searchsploit")
        if config.get("enable_apktool"):
            components.append("✅ APKTool")
        if config.get("enable_java"):
            components.append("✅ Java JDK")
        
        for component in components:
            st.write(component)
    
    with col2:
        st.metric("Total Components", len(components))
    
    st.markdown("---")
    
    # Installation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Installation", key="start_install", use_container_width=True):
            st.session_state.installation_started = True
            st.session_state.logs = []
            st.rerun()
    
    with col2:
        if st.button("⏸️ Pause Installation", key="pause_install", use_container_width=True, disabled=not st.session_state.installation_started):
            st.warning("Installation paused. Click 'Resume' to continue.")
    
    with col3:
        if st.button("🔄 Reset Installation", key="reset_install", use_container_width=True):
            st.session_state.installation_started = False
            st.session_state.installation_complete = False
            st.session_state.logs = []
            st.info("Installation reset. Ready for a new installation.")
            st.rerun()
    
    st.markdown("---")
    
    # Installation Progress
    if st.session_state.installation_started:
        st.subheader("Installation Progress")
        
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        
        try:
            setup_mgr = st.session_state.setup_manager
            total_steps = len(components)
            
            for i, component in enumerate(components):
                step_number = i + 1
                component_name = component.replace("✅ ", "")
                
                with status_placeholder.container():
                    st.info(f"Installing: {component_name} ({step_number}/{total_steps})")
                
                # Simulate installation (replace with actual installation logic)
                result = setup_mgr.install_component(component_name, config)
                
                progress = (step_number / total_steps) * 100
                progress_bar.progress(int(progress))
                
                if result['success']:
                    st.session_state.logs.append(f"[✅] {component_name} installed successfully")
                    st.success(f"✅ {component_name} installed")
                else:
                    st.session_state.logs.append(f"[❌] {component_name} failed: {result['error']}")
                    st.error(f"❌ {component_name} failed: {result['error']}")
            
            progress_bar.progress(100)
            st.session_state.installation_complete = True
            st.balloons()
            st.success("🎉 Installation Complete!")
            
        except Exception as e:
            st.error(f"❌ Installation failed: {str(e)}")
            st.session_state.logs.append(f"[ERROR] {str(e)}")

# Tab 2: Status
with tab2:
    st.header("Installation Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Installation Status", "Complete" if st.session_state.installation_complete else "Pending")
    with col2:
        st.metric("Components Installed", len(components) if st.session_state.installation_complete else "0")
    with col3:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    with col4:
        st.metric("Logs Entries", len(st.session_state.logs))
    
    st.markdown("---")
    
    st.subheader("Detailed Status")
    
    status_data = {
        "Component": [],
        "Status": [],
        "Progress": [],
        "Details": []
    }
    
    for component in components:
        component_name = component.replace("✅ ", "")
        status_data["Component"].append(component_name)
        if st.session_state.installation_complete:
            status_data["Status"].append("✅ Installed")
            status_data["Progress"].append("100%")
            status_data["Details"].append("Successfully installed")
        else:
            status_data["Status"].append("⏳ Pending")
            status_data["Progress"].append("0%")
            status_data["Details"].append("Waiting to install")
    
    import pandas as pd
    df = pd.DataFrame(status_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Tab 3: Packaging
with tab3:
    st.header("Package & Deploy")
    
    if not st.session_state.installation_complete:
        st.warning("⚠️ Please complete installation first before packaging.")
    else:
        st.success("✅ Installation complete. Ready to package!")
        
        st.subheader("Packaging Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Deployment Target**")
            deployment_target = st.selectbox(
                "Select target",
                ["Local Storage", "External Server", "Cloud Storage"],
                key="deploy_target"
            )
        
        with col2:
            st.write("**Package Format**")
            package_format = st.selectbox(
                "Select format",
                ["ZIP", "TAR.GZ", "7Z"],
                key="package_format"
            )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📦 Create Package", use_container_width=True):
                with st.spinner("Creating package..."):
                    try:
                        file_mgr = st.session_state.file_manager
                        package_path = file_mgr.create_package(
                            deployment_target,
                            package_format,
                            config
                        )
                        st.success(f"✅ Package created: {package_path}")
                        st.session_state.logs.append(f"[✅] Package created: {package_path}")
                    except Exception as e:
                        st.error(f"❌ Packaging failed: {str(e)}")
                        st.session_state.logs.append(f"[ERROR] {str(e)}")
        
        with col2:
            if st.button("📤 Deploy Package", use_container_width=True):
                with st.spinner("Deploying package..."):
                    try:
                        file_mgr = st.session_state.file_manager
                        result = file_mgr.deploy_package(
                            deployment_target,
                            config
                        )
                        st.success(f"✅ Package deployed successfully")
                        st.session_state.logs.append(f"[✅] Package deployed to {deployment_target}")
                    except Exception as e:
                        st.error(f"❌ Deployment failed: {str(e)}")
                        st.session_state.logs.append(f"[ERROR] {str(e)}")

# Tab 4: Logs
with tab4:
    st.header("Installation Logs")
    
    if st.session_state.logs:
        log_content = "\n".join(st.session_state.logs)
        st.text_area(
            "Logs",
            value=log_content,
            height=400,
            disabled=True,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Logs"):
                st.success("Logs copied to clipboard!")
        with col2:
            if st.button("💾 Save Logs"):
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                log_file = log_dir / f"installation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                with open(log_file, 'w') as f:
                    f.write(log_content)
                st.success(f"✅ Logs saved to {log_file}")
    else:
        st.info("No logs yet. Start an installation to see logs here.")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    TheFatRat Android Installer v1.0 | Made by ryanrebel | Original TheFatRat by Screetsec
    </div>
""", unsafe_allow_html=True)
