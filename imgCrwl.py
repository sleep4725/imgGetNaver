from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bs
from pathlib import Path
import os

#
# 작성일 : 20200725
# 작성자 : JunHyeon.Kim
# 주소   : https://kin.naver.com/qna/detail.nhn?d1id=1&dirId=104&docId=363350154
#

class ImagGet():


    def __init__(self):

        self.baseUrl    = "https://search.naver.com/search.naver"
        self.baseDir    = "./imgGetDir"
        self.peopleList = {"celebrity": {
                                        "이승기": {"data": None, "path": "/이승기"}, 
                                        "아이유": {"data": None, "path": "/아이유"}}}        
        self.section = 1
        self.dirSetting()        


    def dirSetting(self):
        """ 이미지를 수집하기 전에 디렉토리를 우선 생성
        """
        for v in self.peopleList.values():
            for k in v.keys():        
                # 디렉토리를 생성하기 전에 이미 있는지 확인 
                if not os.path.isdir(self.baseDir + v[k]["path"]):
                    # 디렉토리 생성 
                    Path(self.baseDir + v[k]["path"]).mkdir(parents=True, exist_ok=True)
                    print("make dir ({})".format(self.baseDir + v[k]["path"]))
                else:
                    print("directory({}) exists !!".format(self.baseDir + v[k]["path"]))


    def urlReq(self):
        
        display_ = 100      
         
        for k, v in self.peopleList.items(): 
            for searchImg in v.keys():
                queryParam = urlencode({"query": searchImg})
                
                page_= 51
                
                for _ in range(3):
                    params = "where=image&sm=tab_jum&start="+ str(page_) +"&display="+ str(display_) +"&"+ queryParam

                    url = self.baseUrl +"?"+ params        
                    
                    response = urlopen(url)
                    
                    if response.status == 200:
                        soup = bs(response, "html.parser")            
                        imgList = soup.select("img._img")
                        
                        subUrlList = [u.attrs["data-source"].split("&") for u in imgList]
                        self.peopleList[k][searchImg]["data"] = ["&".join(u[0: len(u)-1]) for u in subUrlList]
                        
                        ##############################
                        #### function call 
                        ##############################
                        self.subUrlReq(searchImg)
                        self.peopleList[k][searchImg]["data"] = None
                        self.section += 1
                    else:
                        ## status_code = 3xx or 4xx or 5xx
                        pass

                    page_ += display_ 

                self.section = 1
            

    def subUrlReq(self, searchImg):
        
        ## 현재 디렉토리 보존 
        currentDir = os.getcwd()
        ## 디렉토리 이동 
        os.chdir(self.baseDir + self.peopleList["celebrity"][searchImg]["path"])    
        
        for c, d in enumerate(self.peopleList["celebrity"][searchImg]["data"]):
            
            try:
                urlretrieve(d, "{}_{}_{}.jpg".format(searchImg, self.section, c+1))
            except:
                print("err => {}".format(d))
            else:
                print("success => {}".format(d))
        
        os.chdir(currentDir)


if __name__ == "__main__":
    obj_ = ImagGet()
    obj_.urlReq()
