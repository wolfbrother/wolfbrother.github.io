import glob

xmls = glob.glob('*.md')
for one_xml in xmls:
    f = open(one_xml, 'r+', encoding='utf-8')
    all_the_lines = f.readlines()
    #print(all_the_lines)
    i, j = -1, -1
    date, title = '', ''
    ret_len = 6
    is_done = False
    for row, line in enumerate(all_the_lines):
        if 'dtindex' in line:
            is_done = True
            break

        lstrip = line.strip()
        if '---' in lstrip:
            if i < 0:
                i = row 
            else:
                j = row
        if i >= 0:
            if 'date' in lstrip:
                date = lstrip.split(':')[1].strip()
            if 'title' in lstrip:
                title = lstrip.split(':')[1].strip()
                if len(title) > ret_len:
                    title = title[:ret_len]
                else:
                    title += '0'*ret_len
                    title = title[:ret_len]
        if j > 0:
            break
    f.close()
    if not is_done:
        all_the_lines.insert(i+1, 'dtindex: '+ date+title+'\n')
        print(i,j, date+title)
        f = open(one_xml, 'w', encoding='utf-8')
        f.write(''.join(all_the_lines))
        f.close()
    
    
    #break