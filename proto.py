# proto.py
import falcon

from bs4 import BeautifulSoup
import requests


class BlueCoatResource:
    BASE_URL = 'http://sitereview.bluecoat.com/rest/categorization'

    def on_get(self, req, resp):
        site = req.get_param('site') or ''
        if len(site) > 0:
            # TODO: url-encoded?
            payload = "url=" + site
            response = requests.post(self.BASE_URL, data=payload, headers={'User-Agent': 'Mozilla/5.0'})
            link = response.json()['categorization']
            bs = BeautifulSoup(link)
            cat = bs.get_text()
            resp.status = falcon.HTTP_200
            resp.body = ('CATEGORY: ' + cat)
        else:
            resp.status = falcon.HTTP_400


app = falcon.API()

bc = BlueCoatResource()

app.add_route('/bc', bc)
