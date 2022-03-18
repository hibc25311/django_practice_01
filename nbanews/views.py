from django.shortcuts import render
from nbanews.models import NbaNews
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from nbanews.beautifulsoup import collectNews

# Create your views here.

def nbanews(request):
   last_ten_news = NbaNews.objects.all().order_by('-id')[:10]

   return render(request, 'nbanews/nbanews.html', {'last_ten_news':last_ten_news})


scheduler = BackgroundScheduler(timezone='Asia/Taipei')
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler.add_job(collectNews, 'interval', seconds=10, id='collectNews', replace_existing=True)
register_events(scheduler)
scheduler.start()
print('scheduler started')