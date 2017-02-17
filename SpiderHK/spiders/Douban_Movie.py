import scrapy
from urllib import request
import csv
from scrapy import FormRequest

class DoubanMovieSpider(scrapy.Spider):
    # Spider for Douban Movie
    name = "Douban_Movie"
    allowed_domains = ["douban.com"]
    count = 0  # Count of the Comments
    movie_link = [
        'https://movie.douban.com/subject/1866479/',  # 《复仇者联盟》
        'https://movie.douban.com/subject/4212172/',  # 《十二生肖》
        'https://movie.douban.com/subject/1292052/',  # 《肖申克的救赎》
        'https://movie.douban.com/subject/10574622/',  # 《泰囧》
        'https://movie.douban.com/subject/25827935/',  # 《七月与安生》
        'https://movie.douban.com/subject/25662329/',  # 《疯狂动物城》
        'https://movie.douban.com/subject/25805741/',  # 《后会无期》
        'https://movie.douban.com/subject/26277313/',  # 《大圣归来》
        'https://movie.douban.com/subject/5045678/',  # 《大鱼海棠》
        'https://movie.douban.com/subject/25986180/',  # 《釜山行》
        'https://movie.douban.com/subject/6982558/',  # 《长城》
        'https://movie.douban.com/subject/26683290/',  # 《你的名字》
    ]
    writer = csv.writer(open('Douban_Avengers.csv', 'w', encoding='utf-8', newline=''))
    writer.writerow(['Number', 'Username', 'Date', 'Star', 'Comment', 'Like'])

    def start_requests(self):
        return [scrapy.Request('https://accounts.douban.com/login?source=movie', meta={'cookiejar': 1}, callback=self.douban_login)]

    def douban_login(self, response):
        # Log in Douban
        # loginurl = 'https://accounts.douban.com/login?source=movie'
        redirurl = 'https://movie.douban.com/'
        loginform = {
            'redir': redirurl,
            'form_email': list(self.userpass().items())[0][0],
            'form_password': list(self.userpass().items())[0][1],
            'login': u'登录'
        }
        print('Login Response:'+str(response))
        captcha = response.xpath('//*[@id="lzform"]/div[@class="item item-captcha"]/div/div/input[@type="hidden"]/@value').extract()
        if len(captcha) != 0:
            captcha_id = captcha[0]
            captcha_piclink = response.xpath('//*[@id="captcha_image"]/@src').extract()[0]
            request.urlretrieve(captcha_piclink, "captcha.jpg")
            captcha_solution = input('请输入验证码：')
            loginform['captcha-solution'] = captcha_solution
            loginform['captcha-id'] = captcha_id
        print('Login Form:'+str(loginform))
        return [FormRequest.from_response(response, meta={'cookiejar': response.meta['cookiejar']}, formdata=loginform, callback=self.after_login, dont_filter=True)]

    def after_login(self, response):
            yield scrapy.Request(self.movie_link[0], meta={'cookiejar': 1}, callback=self.parse_movie)

    def parse_movie(self, response):  # Parse the Movie Page
        # Jump to Short Comments
        shortcommentlink_list = response.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/@href').extract()
        yield scrapy.Request(shortcommentlink_list[0], meta={'cookiejar': 1}, callback=self.parse_shortcomment)
        # Jump to Long Comments
        pass

    def parse_shortcomment(self, response):  # Parse the Short Comments
        shortcomment_list = response.xpath('//*[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]')
        for shortcomment in shortcomment_list:
            # count
            self.count += 1
            # username
            username = shortcomment.xpath('string(h3/span[@class="comment-info"]/a)').extract()[0]
            # comment date
            date = shortcomment.xpath('string(h3/span[2]/span[3])').extract()[0]
            for tempstr in ['\n', ' ']:
                date = date.replace(tempstr, '')
            # star
            star_list = shortcomment.xpath('h3/span[2]/span[2]/@title').extract()
            if len(star_list) != 0:
                star = self.stardict().get(star_list[0])
            else:
                star = '无'
            # comment content
            comment = shortcomment.xpath('string(p)').extract()[0]
            comment = comment.replace('\n', '')
            # number of like
            like = shortcomment.xpath('string(h3/span[@class="comment-vote"]/span[1])').extract()[0]
            # output in console
            # logininfo = response.xpath('//*[@id="db-global-nav"]/div/div[1]/ul/li[2]/a/span[1]').extract()[0]
            # print(logininfo)
            print('Number:'+str(self.count))
            print('Username:'+username)
            print('Date:'+date)
            print('Star:'+star)
            print('Comment:'+comment)
            print('Like:'+like)
            print()
            data = [str(self.count), username, date, star, comment, like]
            self.writer.writerow(data)
            # write'em into a file?
        # go to next page
        nextpage_list = response.xpath('//*[@id="paginator"]/a[@class="next"]/@href').extract()
        for nextpage in nextpage_list:
            nextpage = self.movie_link[0] + 'comments' + nextpage
            yield scrapy.Request(nextpage, meta={'cookiejar': 1}, callback=self.parse_shortcomment)

    def stardict(self):  # Dict of Douban Star
        star_dict = {
            '很差': '1',
            '较差': '2',
            '还行': '3',
            '推荐': '4',
            '力荐': '5',
        }
        return star_dict

    def userpass(self):  # Dict of Douban Usernames and Passwords
        userpass_dict = {
            '361914599@qq.com': 'hdq940623',
        }
        return userpass_dict