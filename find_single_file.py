#利用课程信息查找文件
def get_NotInDir_file_url(course_info,cookie,header):
    import re
    course_id = course_info['id']
    #先用教学进度试一下,以下仅仅打开了app的首页
    if (len(course_info['app_id_and_name'])==0) or course_info['app_id_and_name'][1]['name']!='教学进度':
        return None
    else:
        course_app_url = course_info['app_id_and_name'][1]['app_url']
        import requests
        response = requests.get(course_app_url,headers = header, cookies = cookie)
        #接下来需要打开里面的每条文件内容这里先打开第一个
        ree = 'class="contentList">(.*?)</ul>'
        file_list_html = re.findall(ree,response.text,re.S)
        ree_inside = r'<li.*?<a href="(.*?)".*?</li>'
        file = re.findall(ree_inside,file_list_html[0],re.S)
        firstpart = 'https://bb9.sufe.edu.cn'
        if file:
            filename = firstpart+file[0]
            response = requests.get(filename,headers=header,cookies = cookie)
            return response
def downLoadFile(file_dir_path,response):
    import urllib
    print(response.url)
    fileurl = urllib.request.unquote(response.url)
    filename = fileurl[fileurl.rfind('/') + 1:]
    path = file_dir_path.rstrip('/') + '/' + filename
    with open(path,'wb') as file:
        file.write(response.content)

if __name__ == '__main__':
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    cookie = {'Cookie':'JSESSIONID=98F0D1EBFBF96FC5925DF3AB62E7F7CF; JSESSIONID=5CE0724F0BBF58572CFE6CC26EA5952A; session_id=FD08EB2DC7B2893CABD3B26C33F52FB1; s_session_id=AC19DD3CCD353690CDAB22CA94A15E4E; web_client_cache_guid=6dae88e4-6c48-428f-a9ab-a767d39f559e'}
    info = {'name': 'Python程序语言',
            'id': '_5840_1',
            'app_id_and_name': [{'name': '教学大纲', 'content_id': '_91160_1','app_url': 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_5840_1&content_id=_91160_1&mode=reset'},
                                {'name': '教学进度', 'content_id': '_91161_1', 'app_url': 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_5840_1&content_id=_91161_1&mode=reset'},
                                {'name': '课程文档', 'content_id': '_91162_1', 'app_url': 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_5840_1&content_id=_91162_1&mode=reset'},
                                {'name': '作业', 'content_id': '_91158_1', 'app_url': 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_5840_1&content_id=_91158_1&mode=reset'}]}
    response = get_NotInDir_file_url(info,cookie,header)
    if response:
        downLoadFile('courses/'+info['name']+'/'+info['app_id_and_name'][1]['name'],response)




