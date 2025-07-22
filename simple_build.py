#!/usr/bin/env python3
"""
Simple TOZSolutions Repository Build Script
Detects project types and builds them accordingly
"""

import os
import subprocess
import time
import sys

def run_command(cmd, cwd):
    """Run a command and handle errors"""
    print(f"  💻 Komut: {cmd}")
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=True, check=False, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
        if result.returncode == 0:
            if result.stdout.strip():
                print(f"  ✅ Başarılı: {result.stdout.strip()[:200]}{'...' if len(result.stdout.strip()) > 200 else ''}")
            return True
        else:
            if result.stderr.strip():
                print(f"  ❌ Hata: {result.stderr.strip()[:200]}{'...' if len(result.stderr.strip()) > 200 else ''}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⏰ Timeout: Komut çok uzun sürdü")
        return False
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False

def detect_project_type(folder_path):
    """Detect project type based on files"""
    try:
        files = os.listdir(folder_path)
        
        if "package.json" in files:
            # Check if yarn.lock exists for yarn projects
            if "yarn.lock" in files:
                return "yarn"
            return "node"
        elif "requirements.txt" in files or "setup.py" in files:
            return "python"
        elif "pom.xml" in files:
            return "java-maven"
        elif "build.gradle" in files or "build.gradle.kts" in files:
            return "java-gradle"
        elif "Cargo.toml" in files:
            return "rust"
        elif "go.mod" in files:
            return "go"
        elif "index.html" in files or any(f.endswith('.html') for f in files):
            return "html"
        elif "Dockerfile" in files:
            return "docker"
        else:
            return "unknown"
    except Exception as e:
        print(f"  ❌ Dosya listesi alınamadı: {e}")
        return "error"

def build_node_project(folder_path):
    """Build Node.js project"""
    print("  📦 Node.js projesi tespit edildi")
    
    # Install dependencies
    if not run_command("npm install", folder_path):
        print("  ⚠️  npm install başarısız, yarn deneniyor...")
        if not run_command("yarn install", folder_path):
            return False
    
    # Try to build
    commands_to_try = ["npm run build", "npm run compile", "npm run dist"]
    for cmd in commands_to_try:
        if run_command(cmd, folder_path):
            print("  🎉 Build başarılı!")
            return True
    
    print("  ℹ️  Build script bulunamadı ama dependencies yüklendi")
    return True

def build_yarn_project(folder_path):
    """Build Yarn project"""
    print("  🧶 Yarn projesi tespit edildi")
    
    # Install dependencies
    if not run_command("yarn install", folder_path):
        return False
    
    # Try to build
    commands_to_try = ["yarn build", "yarn compile", "yarn dist"]
    for cmd in commands_to_try:
        if run_command(cmd, folder_path):
            print("  🎉 Build başarılı!")
            return True
    
    print("  ℹ️  Build script bulunamadı ama dependencies yüklendi")
    return True

def build_python_project(folder_path):
    """Build Python project"""
    print("  🐍 Python projesi tespit edildi")
    
    # Try different Python dependency installation methods
    success = False
    if os.path.exists(os.path.join(folder_path, "requirements.txt")):
        success = run_command("pip3 install -r requirements.txt", folder_path)
        if not success:
            success = run_command("python -m pip install -r requirements.txt", folder_path)
    
    if os.path.exists(os.path.join(folder_path, "setup.py")):
        if run_command("python setup.py install", folder_path):
            success = True
    
    # Try to run tests if they exist
    if os.path.exists(os.path.join(folder_path, "test")):
        run_command("python -m pytest", folder_path)
    
    return success

def build_java_maven_project(folder_path):
    """Build Java Maven project"""
    print("  ☕ Java Maven projesi tespit edildi")
    
    if not run_command("mvn clean compile", folder_path):
        return False
    
    run_command("mvn package", folder_path)
    return True

def build_java_gradle_project(folder_path):
    """Build Java Gradle project"""
    print("  ☕ Java Gradle projesi tespit edildi")
    
    # Try gradlew first, then gradle
    gradle_cmd = "./gradlew" if os.path.exists(os.path.join(folder_path, "gradlew")) else "gradle"
    
    if not run_command(f"{gradle_cmd} clean", folder_path):
        return False
    
    run_command(f"{gradle_cmd} build", folder_path)
    return True

def build_rust_project(folder_path):
    """Build Rust project"""
    print("  🦀 Rust projesi tespit edildi")
    return run_command("cargo build --release", folder_path)

