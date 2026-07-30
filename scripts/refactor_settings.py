import re

def main():
    with open('www/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    sections = ['profil', 'template', 'katalog', 'backup', 'tema']
    
    # 1. Extract each sub-sect
    sub_sects = {}
    for sect in sections:
        # We need to extract <div id="sub-sect-NAME" ...> up to the end of the div
        # Since it might have nested divs, we can use a simple regex if we know it ends with certain patterns,
        # but regex for balanced HTML is hard.
        # Let's find the start index:
        start_marker = f'<div id="sub-sect-{sect}" class="settings-sub-section" style="display: none;">'
        start_idx = html.find(start_marker)
        if start_idx == -1:
            print(f"Could not find {start_marker}")
            continue
            
        # Find matching end div
        div_count = 0
        i = start_idx
        end_idx = -1
        while i < len(html):
            if html.startswith('<div', i):
                div_count += 1
                i += 4
            elif html.startswith('</div', i):
                div_count -= 1
                i += 6
                if div_count == 0:
                    end_idx = i
                    break
            else:
                i += 1
                
        if end_idx != -1:
            sub_sects[sect] = html[start_idx:end_idx]
            # Remove from original html
            html = html[:start_idx] + html[end_idx:]
            print(f"Extracted sub-sect-{sect}")
            
    # 2. Insert sub_sects right after their menu-items
    for sect, content in sub_sects.items():
        # Change class to accordion-content
        new_content = content.replace('class="settings-sub-section" style="display: none;"', 'class="settings-sub-section accordion-content"')
        
        # Find the menu item end
        item_start = f'onclick="openSettingsSubPage(\'{sect}\')"'
        idx = html.find(item_start)
        if idx != -1:
            # Replace onclick
            html = html.replace(item_start, f'onclick="toggleAccordion(\'{sect}\')"')
            
            # Find the end of this settings-menu-item
            # It's <div class="settings-menu-item"...> ... </div>
            # We can find the closing </div> of settings-menu-item
            # We know it ends with <span ...>➔</span>\n        </div>
            # Let's search for the next </div> after the ➔
            arrow_idx = html.find('➔</span>', idx)
            if arrow_idx != -1:
                # Add chevron class
                html = html[:arrow_idx-8] + ' class="acc-chevron"' + html[arrow_idx-8:arrow_idx] + '▼</span>' + html[arrow_idx+8:]
                
                # Now find the </div>
                close_div_idx = html.find('</div>', arrow_idx)
                if close_div_idx != -1:
                    insert_pos = close_div_idx + 6
                    # Wrap both in accordion-wrapper? No, just put it after.
                    html = html[:insert_pos] + '\n' + new_content + '\n' + html[insert_pos:]
                    print(f"Inserted {sect} after menu item")

    # 3. Add CSS for accordion
    css = """
    /* ACCORDION SETTINGS */
    .accordion-content {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1);
      background: var(--bk2);
      padding: 0;
      opacity: 0;
    }
    .accordion-content.open {
      max-height: 1200px;
      opacity: 1;
      padding: 10px 0 20px 0;
      border-bottom: 1px solid rgba(255,255,255,0.03);
    }
    .acc-chevron {
      transition: transform 0.3s ease;
    }
    .acc-chevron.open {
      transform: rotate(180deg);
    }
    .settings-menu-item {
      cursor: pointer;
    }
"""
    if '/* ACCORDION SETTINGS */' not in html:
        html = html.replace('</style>', css + '\n  </style>')
        
    # 4. Remove subpage overlay wrapper entirely
    wrapper_start = '<div id="settings-subpage" class="settings-subpage-overlay"'
    w_start = html.find(wrapper_start)
    if w_start != -1:
        # Find closing div
        div_count = 0
        i = w_start
        w_end = -1
        while i < len(html):
            if html.startswith('<div', i):
                div_count += 1
                i += 4
            elif html.startswith('</div', i):
                div_count -= 1
                i += 6
                if div_count == 0:
                    w_end = i
                    break
            else:
                i += 1
        if w_end != -1:
            html = html[:w_start] + html[w_end:]
            print("Removed settings-subpage overlay")
            
    # 5. Add toggleAccordion JS
    js = """
    function toggleAccordion(id) {
      const content = document.getElementById('sub-sect-' + id);
      const menuItem = content.previousElementSibling; // settings-menu-item
      const chevron = menuItem.querySelector('.acc-chevron');
      
      // Toggle
      if (content.classList.contains('open')) {
        content.classList.remove('open');
        if(chevron) chevron.classList.remove('open');
      } else {
        // Optional: Close others
        document.querySelectorAll('.settings-sub-section.accordion-content').forEach(el => {
          el.classList.remove('open');
          const siblingChevron = el.previousElementSibling?.querySelector('.acc-chevron');
          if (siblingChevron) siblingChevron.classList.remove('open');
        });
        
        content.classList.add('open');
        if(chevron) chevron.classList.add('open');
      }
    }
"""
    if 'function toggleAccordion' not in html:
        html = html.replace('function openSettingsSubPage(sectionId) {', js + '\n    function openSettingsSubPage(sectionId) {')
        
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
