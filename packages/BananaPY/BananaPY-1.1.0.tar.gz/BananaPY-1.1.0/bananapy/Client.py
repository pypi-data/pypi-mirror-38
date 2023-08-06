import aiohttp 


class Error(Exception):
    """
    Error that is caused when the client returns a status code other than 200 (success).
    """
    pass


class Client:
    """
    Main Client of BananAPI.

    Params:
    token (str): The BananAPI token.
    """
    def __init__(self, token, session=None):
        self.session = session or aiohttp.ClientSession()
        self.token = token
        self.base_url = "https://bananapi.ml/api/"

    async def _get(self, endpoint, params):
        """
        Private function to request from the API.
        

        This should not be called directly.
        """
        headers = { "Authorization": self.token }
        res = await self.session.get(self.base_url + endpoint, headers=headers, params=params)
        msg = ""
        if res.status != 200:
            try:
                resp = await res.json()
                msg = resp.get("message", "No message found.")
            except:
                msg = await res.text()
            raise Error("{}: {}".format(res.status, resp))
        else:
            return res

    """
    IMAGE-TEXT ENDPOINTS

    Params:

    text (str): Text to use. Check https://bananapi.ml/docs for limits. If you exceed limits, the API will return 400.
    """
        
    async def abandon(self, text):
        res = await self._get("abandon", { "text": text })
        res = await res.read()
        return res

    async def alert(self, text):
        res = await self._get("alert", { "text": text })
        res = await res.read()
        return res

    async def autism(self, text):
        res = await self._get("autism", { "text": text })
        res = await res.read()
        return res
        
    async def disabled(self, text):
        res = await self._get("disabled", { "text": text })
        res = await res.read()
        return res

    async def headache(self, text):
        res = await self._get("headache", { "text": text })
        res = await res.read()
        return res

    async def humansgood(self, text):
        res = await self._get("humansgood", { "text": text })
        res = await res.read()
        return res

    async def hurt(self, text):
        res = await self._get("hurt", { "text": text })
        res = await res.read()
        return res

    async def legends(self, text):
        res = await self._get("abandon", { "text": text })
        res = await res.read()
        return res

    async def note(self, text):
        res = await self._get("note", { "text": text })
        res = await res.read()
        return res  

    async def scroll(self, text):
        res = await self._get("scroll", { "text": text })
        res = await res.read()
        return res  

    async def sleeptight(self, text):
        res = await self._get("sleeptight", { "text": text })
        res = await res.read()
        return res  

    async def stayawake(self, text):
        res = await self._get("stayawake", { "text": text })
        res = await res.read()
        return res  

    async def trumptweet(self, text):
        res = await self._get("trumptweet", { "text": text })
        res = await res.read()
        return res  

    """
    IMAGE-IMAGE ENDPOINTS
    """

    async def peek(self, url):
        res = await self._get("peek", { "url": url })
        res = await res.read()
        return res

    async def retarded(self, url):
        res = await self._get("retarded", { "url": url })
        res = await res.read()
        return res

    async def spit(self, firstImage, secondImage):
        res = await self._get("spit", { "firstImage": firstImage, "secondImage": secondImage })
        res = await res.read()
        return res  

    """
    TEXT ENDPOINTS
    """
    async def eightball(self, question):
        res = await self._get("8ball", { "question": question })
        res = await res.json()
        return res

    async def hash(self, text):
        res = await self._get("hash", { "text": text })
        res = await res.json()
        return res

    async def jsify(self, text):
        res = await self._get("jsify", { "text": text })
        res = await res.json()
        return res

    async def mock(self, text):
        res = await self._get("mock", { "text": text })
        res = await res.json()
        return res

    async def reverse(self, text):
        res = await self._get("reverse", { "text": text })
        res = await res.json()
        return res

    async def star(self, text):
        res = await self._get("star", { "text": text })
        res = await res.json()
        return res
