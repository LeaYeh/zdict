import json

from ..dictionary import DictBase
from ..exceptions import NotFoundError
from ..models import Record

class UrbanDict(DictBase):

    API = 'http://api.urbandictionary.com/v0/define?term={word}'

    @property
    def provider(self):
        return 'urban'

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record, verbose=False):
        content = json.loads(record.content)

        data = content['list'][0]

        # print word
        self.color.print(data.get('word', ''), 'yellow')

        self.color.print(
            data.get('definition', ''),
            'org',
            indent=2,
        )

        for example in data.get('example', '').split('\n'):
            self.color.print(
                example,
                'indigo',
                indent=2,
            )

        print()


    def query(self, word: str, timeout: float, verbose=False):
        content = self._get_raw(word, timeout)

        if "no_results" in content:
            raise NotFoundError(word)

        record = Record(
                    word=word,
                    content=content,
                    source=self.provider,
                 )

        return record
