#!/usr/bin/env python3
"""
TOZSolutions Repository Build Script
Simple and effective build script for all repositories
"""

import os
import subprocess
import time
import sys

def run_command(cmd, cwd):
    """Run a command and handle errors"""
    print(f"  Komut: {cmd}")
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            print(f"  ✅ Çıktı: {result.stdout.strip()}")
        if result.stderr:
            print(f"  ⚠️  Uyarı: {result.stderr.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Hata oluştu: {e.stderr}")
        return False

def detect_project_type(folder_path):
    """Detect project type based on files"""
    files = os.listdir(folder_path)
    
    if "package.json" in files:
        return "node"
    elif "yarn.lock" in files:
        return "yarn"
    elif "requirements.txt" in files:
        return "python"
    elif "pom.xml" in files:
        return "java-maven"
    elif "build.gradle" in files:
        return "java-gradle"
    elif "Cargo.toml" in files:
        return "rust"
    elif "go.mod" in files:
        return "go"
    elif "index.html" in files:
        return "html"
    else:
        return "unknown"

def build_node_project(folder_path):
    """Build Node.js project"""
    print("  📦 Node.js projesi bulundu.")
    success = True
    
    # Install dependencies
    if not run_command("npm install", folder_path):
        success = False
    
    # Try to run build
    if success:
        # Check if build script exists
        try:
            result = subprocess.run("npm run build", cwd=folder_path, shell=True, 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✅ Build başarılı!")
            else:
                print("  ⚠️  Build script bulunamadı veya hata oluştu")
        except:
            print("  ⚠️  Build script bulunamadı")
    
    return success

def build_yarn_project(folder_path):
    """Build Yarn project"""
    print("  🧶 Yarn projesi bulundu.")
    success = True
    
    if not run_command("yarn install", folder_path):
        success = False
    
    if success:
        try:
            result = subprocess.run("yarn build", cwd=folder_path, shell=True,
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✅ Build başarılı!")
            else:
                print("  ⚠️  Build script bulunamadı veya hata oluştu")
        except:
            print("  ⚠️  Build script bulunamadı")
    
    return success

def build_python_project(folder_path):
    """Build Python project"""
    print("  🐍 Python projesi bulundu.")
    return run_command("pip install -r requirements.txt", folder_path)

def build_java_maven_project(folder_path):
    """Build Java Maven project"""
    print("  ☕ Java Maven projesi bulundu.")
    success = True
    
    if not run_command("mvn clean compile", folder_path):
        success = False
    
    if success:
        run_command("mvn package", folder_path)
    
    return success

def build_java_gradle_project(folder_path):
    """Build Java Gradle project"""
    print("  ☕ Java Gradle projesi bulundu.")
    success = True
    
    if not run_command("./gradlew clean", folder_path):
        success = False
    
    if success:
        run_command("./gradlew build", folder_path)
    
    return success

def build_rust_project(folder_path):
    """Build Rust project"""
    print("  🦀 Rust projesi bulundu.")
    return run_command("cargo build --release", folder_path)

def build_go_project(folder_path):
    """Build Go project"""
    print("  🐹 Go projesi bulundu.")
    return run_command("go build", folder_path)

def build_html_project(folder_path):
    """Handle HTML project"""
    print("  🌐 HTML projesi bulundu.")
    print("  ℹ️  HTML projesi için özel build işlemi gerekmiyor.")
    return True

def main():
    """Main build function"""
    start_time = time.time()
    
    # Determine root directory
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = os.getcwd()
    
    print(f"🚀 TOZSolutions Build İşlemi Başlıyor...")
    print(f"📁 Hedef dizin: {root_dir}")
    print(f"⏰ Başlangıç zamanı: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    successful_builds = []
    failed_builds = []
    skipped_builds = []
    
    # Check if we're in a tozsolutions_repos directory
    repos_dir = os.path.join(root_dir, "tozsolutions_repos")
    if os.path.exists(repos_dir):
        print(f"📂 tozsolutions_repos dizini bulundu, o dizini kullanıyoruz...")
        root_dir = repos_dir
    
    # Get all directories
    try:
        folders = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f)) and f != ".git"]
    except PermissionError:
        print(f"❌ Dizin erişim hatası: {root_dir}")
        return
    
    if not folders:
        print("❌ Hiç klasör bulunamadı!")
        return
    
    print(f"🔍 {len(folders)} klasör bulundu: {', '.join(folders[:10])}{'...' if len(folders) > 10 else ''}")
    print("=" * 60)
    
    for folder in folders:
        folder_path = os.path.join(root_dir, folder)
        print(f"\n--- 📁 {folder} klasöründe işlemler başlıyor ---")
        
        try:
            project_type = detect_project_type(folder_path)
            print(f"  🔍 Proje türü: {project_type}")
            
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
            else:
                print("  ❓ Otomatik build komutu bulunamadı (özel bir proje olabilir).")
                skipped_builds.append(folder)
                continue
            
            if success:
                successful_builds.append(folder)
                print(f"  ✅ {folder} başarıyla build edildi!")
            else:
                failed_builds.append(folder)
                print(f"  ❌ {folder} build edilemedi!")
                
        except Exception as e:
            print(f"  ❌ {folder} için beklenmeyen hata: {e}")
            failed_builds.append(folder)
    
    # Final summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("🎉 TÜM BUILD İŞLEMLERİ TAMAMLANDI!")
    print("=" * 60)
    print(f"⏱️  Toplam süre: {duration:.2f} saniye")
    print(f"📊 Toplam proje: {len(folders)}")
    print(f"✅ Başarılı: {len(successful_builds)}")
    print(f"❌ Başarısız: {len(failed_builds)}")
    print(f"⏭️  Atlanan: {len(skipped_builds)}")
    
    if successful_builds:
        print(f"\n✅ Başarılı projeler:")
        for project in successful_builds:
            print(f"   - {project}")
    
    if failed_builds:
        print(f"\n❌ Başarısız projeler:")
        for project in failed_builds:
            print(f"   - {project}")
    
    if skipped_builds:
        print(f"\n⏭️  Atlanan projeler:")
        for project in skipped_builds:
            print(f"   - {project}")
    
    # Generate simple report
    try:
        report_path = os.path.join(root_dir, "build_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("TOZSolutions Build Raporu\n")
            f.write("=" * 30 + "\n")
            f.write(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Süre: {duration:.2f} saniye\n")
            f.write(f"Toplam: {len(folders)} proje\n")
            f.write(f"Başarılı: {len(successful_builds)}\n")
            f.write(f"Başarısız: {len(failed_builds)}\n")
            f.write(f"Atlanan: {len(skipped_builds)}\n\n")
            
            if successful_builds:
                f.write("Başarılı Projeler:\n")
                for project in successful_builds:
                    f.write(f"  - {project}\n")
                f.write("\n")
            
            if failed_builds:
                f.write("Başarısız Projeler:\n")
                for project in failed_builds:
                    f.write(f"  - {project}\n")
                f.write("\n")
            
            if skipped_builds:
                f.write("Atlanan Projeler:\n")
                for project in skipped_builds:
                    f.write(f"  - {project}\n")
        
        print(f"\n📄 Rapor oluşturuldu: {report_path}")
    except Exception as e:
        print(f"⚠️  Rapor oluşturulamadı: {e}")
    
    print("\n🏁 İşlem tamamlandı!")
    
    # Return appropriate exit code
    if failed_builds:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()