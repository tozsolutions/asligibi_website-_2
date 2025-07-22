#!/usr/bin/env python3
"""
Simple TOZSolutions Repository Clone Script
Uses git commands directly without external dependencies
"""

import os
import subprocess
import time

def run_command(cmd, cwd=None):
    """Run a command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def clone_repository(repo_name, base_dir):
    """Clone a single repository"""
    print(f"🔄 Cloning {repo_name}...")
    
    # Different URL formats to try
    urls = [
        f"https://github.com/tozsolutions/{repo_name}.git",
        f"https://github.com/tozsolutions/{repo_name}",
        f"git@github.com:tozsolutions/{repo_name}.git"
    ]
    
    repo_path = os.path.join(base_dir, repo_name)
    
    # If already exists, pull latest
    if os.path.exists(repo_path):
        print(f"  📁 {repo_name} already exists, pulling latest...")
        success, stdout, stderr = run_command("git pull", repo_path)
        if success:
            print(f"  ✅ {repo_name} updated successfully")
            return True
        else:
            print(f"  ⚠️  Pull failed, trying fresh clone...")
            import shutil
            shutil.rmtree(repo_path)
    
    # Try cloning with different URLs
    for i, url in enumerate(urls):
        print(f"  🔄 Attempt {i+1}: {url}")
        success, stdout, stderr = run_command(f"git clone {url} {repo_path}")
        
        if success:
            print(f"  ✅ {repo_name} cloned successfully!")
            return True
        else:
            print(f"  ❌ Failed: {stderr.strip()}")
            if os.path.exists(repo_path):
                import shutil
                shutil.rmtree(repo_path)
    
    print(f"  ❌ All attempts failed for {repo_name}")
    return False

def main():
    """Main clone function"""
    print("🚀 TOZSolutions Simple Clone İşlemi Başlıyor...")
    print("=" * 60)
    
    start_time = time.time()
    base_dir = "tozsolutions_repos"
    
    # Create base directory
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"📁 Created directory: {base_dir}")
    
    # Known repository names (we'll expand this list)
    # These are common repository names that might exist
    known_repos = [
        "asligibi_website-_2",  # Current repo
        "website",
        "portfolio",
        "blog", 
        "app",
        "dashboard",
        "admin",
        "api",
        "backend",
        "frontend",
        "mobile",
        "docs",
        "landing",
        "shop",
        "ecommerce",
        "cms",
        "crm",
        "erp",
        "hr",
        "finance",
        "inventory",
        "booking",
        "reservation",
        "chat",
        "messaging",
        "social",
        "network",
        "platform",
        "service",
        "microservice",
        "auth",
        "authentication",
        "authorization",
        "payment",
        "billing",
        "subscription",
        "notification",
        "email",
        "sms",
        "analytics",
        "monitoring",
        "logging",
        "config",
        "utils",
        "tools",
        "scripts",
        "automation",
        "ci-cd",
        "devops",
        "docker",
        "kubernetes",
        "terraform",
        "ansible"
    ]
    
    # Try to get more repositories using GitHub CLI or API if available
    print("🔍 Trying to discover more repositories...")
    
    # Method 1: Try GitHub CLI
    success, stdout, stderr = run_command("gh repo list tozsolutions --limit 100")
    if success and stdout:
        print("✅ Found repositories via GitHub CLI")
        lines = stdout.strip().split('\n')
        for line in lines:
            if line and '\t' in line:
                repo_name = line.split('\t')[0].split('/')[-1]
                if repo_name not in known_repos:
                    known_repos.append(repo_name)
    
    # Method 2: Try curl with GitHub API (using token from git config)
    if len(known_repos) < 20:  # If we don't have many repos, try API
        print("🔍 Trying GitHub API...")
        success, stdout, stderr = run_command("curl -s https://api.github.com/orgs/tozsolutions/repos?per_page=100")
        if success and stdout and stdout.startswith('['):
            try:
                # Simple JSON parsing without imports
                import json
                repos_data = json.loads(stdout)
                for repo in repos_data:
                    if isinstance(repo, dict) and 'name' in repo:
                        repo_name = repo['name']
                        if repo_name not in known_repos:
                            known_repos.append(repo_name)
                print(f"✅ Found {len(repos_data)} repositories via API")
            except:
                print("⚠️  Could not parse API response")
    
    print(f"📊 Total repositories to try: {len(known_repos)}")
    print("=" * 60)
    
    successful_clones = []
    failed_clones = []
    
    for i, repo_name in enumerate(known_repos, 1):
        print(f"\n[{i}/{len(known_repos)}] Processing: {repo_name}")
        
        if clone_repository(repo_name, base_dir):
            successful_clones.append(repo_name)
        else:
            failed_clones.append(repo_name)
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("🎉 CLONE İŞLEMİ TAMAMLANDI!")
    print("=" * 60)
    print(f"⏱️  Toplam süre: {duration:.2f} saniye")
    print(f"📊 Denenen repository: {len(known_repos)}")
    print(f"✅ Başarılı: {len(successful_clones)}")
    print(f"❌ Başarısız: {len(failed_clones)}")
    
    if successful_clones:
        print(f"\n✅ Başarıyla klonlanan repository'ler:")
        for i, repo in enumerate(successful_clones, 1):
            print(f"   {i:2d}. {repo}")
    
    if failed_clones:
        print(f"\n❌ Klonlanamayan repository'ler:")
        for i, repo in enumerate(failed_clones, 1):
            print(f"   {i:2d}. {repo}")
    
    # Generate simple report
    try:
        report_path = os.path.join(base_dir, "clone_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("TOZSolutions Clone Raporu\n")
            f.write("=" * 30 + "\n")
            f.write(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Süre: {duration:.2f} saniye\n")
            f.write(f"Denenen: {len(known_repos)} repository\n")
            f.write(f"Başarılı: {len(successful_clones)}\n")
            f.write(f"Başarısız: {len(failed_clones)}\n\n")
            
            if successful_clones:
                f.write("Başarılı Repository'ler:\n")
                for repo in successful_clones:
                    f.write(f"  - {repo}\n")
                f.write("\n")
            
            if failed_clones:
                f.write("Başarısız Repository'ler:\n")
                for repo in failed_clones:
                    f.write(f"  - {repo}\n")
        
        print(f"\n📄 Rapor oluşturuldu: {report_path}")
    except Exception as e:
        print(f"⚠️  Rapor oluşturulamadı: {e}")
    
    print(f"\n🏁 İşlem tamamlandı!")
    print(f"📁 Repository'ler {base_dir} dizininde")
    
    return len(successful_clones)

if __name__ == "__main__":
    main()