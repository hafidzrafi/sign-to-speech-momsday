import cv2
from cvzone.ClassificationModule import Classifier
import pygame
import os

# --- 1. SETUP AUDIO ---
pygame.mixer.init()

def play_sound(file_name):
    path = os.path.join("audio", file_name)
    # Gunakan path absolut agar lebih aman
    full_path = os.path.abspath(path)
    
    if os.path.exists(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            print(f"MEMUTAR: {file_name}")
        except Exception as e:
            print(f"❌ Error Pygame: {e}")
    else:
        print(f"⚠️ File tidak ditemukan di: {full_path}")

# --- 2. SETUP AI & KAMERA ---
# Gunakan ID 1 atau 2 sesuai DroidCam (sesuaikan jika perlu)
cap = cv2.VideoCapture(1) 

classifier = Classifier("keras_model.h5", "labels.txt")

# --- 3. MEMBACA LABELS DENGAN BENAR ---
# Kita perlu membuang angka di depan (misal: "0 Netral" menjadi "Netral")
class_names = []
try:
    with open("labels.txt", "r") as f:
        for line in f.readlines():
            # Hapus spasi kiri/kanan, lalu pisahkan berdasarkan spasi
            parts = line.strip().split(" ")
            if len(parts) > 1:
                # Ambil kata kedua sampai akhir (gabungkan jika ada spasi di nama label)
                label_name = " ".join(parts[1:]) 
                class_names.append(label_name)
            else:
                class_names.append(line.strip())
    print(f"Label dimuat: {class_names}") 
    # Hasilnya harusnya: ['Netral', 'Happy', 'Moms', 'Day', 'ILoveYou', 'Mom']
except Exception as e:
    print(f"❌ Gagal membaca labels.txt: {e}")

# --- 4. PEMETAAN AUDIO (Gunakan .wav!) ---
# Pastikan nama Key (kiri) SAMA PERSIS dengan hasil print label di atas
audio_map = {
    "Happy": "Happy.wav",      # GANTI .m4a jadi .wav
    "Mom": "Mom.wav", 
    "Moms": "Moms.wav",
    "Day": "Day.wav",
    "ILoveYou": "ILoveYou.wav"
    # "Netral" tidak perlu dimasukkan karena kita tidak mau ada suara saat diam
}

last_gesture = ""

print("Program berjalan... Tekan 'q' untuk keluar.")

# --- 5. LOOP UTAMA ---
while True:
    success, img = cap.read()
    if not success:
        print("Kamera tidak terdeteksi! Cek DroidCam.")
        break
    
    # Angka 1 artinya flip horizontal (kiri jadi kanan, kanan jadi kiri)
    img = cv2.flip(img, 1)  

    img_predict = img.copy()
    
    # Prediksi
    prediction, index = classifier.getPrediction(img_predict, draw=False)
    
    # Ambil nama label
    if index < len(class_names):
        current_gesture = class_names[index]
    else:
        current_gesture = "Unknown"
        
    confidence = prediction[index]

    text_info = f"{current_gesture} ({int(confidence*100)}%)"
    cv2.putText(img, text_info, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    if current_gesture != last_gesture:
        if confidence > 0.8:
            if current_gesture in audio_map:
                print(f"Terdeteksi: {current_gesture} -> putar {audio_map[current_gesture]}")
                play_sound(audio_map[current_gesture])
                last_gesture = current_gesture
            elif current_gesture == "Netral":
                last_gesture = current_gesture
            else:
                print(f"Label '{current_gesture}' terdeteksi tapi tidak ada di audio_map.")
                last_gesture = current_gesture

    cv2.imshow("Happy Mothers Day", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()