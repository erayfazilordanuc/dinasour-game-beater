import cv2
import numpy as np
import time
from mss import mss
from ultralytics import YOLO

# --- AYARLAR ---
# Ekranın neresini yakalayacağız? (Simülasyon pencerenin boyutuna göre ayarla)
# Örn: Sol üstten başla, 640x480'lik bir alanı al.
monitor = {"top": 100, "left": 100, "width": 640, "height": 480}

# YOLO Modelini Yükle
model = YOLO("yolov8n.pt") # Veya kendi eğittiğin "best.pt"

def main():
    # mss nesnesini başlat (Ekran yakalayıcı)
    sct = mss()
    
    pTime = 0

    print("Ekran yakalama başladı... Çıkmak için 'q' bas.")

    while True:
        # 1. EKRAN GÖRÜNTÜSÜNÜ AL (En kritik kısım)
        # sct.grab bize ham veri döner, bunu numpy dizisine çeviriyoruz.
        screenshot = np.array(sct.grab(monitor))

        # 2. RENK DÜZELTMESİ (ÖNEMLİ!)
        # mss görüntüyü BGRA (Blue-Green-Red-Alpha) olarak verir.
        # OpenCV ve YOLO ise BGR kullanır. Alpha (Şeffaflık) kanalını atmalıyız.
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        # --- BURADAN SONRASI SENİN KLASİK PERCEPTION KODUN ---
        
        # FPS Hesabı
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # YOLO ile Tanıma
        results = model(frame, stream=True, verbose=False, conf=0.5)

        for r in results:
            # Kutuları çiz (YOLO'nun kendi çizim fonksiyonu)
            # İstersen burada kendi "Duba" mantığını kurabilirsin.
            frame = r.plot()

        # FPS Yaz
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)

        # Görüntüyü Göster
        cv2.imshow("Screen Perception (Sim)", frame)

        # Çıkış
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()