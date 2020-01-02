
class Monopoly:
    _name = 'Monopoly'
    _creator = 'Liron Revah and Baruh Shalumov'
    _page_location = None

    def __init__(self, page_loc):
        m_page_location = 'Home Page'

    def getMyName(self):
        return self._name

    def getMyCreator(self):
        return self._creator

    def getElementsXpaths(self):
        elementsXpaths = {

        }

        return elementsXpaths

    def getElementsIDs(self):
        elementsIDs = {

        }

        return elementsIDs

    def stam(self):
        x ={
            #genral
            'new game': '', # do refresh page
            'exit': '', # close browser

            #first Page
            'start': '',
            'number of players': '',
            'player name': '',
            'player color': '',
            'player type': '',

            #seconde page
            'Roll dice': '',
            'Buy label': '',
            'Manage label': '',
            'Trade label': '',
            'View status': '',
            'Turn status': '',
            'Show Card': '',
            'Card Info': '',

            #trade page
            'Propose Trade': '',
            'Cancel Trade': '',
            'Accept Trade': '',
            'Reject Trade': '',
            'Trade partner': '',
            'Offer my Money ' + 'money':'',
            'Offer partner Money ' + 'money': '',
            'Offer my ' + 'item': '',
            'Offer partner ' + 'item': '',
        }
