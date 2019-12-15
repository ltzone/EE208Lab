import os , sys


with open("Fi-index.txt",'r') as f:
    for line in f.readlines():
        pp = line.split('\t')
        url=pp[0]
        webpage = pp[1].strip('\n')
        temp = webpage[14:-5]
        pos = 0
        for i in range(len(temp)):
            if temp[i] == 'm':
                pos = i
        itemID = temp[pos + 1:]
        if (len(webpage) > 35):
            continue
        itemID = int(itemID)

        comment_tag_path = 'jd_cmt_SCORE/httpsitem.jd.com%s.html.txt' % itemID

        if os.path.exists(comment_tag_path):
            with open("NEW_available_idx.txt", 'a+') as file:
                file.write(url + '\t' + comment_tag_path[13:-4] + '\n')
                print(url + '\t' + comment_tag_path[13:-4])





