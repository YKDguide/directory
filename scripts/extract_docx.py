import zipfile
import xml.etree.ElementTree as ET
import json
import os

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def parse_paragraph_node(p_elem):
    parts = []
    for elem in p_elem.iter():
        tag = elem.tag.split('}')[-1]
        if tag == 't' and elem.text:
            parts.append(elem.text)
        elif tag == 'tab':
            parts.append('\t')
    full_text = ''.join(parts)
    
    # If this paragraph is a TOC entry formatted as "Title\tPageNum"
    if '\t' in full_text:
        title, _, pagenum = full_text.rpartition('\t')
        if pagenum.strip().isdigit():
            full_text = title.strip()
            
    return full_text.strip()

def extract_all_elements(elem, elements_list):
    tag = elem.tag.split('}')[-1]
    if tag == 'p':
        full_text = parse_paragraph_node(elem)
        if full_text:
            pPr = elem.find('w:pPr', NS)
            pStyle = pPr.find('w:pStyle', NS) if pPr is not None else None
            style_val = pStyle.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if pStyle is not None else None
            elements_list.append({
                'type': 'paragraph',
                'style': style_val,
                'text': full_text
            })
    elif tag == 'tbl':
        rows = []
        for r in elem.findall('.//w:tr', NS):
            row = []
            for c in r.findall('.//w:tc', NS):
                c_texts = [t.text for t in c.findall('.//w:t', NS) if t.text]
                row.append(''.join(c_texts))
            rows.append(row)
        elements_list.append({
            'type': 'table',
            'rows': rows
        })
    elif tag in ('sdt', 'sdtContent', 'body'):
        for child in elem:
            ctag = child.tag.split('}')[-1]
            if ctag in ('p', 'tbl', 'sdt', 'sdtContent'):
                extract_all_elements(child, elements_list)

def process_docx(file_path):
    elements = []
    with zipfile.ZipFile(file_path) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        body = tree.find('w:body', NS)
        extract_all_elements(body, elements)
        
        if 'word/footnotes.xml' in z.namelist():
            fn_tree = ET.fromstring(z.read('word/footnotes.xml'))
            fn_elements = []
            for fn in fn_tree.findall('.//w:footnote', NS):
                fn_id = fn.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                if fn_id not in ('-1', '0'):
                    extract_all_elements(fn, fn_elements)
            if fn_elements:
                elements.append({'type': 'paragraph', 'style': 'Heading1', 'text': 'Footnotes and References'})
                elements.extend(fn_elements)
    return elements

if __name__ == '__main__':
    os.makedirs('_site_data', exist_ok=True)
    
    doc1_path = '_paper/2026 YK_Regional_Directory Draft.docx'
    doc2_path = '_paper/Yukon-Kuskokwim Delta Housing Resources Guide & Directory (YK Directory) Jan. 27 2026.docx'
    
    data1 = process_docx(doc1_path)
    data2 = process_docx(doc2_path)
    
    with open('_site_data/regional_directory.json', 'w', encoding='utf-8') as f:
        json.dump(data1, f, indent=2, ensure_ascii=False)
        
    with open('_site_data/housing_guide.json', 'w', encoding='utf-8') as f:
        json.dump(data2, f, indent=2, ensure_ascii=False)
        
    print(f"Extracted {len(data1)} blocks from Regional Directory.")
    print(f"Extracted {len(data2)} blocks from Housing Resources Guide.")
