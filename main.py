import cv2
import numpy as np
import time
from mss import mss
from ultralytics import YOLO
import pyautogui
import pygetwindow as gw
import subprocess
import os

# --- EKRAN AYARLARI ---
monitor = {"top": 200, "left": 50, "width": 640, "height": 350}

model = YOLO(r'runs/detect/dino_v1/weights/best.pt')

def find_chrome_path():
    """Bilgisayardaki Chrome.exe'nin yerini bulur"""
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe"
    ]
    for path in paths:
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path):
            return expanded_path
    return None

def open_and_arrange_windows():
    print("🔍 Oyun ortamı hazırlanıyor...")
    
    TARGET_URL = "https://dinosaur-game.io/"
    
    target_window = None
    possible_titles = ['Dinosaur Game', 'Play Chrome Dino', 'T-Rex Dinosaur']
    
    for title in possible_titles:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            target_window = windows[0]
            print(f"✅ Oyun zaten açık: {target_window.title}")
            break
    
    if not target_window:
        chrome_path = find_chrome_path()
        if chrome_path:
            print(f"🚀 Site açılıyor: {TARGET_URL}")
            subprocess.Popen([chrome_path, TARGET_URL])
        else:
            import webbrowser
            webbrowser.open(TARGET_URL)
        
        print("⏳ Sayfa yükleniyor...")
        time.sleep(5) 
        target_window = gw.getActiveWindow()

    # CHROME'U SOLA YASLA
    if target_window:
        try:
            if not target_window.isMinimized:
                target_window.minimize()
                time.sleep(0.2)
            target_window.restore()
            target_window.activate()
            time.sleep(0.5)
            
            # SOL TARAFA YERLEŞTİR
            target_window.moveTo(0, 0)
            target_window.resizeTo(960, 1080) 
            
            print("✅ Chrome SOLA yaslandı.")
            pyautogui.click(400, 500) 
            
        except Exception as e:
            print(f"⚠️ Pencere ayarında pürüz: {e}")

def main():
    open_and_arrange_windows()

    sct = mss()
    pTime = 0
    print("Ekran yakalama başladı... Çıkmak için 'q' bas.")

    game_ready = False 
    cv2_window_name = "AI Vision (Debug)"

    # --- PENCERE BOYUTLANDIRMA (ORANTILI) ---
    cv2.namedWindow(cv2_window_name, cv2.WINDOW_NORMAL)
    
    # Orijinal boyutları al
    orig_w = monitor["width"]
    orig_h = monitor["height"]
    
    # Ölçekleme Faktörü (1.0 = Orijinal, 1.5 = %50 Büyüt)
    # 1.3 yaparak biraz büyüttük ama oranı bozmadık.
    SCALE = 1.3 
    
    new_w = int(orig_w * SCALE)
    new_h = int(orig_h * SCALE)
    
    # Yeni boyutları uygula (Böylece görüntü yayvanlaşmaz)
    cv2.resizeWindow(cv2_window_name, new_w, new_h)
    
    # Pencereyi ekranın sağına, biraz aşağıya koy (Chrome'un yanına)
    cv2.moveWindow(cv2_window_name, 970, 50)

    # --- OYUN MANTIĞI ---
    NORMAL_JUMP_DIST = 168 
    WIDE_OBSTACLE_WIDTH = 75   
    LATE_JUMP_DIST = 160
    BIRD_JUMP_DIST = 200
    GAP_THRESHOLD = 150        
    EARLY_JUMP_DIST = 180 

    while True:
        screenshot = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        results = model(frame, stream=True, verbose=False, conf=0.5)

        cacti = [] 
        birds = []
        dino_x = 0 

        for r in results:
            frame = r.plot()
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls_id = int(box.cls[0].item())
                name = r.names[cls_id]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                if name == "dinosaur":
                    dino_x = x2 
                    if not game_ready:
                        game_ready = True
                        pyautogui.press('space')
                
                elif name == "cactus":
                    width = x2 - x1
                    cacti.append({'x1': x1, 'x2': x2, 'w': width})
                
                elif name == "bird":
                    birds.append({'x1': x1, 'y1': y1})

        if game_ready:
            cacti.sort(key=lambda c: c['x1'])

            if len(cacti) > 0:
                closest = cacti[0]     
                dist = closest['x1']   

                trigger_point = NORMAL_JUMP_DIST
                jump_reason = "Normal"
                should_long_press = False

                if len(cacti) > 1:
                    second_cactus = cacti[1]
                    gap = second_cactus['x1'] - closest['x2']
                    if gap < GAP_THRESHOLD:
                        trigger_point = EARLY_JUMP_DIST 
                        jump_reason = "Seri Engel"
                        # should_long_press = True 
                
                elif closest['w'] > WIDE_OBSTACLE_WIDTH:
                    trigger_point = LATE_JUMP_DIST 
                    jump_reason = "Genis (3'lu)"

                cv2.putText(frame, f"Kaktus Hedef: <{trigger_point}px", (100, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                if dist < trigger_point:
                    if should_long_press:
                        pyautogui.keyDown('space')
                        time.sleep(0.12) 
                        pyautogui.keyUp('space')
                    else:
                        pyautogui.press('space')
                    print(f"ZIPLAMA: {jump_reason} | Mesafe: {dist} | Uzun Basma: {should_long_press}")

            for bird in birds:
                if bird['x1'] < BIRD_JUMP_DIST:
                    if bird['y1'] < 90:
                        pyautogui.press('down')
                        print(f"EGIL: Alcak Kus (y={bird['y1']})")
                    else:
                         pyautogui.press('space')
                         print(f"ZIPLA: Yuksek Kus (y={bird['y1']})")

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # --- PENCERE YÖNETİMİ ---
        cv2.imshow(cv2_window_name, frame)
        cv2.setWindowProperty(cv2_window_name, cv2.WND_PROP_TOPMOST, 1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()