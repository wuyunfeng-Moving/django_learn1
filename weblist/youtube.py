from youtube_transcript_api import YouTubeTranscriptApi
from .models import YoutubeLink
from readability import Readability
from django.utils import timezone
from django.shortcuts import render
import json
from django.http import JsonResponse

def words_numcal(argus):
    char = 0
    word = 1
    for i in argus:
        char = char + 1
        if (i == ' '):
            word = word + 1
    return word


def scan_models(argus):
    y = argus["link"].rsplit("?v=")    
    temp_ob = YoutubeLink.objects.filter(address=y[1])
    print(y[1])
    if temp_ob.exists():
        print("data already exist in library")
        return temp_ob[0].score
    else:
        try:
            page_data = YouTubeTranscriptApi.get_transcript(
                y[1])  #get the txt in html
        except:
            print("get data from transcript fail")
        else:
            string_txt = ''
            for i in page_data:
                string_txt += i["text"]
            #print(string_txt)
            if (words_numcal(string_txt) < 100):
                print("length isnot enough!")
                return float(0)
            resault = Readability(string_txt)
            try:                           
                yl = YoutubeLink(
                    address=y[1],
                    score=resault.dale_chall().score,
                    title=argus["title"],
                    words_num=words_numcal(string_txt),
                    pub_date=timezone.now(),
                    timelength=argus["timelen"],
                )
                yl.save()
            except:
                print("open SQL error\n")
            else:
                print("link save success")
                return resault.dale_chall().score


def scan_youtube(argus):
    a_s = []
    index =0
    for x in argus["link"]:
        score = scan_models(x)
        a_s.append(score)
    return a_s
    '''
    url = "https://www.youtube.com/watch?v=T4M_EJzjItk"
    temp_ob = WebLink.objects.filter(web_address=url)
    if temp_ob.exists():
        print(temp_ob.first())
    else:
        page_data = YouTubeTranscriptApi.get_transcript(
            "o69TvQqyGdg&list=PL8dPuuaLjXtMwmepBjTSG593eG7ObzO7s&index=3"
        )  #get the txt in html
        #print(type(page_data))
        string_txt = ''
        for i in page_data:
            if (len(string_txt) < 10000):
                string_txt += i["text"]
            else:
                break
        print(string_txt)
        resault = Readability(string_txt)
        print(resault.dale_chall().score)
  '''

  
def youtubelist(request):
    if ('POST' == request.method):
        range = json.loads(request.body)
        print(range["low"] + '***********' + range["high"])
        # print(type(range["low"]))
        weblist = YoutubeLink.objects.filter(
            score__range=(range["low"], range["high"])).order_by(
                'score')  #get the queryset data library
        data = []
        for x in weblist:
            data.append({
                'address': "https://www.youtube.com/watch?v=" + x.address,
                'score': x.score,
                'title': x.title,
                'timelen':x.timelength,
                'wordsnum':x.words_num,
            })
        print(data)
        return JsonResponse({'weblist': data})
    return render(request, "templates/youtubelist.html")


