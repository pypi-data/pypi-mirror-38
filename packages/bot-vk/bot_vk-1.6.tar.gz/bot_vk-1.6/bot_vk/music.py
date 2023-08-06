import re,lxml.html, requests,json,urllib,time
class audio(object):
        def __init__(self,login,password):
                url='https://vk.com/'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':'gzip, deflate',
                    'Connection':'keep-alive',
                    'DNT':'1'}
                session = requests.session()
                data = session.get(url, headers=headers)
                page = lxml.html.fromstring(data.content)

                form = page.forms[0]
                form.fields['email'] = login
                form.fields['pass'] = password

                response = session.post(form.action, data=form.form_values())
                if 'onLoginDone' in response.text:
                        self.session = session
                else:
                        raise PermissionError("login or password is wrong")

                self.hash = hashe(self.session)
        def code(self,code):
                """вызывает метод execute."""
                q =  self.session.post(
                        "https://vk.com/dev/execute?params[code]="+code+"&params[v]=5.87",
                        data={"act": "a_run_method",
                              "al": 1,
                              "method":"execute",
                              "param_code": code,
                              "param_v": 5.87,
                              "hash": self.hash},headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0','Accept': '*/*',
                                                        'Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Content-Type': 'application/x-www-form-urlencoded','Connection': 'keep-alive',
                })
                
                audio = json.loads(q.text[38:len(q.text)])
                if "response" in audio:
                        return audio["response"]
                else:
                        return audio
        def get(self,owner_id= None,album_id =None,NeedUser =False ):
                """вызывает метод auido.get"""
                """owner_id - id пользователя или
                        группы( отрицательные значения
                album_id - id альбома
                NeedUser - если True, то возращает информацию о исполнители песен"""
                code_response = ""
                if owner_id:
                        code_response += "owner_id:"+str(owner_id)
                if album_id:
                        code_response += ",album_id:"+str(album_id)
                if NeedUser:
                        code_response += ",NeedUser:1"
                q = code_response.lstrip(",")
                
                code = r'return API.audio.get({'+q+r'});'
                return self.code(code)
        def search(self,q='imagine dragons',owner_id=None,offset=0,PerformerOnly=False,):
                code_response = ""
                code_response+='q:"{q}"'.format(q=q)
                if owner_id:
                        code_response += ",owner_id:"+str(owner_id)
                if PerformerOnly:
                        code_response += ",PerformerOnly:1"
                if offset!=0:
                        if str(offset).isdsgst():
                                code_response += ",NeedUser:1"
                        else:
                                raise NameError("offset has to be an digit")
                
                
                code_response = code_response.lstrip(",")

                code = r'return API.audio.search({'+code_response+r'});'
                
                return self.code(code)
        def add(self,owner_id=1234567,audio_id=456239029):
                code_response = ""
                code_response += "owner_id:{owner_id},audio_id:{audio_id}".format(owner_id=str(owner_id),audio_id=str(audio_id))
                code = r'return API.audio.add({'+code_response+r'});'
                
                return self.code(code)
	
def hashe(session):
        qw = session.get("https://vk.com/dev/execute").text
        return re.findall('onclick="Dev.methodRun\(\'(.+)\', this\);"',qw)[0]



