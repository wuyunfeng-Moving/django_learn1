from .models import WebLink
from django.utils import timezone


def post_link(argus):
    print(argus)
    if argus is None:
        print("no new data added!\n")
    else:
        print("add a new data!\n")
        try:
            wl = WebLink(web_address=argus,
                         language_scores=float('10'),
                         pub_date=timezone.now())
        except:
            print("error\n")
        else:
            print("save db")
            wl.save()
            print(WebLink.objects.all())
