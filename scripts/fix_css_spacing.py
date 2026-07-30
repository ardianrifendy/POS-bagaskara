with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update history-month-group
old_group = """    .history-month-group {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 18px;
      margin-bottom: 16px;
      padding: 6px;
    }"""
new_group = """    .history-month-group {
      background: var(--bk2);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 18px;
      margin-bottom: 16px;
      padding: 8px;
    }"""
html = html.replace(old_group, new_group)

# 2. Update history-month-header
old_header = """    .history-month-header {
      background: rgba(255,255,255,0.05);
      padding: 14px 16px;
      border-radius: 12px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      font-weight: 700;
      font-size: 14px;
      color: var(--white);
      transition: background 0.2s;
      border: 1px solid rgba(255,255,255,0.08);
    }
    .history-month-header:active {
      background: rgba(255,255,255,0.08);
    }"""
new_header = """    .history-month-header {
      background: transparent;
      padding: 10px 12px;
      border-radius: 12px;
      margin-bottom: 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      font-weight: 700;
      font-size: 14px;
      color: var(--white);
      transition: background 0.2s;
      border: none;
    }
    .history-month-header:active {
      background: rgba(255,255,255,0.05);
    }"""
html = html.replace(old_header, new_header)

# 3. Update history-acc-content.open
old_acc = """    .history-acc-content.open {
      max-height: 4000px;
      opacity: 1;
      padding-bottom: 12px;
    }"""
new_acc = """    .history-acc-content.open {
      max-height: 4000px;
      opacity: 1;
      padding-top: 8px;
    }"""
html = html.replace(old_acc, new_acc)

# 4. Update history-card
old_card = """    .history-card {
      background: var(--bk2);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 18px;
      padding: 14px;
      margin-bottom: 8px;
      position: relative;
      transition: transform 0.2s ease;
    }"""
new_card = """    .history-card {
      background: var(--bk3);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 14px;
      padding: 14px;
      margin-bottom: 8px;
      position: relative;
      transition: transform 0.2s ease;
    }"""
html = html.replace(old_card, new_card)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
