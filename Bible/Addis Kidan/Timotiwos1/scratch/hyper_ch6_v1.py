import fitz

doc = fitz.open(r"C:\Users\Abraham.sisay\Documents\Bible Assets\New testament\timotiwos1.pdf")
page = doc[5]
mat = fitz.Matrix(25, 25)

# Ch 6 heading down to end of page
clip = fitz.Rect(45, 680, 285, 750)
page.get_pixmap(matrix=mat, clip=clip).save(r"C:\Users\Abraham.sisay\Documents\Kidase\Bible\Addis Kidan\Timotiwos1\scratch\p06_hyper_ch6_v1.png")
print("Saved ch6 v1 hyper.")
