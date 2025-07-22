# 🌟 Aslı Gibi Website

Modern, professional, and responsive website built with cutting-edge web technologies.

![Website Preview](https://via.placeholder.com/800x400/0d6efd/ffffff?text=Aslı+Gibi+Website)

## 🚀 Live Demo

- **Production (GitHub Pages)**: [https://tozsolutions.github.io/asligibi_website-_2](https://tozsolutions.github.io/asligibi_website-_2)
- **Staging (Vercel)**: Available when configured
- **Development (Netlify)**: Available when configured

## ✨ Features

- 🎨 **Modern Design** - Clean, professional, and visually appealing
- 📱 **Fully Responsive** - Perfect on all devices and screen sizes
- ⚡ **Fast Performance** - Optimized for speed and SEO
- 🎯 **User-Friendly** - Intuitive navigation and smooth interactions
- 🛡️ **Secure** - Built with security best practices
- ♿ **Accessible** - WCAG compliant for all users
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 🔄 **Auto Deployment** - CI/CD pipeline with GitHub Actions

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **Fonts**: Google Fonts (Inter)
- **Build Tools**: npm, Terser, CleanCSS
- **Testing**: Jest, JSDOM
- **Linting**: ESLint, Prettier, Stylelint
- **Deployment**: GitHub Actions, Vercel, Netlify, GitHub Pages

## 📋 Prerequisites

- Node.js (v16 or higher)
- npm (v8 or higher)
- Git

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/tozsolutions/asligibi_website-_2.git
   cd asligibi_website-_2
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

## 📁 Project Structure

```
asligibi_website-_2/
├── 📄 index.html              # Main HTML file
├── 📁 styles/
│   └── 📄 main.css           # Main stylesheet
├── 📁 scripts/
│   └── 📄 main.js            # Main JavaScript file
├── 📁 assets/
│   └── 📄 favicon.ico        # Favicon
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 deploy.yml     # CI/CD pipeline
├── 📄 package.json           # Dependencies and scripts
├── 📄 .gitignore            # Git ignore rules
└── 📄 README.md             # This file
```

## 🔧 Available Scripts

### Development
- `npm start` - Start development server
- `npm run dev` - Same as start
- `npm run format` - Format code with Prettier
- `npm run lint` - Lint JavaScript files
- `npm run lint:fix` - Fix linting issues

### Building
- `npm run build` - Build for production
- `npm run clean` - Clean build directory
- `npm run serve:prod` - Serve production build

### Testing & Validation
- `npm test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage
- `npm run validate-html` - Validate HTML
- `npm run validate-css` - Validate CSS

### Deployment
- `npm run deploy:vercel` - Deploy to Vercel
- `npm run deploy:netlify` - Deploy to Netlify
- `npm run deploy:github` - Deploy to GitHub Pages

## 🚀 Deployment

### Automatic Deployment

The project uses GitHub Actions for automatic deployment:

1. **GitHub Pages** - Automatically deployed on push to main branch
2. **Vercel** - Deployed when Vercel secrets are configured
3. **Netlify** - Deployed when Netlify secrets are configured

### Manual Deployment

#### GitHub Pages
```bash
npm run build
npm run deploy:github
```

#### Vercel
```bash
npm install -g vercel
vercel login
npm run deploy:vercel
```

#### Netlify
```bash
npm install -g netlify-cli
netlify login
npm run deploy:netlify
```

## 🔐 Environment Variables

For deployment, you may need to set these secrets in GitHub:

### Vercel
- `VERCEL_TOKEN` - Vercel authentication token
- `VERCEL_ORG_ID` - Vercel organization ID
- `VERCEL_PROJECT_ID` - Vercel project ID

### Netlify
- `NETLIFY_AUTH_TOKEN` - Netlify authentication token
- `NETLIFY_SITE_ID` - Netlify site ID

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

## 📊 Performance

The website is optimized for performance:

- ⚡ Minified CSS and JavaScript
- 🖼️ Optimized images with lazy loading
- 📦 Efficient bundling and compression
- 🔄 Service worker for caching
- 📱 Mobile-first responsive design

## ♿ Accessibility

- ✅ WCAG 2.1 AA compliant
- ⌨️ Full keyboard navigation support
- 🔊 Screen reader friendly
- 🎨 High contrast mode support
- 🎯 Focus indicators and skip links

## 🌐 Browser Support

- ✅ Chrome (last 2 versions)
- ✅ Firefox (last 2 versions)
- ✅ Safari (last 2 versions)
- ✅ Edge (last 2 versions)
- ✅ Mobile browsers

## 🎨 Customization

### Colors
Edit CSS custom properties in `styles/main.css`:

```css
:root {
  --primary-color: #0d6efd;
  --secondary-color: #6c757d;
  /* ... other colors */
}
```

### Fonts
Change the font family in `styles/main.css`:

```css
:root {
  --font-family-primary: 'Inter', sans-serif;
}
```

### Content
Edit the content in `index.html` and update the corresponding sections.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **TOZSolutions** - Development Team

## 📞 Support

For support and questions:

- 📧 Email: info@tozsolutions.com
- 🌐 Website: [https://tozsolutions.com](https://tozsolutions.com)
- 📱 GitHub Issues: [Create an issue](https://github.com/tozsolutions/asligibi_website-_2/issues)

## 🙏 Acknowledgments

- Bootstrap team for the amazing framework
- Font Awesome for the beautiful icons
- Google Fonts for the typography
- All open source contributors

---

<div align="center">
  <p>Made with ❤️ by <strong>TOZSolutions</strong></p>
  <p>⭐ Star this repository if you found it helpful!</p>
</div>
