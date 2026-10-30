import cv2

img = cv2.imread('scratch/p06_render.png')
h, w = img.shape[:2]

# 1. v22: line 10
cv2.imwrite('scratch/p06_v22.png', img[int(h*0.25):int(h*0.32), :int(w*0.5)])

# 2. v24: line 13-14
cv2.imwrite('scratch/p06_v24.png', img[int(h*0.31):int(h*0.38), :int(w*0.5)])

# 3. v28: line 20
cv2.imwrite('scratch/p06_v28.png', img[int(h*0.44):int(h*0.52), :int(w*0.5)])

# 4. v29: line 23
cv2.imwrite('scratch/p06_v29.png', img[int(h*0.50):int(h*0.58), :int(w*0.5)])

# 5. v30: line 25
cv2.imwrite('scratch/p06_v30.png', img[int(h*0.54):int(h*0.62), :int(w*0.5)])

# 6. Ch 5 Section 7 heading + v1
cv2.imwrite('scratch/p06_sec7.png', img[int(h*0.68):int(h*0.78), :int(w*0.5)])

# 7. Ch 5 v4 and v5
cv2.imwrite('scratch/p06_ch5_v4_v5.png', img[int(h*0.84):, :int(w*0.5)])

print("P06 spots saved.")
