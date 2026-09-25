import json
import zipfile
import xml.etree.ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def verify_file(doc_path, json_path):
    with zipfile.ZipFile(doc_path) as z:
        xml_content = z.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    raw_texts = [t.text for t in tree.findall('.//w:t', NS) if t.text]
    raw_total_chars = sum(len(t) for t in raw_texts)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    extracted_chars = 0
    for item in data:
        if item['type'] == 'paragraph':
            extracted_chars += len(item['text'])
        elif item['type'] == 'table':
            for row in item['rows']:
                for cell in row:
                    extracted_chars += len(cell)
                    
    print(f"File: {doc_path}")
    print(f"  Raw XML total characters: {raw_total_chars}")
    print(f"  Extracted JSON total characters: {extracted_chars}")
    print(f"  Character Match Ratio: {extracted_chars / raw_total_chars:.4%}")

if __name__ == '__main__':
    verify_file('_paper/2026 YK_Regional_Directory Draft.docx', '_site_data/regional_directory.json')
    verify_file('_paper/Yukon-Kuskokwim Delta Housing Resources Guide & Directory (YK Directory) Jan. 27 2026.docx', '_site_data/housing_guide.json')
