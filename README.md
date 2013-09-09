# Google WMTS

使用 WMTS 协议访问 Google 底图

个人有这样的体验过程：

* 扫描纸质地图，然后配准矢量化
* 下载 Google Tile，拼接，再配准矢量化
* 下载 Google Tile，替换 ArcGIS Server Cache，ArcMap 加载 MapServer，不用配准了，矢量化
* 使用这个


其实还有其它办法，比如在 QGIS 中，通过 OpenLayers Plugin ...


## 使用场景

* 使用 ArcMap 加载 WMTS 协议的栅格底图，进行矢量化

## 使用方法

*使用前请确保你安装了 Python 以及 Tornado*

	python wmts.py
    