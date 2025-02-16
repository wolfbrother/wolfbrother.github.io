import glob

xmls = glob.glob('*.md')
for one_xml in xmls:
    print(one_xml)
    f = open(one_xml, 'r+', encoding='utf-8')
    all_the_lines = f.readlines()
    for row, line in enumerate(all_the_lines):
        if 'title:' in line:
            a, b = line.strip().split()
            b = '剑指'+b 
            line = a + ' ' + b+'\n'
            print(line)
            all_the_lines[row] = line
            break    
            
    f.close()
    if True:
        f = open(one_xml, 'w', encoding='utf-8')
        f.write(''.join(all_the_lines))
        f.close()