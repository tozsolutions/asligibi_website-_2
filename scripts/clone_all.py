#!/usr/bin/env python3
"""
TOZSolutions Repository Clone and Setup Script
Clones all repositories from tozsolutions organization and sets up deployment configurations
"""

import os
import sys
import subprocess
import json
import requests
import shutil
from pathlib import Path
import argparse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clone_all.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TOZSolutionsCloner:
    def __init__(self, github_token=None, base_dir="./tozsolutions_repos"):
        self.github_token = github_token
        self.base_dir = Path(base_dir)
        self.org_name = "tozsolutions"
        self.repos = []
        self.failed_repos = []
        self.successful_repos = []
        
    def setup_base_directory(self):
        """Create base directory for all repositories"""
        try:
            self.base_dir.mkdir(exist_ok=True)
            logger.info(f"📁 Base directory created: {self.base_dir}")
        except Exception as e:
            logger.error(f"❌ Failed to create base directory: {e}")
            sys.exit(1)
    
    def get_org_repositories(self):
        """Get all repositories from tozsolutions organization"""
        url = f"https://api.github.com/orgs/{self.org_name}/repos"
        headers = {}
        
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        
        all_repos = []
        page = 1
        
        try:
            while True:
                response = requests.get(url, headers=headers, params={'per_page': 100, 'page': page})
                
                if response.status_code == 200:
                    repos_page = response.json()
                    if not repos_page:  # No more repos
                        break
                    all_repos.extend(repos_page)
                    logger.info(f"📄 Page {page}: Found {len(repos_page)} repositories")
                    page += 1
                elif response.status_code == 404:
                    logger.warning(f"⚠️  Organization {self.org_name} not found or private")
                    # Try to get known repositories
                    self.get_known_repositories()
                    return True
                else:
                    logger.error(f"❌ Failed to fetch repositories: {response.status_code} - {response.text}")
                    if page == 1:  # If first page fails, try known repos
                        self.get_known_repositories()
                        return True
                    break
            
            self.repos = all_repos
            logger.info(f"✅ Found total {len(self.repos)} repositories in {self.org_name}")
            
            # Log repository names for debugging
            repo_names = [repo['name'] for repo in self.repos]
            logger.info(f"📋 Repository names: {', '.join(repo_names[:10])}{'...' if len(repo_names) > 10 else ''}")
            
            return True
                
        except Exception as e:
            logger.error(f"❌ Error fetching repositories: {e}")
            self.get_known_repositories()
            return True
    
    def get_known_repositories(self):
        """Get known repositories if API fails"""
        known_repos = [
            {
                'name': 'asligibi_website-_2',
                'clone_url': 'https://github.com/tozsolutions/asligibi_website-_2.git',
                'description': 'Aslı Gibi Website - Modern and professional website',
                'language': 'HTML',
                'private': False
            }
            # Add more known repositories here
        ]
        
        self.repos = known_repos
        logger.info(f"📋 Using {len(known_repos)} known repositories")
    
    def clone_repository(self, repo):
        """Clone a single repository"""
        repo_name = repo['name']
        repo_url = repo.get('clone_url', repo.get('git_url', ''))
        ssh_url = repo.get('ssh_url', '')
        html_url = repo.get('html_url', '')
        repo_path = self.base_dir / repo_name
        
        # Try different URL formats if one fails
        urls_to_try = [
            repo_url,
            f"https://github.com/{self.org_name}/{repo_name}.git",
            ssh_url,
            html_url + ".git" if html_url else ""
        ]
        urls_to_try = [url for url in urls_to_try if url]  # Remove empty URLs
        
        try:
            if repo_path.exists():
                logger.info(f"📁 {repo_name} already exists, pulling latest changes...")
                result = subprocess.run(
                    ['git', 'pull'], 
                    cwd=repo_path, 
                    capture_output=True, 
                    text=True,
                    timeout=300  # 5 minutes timeout
                )
                if result.returncode == 0:
                    logger.info(f"✅ {repo_name} updated successfully")
                    self.successful_repos.append(repo_name)
                    return True
                else:
                    logger.warning(f"⚠️  {repo_name} pull failed: {result.stderr}")
                    # Continue to try cloning fresh
                    import shutil
                    shutil.rmtree(repo_path)
            
            # Try cloning with different URLs
            for i, url in enumerate(urls_to_try):
                logger.info(f"🔄 Cloning {repo_name} (attempt {i+1}/{len(urls_to_try)})...")
                logger.info(f"   URL: {url}")
                
                try:
                    result = subprocess.run(
                        ['git', 'clone', url, str(repo_path)],
                        capture_output=True,
                        text=True,
                        timeout=600  # 10 minutes timeout
                    )
                    
                    if result.returncode == 0:
                        logger.info(f"✅ {repo_name} cloned successfully")
                        self.successful_repos.append(repo_name)
                        return True
                    else:
                        logger.warning(f"⚠️  Attempt {i+1} failed for {repo_name}: {result.stderr}")
                        if repo_path.exists():
                            import shutil
                            shutil.rmtree(repo_path)  # Clean up partial clone
                        
                except subprocess.TimeoutExpired:
                    logger.error(f"⏰ Clone timeout for {repo_name} with URL: {url}")
                    if repo_path.exists():
                        import shutil
                        shutil.rmtree(repo_path)
                    continue
                except Exception as e:
                    logger.error(f"❌ Clone error for {repo_name}: {e}")
                    if repo_path.exists():
                        import shutil
                        shutil.rmtree(repo_path)
                    continue
            
            # If all attempts failed
            error_msg = f"All clone attempts failed for {repo_name}"
            logger.error(f"❌ {error_msg}")
            self.failed_repos.append({
                'name': repo_name,
                'reason': 'All clone attempts failed',
                'urls_tried': urls_to_try
            })
            return False
            
        except Exception as e:
            logger.error(f"❌ Unexpected error cloning {repo_name}: {e}")
            self.failed_repos.append({
                'name': repo_name,
                'reason': f'Unexpected error: {str(e)}',
                'urls_tried': urls_to_try
            })
            return False
    
    def setup_deployment_config(self, repo_name):
        """Setup deployment configuration for a repository"""
        repo_path = self.base_dir / repo_name
        
        if not repo_path.exists():
            logger.warning(f"⚠️  Repository {repo_name} not found, skipping deployment setup")
            return False
        
        try:
            # Detect project type
            project_type = self.detect_project_type(repo_path)
            logger.info(f"🔍 Detected project type for {repo_name}: {project_type}")
            
            # Setup based on project type
            if project_type == 'html':
                self.setup_html_deployment(repo_path, repo_name)
            elif project_type == 'node':
                self.setup_node_deployment(repo_path, repo_name)
            elif project_type == 'python':
                self.setup_python_deployment(repo_path, repo_name)
            elif project_type == 'java':
                self.setup_java_deployment(repo_path, repo_name)
            else:
                self.setup_generic_deployment(repo_path, repo_name)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting up deployment for {repo_name}: {e}")
            return False
    
    def detect_project_type(self, repo_path):
        """Detect the type of project"""
        if (repo_path / 'package.json').exists():
            return 'node'
        elif (repo_path / 'requirements.txt').exists() or (repo_path / 'setup.py').exists():
            return 'python'
        elif (repo_path / 'pom.xml').exists() or (repo_path / 'build.gradle').exists():
            return 'java'
        elif (repo_path / 'index.html').exists():
            return 'html'
        else:
            return 'unknown'
    
    def setup_html_deployment(self, repo_path, repo_name):
        """Setup deployment for HTML projects"""
        logger.info(f"🌐 Setting up HTML deployment for {repo_name}")
        
        # Copy deployment configs from current project
        current_dir = Path('.')
        configs_to_copy = [
            '.github/workflows/deploy.yml',
            'vercel.json',
            'netlify.toml',
            'lighthouse.json',
            'package.json',
            '.gitignore',
            '.eslintrc.json',
            '.prettierrc'
        ]
        
        for config in configs_to_copy:
            src = current_dir / config
            dst = repo_path / config
            
            if src.exists():
                try:
                    # Create directory if needed
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy and customize config
                    if config == 'package.json':
                        self.customize_package_json(src, dst, repo_name)
                    elif config == 'vercel.json':
                        self.customize_vercel_config(src, dst, repo_name)
                    else:
                        shutil.copy2(src, dst)
                    
                    logger.info(f"✅ Copied {config} to {repo_name}")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to copy {config}: {e}")
    
    def setup_node_deployment(self, repo_path, repo_name):
        """Setup deployment for Node.js projects"""
        logger.info(f"📦 Setting up Node.js deployment for {repo_name}")
        
        # Check if package.json exists and update it
        package_json_path = repo_path / 'package.json'
        if package_json_path.exists():
            self.update_node_package_json(package_json_path, repo_name)
        
        # Copy workflow and configs
        self.copy_deployment_configs(repo_path, repo_name)
    
    def setup_python_deployment(self, repo_path, repo_name):
        """Setup deployment for Python projects"""
        logger.info(f"🐍 Setting up Python deployment for {repo_name}")
        
        # Create basic deployment configs
        self.create_python_configs(repo_path, repo_name)
    
    def setup_java_deployment(self, repo_path, repo_name):
        """Setup deployment for Java projects"""
        logger.info(f"☕ Setting up Java deployment for {repo_name}")
        
        # Create basic deployment configs
        self.create_java_configs(repo_path, repo_name)
    
    def setup_generic_deployment(self, repo_path, repo_name):
        """Setup generic deployment"""
        logger.info(f"📄 Setting up generic deployment for {repo_name}")
        
        # Copy basic configs
        self.copy_basic_configs(repo_path, repo_name)
    
    def customize_package_json(self, src, dst, repo_name):
        """Customize package.json for the specific repository"""
        try:
            with open(src, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # Update name and description
            package_data['name'] = repo_name.lower().replace('_', '-')
            package_data['description'] = f"TOZSolutions - {repo_name}"
            package_data['repository']['url'] = f"https://github.com/tozsolutions/{repo_name}.git"
            package_data['bugs']['url'] = f"https://github.com/tozsolutions/{repo_name}/issues"
            package_data['homepage'] = f"https://{repo_name.lower()}.vercel.app"
            
            with open(dst, 'w', encoding='utf-8') as f:
                json.dump(package_data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"⚠️  Failed to customize package.json: {e}")
            shutil.copy2(src, dst)
    
    def customize_vercel_config(self, src, dst, repo_name):
        """Customize Vercel config for the specific repository"""
        try:
            with open(src, 'r', encoding='utf-8') as f:
                vercel_data = json.load(f)
            
            # Update name
            vercel_data['name'] = repo_name.lower().replace('_', '-')
            
            with open(dst, 'w', encoding='utf-8') as f:
                json.dump(vercel_data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"⚠️  Failed to customize vercel.json: {e}")
            shutil.copy2(src, dst)
    
    def copy_deployment_configs(self, repo_path, repo_name):
        """Copy deployment configurations"""
        current_dir = Path('.')
        
        configs = [
            '.github/workflows/deploy.yml',
            'vercel.json',
            'netlify.toml',
            'lighthouse.json'
        ]
        
        for config in configs:
            src = current_dir / config
            dst = repo_path / config
            
            if src.exists():
                try:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    logger.info(f"✅ Copied {config}")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to copy {config}: {e}")
    
    def generate_summary_report(self):
        """Generate a summary report"""
        report_path = self.base_dir / 'clone_summary.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# TOZSolutions Repository Clone Summary\n\n")
            f.write(f"**Date:** {subprocess.check_output(['date']).decode().strip()}\n")
            f.write(f"**Total Repositories:** {len(self.repos)}\n")
            f.write(f"**Successfully Cloned:** {len(self.successful_repos)}\n")
            f.write(f"**Failed:** {len(self.failed_repos)}\n\n")
            
            if self.successful_repos:
                f.write("## ✅ Successfully Cloned Repositories\n\n")
                for repo in self.successful_repos:
                    f.write(f"- {repo}\n")
                f.write("\n")
            
            if self.failed_repos:
                f.write("## ❌ Failed Repositories\n\n")
                for repo in self.failed_repos:
                    f.write(f"- {repo}\n")
                f.write("\n")
            
            f.write("## 🚀 Next Steps\n\n")
            f.write("1. Review failed repositories and fix issues\n")
            f.write("2. Run `python build_all.py` to build all projects\n")
            f.write("3. Set up GitHub secrets for deployment\n")
            f.write("4. Test deployments\n")
        
        logger.info(f"📊 Summary report generated: {report_path}")
    
    def run(self):
        """Run the complete clone and setup process"""
        logger.info("🚀 Starting TOZSolutions repository clone and setup...")
        
        # Setup
        self.setup_base_directory()
        
        # Get repositories
        if not self.get_org_repositories():
            logger.error("❌ Failed to get repositories")
            sys.exit(1)
        
        # Clone repositories
        logger.info(f"📥 Cloning {len(self.repos)} repositories...")
        for repo in self.repos:
            if self.clone_repository(repo):
                self.setup_deployment_config(repo['name'])
        
        # Generate report
        self.generate_summary_report()
        
        logger.info("🎉 Clone and setup process completed!")
        logger.info(f"✅ Successful: {len(self.successful_repos)}")
        logger.info(f"❌ Failed: {len(self.failed_repos)}")

def main():
    parser = argparse.ArgumentParser(description='Clone and setup TOZSolutions repositories')
    parser.add_argument('--token', help='GitHub personal access token')
    parser.add_argument('--dir', default='./tozsolutions_repos', help='Base directory for repositories')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get token from environment if not provided
    github_token = args.token or os.getenv('GITHUB_TOKEN')
    
    cloner = TOZSolutionsCloner(github_token=github_token, base_dir=args.dir)
    cloner.run()

if __name__ == "__main__":
    main()