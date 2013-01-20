FOX_URL = 'http://www.fox.com'
FOX_SHOW_LIST = 'http://www.fox.com/full-episodes/'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################
def Start():

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = 'FOX'
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'

####################################################################################################
@handler('/video/fox', 'FOX', thumb=ICON, art=ART)
def MainMenu():

	oc = ObjectContainer()
	content = HTML.ElementFromURL(FOX_SHOW_LIST)

	for item in content.xpath('//li[@class="episodeListItem"]/div[@class="showInfo"]'):
		titles = item.xpath('./a')
		link = titles[1].get('href')

		if link.startswith('http'):
			title_url = link
		elif link == '':
			continue
		else:
			title_url = FOX_URL + link

		if 'americasmostwanted' in title_url:
			continue

		title = item.xpath('./h3')[0].text
		summary = item.xpath('./h4')[0].text

		oc.add(DirectoryObject(
			key = Callback(Show, url=title_url, title=title),
			title = title,
			summary = summary
		))

	return oc

####################################################################################################
@route('/video/fox/show')
def Show(url, title):

	oc = ObjectContainer(title2=title)
	content = HTML.ElementFromURL(url)

	for episode in content.xpath('//ul[@id="fullEpisodesList"]/li[contains(@class,"episode")]'):
		details = JSON.ObjectFromString(episode.xpath('.//script[@class="videoObject"]')[0].text)
		id = str(details['id'])
		episode_html = content.xpath('//li[@data-video-id="'+id+'"]')[0]
		locked = episode_html.xpath('.//span[@class="playerStatus padlock"]')

		if len(locked) > 0:
			Log("Episode Locked. Skipping")
			continue

		episode_title = details['name']
		summary = details['shortDescription']

		thumbs = []
		if details['videoStillURL']:
			thumbs.append(details['videoStillURL'])
		if details['thumbnailURL']:
			thumbs.append(details['thumbnailURL'])

		if url.endswith('/'):
			video_url = url + '%s/' % details['id']
		else:
			video_url = url + '/%s/' % details['id']

		duration = int(details['length'])*1000
		index = int(details['episode'])
		season = int(details['season'])
		rating = details['rating']
		date = Datetime.ParseDate(details['airdate']).date()

		oc.add(EpisodeObject(
			url = video_url,
			title = episode_title,
			show = title,
			summary = summary,
			index = index,
			season = season,
			duration = duration,
			content_rating = rating,
			originally_available_at = date,
			thumb = Resource.ContentsOfURLWithFallback(url=thumbs, fallback=ICON)
		))

	oc.objects.sort(key=lambda obj: obj.originally_available_at, reverse=True)
	return oc