def build_go_project(folder_path):
    """Build Go project"""
    print("  🐹 Go projesi tespit edildi")
    
    # Initialize go modules if needed
    run_command("go mod tidy", folder_path)
    return run_command("go build", folder_path)

def build_html_project(folder_path):
    """Handle HTML project"""
    print("  🌐 HTML projesi tespit edildi")
    print("  ℹ️  HTML projesi için build işlemi gerekmiyor")
    return True

def build_docker_project(folder_path):
    """Handle Docker project"""
    print("  🐳 Docker projesi tespit edildi")
    print("  ℹ️  Docker build atlanıyor (manuel olarak yapılabilir)")
    return True

def main():
    """Main build function"""
    start_time = time.time()
    
    # Determine root directory
    root_dir = "tozsolutions_repos" if os.path.exists("tozsolutions_repos") else "."
    
    print("🚀 TOZSolutions Build İşlemi Başlıyor...")
    print(f"📁 Hedef dizin: {os.path.abspath(root_dir)}")
    print(f"⏰ Başlangıç zamanı: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    successful_builds = []
    failed_builds = []
    skipped_builds = []
    
    # Get all directories
    try:
        folders = [f for f in os.listdir(root_dir) 
                  if os.path.isdir(os.path.join(root_dir, f)) 
                  and not f.startswith('.') 
                  and f not in ['node_modules', '__pycache__', 'target', 'build', 'dist']]
    except Exception as e:
        print(f"❌ Dizin erişim hatası: {e}")
        return
    
    if not folders:
        print("❌ Hiç proje klasörü bulunamadı!")
        return
    
    print(f"🔍 {len(folders)} proje bulundu:")
    for i, folder in enumerate(folders, 1):
        print(f"  {i:2d}. {folder}")
    print("=" * 70)
    
    for i, folder in enumerate(folders, 1):
        folder_path = os.path.join(root_dir, folder)
        print(f"\n[{i}/{len(folders)}] 📁 {folder} - İşlem başlıyor...")
        
        try:
            project_type = detect_project_type(folder_path)
            print(f"  🔍 Proje türü: {project_type}")
            
            if project_type == "error":
                skipped_builds.append(folder)
                continue
            
            success = False
            
            if project_type == "node":
                success = build_node_project(folder_path)
            elif project_type == "yarn":
                success = build_yarn_project(folder_path)
            elif project_type == "python":
                success = build_python_project(folder_path)
            elif project_type == "java-maven":
                success = build_java_maven_project(folder_path)
            elif project_type == "java-gradle":
                success = build_java_gradle_project(folder_path)
            elif project_type == "rust":
                success = build_rust_project(folder_path)
            elif project_type == "go":
                success = build_go_project(folder_path)
            elif project_type == "html":
                success = build_html_project(folder_path)
                skipped_builds.append(folder)  # HTML doesn't need building
                continue
            elif project_type == "docker":
                success = build_docker_project(folder_path)
                skipped_builds.append(folder)  # Docker skipped
                continue
            elif project_type == "unknown":
                print("  ❓ Bilinmeyen proje türü, atlanıyor...")
                skipped_builds.append(folder)
                continue
            
            if success:
                successful_builds.append(folder)
                print(f"  ✅ {folder} başarıyla build edildi!")
            else:
                failed_builds.append(folder)
                print(f"  ❌ {folder} build edilemedi!")
                
        except Exception as e:
            print(f"  ❌ Beklenmeyen hata: {e}")
            failed_builds.append(folder)
    
    # Final summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 70)
    print("🎯 BUILD ÖZET RAPORU")
    print("=" * 70)
    print(f"⏱️  Toplam süre: {duration:.1f} saniye")
    print(f"📊 Toplam proje: {len(folders)}")
    print(f"✅ Başarılı: {len(successful_builds)}")
    print(f"❌ Başarısız: {len(failed_builds)}")
    print(f"⏭️  Atlanan: {len(skipped_builds)}")
    
    if successful_builds:
        print(f"\n🎉 Başarılı projeler:")
        for proj in successful_builds:
            print(f"  ✅ {proj}")
    
    if failed_builds:
        print(f"\n💥 Başarısız projeler:")
        for proj in failed_builds:
            print(f"  ❌ {proj}")
    
    if skipped_builds:
        print(f"\n⏭️  Atlanan projeler:")
        for proj in skipped_builds:
            print(f"  ⏭️  {proj}")
    
    print("\n🏁 Build işlemi tamamlandı!")
    
    if failed_builds:
        print("⚠️  Bazı projeler başarısız oldu. Loglara bakarak sorunları çözebilirsiniz.")
    
    return len(failed_builds) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)