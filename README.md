# nice to meet you  
Second project  
demo網址:https://djangonba.herokuapp.com/  
  
1. 抓取 https://nba.udn.com/nba/index?gr=www 中的焦點新聞。(完成)  
2. 使用 [Django](https://www.djangoproject.com/) 設計恰當的 Model，并將所抓取新聞存儲至 DB。(完成)  
   DB table:  
     title-標題  
     author-作者  
     news_link-新聞詳情連結  
     body-內文  
     image_link-新聞圖片連結  
     video_link-新聞影音連結  
     
3. 使用 [Django REST Framework](http://www.django-rest-framework.org/) 配合 AJAX 實現以下頁面：(完成)  
	 * 焦點新聞列表  
	 * 新聞詳情頁面  
	 由jquery通過AJAX獲取serializers的json data  
	 
4. 以 Pull-Request 的方式將代碼提交。(完成)  
	
## 進階要求  
1. 實現爬蟲自動定時抓取。(未完成)  
   透過python schedule library設定每隔一小時自動抓取焦點新聞  
   在本地端可以啟動，crawl.py放在heroku worker啟動一次後便無法自動抓蟲。  
   
2. 每當抓取到新的新聞時立即通知頁面。(未完成)  
3. 将本 demo 部署至服务器并可正确运行。(完成)  
   demo網址:https://djangonba.herokuapp.com/  
