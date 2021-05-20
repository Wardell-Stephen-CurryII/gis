

XMin = 12945527.988958586
XMax = 12950114.210656324
YMin = 4864452.477985988
YMax = 4864911.100155763

x_one = (XMax-XMin)/30
y_one = (YMax-YMin)/3
print(x_one)
print(y_one)

x_gis = XMin + x_one*(229/256 + 22)
y_gis = YMin + y_one*((256-22)/256 + 2)
print(x_gis)
print(y_gis)