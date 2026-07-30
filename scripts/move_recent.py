with open('www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<div class="card-title">Riwayat Terbaru</div>' in line:
        start_idx = i - 1  # The <div class="card"> before it
        break

if start_idx != -1:
    end_idx = start_idx + 6
    card_lines = lines[start_idx:end_idx]
    
    # delete from original location
    del lines[start_idx:end_idx]
    
    # find where to insert
    insert_idx = -1
    for i in range(len(lines)):
        if '<!-- TAB 2: BUAT INVOICE (FORM) -->' in lines[i]:
            # we want to insert right before the closing div of tab-dashboard
            # which is lines[i-2] usually
            insert_idx = i - 2
            break
            
    if insert_idx != -1:
        # Just to be safe, insert a spacer div
        card_lines.insert(0, '\\n      <!-- RIWAYAT TERBARU (MOVED TO BOTTOM) -->\\n')
        for idx, cl in enumerate(card_lines):
            lines.insert(insert_idx + idx, cl)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done!')
