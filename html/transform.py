from lxml import etree
import glob
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XML_DIR = os.path.join(BASE_DIR, "xml")
OUT_DIR = os.path.join(BASE_DIR, "output")
XSL_PATH = os.path.join(BASE_DIR, "transform.xsl")


xsl_doc = etree.parse(XSL_PATH)
transform = etree.XSLT(xsl_doc)


os.makedirs(OUT_DIR, exist_ok=True)


all_content = ""


xml_files = sorted(glob.glob(os.path.join(XML_DIR, "*.xml")))

for xml_path in xml_files:
    xml_doc = etree.parse(xml_path)

    html_fragment = transform(xml_doc)
  
    all_content += str(html_fragment)


final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Virginia Woolf Collection</title>
    <style>
        body {{ font-family: Georgia, serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #003366; }}
        h2 {{ margin-top: 1.5em; }}
        section.tei-item {{ border-bottom: 2px solid #ccc; padding-bottom: 2em; margin-bottom: 2em; }}
        .meta {{ color: #666; font-size: 0.9em; margin-bottom: 1.5em; }}
    </style>
</head>
<body>
    <h1>Virginia Woolf Digital Collection</h1>
    {all_content}
</body>
</html>
"""


out_path = os.path.join(OUT_DIR, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"🎉 All XML files merged into {out_path}")
