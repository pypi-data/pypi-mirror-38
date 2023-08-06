import jinja2
import re
import time
from flask_debugtoolbar.panels import DebugPanel
from itertools import groupby
from sqlalchemy.engine import Engine
from sqlalchemy.event import listen


class SQLAlchemyPanel(DebugPanel):
    """SQL inspection panel for Flask Debug Toolbar.

    Shows executed database queries and helps find slow/repeated queries.

    SQL Alchemy query profiling docs:
    https://docs.sqlalchemy.org/en/latest/faq/performance.html#query-profiling
    """
    name = "SQLAlchemy Panel"
    has_content = True

    def __init__(self, jinja_env, context={}):
        super().__init__(jinja_env, context=context)

        self.queries = []

        # Add path to template loader
        self.jinja_env.loader = jinja2.ChoiceLoader([
            self.jinja_env.loader,
            jinja2.PrefixLoader({
                'sql_panel': jinja2.PackageLoader(__name__, 'templates')
            })
        ])

        # Listen to query events
        listen(Engine, "before_cursor_execute", self.before_cursor_execute)
        listen(Engine, "after_cursor_execute", self.after_cursor_execute)

    def before_cursor_execute(self, conn, cursor, statement, parameters, *args):
        conn.info.setdefault('query_start_time', []).append(time.time())

    def after_cursor_execute(self, conn, cursor, statement, parameters, *args):
        duration = time.time() - conn.info['query_start_time'].pop(-1)
        self.queries.append({
            "statement": statement,
            "parameters": parameters,
            "duration": duration * 1000,  # in milliseconds
        })

    def nav_title(self):
        return "SQLAlchemy"

    def nav_subtitle(self):
        count = len(self.queries)
        time_ms = sum(q['duration'] for q in self.queries)
        return f"{count} queries in {time_ms:.1f}ms"

    def title(self):
        return self.nav_title()

    def url(self):
        return ""

    def content(self):
        if not self.queries:
            return "No queries performed."

        return self.render('sql_panel/sql_panel.html', self.get_context_data())

    def process_request(self, request):
        """Reset queries for each request."""
        self.queries = []

    def nice_statement(self, query):
        statement = re.sub(r"\s+", " ", query['statement'])
        statement = re.sub(r"SELECT[^(]{10,}?FROM", "SELECT ... FROM", statement)

        for k, v in query['parameters'].items():
            search = f"%({k})s"
            replace = f"'{v}'" if isinstance(v, str) else str(v)
            statement = statement.replace(search, replace)

        return statement

    def get_context_data(self):
        queries = self.queries
        total_duration = sum(q['duration'] for q in queries)
        repeated_counts = self.get_repeated_statements(queries)

        for query in queries:
            query['perc_of_total'] = 100 * query['duration'] / total_duration
            query['nice_statement'] = self.nice_statement(query)
            query['repeat_count'] = repeated_counts[query['statement']]

        return {
            "queries": queries,
            "total_duration": total_duration,
        }

    def get_repeated_statements(self, queries):
        """Finds statements repeated multiple times, possibly with different
        parameters. Returns a dict of {statement: repeat_count}."""
        def _sort_key(query):
            return query['statement']

        sorted_queries = sorted(queries, key=_sort_key)
        groups = groupby(sorted_queries, key=_sort_key)
        return {k: len(list(v)) for k, v in groups}
