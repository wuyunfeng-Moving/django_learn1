from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import WebLink
from .models import YoutubeLink

from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from readability import Readability
import nltk
from weblist.youtube import scan_youtube,youtubelist
import json

nltk.download('punkt')

# Create your views here.


def download_page(url):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    }
    r = requests.get(url, headers=headers)  # 增加headers, 模拟浏览器
    return r.text


def analyze_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    con = soup.find_all("p")
    txtsum = ''
    score = float(0)
    for i in con:
        if (len(txtsum) < 10000):
            if (len(i.text) > 100):
                txtsum = txtsum + i.text
        else:
            break

    if (len(txtsum) > 2000):
        resault = Readability(txtsum)
        score = resault.dale_chall().score

    #find title
    title_str = soup.find("title").text

    title_start_index = title_str.find("of")
    title_end_index = title_str.find(",")
    title = ''
    title = title_str[(title_start_index + 2):title_end_index]
    author_start_index = title_str.find("by")
    author = ''
    author = title_str[(author_start_index + 2):]
    return [score, title, author]


def scan_gutenberg():
    for j in range(10000, 50000):
        url = 'https://www.gutenberg.org/files/{}/{}-h/{}-h.htm'.format(
            j, j, j)
        temp_ob = WebLink.objects.filter(web_address=url)
        if temp_ob.exists():
            print(temp_ob.first())
        else:
            page_data = download_page(url)  #get the txt in html
            article_info = analyze_link(page_data)  #get the score of the html
            try:
                wl = WebLink(web_address=url,
                             language_scores=article_info[0],
                             title=article_info[1],
                             pub_date=timezone.now())
            except:
                print("error\n")
            else:
                print("save db" + str(j))
                wl.save()
                #print(WebLink.objects.all())


def f_print(argus):
    gutenberg_inputword = "123456789"

    if argus == gutenberg_inputword:
        print("start to add data!\n")
        scan_gutenberg()


def youtube(request):
    if ('POST' == request.method):
        name = json.loads(request.body)
        data = scan_youtube(name)
        return JsonResponse({'data': 'you get it!', 'data1': data})
    return render(request, "templates/youtube.html")


def linkinput(request):
    tartget_url = request.POST.get("link")
    print(tartget_url)
    f_print(tartget_url)
    return render(request, "templates/linkinput.html")


def linkdisplay(request):
    if ('POST' == request.method):
        range = json.loads(request.body)
        print(range["low"] + '***********' + range["high"])
        # print(type(range["low"]))
        weblist = WebLink.objects.filter(
            language_scores__range=(range["low"], range["high"])).order_by(
                'language_scores')  #get the queryset data library
        data = []
        for x in weblist:
            data.append({
                'address': x.web_address,
                'score': x.language_scores,
                'title': x.title
            })
        print(data)
        return JsonResponse({'weblist': data})
    return render(request, "templates/linkdisplay.html")
    #for item in weblist:
    #   print(item.web_address)


def savetext(request):
    return render(request, "templates/test_savefile.html")
