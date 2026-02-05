# 🦖 Chrome Dino Game AI Bot (YOLOv11)

An autonomous bot that plays the Chrome Dinosaur Game using real-time object detection. Powered by **YOLOv11**, **MSS** (for high-speed screen capture), and **Roboflow**.

![Status](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![YOLO](https://img.shields.io/badge/Model-YOLOv11n-orange)

## 🚀 Features
- **Real-time Object Detection:** Detects Cacti, Birds, and the Dino using YOLOv11 Nano.
- **High Performance:** Uses `mss` for screen capture (>60 FPS on RTX 4060).
- **Smart Logic:** Calculates distance between Dino and obstacles to trigger jumps or ducks.
- **Local Training:** Custom dataset trained on Roboflow and exported for local GPU inference.

## 🛠️ Tech Stack
- **Python 3.9+**
- **Ultralytics YOLOv11** (Object Detection)
- **MSS** (Screen Capture)
- **PyAutoGUI** (Keyboard Control)
- **OpenCV** (Image Processing)
- **Roboflow** (Dataset Management)

---

## 📋 Ön Koşullar

- Python 3.9 veya daha yüksek
- pip (Python paket yöneticisi)
- macOS, Linux veya Windows
- GPU (opsiyonel, CPU ile de çalışır)

---

## ⚙️ Kurulum

### 1. Projeyi Klonlayın

```bash
git clone <repository-url>
cd dinasour\ game\ beater
```

### 2. Sanal Ortam Oluşturun (İsteğe Bağlı Ama Önerilir)

```bash
# Python sanal ortam oluştur
python3 -m venv venv

# Sanal ortamı etkinleştir
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Kütüphaneleri Kurun

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Gerekli Kütüphaneler:**
- `ultralytics` - YOLOv11 modeli
- `mss` - Ekran görüntüsü alma
- `opencv-python` - Görüntü işleme
- `pyautogui` - Klavye kontrolü
- `roboflow` - Dataset yönetimi
- `numpy` - Sayısal işlemler
- `python-dotenv` - Ortam değişkenleri

---

## 🎓 Modeli Eğitme

### Dataset Hazırlığı

Dataset zaten `dataset/` klasöründe bulunmaktadır ve Roboflow üzerinde yönetilmektedir.

```bash
# (Opsiyonel) Dataset'i Roboflow'dan indirmek için
python get_dataset.py
```

### Eğitim Komutu

Aşağıdaki komut ile YOLOv11 modelini eğitebilirsiniz:

```bash
yolo detect train \
  data=dataset/data.yaml \
  model=yolo11n.pt \
  epochs=50 \
  imgsz=640 \
  device=mps
```

**Komut Parametreleri:**
- `data=dataset/data.yaml` - Dataset konfigürasyon dosyası
- `model=yolo11n.pt` - Kullanılan model (nano sürümü)
- `epochs=50` - Eğitim dönem sayısı
- `imgsz=640` - Giriş görüntü boyutu
- `device=mps` - Apple Silicon GPU kullanımı (Intel GPU: `0`, CPU: `cpu`)

**Cihazınız için device parametresi:**
- Apple Silicon (M1/M2/M3): `device=mps`
- NVIDIA GPU: `device=0` (veya GPU index numarası)
- CPU: `device=cpu`

Eğitim tamamlandığında model `runs/detect/train/weights/best.pt` klasöründe kaydedilir.

---

## 🎮 Uygulamayı Başlatın

### Main Script'i Çalıştırın

```bash
python main.py
```

**Kullanım:**
1. Chrome veya Brave tarayıcısında Dino oyununu açın
2. Script'i başlatın
3. Bot otomatik olarak oyunu oynayacaktır

### Screen Processing (Ayarlamalar İçin)

Ekran işleme parametrelerini test etmek için:

```bash
python screen_processing.py
```

---

## 📁 Proje Yapısı

```
dinasour game beater/
├── README.md                 # Bu dosya
├── requirements.txt          # Python bağımlılıkları
├── main.py                   # Ana oyun bot scripti
├── screen_processing.py      # Ekran görüntüsü işleme
├── get_dataset.py           # Roboflow dataset indirme
├── training_command.txt      # Eğitim komutları referansı
├── .env                      # Ortam değişkenleri (git ignore)
├── .env.example              # Örnek ortam değişkenleri
└── dataset/                  # Dataset dosyaları
    ├── data.yaml             # Dataset konfigürasyonu
    ├── train/                # Eğitim görüntüleri
    └── val/                  # Doğrulama görüntüleri
```

---

## 🔧 Sorun Giderme

### `ModuleNotFoundError: No module named 'ultralytics'`
```bash
pip install ultralytics
```

### `ModuleNotFoundError: No module named 'mss'`
```bash
pip install mss
```

### GPU Tanıması Sorunu
```bash
# Doğru device parametresini belirleyin
yolo detect train ... device=cpu  # CPU'da eğitin
```

### Bot Oyunu Oynamıyor
- Chrome DevTools açılı mı kontrol edin
- Oyun penceresinin en üstte olduğundan emin olun
- `screen_processing.py` ile ekran görüntülemesini test edin

---

## 📝 Lisans

Bu proje açık kaynaklıdır. Detaylar için LICENSE dosyasına bakınız.

---

## 💡 İpuçları

- Sanal ortam kullanmak bağımlılık çakışmalarını önler
- GPU ile eğitim, CPU ile eğitimden **50-100x daha hızlıdır**
- Dataset'i düzenli olarak güncelleyin
- Oyun parametreleri değişirse `screen_processing.py`'de ayarlamalar yapın
