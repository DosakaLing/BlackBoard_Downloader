import re,requests
from lxml import etree
def define_if_dir_or_return_response(response,dirname,filelist,header,cookie):
    dir_name = dirname
    listhtml = response.text
    #接受列表界面所有的li标签如果不是文件夹就返回文件响应，如果是文件夹就返回里层的response
    xph_for_find_list_container = r'//ul[@id="content_listContainer"]/li'
    selector = etree.HTML(listhtml)
    lis = selector.xpath(xph_for_find_list_container)
    for li in lis:
        xph_for_find_FileDir_type = r'img/@alt'
        file_dir_type = li.xpath(xph_for_find_FileDir_type)[0]
        if file_dir_type =='项目':
            #假设项目之后一定是文件
            xph_for_find_project_name = r'div[1]/h3/span[2]/text()'
            xph_for_find_project_lis_list = r'div[2]/div/div[2]/ul/li'
            projectname = li.xpath(xph_for_find_project_name)[0]
            final_dir_name = dir_name+'/'+projectname
            project_files_lis_list = li.xpath(xph_for_find_project_lis_list)
            for li in project_files_lis_list:
                xph_for_file_url = r'a/@href'
                xph_for_file_name = r'a/text()'
                file_url = 'https://bb9.sufe.edu.cn'+li.xpath(xph_for_file_url)[0]
                file_name = li.xpath(xph_for_file_name)[0].lstrip()
                file = File()
                file.name = file_name
                file.dirs = final_dir_name
                file.url = file_url
                filelist.append(file)
        elif file_dir_type =='内容文件夹':
            xph_for_find_dir_url = r'div[1]/h3/a/@href'
            dir_url = 'https://bb9.sufe.edu.cn'+li.xpath(xph_for_find_dir_url)[0]
            xph_for_find_dir_name = r'div[1]/h3/a/span/text()'
            response = requests.get(dir_url,headers = header,cookies = cookie)
            realdir_name = dir_name + '/'+li.xpath(xph_for_find_dir_name)[0]
            define_if_dir_or_return_response(response,realdir_name,filelist,header,cookie)
            pass
        elif file_dir_type =='文件':
            file_dir_name = dir_name
            xph_for_find_file_name = r'div[1]/h3/a/span/text()'
            xph_for_find_file_url = r'div[1]/h3/a/@href'
            file_name = li.xpath(xph_for_find_file_name)[0]
            realfile_url = li.xpath(xph_for_find_file_url)[0]
            file = File()
            file.name = file_name
            file.url = 'https://bb9.sufe.edu.cn'+realfile_url
            #print(file.url)
            file.dirs = file_dir_name
            filelist.append(file)
            pass
        pass

class File():
    def __init__(self):
        self.name = ''
        self.dirs = ''
        self.url = ''
    def __str__(self):
        str=''
        str = '文件名:'+self.name+'    深度:'+self.dirs
        return str

if __name__ == '__main__':
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    cookie = {'Cookie':'JSESSIONID=98F0D1EBFBF96FC5925DF3AB62E7F7CF; JSESSIONID=5CE0724F0BBF58572CFE6CC26EA5952A; session_id=FD08EB2DC7B2893CABD3B26C33F52FB1; s_session_id=AC19DD3CCD353690CDAB22CA94A15E4E; web_client_cache_guid=6dae88e4-6c48-428f-a9ab-a767d39f559e'}
    info = {'name': '高等数学（经管类）II', 'id': '_6501_1', 'app_id_and_name': [{'name': '教学大纲', 'content_id': '_95125_1', 'app_url': 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_6501_1&content_id=_95125_1&mode=reset'}, {'name': '教学进度', 'content_id': '_95126_1', 'app_url': 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_6501_1&content_id=_95126_1&mode=reset'}, {'name': '课程文档', 'content_id': '_95127_1', 'app_url': 'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_6501_1&content_id=_95127_1&mode=reset'}]}
    url1 = r'https://bb9.sufe.edu.cn/bbcswebdav/pid-99870-dt-content-rid-179991_1/xid-179991_1'
    url2 = r'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_6501_1&content_id=_99866_1'
    url3 = r'https://bb9.sufe.edu.cn/webapps/blackboard/content/listContent.jsp?course_id=_5840_1&content_id=_91162_1&mode=reset'
    response = requests.get(url3,headers=header,cookies = cookie)
    filelist = []
    define_if_dir_or_return_response(response,'',filelist)
    print(filelist)
    for file in filelist:
        print(file)
        print()
        pass