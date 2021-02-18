from xbrlfactory import weaver
import inspect


class HtmlMaker:
    def __init__(self, data_pool):
        self.handlers = {
            'concept_short': self.r_concept_short,
            'concept_row': self.r_concept_row,
            'concepts': self.r_concepts,
            'base_set': self.r_base_set,
            'base_sets': self.r_base_sets
        }
        self.output = []
        self.weaver = weaver.Weaver(data_pool, self.handlers)

    def render(self, name):
        render_method = self.handlers.get(name)
        if not render_method:
            return
        render_method()

    def loop_list(self, lst, title, columns=None):
        if title:
            self.output = []  # At first recursion level initialize output
            self.html_header(title)
            self.table_header(columns)
        for obj in lst:
            if isinstance(obj, list):
                self.output.append('<tr>')
                self.loop_list(obj, None)
                self.output.append('</tr>')
                continue
            if isinstance(obj, str):
                self.output.append(f'<td>{obj}</td>')
                continue
            self.output.append('<tr>')
            if isinstance(obj, dict):
                self.loop_dict(obj, columns)
            else:
                self.loop_object(obj)
            self.output.append('</tr>')
        if title:
            self.table_footer()
            self.html_footer()

    def loop_list_row(self, lst):
        for obj in lst:
            self.loop_object(obj)

    def loop_dict(self, dct, columns):
        for c in columns:
            v = dct.get(c)
            self.output.append(f'<td>{v if v else "&nbsp;"}</td>')

    def loop_object(self, obj):
        for i in inspect.getmembers(obj):
            # Ignores anything starting with underscore
            # (that is, private and protected attributes)
            if not i[0].startswith('_'):
                # Ignores methods
                if not inspect.ismethod(i[1]):
                    self.output.append(f'<td>{i}</td>')

    def r_base_sets(self):
        self.output = []
        self.html_header('Base Sets')
        self.table_header()
        self.weaver.loop_base_sets()
        self.table_footer()
        self.html_footer()

    def r_concepts(self):
        self.output = []
        self.html_header('Concepts')
        self.table_header({
            'substitution_group': 'Substitution Group',
            'qname': 'QName',
            'label': 'Standard Label',
            'type': 'Data Type',
            'balance': 'Balance',
            'period': 'Period Type'})
        self.weaver.loop_concepts()
        self.table_footer()
        self.html_footer()

    def table_header(self, columns=None):
        self.output.append('<table border="1" cellspacing="0" cellpadding="5">')
        if not columns:
            return
        self.output.append('<tr>')
        for c in columns.items():
            self.output.append(f'<th>{c[1]}</th>')
        self.output.append('</tr>')

    def table_footer(self):
        self.output.append('</table>')

    def html_header(self, title):
        self.output.append(
            f'<html><head>'
            f'<meta charset="utf-8">'
            f'<title>{title}</title>'
            f'<style>'
            f'th {{color: #ffffa0; background-color: Navy; border-color: Silver; text-align: center;}}'
            f'</style>'
            f'</head>')
        self.output.append('<body>')

    def html_footer(self):
        self.output.append('</body>')
        self.output.append('</html>')

    def r_concept_row(self, concept, level):
        lbl = concept.get_label()
        lbltxt = lbl.text if lbl else '&nbsp;'
        self.output.append(
            f'<tr>'
            f'<td>{concept.substitution_group}</td>'
            f'<td>{concept.qname}</td>'
            f'<td nowrap>{lbltxt}</td>'
            f'<td>{concept.data_type}</td>'
            f'<td>{concept.balance}</td>'
            f'<td>{concept.period_type}</td>'
            f'</tr>')

    def r_concept_short(self, concept, level):
        lbl = concept.get_label()
        self.output.append(
            f'<tr>'
            f'<td style="text-indent: {level * 10}">{concept.qname if not lbl else lbl.text}</td>'
            f'</tr>')

    def r_base_set(self, bs, level):
        parts = bs[0].split('|')
        self.output.append(
            f'<tr style="color: White; background-color: Navy;"><td>'
            f'{parts[0]}<br/>'
            f'{parts[1]}<br/>'
            f'{parts[2]}</td></tr>')
