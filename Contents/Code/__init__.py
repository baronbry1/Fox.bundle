PLUGIN_PREFIX               = "/video/fox"
FOX_URL                     = "http://www.fox.com"
FOX_FULL_EPISODES_SHOW_LIST = "http://www.fox.com/full-episodes/"
FOX_FEED                    = "http://www.fox.com/fod"
FOX_ART                     = "art-default.jpg"
FOX_THUMB                   = "icon-default.png"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "FOX", FOX_THUMB, FOX_ART)

  ObjectContainer.art        = R(FOX_ART)
  DirectoryObject.thumb       = R(FOX_THUMB)
  
  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-agent'] = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11"

####################################################################################################
def MainMenu():
    oc = ObjectContainer()
    content = HTML.ElementFromURL(FOX_FULL_EPISODES_SHOW_LIST)

    for item in content.xpath('//li[@class="episodeListItem"]/div[@class="showInfo"]'):
      titles = item.xpath("a")
      titleUrl = FOX_URL + titles[1].get('href')
      title = item.xpath("h3")[0].text
      summary = item.xpath("h4")[0].text

      if (titleUrl.count('americasmostwanted')) == 0:
          oc.add(DirectoryObject(key=Callback(VideoPage, pageUrl=titleUrl, title=title), title=title, summary=summary))
    return oc

####################################################################################################
def VideoPage(pageUrl):
    oc = ObjectContainer(title2=title)
    content = HTML.ElementFromURL(pageUrl)

    for episode in content.xpath('//ul[@id="fullEpisodesList"]/li[contains(@class,"episode")]'):
        details = JSON.ObjectFromString(episode.xpath('.//script[@class="videoObject"]')[0].text)
        episode_title = details['name']
        summary = details['shortDescription']
        thumbs = [details['videoStillURL'], details['thumbnailURL']]
        video_url = details['videoURL']
        duration = int(details['length'])*1000
        index = int(details['episode'])
        season = int(details['season'])
        rating = details['rating']
        date = Datetime.ParseDate(details['airdate']).date()
      
        oc.add(EpisodeObject(url=video_url, title=episode_title, show=title, summary=summary, index=index,
            season=season, duration=duration, content_rating=rating, originally_available_at=date,
            thumb=Resource.ContentsOfURLWithFallback(url=thumbs, fallback=FOX_THUMB)))
            
    return oc
