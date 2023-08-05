from flask import render_template, request

class Demo:

    def __init__(self, server):
        self.__server = server
        self.add_url_rules(server.get_app())

    def add_url_rules(self, app):
        app.add_url_rule('/', 'home', self.page_home)
        app.add_url_rule('/files', 'files', self.page_files)
        app.add_url_rule('/xls/<name>', 'xls', self.page_xls)
        app.add_url_rule('/xls/<name>/<sheet>', 'xls_sheet', self.page_xls)
        app.add_url_rule('/xls/<name>/<sheet>/records', 'xls_records', self.page_xls_records)
        app.add_url_rule('/xls/<name>/<sheet>/edit', 'xls_edit', self.page_xls_edit)

    def page_home(self):
        return render_template('home.html')

    def page_files(self):
        return render_template('files.html', files=[])

    def page_xls(self, name, sheet=None):
        return render_template('xls.html', name=name, sheet=sheet)

    def page_xls_edit(self, name, sheet=None):
        return render_template('xls_edit.html', name=name, sheet=sheet)

    def page_xls_records(self, name, sheet=None):
        return render_template('records.html', name=name, sheet=sheet)
