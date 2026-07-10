import os
import sys
import subprocess
import shutil

def run_command(command, env=None):
    """Helper to run system commands and stream the output to the console"""
    process = subprocess.Popen(
        command, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        shell=True, 
        text=True,
        env=env
    )
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    venv_dir = os.path.join(current_dir, "builder_env")
    
    # Calculate the root folder path (my_universal_dropdowns)
    # Moving up two levels from: .../my_universal_dropdowns/generator/build.py
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    final_exe_path = os.path.join(root_dir, "Node Builder Assistant.exe")
    
    print("🚀 Starting One-Click Standalone Executable Builder...\n")

    # 1. Create Virtual Environment
    if not os.path.exists(venv_dir):
        print("📦 Step 1: Creating isolated virtual environment...")
        if run_command(f'"{sys.executable}" -m venv builder_env') != 0:
            print("❌ Failed to create virtual environment.")
            sys.exit(1)
    else:
        print("✨ Virtual environment already exists, skipping creation.")

    # Determine paths inside venv based on OS
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
        pyinstaller_path = os.path.join(venv_dir, "Scripts", "pyinstaller.exe")
    else:  # Mac/Linux fallback
        pip_path = os.path.join(venv_dir, "bin", "pip")
        pyinstaller_path = os.path.join(venv_dir, "bin", "pyinstaller")

    # 2. Upgrade pip and install requirements
    print("\n📥 Step 2: Installing requirements into isolated environment...")
    run_command(f'"{pip_path}" install --upgrade pip')
    
    req_file = os.path.join(current_dir, "requirements.txt")
    if os.path.exists(req_file):
        if run_command(f'"{pip_path}" install -r "{req_file}"') != 0:
            print("❌ Failed to install dependencies.")
            sys.exit(1)
    else:
        print("❌ requirements.txt not found! Please create it first.")
        sys.exit(1)

    # 3. Compile with PyInstaller
    print("\n🛠️ Step 3: Compiling hyper-lean executable via PyInstaller...")
    build_cmd = f'"{pyinstaller_path}" --clean --noconsole --onefile --add-data "generator.html;." app.py'
    
    if run_command(build_cmd) == 0:
        print("\n✅ Compilation successful!")
        
        # 4. Relocate and Rename the Executable
        print("\n🚚 Step 4: Moving and renaming executable to root directory...")
        compiled_exe = os.path.join(current_dir, "dist", "app.exe")
        
        try:
            # Overwrite if it already exists from a previous build
            if os.path.exists(final_exe_path):
                os.remove(final_exe_path)
            
            shutil.move(compiled_exe, final_exe_path)
            print(f"✨ Successfully deployed to: {final_exe_path}")
        except Exception as e:
            print(f"❌ Failed to move or rename executable: {e}")
        
        # 5. Clean up temporary build clutter
        print("\n扫 Step 5: Cleaning up temporary build clutter...")
        build_folder = os.path.join(current_dir, "build")
        dist_folder = os.path.join(current_dir, "dist")
        spec_file = os.path.join(current_dir, "app.spec")
        
        if os.path.exists(build_folder):
            shutil.rmtree(build_folder)
        if os.path.exists(dist_folder):
            shutil.rmtree(dist_folder)
        if os.path.exists(spec_file):
            os.remove(spec_file)
            
        print("✨ Temporary build cache deleted. Process complete!")
    else:
        print("\n❌ PyInstaller compilation failed.")