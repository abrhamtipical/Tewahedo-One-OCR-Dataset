import cv2, os

scratch = r'C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Filipisius\scratch'
lines_dir = os.path.join(scratch, 'p06_lines')

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

inspect_lines([14, 15, 16, 17, 18], 'p06_zoom_14_18.png')
inspect_lines([24, 25, 26, 27, 28], 'p06_zoom_24_28.png')
inspect_lines([32, 33, 34, 35, 36], 'p06_zoom_32_36.png')
inspect_lines([38, 39, 40, 41, 42, 43], 'p06_zoom_38_43.png')
