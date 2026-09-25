import json
import os
import html

def build_site():
    with open('_site_data/regional_directory.json', 'r', encoding='utf-8') as f:
        dir_data = json.load(f)
        
    with open('_site_data/housing_guide.json', 'r', encoding='utf-8') as f:
        guide_data = json.load(f)
        
    # Serialize JSON for embedded client-side search and rendering
    dir_json_str = json.dumps(dir_data, ensure_ascii=False)
    guide_json_str = json.dumps(guide_data, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yukon-Kuskokwim Delta Regional Directory & Housing Resources Guide</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #475569;
            --border-color: #e2e8f0;
            --primary: #1e3a8a;
            --primary-hover: #1e40af;
            --accent: #0284c7;
            --accent-light: #e0f2fe;
            --heading-color: #0f172a;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --radius: 8px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}

        /* Header Navigation */
        .site-header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #ffffff;
            padding: 1.5rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}

        .header-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        @media (min-width: 768px) {{
            .header-container {{
                flex-direction: row;
                align-items: center;
                justify-content: space-between;
            }}
        }}

        .brand-title {{
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: #ffffff;
        }}

        .brand-subtitle {{
            font-size: 0.875rem;
            color: #94a3b8;
            font-weight: 400;
        }}

        .nav-tabs {{
            display: flex;
            gap: 0.5rem;
            background: rgba(255, 255, 255, 0.1);
            padding: 0.25rem;
            border-radius: var(--radius);
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: #cbd5e1;
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .tab-btn:hover {{
            color: #ffffff;
            background: rgba(255, 255, 255, 0.15);
        }}

        .tab-btn.active {{
            background: #ffffff;
            color: var(--primary);
            box-shadow: var(--shadow-sm);
        }}

        /* Search Controls */
        .search-bar-wrapper {{
            background: #ffffff;
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            position: sticky;
            top: 80px;
            z-index: 90;
            box-shadow: var(--shadow-sm);
        }}

        .search-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            gap: 1rem;
            align-items: center;
        }}

        .search-input {{
            flex: 1;
            padding: 0.75rem 1.25rem;
            font-size: 0.95rem;
            border: 2px solid var(--border-color);
            border-radius: var(--radius);
            outline: none;
            transition: border-color 0.2s ease;
        }}

        .search-input:focus {{
            border-color: var(--accent);
        }}

        .search-stats {{
            font-size: 0.875rem;
            color: var(--text-muted);
            white-space: nowrap;
        }}

        /* Main Layout */
        .main-container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 1.5rem;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 2rem;
        }}

        @media (max-width: 1024px) {{
            .main-container {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Sidebar Toc */
        .sidebar {{
            position: sticky;
            top: 160px;
            max-height: calc(100vh - 180px);
            overflow-y: auto;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 1rem;
        }}

        .sidebar-title {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
            font-weight: 700;
        }}

        .toc-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .toc-item a {{
            display: block;
            padding: 0.4rem 0.6rem;
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.875rem;
            border-radius: 4px;
            transition: background 0.15s ease, color 0.15s ease;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .toc-item a:hover {{
            background: var(--accent-light);
            color: var(--primary);
        }}

        /* Content Area */
        .content-area {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 2.5rem;
            box-shadow: var(--shadow-sm);
            min-height: 800px;
        }}

        /* Section & Paragraph Styling */
        .doc-heading1 {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            scroll-margin-top: 170px;
        }}

        .doc-heading2 {{
            font-size: 1.35rem;
            font-weight: 600;
            color: var(--heading-color);
            margin-top: 1.75rem;
            margin-bottom: 0.75rem;
            scroll-margin-top: 170px;
        }}

        .doc-heading3 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
        }}

        .doc-paragraph {{
            margin-bottom: 1rem;
            color: var(--text-main);
            font-size: 0.95rem;
            white-space: pre-wrap;
        }}

        /* Table Styling */
        .doc-table-wrapper {{
            overflow-x: auto;
            margin: 1.5rem 0;
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
        }}

        .doc-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            text-align: left;
        }}

        .doc-table th, .doc-table td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
        }}

        .doc-table tr:nth-child(even) {{
            background-color: #f8fafc;
        }}

        .doc-table th {{
            background-color: #f1f5f9;
            font-weight: 600;
            color: var(--heading-color);
        }}

        /* Highlight match */
        mark.highlight {{
            background-color: #fef08a;
            color: #854d0e;
            padding: 0.1em 0.2em;
            border-radius: 2px;
        }}

        .hidden {{
            display: none !important;
        }}

        /* Footer */
        .site-footer {{
            max-width: 1400px;
            margin: 3rem auto 2rem auto;
            padding: 1.5rem;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>

    <header class="site-header">
        <div class="header-container">
            <div>
                <h1 class="brand-title">Yukon-Kuskokwim Delta Housing Resources & Regional Directory</h1>
                <div class="brand-subtitle">Complete Verbatim Reference System — 2026 Edition</div>
            </div>
            <nav class="nav-tabs">
                <button class="tab-btn active" id="tab-dir" onclick="switchTab('dir')">Regional Directory</button>
                <button class="tab-btn" id="tab-guide" onclick="switchTab('guide')">Housing Resources Guide</button>
            </nav>
        </div>
    </header>

    <div class="search-bar-wrapper">
        <div class="search-container">
            <input type="text" id="search-input" class="search-input" placeholder="Search communities, phone numbers, housing authorities, organizations, footnotes..." oninput="handleSearch()">
            <div id="search-stats" class="search-stats">Showing all entries</div>
        </div>
    </div>

    <main class="main-container">
        <aside class="sidebar">
            <div class="sidebar-title" id="toc-title">Table of Contents</div>
            <ul class="toc-list" id="toc-list">
                <!-- TOC links populated via JS -->
            </ul>
        </aside>

        <section class="content-area" id="content-root">
            <!-- Rendered content -->
        </section>
    </main>

    <footer class="site-footer">
        <div>Yukon-Kuskokwim Delta Regional Directory & Housing Resources Guide</div>
        <div>Verbatim Data Preservation System — Static HTML build for GitHub Pages</div>
    </footer>

    <script>
        const dirData = {dir_json_str};
        const guideData = {guide_json_str};

        let currentTab = 'dir';

        function switchTab(tab) {{
            currentTab = tab;
            document.getElementById('tab-dir').classList.toggle('active', tab === 'dir');
            document.getElementById('tab-guide').classList.toggle('active', tab === 'guide');
            
            document.getElementById('search-input').value = '';
            renderContent();
        }}

        function slugify(text) {{
            return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        }}

        function renderContent() {{
            const data = currentTab === 'dir' ? dirData : guideData;
            const searchVal = document.getElementById('search-input').value.trim().toLowerCase();
            const root = document.getElementById('content-root');
            const tocList = document.getElementById('toc-list');
            
            root.innerHTML = '';
            tocList.innerHTML = '';
            
            let matchCount = 0;
            let totalBlocks = 0;
            
            data.forEach((item, index) => {{
                totalBlocks++;
                let matchesSearch = true;
                let textContent = '';
                
                if (item.type === 'paragraph') {{
                    textContent = item.text;
                }} else if (item.type === 'table') {{
                    textContent = item.rows.map(r => r.join(' ')).join(' ');
                }}

                if (searchVal !== '') {{
                    matchesSearch = textContent.toLowerCase().includes(searchVal);
                }}

                if (matchesSearch) {{
                    matchCount++;
                    
                    if (item.type === 'paragraph') {{
                        const isHeading2 = item.style === 'Heading2';
                        const isHeading1 = item.style === 'Heading1' || item.style === 'Title';
                        
                        const pEl = document.createElement(isHeading1 ? 'h1' : (isHeading2 ? 'h2' : 'p'));
                        
                        if (isHeading1) pEl.className = 'doc-heading1';
                        else if (isHeading2) pEl.className = 'doc-heading2';
                        else pEl.className = 'doc-paragraph';

                        const elementId = slugify(item.text) || ('block-' + index);
                        if (isHeading1 || isHeading2) {{
                            pEl.id = elementId;
                            
                            // Add TOC entry
                            const li = document.createElement('li');
                            li.className = 'toc-item';
                            li.innerHTML = `<a href="#${{elementId}}">${{escapeHtml(item.text)}}</a>`;
                            tocList.appendChild(li);
                        }}
                        
                        if (searchVal !== '' && !isHeading1 && !isHeading2) {{
                            pEl.innerHTML = highlightText(item.text, searchVal);
                        }} else {{
                            pEl.textContent = item.text;
                        }}
                        
                        root.appendChild(pEl);
                    }} else if (item.type === 'table') {{
                        const wrap = document.createElement('div');
                        wrap.className = 'doc-table-wrapper';
                        
                        const tbl = document.createElement('table');
                        tbl.className = 'doc-table';
                        
                        item.rows.forEach((row, rIdx) => {{
                            const tr = document.createElement('tr');
                            row.forEach(cell => {{
                                const td = document.createElement(rIdx === 0 ? 'th' : 'td');
                                if (searchVal !== '') {{
                                    td.innerHTML = highlightText(cell, searchVal);
                                }} else {{
                                    td.textContent = cell;
                                }}
                                tr.appendChild(td);
                            }});
                            tbl.appendChild(tr);
                        }});
                        
                        wrap.appendChild(tbl);
                        root.appendChild(wrap);
                    }}
                }}
            }});

            const statsEl = document.getElementById('search-stats');
            if (searchVal === '') {{
                statsEl.textContent = `Showing all ${{totalBlocks}} entries`;
            }} else {{
                statsEl.textContent = `Found ${{matchCount}} matching entries`;
            }}
        }}

        function handleSearch() {{
            renderContent();
        }}

        function highlightText(text, search) {{
            if (!search) return escapeHtml(text);
            const re = new RegExp('(' + escapeRegExp(search) + ')', 'gi');
            return escapeHtml(text).replace(re, '<mark class="highlight">$1</mark>');
        }}

        function escapeHtml(str) {{
            return str
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        function escapeRegExp(string) {{
            return string.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
        }}

        // Initial render
        renderContent();
    </script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("Site HTML files successfully built: index.html & docs/index.html")

if __name__ == '__main__':
    build_site()
