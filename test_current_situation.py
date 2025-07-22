#!/usr/bin/env python3
"""
Test script to understand current situation
"""
import os
import subprocess

def test_current_situation():
    """Test current directory and available repositories"""
    print("🔍 Mevcut Durum Analizi")
    print("=" * 50)
    
    # Current directory
    current_dir = os.getcwd()
    print(f"📁 Şu anki dizin: {current_dir}")
    
    # List all items in current directory
    print(f"\n📋 Mevcut dizindeki içerik:")
    try:
        items = os.listdir(current_dir)
        for item in sorted(items):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                print(f"   📁 {item}/")
            else:
                print(f"   📄 {item}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # Check if this is a git repository
    git_dir = os.path.join(current_dir, '.git')
    if os.path.exists(git_dir):
        print(f"\n✅ Bu bir Git repository'si")
        
        # Get remote info
        try:
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"🌐 Remote bilgileri:")
                for line in result.stdout.strip().split('\n'):
                    if line:
                        print(f"   {line}")
        except Exception as e:
            print(f"⚠️  Git remote bilgisi alınamadı: {e}")
    
    # Check for tozsolutions_repos directory
    repos_dir = os.path.join(current_dir, "tozsolutions_repos")
    if os.path.exists(repos_dir):
        print(f"\n📂 tozsolutions_repos dizini bulundu!")
        try:
            repos = [item for item in os.listdir(repos_dir) 
                    if os.path.isdir(os.path.join(repos_dir, item)) and item != '.git']
            print(f"📊 Klonlanmış repository sayısı: {len(repos)}")
            print(f"📋 Repository'ler:")
            for i, repo in enumerate(sorted(repos), 1):
                print(f"   {i:2d}. {repo}")
        except Exception as e:
            print(f"❌ tozsolutions_repos dizini okunamadı: {e}")
    else:
        print(f"\n❌ tozsolutions_repos dizini bulunamadı")
    
    # Check for Python and required tools
    print(f"\n🔧 Sistem Gereksinimleri:")
    
    tools = [
        ('python3', 'Python 3'),
        ('git', 'Git'),
        ('npm', 'Node.js/npm'),
        ('node', 'Node.js')
    ]
    
    for cmd, name in tools:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                print(f"   ✅ {name}: {version}")
            else:
                print(f"   ❌ {name}: Bulunamadı")
        except FileNotFoundError:
            print(f"   ❌ {name}: Kurulu değil")
        except Exception as e:
            print(f"   ⚠️  {name}: Test edilemedi ({e})")
    
    print(f"\n" + "=" * 50)
    print("🎯 Öneriler:")
    
    if not os.path.exists(repos_dir):
        print("1. İlk olarak clone_all.py script'ini çalıştırın")
        print("   python scripts/clone_all.py")
    else:
        print("1. Mevcut repository'ler var, build işlemine geçebilirsiniz")
        print("   python scripts/build_all.py")
    
    print("2. GitHub token kullanarak daha fazla repository'ye erişin")
    print("3. Eksik olan araçları kurun (Node.js, Git, vs.)")

if __name__ == "__main__":
    test_current_situation()