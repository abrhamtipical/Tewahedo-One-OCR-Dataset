import cv2, os

scratch = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Filipisius\scratch'
lines_dir = os.path.join(scratch, 'p05_lines')

def inspect_lines(line_nums, out_name):
    imgs = []
    for num in line_nums:
        fpath = os.path.join(lines_dir, f'line_{num:02d}.png')
        if os.path.exists(fpath):
            img = cv2.imread(fpath)
            h, w = img.shape[:2]
            zoomed = cv2.resize(img, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
            imgs.append(zoomed)
    if imgs:
        max_w = max(im.shape[1] for im in imgs)
        padded = []
        for im in imgs:
            h, w = im.shape[:2]
            pad_img = cv2.copyMakeBorder(im, 4, 4, 0, max_w - w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            padded.append(pad_img)
        stacked = cv2.vconcat(padded)
        cv2.imwrite(os.path.join(scratch, out_name), stacked)
        print(f"Saved {out_name}")

inspect_lines([9, 10, 11], 'p05_zoom_09_11.png')
inspect_lines([16, 17, 18], 'p05_zoom_16_18.png')
inspect_lines([20, 21, 22], 'p05_zoom_20_22.png')
inspect_lines([27, 28, 29], 'p05_zoom_27_29.png')
inspect_lines([33, 34, 35], 'p05_zoom_33_35.png')
