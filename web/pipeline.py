from biothings.web.pipeline import ESResultTransform
import re


class ResourceTransform(ESResultTransform):

    def transform_hit(self, path, doc, options):

        if path == '':
            _index = doc.pop('_index')
            doc.pop('_type', None)    # not available by default on es7
            doc.pop('sort', None)     # added when using sort
            doc.pop('_node', None)    # added when using explain
            doc.pop('_shard', None)   # added when using explain
            if 'zenodo' in _index:
                # simplify id
                doc['_id'] = 'zenodo.' + doc.pop('_id').split('.')[-1]
                # fix fake list
                if 'keywords' in doc and len(doc['keywords']) == 1:
                    doc['keywords'] = re.split(r', |,|; |;', doc['keywords'][0])
            # add more source customizations here
