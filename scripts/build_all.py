#!/usr/bin/env python3
"""
TOZSolutions Repository Build Script
Builds all repositories from tozsolutions organization with proper configuration
"""

import os
import subprocess
import time
import sys

class TOZSolutionsBuilder:
    def __init__(self, base_dir="./tozsolutions_repos", parallel=True, max_workers=4):
        self.base_dir = Path(base_dir)
        self.parallel = parallel
        self.max_workers = max_workers
        self.build_results = {}
        self.successful_builds = []
        self.failed_builds = []
        self.skipped_builds = []
        
        # Build configurations for different project types
        self.build_configs = {
            'html': {
                'commands': [
                    'npm install',
                    'npm run build'
                ],
                'build_dir': 'dist',
                'required_files': ['package.json']
            },
            'node': {
                'commands': [
                    'npm install',
                    'npm run lint:fix',
                    'npm run test',
                    'npm run build'
                ],
                'build_dir': 'dist',
                'required_files': ['package.json']
            },
            'python': {
                'commands': [
                    'pip install -r requirements.txt',
                    'python -m pytest',
                    'python setup.py build'
                ],
                'build_dir': 'build',
                'required_files': ['requirements.txt', 'setup.py']
            },
            'java': {
                'commands': [
                    'mvn clean compile',
                    'mvn test',
                    'mvn package'
                ],
                'build_dir': 'target',
                'required_files': ['pom.xml']
            },
            'gradle': {
                'commands': [
                    './gradlew clean',
                    './gradlew test',
                    './gradlew build'
                ],
                'build_dir': 'build',
                'required_files': ['build.gradle']
            },
            'react': {
                'commands': [
                    'npm install',
                    'npm run lint:fix',
                    'npm run test -- --coverage --watchAll=false',
                    'npm run build'
                ],
                'build_dir': 'build',
                'required_files': ['package.json']
            },
            'vue': {
                'commands': [
                    'npm install',
                    'npm run lint:fix',
                    'npm run test:unit',
                    'npm run build'
                ],
                'build_dir': 'dist',
                'required_files': ['package.json']
            },
            'angular': {
                'commands': [
                    'npm install',
                    'ng lint --fix',
                    'ng test --watch=false --browsers=ChromeHeadless',
                    'ng build --prod'
                ],
                'build_dir': 'dist',
                'required_files': ['package.json', 'angular.json']
            }
        }
    
    def discover_repositories(self) -> List[Path]:
        """Discover all repositories in the base directory"""
        if not self.base_dir.exists():
            logger.error(f"❌ Base directory does not exist: {self.base_dir}")
            return []
        
        repos = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and (item / '.git').exists():
                repos.append(item)
                logger.info(f"📁 Found repository: {item.name}")
        
        logger.info(f"🔍 Discovered {len(repos)} repositories")
        return repos
    
    def detect_project_type(self, repo_path: Path) -> str:
        """Detect the type of project"""
        try:
            # Check for specific framework indicators
            if (repo_path / 'package.json').exists():
                with open(repo_path / 'package.json', 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    dependencies = package_data.get('dependencies', {})
                    dev_dependencies = package_data.get('devDependencies', {})
                    
                    # Check for React
                    if 'react' in dependencies or 'react' in dev_dependencies:
                        return 'react'
                    
                    # Check for Vue
                    if 'vue' in dependencies or '@vue/cli-service' in dev_dependencies:
                        return 'vue'
                    
                    # Check for Angular
                    if '@angular/core' in dependencies or '@angular/cli' in dev_dependencies:
                        return 'angular'
                    
                    # Default to node if package.json exists
                    return 'node'
            
            # Check for Python
            if (repo_path / 'requirements.txt').exists() or (repo_path / 'setup.py').exists():
                return 'python'
            
            # Check for Java Maven
            if (repo_path / 'pom.xml').exists():
                return 'java'
            
            # Check for Gradle
            if (repo_path / 'build.gradle').exists():
                return 'gradle'
            
            # Check for HTML projects
            if (repo_path / 'index.html').exists():
                return 'html'
            
            return 'unknown'
            
        except Exception as e:
            logger.warning(f"⚠️  Error detecting project type for {repo_path.name}: {e}")
            return 'unknown'
    
    def check_prerequisites(self, repo_path: Path, project_type: str) -> bool:
        """Check if all prerequisites for building are met"""
        if project_type == 'unknown':
            logger.warning(f"⚠️  Unknown project type for {repo_path.name}, skipping")
            return False
        
        config = self.build_configs.get(project_type, {})
        required_files = config.get('required_files', [])
        
        for file_name in required_files:
            if not (repo_path / file_name).exists():
                logger.warning(f"⚠️  Missing required file {file_name} in {repo_path.name}")
                return False
        
        return True
    
    def setup_build_environment(self, repo_path: Path, project_type: str) -> bool:
        """Setup build environment for the project"""
        try:
            # Ensure build directory exists and is clean
            config = self.build_configs.get(project_type, {})
            build_dir = repo_path / config.get('build_dir', 'dist')
            
            if build_dir.exists():
                logger.info(f"🧹 Cleaning existing build directory: {build_dir}")
                shutil.rmtree(build_dir)
            
            # Setup Node.js projects
            if project_type in ['html', 'node', 'react', 'vue', 'angular']:
                node_modules = repo_path / 'node_modules'
                if node_modules.exists():
                    logger.info(f"🧹 Cleaning node_modules: {node_modules}")
                    shutil.rmtree(node_modules)
            
            # Setup Python projects
            elif project_type == 'python':
                # Create virtual environment if it doesn't exist
                venv_path = repo_path / 'venv'
                if not venv_path.exists():
                    logger.info(f"🐍 Creating virtual environment: {venv_path}")
                    subprocess.run(['python', '-m', 'venv', str(venv_path)], 
                                 cwd=repo_path, check=True)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting up build environment for {repo_path.name}: {e}")
            return False
    
    def run_build_commands(self, repo_path: Path, project_type: str) -> Dict:
        """Run build commands for a repository"""
        build_start_time = time.time()
        result = {
            'repo': repo_path.name,
            'project_type': project_type,
            'success': False,
            'duration': 0,
            'commands': [],
            'errors': []
        }
        
        try:
            config = self.build_configs.get(project_type, {})
            commands = config.get('commands', [])
            
            logger.info(f"🔨 Building {repo_path.name} ({project_type})...")
            
            for i, command in enumerate(commands):
                logger.info(f"▶️  Running: {command}")
                command_start_time = time.time()
                
                # Handle Python virtual environment activation
                if project_type == 'python' and 'pip' in command:
                    if os.name == 'nt':  # Windows
                        command = f"venv\\Scripts\\activate && {command}"
                    else:  # Unix/Linux
                        command = f"source venv/bin/activate && {command}"
                
                try:
                    process = subprocess.run(
                        command,
                        shell=True,
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=600  # 10 minutes timeout
                    )
                    
                    command_duration = time.time() - command_start_time
                    
                    command_result = {
                        'command': command,
                        'duration': command_duration,
                        'return_code': process.returncode,
                        'stdout': process.stdout,
                        'stderr': process.stderr
                    }
                    
                    result['commands'].append(command_result)
                    
                    if process.returncode != 0:
                        error_msg = f"Command failed: {command}\nError: {process.stderr}"
                        logger.error(f"❌ {error_msg}")
                        result['errors'].append(error_msg)
                        return result
                    else:
                        logger.info(f"✅ Command completed in {command_duration:.2f}s")
                
                except subprocess.TimeoutExpired:
                    error_msg = f"Command timed out: {command}"
                    logger.error(f"⏰ {error_msg}")
                    result['errors'].append(error_msg)
                    return result
                
                except Exception as e:
                    error_msg = f"Command error: {command} - {str(e)}"
                    logger.error(f"❌ {error_msg}")
                    result['errors'].append(error_msg)
                    return result
            
            # Check if build artifacts were created
            build_dir = repo_path / config.get('build_dir', 'dist')
            if build_dir.exists() and any(build_dir.iterdir()):
                result['success'] = True
                logger.info(f"✅ Build successful for {repo_path.name}")
            else:
                error_msg = f"Build directory {build_dir} is empty or doesn't exist"
                logger.warning(f"⚠️  {error_msg}")
                result['errors'].append(error_msg)
            
        except Exception as e:
            error_msg = f"Build process error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            result['errors'].append(error_msg)
        
        finally:
            result['duration'] = time.time() - build_start_time
        
        return result
    
    def build_repository(self, repo_path: Path) -> Dict:
        """Build a single repository"""
        logger.info(f"🚀 Starting build for {repo_path.name}")
        
        try:
            # Detect project type
            project_type = self.detect_project_type(repo_path)
            logger.info(f"🔍 Detected project type: {project_type}")
            
            # Check prerequisites
            if not self.check_prerequisites(repo_path, project_type):
                result = {
                    'repo': repo_path.name,
                    'project_type': project_type,
                    'success': False,
                    'skipped': True,
                    'reason': 'Prerequisites not met'
                }
                self.skipped_builds.append(repo_path.name)
                return result
            
            # Setup build environment
            if not self.setup_build_environment(repo_path, project_type):
                result = {
                    'repo': repo_path.name,
                    'project_type': project_type,
                    'success': False,
                    'reason': 'Failed to setup build environment'
                }
                self.failed_builds.append(repo_path.name)
                return result
            
            # Run build
            result = self.run_build_commands(repo_path, project_type)
            
            if result['success']:
                self.successful_builds.append(repo_path.name)
            else:
                self.failed_builds.append(repo_path.name)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Unexpected error building {repo_path.name}: {e}")
            result = {
                'repo': repo_path.name,
                'project_type': 'unknown',
                'success': False,
                'reason': f'Unexpected error: {str(e)}'
            }
            self.failed_builds.append(repo_path.name)
            return result
    
    def build_all_repositories(self, repos: List[Path]) -> Dict:
        """Build all repositories"""
        logger.info(f"🏗️  Starting build process for {len(repos)} repositories...")
        start_time = time.time()
        
        if self.parallel and len(repos) > 1:
            logger.info(f"🔄 Using parallel build with {self.max_workers} workers")
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_repo = {executor.submit(self.build_repository, repo): repo for repo in repos}
                
                for future in concurrent.futures.as_completed(future_to_repo):
                    repo = future_to_repo[future]
                    try:
                        result = future.result()
                        self.build_results[repo.name] = result
                    except Exception as e:
                        logger.error(f"❌ Error in parallel build for {repo.name}: {e}")
                        self.build_results[repo.name] = {
                            'repo': repo.name,
                            'success': False,
                            'reason': f'Parallel execution error: {str(e)}'
                        }
        else:
            logger.info("🔄 Using sequential build")
            for repo in repos:
                result = self.build_repository(repo)
                self.build_results[repo.name] = result
        
        total_duration = time.time() - start_time
        
        summary = {
            'total_repos': len(repos),
            'successful': len(self.successful_builds),
            'failed': len(self.failed_builds),
            'skipped': len(self.skipped_builds),
            'total_duration': total_duration,
            'results': self.build_results
        }
        
        return summary
    
    def generate_build_report(self, summary: Dict):
        """Generate a comprehensive build report"""
        report_path = self.base_dir / 'build_report.md'
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("# TOZSolutions Build Report\n\n")
                f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total Duration:** {summary['total_duration']:.2f} seconds\n\n")
                
                # Summary
                f.write("## 📊 Build Summary\n\n")
                f.write(f"- **Total Repositories:** {summary['total_repos']}\n")
                f.write(f"- **✅ Successful:** {summary['successful']}\n")
                f.write(f"- **❌ Failed:** {summary['failed']}\n")
                f.write(f"- **⏭️ Skipped:** {summary['skipped']}\n")
                f.write(f"- **Success Rate:** {(summary['successful'] / summary['total_repos'] * 100):.1f}%\n\n")
                
                # Successful builds
                if self.successful_builds:
                    f.write("## ✅ Successful Builds\n\n")
                    for repo in self.successful_builds:
                        result = summary['results'][repo]
                        f.write(f"### {repo} ({result['project_type']})\n")
                        f.write(f"- **Duration:** {result.get('duration', 0):.2f}s\n")
                        f.write(f"- **Commands:** {len(result.get('commands', []))}\n\n")
                
                # Failed builds
                if self.failed_builds:
                    f.write("## ❌ Failed Builds\n\n")
                    for repo in self.failed_builds:
                        result = summary['results'][repo]
                        f.write(f"### {repo} ({result.get('project_type', 'unknown')})\n")
                        if 'reason' in result:
                            f.write(f"- **Reason:** {result['reason']}\n")
                        if 'errors' in result:
                            f.write("- **Errors:**\n")
                            for error in result['errors']:
                                f.write(f"  - {error}\n")
                        f.write("\n")
                
                # Skipped builds
                if self.skipped_builds:
                    f.write("## ⏭️ Skipped Builds\n\n")
                    for repo in self.skipped_builds:
                        result = summary['results'][repo]
                        f.write(f"- **{repo}:** {result.get('reason', 'Unknown reason')}\n")
                    f.write("\n")
                
                # Next steps
                f.write("## 🚀 Next Steps\n\n")
                if self.failed_builds:
                    f.write("1. Review failed builds and fix issues\n")
                    f.write("2. Check build logs for detailed error information\n")
                f.write("3. Deploy successful builds\n")
                f.write("4. Set up monitoring for deployed applications\n")
            
            logger.info(f"📊 Build report generated: {report_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to generate build report: {e}")
    
    def run(self):
        """Run the complete build process"""
        logger.info("🚀 Starting TOZSolutions build process...")
        
        # Discover repositories
        repos = self.discover_repositories()
        if not repos:
            logger.error("❌ No repositories found to build")
            return
        
        # Build all repositories
        summary = self.build_all_repositories(repos)
        
        # Generate report
        self.generate_build_report(summary)
        
        # Final summary
        logger.info("🎉 Build process completed!")
        logger.info(f"✅ Successful: {summary['successful']}")
        logger.info(f"❌ Failed: {summary['failed']}")
        logger.info(f"⏭️ Skipped: {summary['skipped']}")
        logger.info(f"⏱️  Total time: {summary['total_duration']:.2f}s")
        
        # Return exit code based on results
        if summary['failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Build all TOZSolutions repositories')
    parser.add_argument('--dir', default='./tozsolutions_repos', 
                       help='Base directory containing repositories')
    parser.add_argument('--sequential', action='store_true', 
                       help='Build repositories sequentially instead of parallel')
    parser.add_argument('--workers', type=int, default=4, 
                       help='Number of parallel workers (default: 4)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Verbose logging')
    parser.add_argument('--repo', action='append', 
                       help='Build specific repository (can be used multiple times)')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    builder = TOZSolutionsBuilder(
        base_dir=args.dir,
        parallel=not args.sequential,
        max_workers=args.workers
    )
    
    # If specific repositories are specified, filter them
    if args.repo:
        logger.info(f"🎯 Building specific repositories: {', '.join(args.repo)}")
        # This would require modifying the discover_repositories method
        # to filter based on the specified repositories
    
    builder.run()

if __name__ == "__main__":
    main()