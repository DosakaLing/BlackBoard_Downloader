import re
import file_operation
def find_app_list(html_text):
    ree_for_list = r'listContent(.*?)</span></a>'
    ree_for_course_id = r'course_id=(.*?)"'
    ree_for_content = r'content_id=(.*?)&mode.*?title="(.*?)"'
    content = re.findall(ree_for_list, html_text,re.S)
    course_id = re.search(ree_for_course_id,html_text,re.S).group(1)
    content_info = []
    for item in content:
        #print(item)
        content_detail = re.findall(ree_for_content,item)

        for contentid,name in content_detail:
            content_detail_dict = {}
            content_detail_dict['name'] = name
            content_detail_dict['content_id'] = contentid
            app_url = 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=%s&' \
                      'content_id=%s&mode=reset' % (course_id,contentid)
            content_detail_dict['app_url'] =app_url
            content_info.append(content_detail_dict)
    return course_id,content_info
if __name__ == '__main__':
    with open('courses/政治经济学_5887_1.html',encoding='utf-8') as f:
        conetent = f.read()
    course_id, contentlist = find_app_list(conetent)
    print('----------')
    print(course_id,contentlist)
    jindu_dict = contentlist[1]
    jindu_id = jindu_dict['content_id']


    jindu_url = 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_5840_1' \
          '&content_id=_91161_1&mode=reset'
    print(contentlist)