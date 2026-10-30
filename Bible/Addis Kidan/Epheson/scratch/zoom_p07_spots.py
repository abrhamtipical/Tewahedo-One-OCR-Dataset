import cv2

img = cv2.imread('scratch/p07_render.png')
h, w = img.shape[:2]

# 1. v7 & v8
cv2.imwrite('scratch/p07_v7_v8.png', img[int(h*0.14):int(h*0.22), :int(w*0.5)])

# 2. v10
cv2.imwrite('scratch/p07_v10.png', img[int(h*0.24):int(h*0.30), :int(w*0.5)])

# 3. v13
cv2.imwrite('scratch/p07_v13.png', img[int(h*0.32):int(h*0.38), :int(w*0.5)])

# 4. v16 & v17
cv2.imwrite('scratch/p07_v16_v17.png', img[int(h*0.42):int(h*0.52), :int(w*0.5)])

# 5. v18 & v19
cv2.imwrite('scratch/p07_v18_v19.png', img[int(h*0.51):int(h*0.62), :int(w*0.5)])

# 6. Sec 8 + v21, v22, v25
cv2.imwrite('scratch/p07_sec8_v21_v25.png', img[int(h*0.62):int(h*0.85), :int(w*0.5)])

print("P07 spots saved.")
