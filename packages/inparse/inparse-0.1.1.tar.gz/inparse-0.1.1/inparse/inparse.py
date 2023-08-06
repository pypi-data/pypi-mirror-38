import requests
import lxml.html
import lxml.html.clean
from lxml.cssselect import CSSSelector

from lxml import etree
from lxml.etree import tostring

import json
import pprint
from dateutil.parser import parse as date_parser

class InparseException(Exception):
     pass
class Inparse(object):

        TEST_MODE=False
        REPO_URI='http://inparse.com/api/parser?parser_no={}&access_token={}'
        TEST_REPO_URI = 'http://0.0.0.0:8080/api/parser?parser_no={}&access_token={}'
        def __init__(self,parser_no,access_token,parser_json=None):

            if parser_json:
                self.parser_json = json.loads(parser_json)
            else:
                self.parser_no=parser_no
                self.access_token=access_token
                if self.TEST_MODE:
                    url=self.TEST_REPO_URI.format(parser_no,access_token)
                else:
                    url = self.REPO_URI.format(parser_no, access_token)
                res=requests.get(url)
                self.parser_json=res.json()

            self.downloader=requests
            self.rules=self.bulid_rule_dict(self.parser_json['selectors'])
            self.rule_list=self.parser_json['selectors']


        def bulid_rule_dict(self,rl):
            rule_dict={}
            for r in rl:
                rule_dict[r['name']]=r
                if 'parent_name' not in r:
                    r['parent_name'] = None


            return rule_dict

        def parse_url(self,url):
            if url is None :
                raise InparseException('empty input')
            html = self.downloader.get(url).text
            return self.parse(html)


        def parse_item(self,doc,rules):
            result={}
            for rule in rules:
                result[rule['name']]=self.get_val_by_rule(doc, rule['selector'])

            return result

        def parse(self,html):
            if html is None :
                raise InparseException('empty input')

            htmlparser = etree.HTMLParser()
            doc = etree.HTML(html,htmlparser)


            parent_name=set()
            for id,r in self.rules.items():
                if   r['parent_name']:
                    parent_name.add(r['parent_name'])






            #basic level item
            result_nodes = self.parse_item(doc,[ r for r in self.rule_list if r['name'] not in  parent_name and r['parent_name'] is None])

            for name in parent_name:
                result_nodes[name]=[]
                rule=self.rules[name]
                sub_rule=[ r for r in self.rule_list if  r['parent_name'] == name]
                parent_nodes=self.get_val_by_rule(doc,rule['selector'])
                for node in parent_nodes:
                    item=self.parse_item(node,sub_rule)
                    result_nodes[name].append(item)




            return self.post_clean(result_nodes)

        def get_val_by_rule(self,dom,rule):
            if 'inparse.' in rule:
                func_name=rule.split('.')[1]
                return getattr(self,func_name)(dom)
            else:
                return  CSSSelector(rule)(dom)
        def table(self,doc):






            tables = doc.xpath('.//table')

            return tables
        def table_header(self,table):
            rows = []

            for thead in table.xpath('thead'):
                rows.extend(thead.xpath('./tr'))




            return rows

        def table_body(self,table):
            from_tbody = table.xpath('.//tbody//tr')
            from_root = table.xpath('./tr')

            return from_tbody + from_root

        @classmethod
        def article_clean(cls,nodes):

            ## will keep tgas
            content=''
            for n in nodes:
                content+=tostring(n,encoding='unicode')

            article_cleaner = lxml.html.clean.Cleaner()
            article_cleaner.javascript = True
            article_cleaner.style = True
            article_cleaner.safe_attrs_only=True
            article_cleaner.safe_attrs=['href','src','alt','height','width']
            article_cleaner.inline_style=True
            article_cleaner.allow_tags = [
                'a', 'span', 'p', 'br', 'strong', 'b',
                'em', 'i', 'tt', 'code', 'pre', 'blockquote', 'img', 'h1',
                'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'dl', 'dt', 'dd']
            article_cleaner.remove_unknown_tags = False
            return article_cleaner.clean_html(content)





        @classmethod
        def image_clean(cls,nodes):
            src=set()
            for n in nodes:
                if n.tag == 'img' and 'src' in n.attrib:
                    src.add(n.attrib['src'])
                else:
                    for cn in n.xpath('//img'):
                        if cn.tag == 'img' and 'src' in n.attrib:
                            src.add(n.attrib['src'])


            return list(src)


        @classmethod
        def date_clean(cls,nodes):

            for node in nodes:
                if node.xpath('//time'):
                    try:
                        text=node.xpath('//time')[0].text
                        return date_parser(text)
                    except:
                        pass

                for t in node.itertext():

                    try:

                        return date_parser(t)
                    except:
                        for tt in t.split(' '):
                            if len(tt) <6:
                                continue
                            try:
                                return date_parser(tt)
                            except:
                                pass
                        pass



        @classmethod
        def text_clean(cls,nodes):
            text=''
            for node in nodes:

                text+=' '.join(node.itertext()).strip()
            return text.strip(' ')





        @classmethod
        def table_cell_clean(cls,node):
            return ' '.join(node.itertext()).strip()
        @classmethod
        def table_clean(cls,nodes):
            result=[]
            for table in nodes:
                header=table['table_header']
                header_row=[]
                body_rows=[]
                body=table['table_body']

                if not header and body and body[0][0].tag == 'th' :

                    header.append(body.pop(0))


                    for t in header[0].xpath('./td|./th'):
                        header_row.append(cls.table_cell_clean(t))

                for row in body:
                    r=[]
                    for t in row.xpath('./td|./th'):
                        r.append(cls.table_cell_clean(t))

                    body_rows.append(r)

                result.append(

                    {
                        'table_header':header_row,
                        'table_body':body_rows
                    }
                )

            return result




        @classmethod
        def post_clean(cls,result_nodes,level=0):

            result={}
            for name,nodes in result_nodes.items():

                if 'article' in name:
                    result[name]=cls.article_clean(nodes)

                elif 'image' in name:

                    result[name] = cls.image_clean(nodes)

                elif  'date' in name:

                    result[name] = cls.date_clean(nodes)
                elif 'table' == name:
                    result[name] = cls.table_clean(nodes)
                else:

                    result[name] = cls.text_clean(nodes)


            return result

        @classmethod
        def pretty_print(cls,d):
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(d)
