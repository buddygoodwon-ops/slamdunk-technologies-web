# -*- coding: utf-8 -*-
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(HERE, "index.html")

txt = open(index_path, encoding="utf-8").read()

# Force pages.css to v7 for cache bust
txt = re.sub(r'pages\.css\\?v=\\d+', 'pages.css?v=7', txt)

open(index_path, "w", encoding="utf-8", newline="").write(txt)
print("index.html pages.css version updated to v7.")