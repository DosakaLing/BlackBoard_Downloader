import requests
import time,re
from findjindu import find_app_list
import file_operation
import get_mutiple_file

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

timestr = str(int(time.time()*1000))
print('=============================')
user = input('请输入账号:')
print('-----------------------------')
pwd = input('请输入密码:')
print('=============================')
'''
'''
import base64
def generate_Pstring(pwd):
    encodestr = base64.b64encode(pwd.encode('utf-8'))
    return str(encodestr)[2:][:-1]
pwdstr = generate_Pstring(pwd)
data = {'user_id': user,
    'password': pwd,
    'action':'login',
    'remote-user':'' ,
    'new_loc':'' ,
    'auth_type':'' ,
    'one_time_token': '',
    'encoded_pw':'' ,
    'encoded_pw_unicode':'' ,
    'tstring': timestr,
    'pstring': pwdstr}


url4 = 'https://bb9.sufe.edu.cn/webapps/bb-shcjcas-BBLEARN/index.jsp'
html_post = requests.post(url4,headers = header,data=data)
cook = html_post.request.headers['Cookie']
cookie = {'Cookie': cook}

#生成课程列表，包含课程名称和课程id,创建课程目录，利用find_jindu模块查找每门课程的app，比如教学进度等
ree = r'coursefakeclass ">(.*?)</ul>'
courselist = re.search(ree,html_post.text,re.S)
ree_for_find_item = r'<li>(.*?)</li>'
courses = re.findall(ree_for_find_item,courselist.group(),re.S)
courses_info_list = []
for course in courses:
    course_info = {}
    ree_for_name = r'"_top">(.*?)</a>'
    ree_course_id = r'Course&id=(.*?)&url'
    name = re.findall(ree_for_name, course, re.S)[0]
    file_operation.mkdir('courses/'+name)
    course_id = re.findall(ree_course_id, course, re.S)[0]
    course_info['name'] = name
    course_info['id'] = course_id
    course_index_url = 'https://bb9.sufe.edu.cn/webapps/blackboard/execute/launcher?type=Course&id=%s&url=' % course_id
    g = requests.get(course_index_url,headers = header, cookies = cookie)
#    with open('courses/%s/%s%s.html' % (name,name,course_id), 'wb') as f:
#        f.write(g.content)
    ree_for_find_content = r'content_id=(.*?)&mode'
    _, course_info['app_id_and_name'] = find_app_list(g.text)
    '''    for item in course_info['app_id_and_name']:
        for key,value in item.items():
            if key=='name':
                file_operation.mkdir('courses/'+name+'/'+value)'''
    courses_info_list.append(course_info)
print(courses_info_list)
files_lists = []
for course in courses_info_list:
    coursename = course['name']
    courseid = course['id']
    for apps in course['app_id_and_name']:
        app_name = apps['name']
        app_url = apps['app_url']
        response = requests.get(app_url,headers = header,cookies = cookie)
        dir_name = 'courses/%s/%s'% (coursename,app_name)
        new_files_lists = []
        get_mutiple_file.define_if_dir_or_return_response(response,dir_name,new_files_lists,header,cookie)
        files_lists.extend(new_files_lists)
#print(files_lists)
def file_downloader(header,cookie,url,path):
    import urllib
    response = requests.get(url,headers = header,cookies = cookie)
    fileurl = urllib.request.unquote(response.url)
    print(fileurl)
    realfilename = fileurl[fileurl.rfind('/') + 1:]
    file_operation.mkdir(path)
    with open(path+'/'+realfilename,'wb') as file:
        file.write(response.content)
for file in files_lists:
    file_downloader(header,cookie,file.url,file.dirs)
    pass
print('====================================complete===================================')
import os
os.system('pause')





