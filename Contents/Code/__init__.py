import re, random

##################################################################################################FOX

PLUGIN_PREFIX               = "/video/fox"
FOX_URL                     = "http://www.fox.com"
FOX_FULL_EPISODES_SHOW_LIST = "http://www.fox.com/full-episodes/"
FOX_FEED                    = "http://www.fox.com/fod"
FOX_ART                     = "art-default.jpg"
FOX_THUMB                   = "icon-default.png"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "FOX", FOX_ART, FOX_THUMB)
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

  MediaContainer.art        = R(FOX_ART)
  DirectoryItem.thumb       = R(FOX_THUMB)
  WebVideoItem.thumb        = R(FOX_THUMB)

  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-agent'] = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11"

####################################################################################################
def MainMenu():
    dir = MediaContainer(mediaType='video')
    content = HTML.ElementFromURL(FOX_FULL_EPISODES_SHOW_LIST)

    for item in content.xpath('//li[@class="episodeListItem"]/div[@class="showInfo"]'):
      titles = item.xpath("a")
      titleUrl = FOX_URL + titles[1].get('href')
      title = item.xpath("h3")[0].text
      summary = item.xpath("h4")[0].text

      if (titleUrl.count('americasmostwanted')) == 0:
        dir.Append(Function(DirectoryItem(VideoPage, title, summary), pageUrl=titleUrl))
    return dir 

####################################################################################################
def VideoPage(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    content = HTML.ElementFromURL(pageUrl)

    for item2 in content.xpath('//ul[@id="fullEpisodesList"]/li[contains(@class,"episode")]/ul'):
      vidUrl = FOX_URL + item2.xpath('li[@class="episodeName"]/span/a')[0].get('href')
      title2 = item2.xpath('li[@class="episodeName"]/span/a')[0].text
      title1 = item2.xpath('li[@class="episodeName"]/span/a')[0].text
      summary = item2.xpath('li[@class="description"]')[0].get('href')
      airdate = item2.xpath('li[@class="airDate"]')[0].text
      title2 = title2 + " - " + airdate

      content2 = HTML.ElementFromURL(vidUrl)
      pageUrl2 = pageUrl
      pageUrl2 = pageUrl2.replace("/","%2F")
      pageUrl2 = pageUrl2.replace(":","%3A")
      pageUrl2 = pageUrl2 + "&%40"

      videoID = content2.xpath('//div[@id="player"]//object/param[@name="@videoPlayer"]')[0].get("value")
      bgcolor = content2.xpath('//div[@id="player"]//object/param[@name="bgcolor"]')[0].get("value")
      bgcolor = bgcolor.replace("#","%23")
      width = content2.xpath('//div[@id="player"]//object/param[@name="width"]')[0].get("value")
      height = content2.xpath('//div[@id="player"]//object/param[@name="height"]')[0].get("value")
      playerID = content2.xpath('//div[@id="player"]//object/param[@name="playerID"]')[0].get("value")
      publisherID = content2.xpath('//div[@id="player"]//object/param[@name="publisherID"]')[0].get("value")
      isVid = content2.xpath('//div[@id="player"]//object/param[@name="isVid"]')[0].get("value")
      videoPlayer = content2.xpath('//div[@id="player"]//object/param[@name="@videoPlayer"]')[0].get("value")
      wmode = content2.xpath('//div[@id="player"]//object/param[@name="wmode"]')[0].get("value")
      adZone = content2.xpath('//div[@id="player"]//object/param[@name="adZone"]')[0].get("value")
      showCode = content2.xpath('//div[@id="player"]//object/param[@name="showCode"]')[0].get("value")
      omnitureAccountID = content2.xpath('//div[@id="player"]//object/param[@name="omnitureAccountID"]')[0].get("value")
      dynamicStreaming = content2.xpath('//div[@id="player"]//object/param[@name="dynamicStreaming"]')[0].get("value")
      optimizedContentLoad = content2.xpath('//div[@id="player"]//object/param[@name="optimizedContentLoad"]')[0].get("value")
      convivaEnabled = content2.xpath('//div[@id="player"]//object/param[@name="convivaEnabled"]')[0].get("value")
      convivaID = content2.xpath('//div[@id="player"]//object/param[@name="convivaID"]')[0].get("value")

      truevidUrl = "http://admin.brightcove.com/viewer/us1.24.00.06a/BrightcoveBootloader.swf?purl=" + pageUrl2 + "videoPlayer=" + videoID + "&adZone=" + adZone + "&autoStart=true" + "&bgcolor=" + bgcolor + "&convivaEnabled=" + convivaEnabled + "&convivaID=" + convivaID + "&dynamicStreaming=" + dynamicStreaming + "&flashID=myExperience" + "&height=" + height + "&isVid=" + isVid + "&omnitureAccountID=" + omnitureAccountID + "&optimizedContentLoad=" + optimizedContentLoad + "&playerID=" + playerID + "&publisherID=" + publisherID + "&showcode=" + showCode + "&width=" + width +"&wmode=" + wmode

      dir.Append(WebVideoItem(truevidUrl, title=title2, subtitle=title1, summary=summary))
    return dir
