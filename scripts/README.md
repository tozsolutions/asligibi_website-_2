# 🚀 TOZSolutions Automation Scripts

Bu klasörde TOZSolutions organizasyonundaki tüm repository'leri otomatik olarak klonlayan ve build eden Python scriptleri bulunmaktadır.

## 📁 Dosyalar

- **`clone_all.py`** - Tüm repository'leri klonlar ve deployment yapılandırması yapar
- **`build_all.py`** - Tüm repository'leri build eder ve deploy eder
- **`main.js`** - Website için JavaScript dosyası

## 🔧 Gereksinimler

### Python Gereksinimleri
```bash
pip install requests pathlib
```

### Sistem Gereksinimleri
- **Git** - Repository klonlamak için
- **Node.js & npm** - JavaScript/HTML projeleri için
- **Python 3.8+** - Python projeleri için
- **Java & Maven** - Java projeleri için (opsiyonel)

## 📖 Kullanım Kılavuzu

### 1️⃣ Repository'leri Klonlama

```bash
# Basit kullanım
python scripts/clone_all.py

# GitHub token ile (daha fazla repository erişimi için)
python scripts/clone_all.py --token YOUR_GITHUB_TOKEN

# Özel dizin belirtme
python scripts/clone_all.py --dir ./my_repos

# Verbose logging
python scripts/clone_all.py --verbose
```

**Parametreler:**
- `--token`: GitHub Personal Access Token (opsiyonel)
- `--dir`: Repository'lerin klonlanacağı dizin (varsayılan: `./tozsolutions_repos`)
- `--verbose, -v`: Detaylı log çıktısı

**Çıktılar:**
- `clone_all.log`: Detaylı log dosyası
- `tozsolutions_repos/clone_summary.md`: Özet rapor

### 2️⃣ Tüm Projeleri Build Etme

```bash
# Basit kullanım (paralel build)
python scripts/build_all.py

# Sıralı build (daha güvenli)
python scripts/build_all.py --sequential

# Özel dizin ve worker sayısı
python scripts/build_all.py --dir ./my_repos --workers 2

# Belirli repository'leri build etme
python scripts/build_all.py --repo asligibi_website-_2 --repo another_repo

# Verbose logging
python scripts/build_all.py --verbose
```

**Parametreler:**
- `--dir`: Repository'lerin bulunduğu dizin (varsayılan: `./tozsolutions_repos`)
- `--sequential`: Paralel yerine sıralı build
- `--workers`: Paralel worker sayısı (varsayılan: 4)
- `--repo`: Sadece belirtilen repository'leri build et (tekrarlanabilir)
- `--verbose, -v`: Detaylı log çıktısı

**Çıktılar:**
- `build_all.log`: Detaylı log dosyası
- `tozsolutions_repos/build_report.md`: Build raporu

## 🔄 Tam İş Akışı

### Adım 1: Repository'leri Klonla
```bash
cd C:\Users\Admin\Documents\WEBX1\toz-netlify
python scripts/clone_all.py --verbose
```

### Adım 2: Tüm Projeleri Build Et
```bash
python scripts/build_all.py --verbose
```

### Adım 3: Sonuçları Kontrol Et
```bash
# Clone sonuçları
type tozsolutions_repos\clone_summary.md

# Build sonuçları
type tozsolutions_repos\build_report.md
```

## 🎯 Desteklenen Proje Türleri

### HTML/Static Sites
- **Gereksinimler**: `package.json`, `index.html`
- **Build**: `npm install` → `npm run build`
- **Çıktı**: `dist/` klasörü

### Node.js Projeleri
- **Gereksinimler**: `package.json`
- **Build**: `npm install` → `lint` → `test` → `build`
- **Çıktı**: `dist/` klasörü

### React Projeleri
- **Gereksinimler**: `package.json` + React dependencies
- **Build**: `npm install` → `lint` → `test` → `build`
- **Çıktı**: `build/` klasörü

### Vue.js Projeleri
- **Gereksinimler**: `package.json` + Vue dependencies
- **Build**: `npm install` → `lint` → `test` → `build`
- **Çıktı**: `dist/` klasörü

### Angular Projeleri
- **Gereksinimler**: `package.json` + Angular dependencies
- **Build**: `npm install` → `ng lint` → `ng test` → `ng build`
- **Çıktı**: `dist/` klasörü

### Python Projeleri
- **Gereksinimler**: `requirements.txt` veya `setup.py`
- **Build**: `pip install` → `pytest` → `python setup.py build`
- **Çıktı**: `build/` klasörü

### Java (Maven) Projeleri
- **Gereksinimler**: `pom.xml`
- **Build**: `mvn clean compile` → `mvn test` → `mvn package`
- **Çıktı**: `target/` klasörü

### Java (Gradle) Projeleri
- **Gereksinimler**: `build.gradle`
- **Build**: `./gradlew clean` → `./gradlew test` → `./gradlew build`
- **Çıktı**: `build/` klasörü

## 🛠️ Troubleshooting

### Yaygın Hatalar

#### 1. "No repositories found"
```bash
# Çözüm: GitHub token kullanın
export GITHUB_TOKEN=your_token_here
python scripts/clone_all.py
```

#### 2. "npm: command not found"
```bash
# Node.js kurulumunu kontrol edin
node --version
npm --version
```

#### 3. "Permission denied" (Git)
```bash
# SSH anahtarlarınızı kontrol edin
ssh -T git@github.com
```

#### 4. Build hatası
```bash
# Verbose mode ile detayları görün
python scripts/build_all.py --verbose

# Tek repository'yi test edin
python scripts/build_all.py --repo asligibi_website-_2 --verbose
```

### Log Dosyaları
- `clone_all.log` - Klonlama işlem logları
- `build_all.log` - Build işlem logları
- Her repository'nin kendi build logları

## 📊 Raporlar

### Clone Raporu (`clone_summary.md`)
- Başarılı klonlanan repository'ler
- Başarısız olan repository'ler
- Toplam istatistikler

### Build Raporu (`build_report.md`)
- Başarılı build'ler
- Başarısız build'ler
- Atlanan projeler
- Build süreleri
- Hata detayları

## 🚀 İleri Düzey Kullanım

### Özel Konfigürasyon
```python
# clone_all.py'yi özelleştirme
cloner = TOZSolutionsCloner(
    github_token="your_token",
    base_dir="./custom_repos"
)
```

### Paralel Build Optimizasyonu
```bash
# CPU çekirdeği sayısına göre worker ayarlayın
python scripts/build_all.py --workers 8
```

### Belirli Repository'leri Hedefleme
```bash
# Sadece web projeleri
python scripts/build_all.py --repo asligibi_website-_2 --repo another_website
```

## 🔐 Güvenlik

### GitHub Token
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token" tıklayın
3. `repo` yetkilerini verin
4. Token'ı environment variable olarak ayarlayın:
   ```bash
   export GITHUB_TOKEN=your_token_here
   ```

### Güvenli Saklama
```bash
# .env dosyası oluşturun (Git'e eklemeyin!)
echo "GITHUB_TOKEN=your_token_here" > .env
```

## 🤝 Katkıda Bulunma

1. Script'leri geliştirmek için pull request gönderin
2. Yeni proje türü desteği ekleyin
3. Bug raporları gönderin
4. Dokümantasyonu geliştirin

## 📞 Destek

- **Issues**: GitHub repository'sindeki issues bölümünü kullanın
- **Dokümantasyon**: Bu README dosyasını güncel tutun
- **Loglar**: Hata durumunda log dosyalarını paylaşın

---

**TOZSolutions Team** 🌟