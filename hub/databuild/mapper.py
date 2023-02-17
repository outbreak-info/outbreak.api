import datetime

import biothings.hub.databuild.mapper as mapper

def add_date(doc):
    dates = []
    if doc.get('date'):
        dates.append(doc.get('date'))
    if doc.get('dateCreated'):
        dates.append(doc.get('dateCreated'))
    if doc.get('dateModified'):
        dates.append(doc.get('dateModified'))
    if doc.get('datePublished'):
        dates.append(doc.get('datePublished'))
    if dates:
        try:
            dates.sort()
            date = datetime.datetime.fromisoformat(dates[-1]).date().isoformat()
            doc['date'] = date
        except:
            doc['date'] = None

    return doc

class DateMapper(mapper.BaseMapper):
    def load(self):
        pass

    def process(self, docs):
        for doc in docs:
            doc_with_date = add_date(doc)
            yield doc_with_date
