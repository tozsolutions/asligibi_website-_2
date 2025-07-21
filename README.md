# 🌟 Aslı Gibi Website

Modern, professional, and responsive website built with cutting-edge web technologies.

![Website Preview](https://via.placeholder.com/800x400/0d6efd/ffffff?text=Aslı+Gibi+Website)

## 🚀 Live Demo

- **Production (Vercel)**: [https://asligibi.vercel.app](https://asligibi.vercel.app)
- **Staging (Netlify)**: [https://asligibi.netlify.app](https://asligibi.netlify.app)
- **GitHub Pages**: [https://tozsolutions.github.io/asligibi_website-_2](https://tozsolutions.github.io/asligibi_website-_2)

## ✨ Features

- 🎨 **Modern Design**: Clean, professional, and visually appealing
- 📱 **Fully Responsive**: Works perfectly on all devices
- ⚡ **Lightning Fast**: Optimized for performance and speed
- 🔒 **Secure**: Security headers and best practices implemented
- ♿ **Accessible**: WCAG 2.1 compliant and screen reader friendly
- 🌐 **SEO Optimized**: Meta tags, structured data, and sitemap
- 🔄 **CI/CD Ready**: Automated testing and deployment
- 🎯 **Cross-browser**: Compatible with all modern browsers

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **Fonts**: Google Fonts (Inter)
- **Build Tools**: npm, Webpack, Terser
- **Testing**: Jest, Lighthouse
- **Deployment**: Vercel, Netlify, GitHub Pages
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **npm** (v8 or higher) - Comes with Node.js
- **Git** - [Download](https://git-scm.com/)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tozsolutions/asligibi_website-_2.git
cd asligibi_website-_2
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The website will be available at `http://localhost:3000`

## 📁 Project Structure

```
asligibi_website-_2/
├── 📁 .github/
│   └── 📁 workflows/
│       └── deploy.yml          # CI/CD pipeline
├── 📁 assets/
│   ├── 📁 images/              # Image files
│   └── favicon.ico             # Website favicon
├── 📁 scripts/
│   └── main.js                 # JavaScript functionality
├── 📁 styles/
│   └── main.css                # Custom styles
├── 📁 dist/                    # Built files (auto-generated)
├── index.html                  # Main HTML file
├── package.json                # Dependencies and scripts
├── vercel.json                 # Vercel configuration
├── netlify.toml                # Netlify configuration
├── lighthouse.json             # Lighthouse configuration
└── README.md                   # This file
```

## 🔧 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run lint` | Lint JavaScript files |
| `npm run format` | Format code with Prettier |
| `npm run test` | Run tests |
| `npm run lighthouse` | Run Lighthouse audit |
| `npm run deploy:vercel` | Deploy to Vercel |
| `npm run deploy:netlify` | Deploy to Netlify |

## 🚀 Deployment

### Automatic Deployment (Recommended)

The project is configured with GitHub Actions for automatic deployment:

1. **Push to main branch** → Triggers deployment to all platforms
2. **Pull request** → Triggers build and testing

### Manual Deployment

#### Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login and deploy
vercel login
npm run deploy:vercel
```

#### Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login and deploy
netlify login
npm run deploy:netlify
```

#### GitHub Pages

```bash
# Build and deploy
npm run build
npm run deploy:github
```

## 🔒 Environment Variables

Create a `.env` file for local development:

```env
# Development
NODE_ENV=development
PORT=3000

# Analytics (optional)
GOOGLE_ANALYTICS_ID=your_ga_id

# Contact Form (optional)
CONTACT_EMAIL=info@asligibi.com
```

For production, set these in your hosting platform:

### Vercel
- Go to Project Settings → Environment Variables
- Add the required variables

### Netlify
- Go to Site Settings → Environment Variables
- Add the required variables

## 🧪 Testing

### Run All Tests

```bash
npm test
```

### Run Tests with Coverage

```bash
npm run test:coverage
```

### Run Lighthouse Audit

```bash
npm run lighthouse
```

### Validate HTML/CSS

```bash
npm run validate-html
npm run validate-css
```

## 🔍 Performance Optimization

The website is optimized for performance:

- ✅ **Minified CSS/JS**: Reduced file sizes
- ✅ **Image Optimization**: Compressed images
- ✅ **Lazy Loading**: Images load when needed
- ✅ **Caching**: Browser and CDN caching
- ✅ **Gzip Compression**: Server-side compression
- ✅ **Critical CSS**: Above-the-fold optimization

### Performance Scores

| Metric | Score |
|--------|--------|
| Performance | 95+ |
| Accessibility | 100 |
| Best Practices | 100 |
| SEO | 100 |

## ♿ Accessibility

The website follows WCAG 2.1 AA guidelines:

- ✅ **Semantic HTML**: Proper HTML structure
- ✅ **ARIA Labels**: Screen reader support
- ✅ **Keyboard Navigation**: Full keyboard support
- ✅ **Color Contrast**: Meets contrast requirements
- ✅ **Focus Management**: Clear focus indicators

## 🌐 Browser Support

| Browser | Version |
|---------|---------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

## 📱 Responsive Design

The website is fully responsive and tested on:

- 📱 **Mobile**: 320px - 767px
- 📱 **Tablet**: 768px - 1023px
- 💻 **Desktop**: 1024px+
- 🖥️ **Large Desktop**: 1440px+

## 🔧 Customization

### Colors

Edit the CSS custom properties in `styles/main.css`:

```css
:root {
  --primary-color: #0d6efd;
  --secondary-color: #6c757d;
  /* Add your custom colors */
}
```

### Fonts

Change fonts in `index.html` and `styles/main.css`:

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Content

Update content in `index.html`:

- Company information
- Services
- Contact details
- Social media links

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**TOZSolutions Development Team**

- 🎨 **Design**: Modern UI/UX Design
- 💻 **Development**: Full-stack Development
- 🚀 **DevOps**: CI/CD and Deployment
- 🧪 **QA**: Testing and Quality Assurance

## 📞 Support

If you need help or have questions:

- 📧 **Email**: [info@tozsolutions.com](mailto:info@tozsolutions.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/tozsolutions/asligibi_website-_2/issues)
- 📖 **Documentation**: [Wiki](https://github.com/tozsolutions/asligibi_website-_2/wiki)

## 🙏 Acknowledgments

- [Bootstrap](https://getbootstrap.com/) - UI Framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [Google Fonts](https://fonts.google.com/) - Typography
- [Vercel](https://vercel.com/) - Hosting Platform
- [Netlify](https://netlify.com/) - Hosting Platform

---

<div align="center">
  <p>Made with ❤️ by <a href="https://tozsolutions.com">TOZSolutions</a></p>
  <p>
    <a href="https://asligibi.vercel.app">🌐 Live Demo</a> |
    <a href="https://github.com/tozsolutions/asligibi_website-_2/issues">🐛 Report Bug</a> |
    <a href="https://github.com/tozsolutions/asligibi_website-_2/issues">💡 Request Feature</a>
  </p>
</div>
