# Copyright 2018 by Teradata Corporation. All rights reserved.

from itertools import groupby
from sqlalchemy import pool, String, Numeric
from sqlalchemy import Table, Column, Index
from sqlalchemy.engine import default
from sqlalchemy.sql import select, and_, or_
from sqlalchemy.sql.expression import text, table, column, asc
from teradatasqlalchemy.base import TeradataIdentifierPreparer, TeradataExecutionContext
from teradatasqlalchemy.resolver import TeradataTypeResolver

from sqlalchemy import exc
from sqlalchemy.sql import compiler

import teradatasqlalchemy as sqlalch_td
import sqlalchemy.types as sqltypes
import teradatasqlalchemy.types as tdtypes

import json


# ischema names is used for reflecting columns (see get_columns in the dialect)
ischema_names = {

    # SQL standard types (modified only to extend _TDComparable)
    'I' : tdtypes.INTEGER,
    'I2': tdtypes.SMALLINT,
    'I8': tdtypes.BIGINT,
    'D' : tdtypes.DECIMAL,
    'DA': tdtypes.DATE,

    # Numeric types
    'I1': tdtypes.BYTEINT,
    'F' : tdtypes.FLOAT,
    'N' : tdtypes.NUMBER,

    # Character types
    'CF': tdtypes.CHAR,
    'CV': tdtypes.VARCHAR,
    'CO': tdtypes.CLOB,

    # Datetime types
    'TS': tdtypes.TIMESTAMP,
    'SZ': tdtypes.TIMESTAMP,    # Timestamp with timezone
    'AT': tdtypes.TIME,
    'TZ': tdtypes.TIME,         # Time with timezone

    # Binary types
    'BF': tdtypes.BYTE,
    'BV': tdtypes.VARBYTE,
    'BO': tdtypes.BLOB,

    # Interval types
    'DH': tdtypes.INTERVAL_DAY_TO_HOUR,
    'DM': tdtypes.INTERVAL_DAY_TO_MINUTE,
    'DS': tdtypes.INTERVAL_DAY_TO_SECOND,
    'DY': tdtypes.INTERVAL_DAY,
    'HM': tdtypes.INTERVAL_HOUR_TO_MINUTE,
    'HR': tdtypes.INTERVAL_HOUR,
    'HS': tdtypes.INTERVAL_HOUR_TO_SECOND,
    'MI': tdtypes.INTERVAL_MINUTE,
    'MO': tdtypes.INTERVAL_MONTH,
    'MS': tdtypes.INTERVAL_MINUTE_TO_SECOND,
    'SC': tdtypes.INTERVAL_SECOND,
    'YM': tdtypes.INTERVAL_YEAR_TO_MONTH,
    'YR': tdtypes.INTERVAL_YEAR,

    # Period types
    'PD': tdtypes.PERIOD_DATE,
    'PT': tdtypes.PERIOD_TIME,
    'PZ': tdtypes.PERIOD_TIME,
    'PS': tdtypes.PERIOD_TIMESTAMP,
    'PM': tdtypes.PERIOD_TIMESTAMP
}

stringtypes=[ t for t in ischema_names if issubclass(ischema_names[t],sqltypes.String)]

class TeradataCompiler(compiler.SQLCompiler):

    def __init__(self, dialect, statement, column_keys=None, inline=False, **kwargs):
        super(TeradataCompiler, self).__init__(dialect, statement, column_keys, inline, **kwargs)

    def get_select_precolumns(self, select, **kwargs):
        """
        handles the part of the select statement before the columns are specified.
        Note: Teradata does not allow a 'distinct' to be specified when 'top' is
              used in the same select statement.

              Instead if a user specifies both in the same select clause,
              the DISTINCT will be used with a ROW_NUMBER OVER(ORDER BY) subquery.
        """

        pre = select._distinct and "DISTINCT " or ""

        #TODO: decide whether we can replace this with the recipe...
        if (select._limit is not None and select._offset is None):
            pre += "TOP %d " % (select._limit)

        return pre

    def visit_mod_binary(self, binary, operator, **kw):
        return self.process(binary.left, **kw) + " MOD " + \
            self.process(binary.right, **kw)

    def visit_ne_binary(self, binary, operator, **kw):
        return self.process(binary.left, **kw) + " <> " + \
            self.process(binary.right, **kw)

    def limit_clause(self, select, **kwargs):
        """Limit after SELECT is implemented in get_select_precolumns"""
        return ""

class TeradataDDLCompiler(compiler.DDLCompiler):

    def visit_create_index(self, create, include_schema=False,
                           include_table_schema=True):
        index = create.element
        self._verify_index_table(index)
        preparer = self.preparer
        text = "CREATE "
        if index.unique:
            text += "UNIQUE "
        text += "INDEX %s (%s) ON %s" \
            % (
                self._prepared_index_name(index,
                                          include_schema=include_schema),
                ', '.join(
                    self.sql_compiler.process(
                        expr, include_table=False, literal_binds=True) for
                    expr in index.expressions),
                preparer.format_table(index.table,
                                      use_schema=include_table_schema)
            )
        return text

    def create_table_suffix(self, table):
        """
        This hook processes the optional keyword teradata_suffixes
        ex.
        from teradatasqlalchemy.compiler import\
                        TDCreateTableSuffix as Opts
        t = Table( 'name', meta,
                   ...,
                   teradata_suffixes=Opts.
                                      fallback().
                                      log().
                                      with_journal_table(t2.name)

        CREATE TABLE name, fallback,
        log,
        with journal table = [database/user.]table_name(
          ...
        )

        teradata_suffixes can also be a list of strings to be appended
        in the order given.
        """
        post=table.dialect_kwargs['teradatasql_suffixes']

        if isinstance(post, TDCreateTableSuffix):
            if post.opts:
                return ',\n' + post.compile()
            else:
                return post
        elif post:
            assert type(post) is list
            res = ',\n ' + ',\n'.join(post)
        else:
            return ''

    def post_create_table(self, table):

        """
        This hook processes the TDPostCreateTableOpts given by the
        teradata_post_create dialect kwarg for Table.

        Note that there are other dialect kwargs defined that could possibly
        be processed here.

        See the kwargs defined in dialect.TeradataDialect

        Ex.
        from teradatasqlalchemy.compiler import TDCreateTablePost as post
        Table('t1', meta,
               ...
               ,
               teradata_post_create = post().
                                        fallback().
                                        checksum('on').
                                        mergeblockratio(85)

        creates ddl for a table like so:

        CREATE TABLE "t1" ,
             checksum=on,
             fallback,
             mergeblockratio=85 (
               ...
        )

        """
        kw = table.dialect_kwargs['teradatasql_post_create']
        if isinstance(kw, TDCreateTablePost):
            if kw:
              return '\n' + kw.compile()
        return ''

    def get_column_specification(self, column, **kwargs):

        if column.table is None:
            raise exc.CompileError(
                "Teradata requires Table-bound columns "
                "in order to generate DDL")

        colspec = (self.preparer.format_column(column) + " " +\
                        self.dialect.type_compiler.process(
                          column.type, type_expression=column))

        # Null/NotNull
        if column.nullable is not None:
            if not column.nullable or column.primary_key:
                colspec += " NOT NULL"

        return colspec

class TeradataTypeCompiler(compiler.GenericTypeCompiler):

    def _get(self, key, type_, kw):
        return kw.get(key, getattr(type_, key, None))

    def visit_datetime(self, type_, **kw):
        return self.visit_TIMESTAMP(type_, precision=6, **kw)

    def visit_date(self, type_, **kw):
        return self.visit_DATE(type_, **kw)

    def visit_text(self, type_, **kw):
        return self.visit_CLOB(type_, **kw)

    def visit_time(self, type_, **kw):
        return self.visit_TIME(type_, precision=6, **kw)

    def visit_unicode(self, type_, **kw):
        return self.visit_VARCHAR(type_, charset='UNICODE', **kw)

    def visit_unicode_text(self, type_, **kw):
        return self.visit_CLOB(type_, charset='UNICODE', **kw)

    def visit_boolean(self, type_, **kw):
        return self.visit_BYTEINT(type_, **kw)

    def visit_INTERVAL_YEAR(self, type_, **kw):
        return 'INTERVAL YEAR{}'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_YEAR_TO_MONTH(self, type_, **kw):
        return 'INTERVAL YEAR{} TO MONTH'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_MONTH(self, type_, **kw):
        return 'INTERVAL MONTH{}'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_DAY(self, type_, **kw):
        return 'INTERVAL DAY{}'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_DAY_TO_HOUR(self, type_, **kw):
        return 'INTERVAL DAY{} TO HOUR'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_DAY_TO_MINUTE(self, type_, **kw):
        return 'INTERVAL DAY{} TO MINUTE'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_DAY_TO_SECOND(self, type_, **kw):
        return 'INTERVAL DAY{} TO SECOND{}'.format(
            '('+str(type_.precision)+')' if type_.precision else '',
            '('+str(type_.frac_precision)+')' if type_.frac_precision is not None  else '')

    def visit_INTERVAL_HOUR(self, type_, **kw):
        return 'INTERVAL HOUR{}'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_HOUR_TO_MINUTE(self, type_, **kw):
        return 'INTERVAL HOUR{} TO MINUTE'.format(
            '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_HOUR_TO_SECOND(self, type_, **kw):
        return 'INTERVAL HOUR{} TO SECOND{}'.format(
            '('+str(type_.precision)+')' if type_.precision else '',
            '('+str(type_.frac_precision)+')' if type_.frac_precision is not None else '')

    def visit_INTERVAL_MINUTE(self, type_, **kw):
        return 'INTERVAL MINUTE{}'.format(
              '('+str(type_.precision)+')' if type_.precision else '')

    def visit_INTERVAL_MINUTE_TO_SECOND(self, type_, **kw):
        return 'INTERVAL MINUTE{} TO SECOND{}'.format(
            '('+str(type_.precision)+')' if type_.precision else '',
            '('+str(type_.frac_precision)+')' if type_.frac_precision is not None else '')

    def visit_INTERVAL_SECOND(self, type_, **kw):
        if type_.frac_precision is not None and type_.precision:
          return 'INTERVAL SECOND{}'.format(
              '('+str(type_.precision)+', '+str(type_.frac_precision)+')')
        else:
          return 'INTERVAL SECOND{}'.format(
              '('+str(type_.precision)+')' if type_.precision else '')

    def visit_PERIOD_DATE(self, type_, **kw):
        return 'PERIOD(DATE)' +\
            (" FORMAT '" + type_.format + "'" if type_.format is not None else '')

    def visit_PERIOD_TIME(self, type_, **kw):
        return 'PERIOD(TIME{}{})'.format(
                '(' + str(type_.frac_precision) + ')'
                    if type_.frac_precision is not None
                    else '',
                ' WITH TIME ZONE' if type_.timezone else '') +\
            (" FORMAT '" + type_.format + "'" if type_.format is not None else '')

    def visit_PERIOD_TIMESTAMP(self, type_, **kw):
        return 'PERIOD(TIMESTAMP{}{})'.format(
                '(' + str(type_.frac_precision) + ')'
                    if type_.frac_precision is not None
                    else '',
                ' WITH TIME ZONE' if type_.timezone else '') +\
            (" FORMAT '" + type_.format + "'" if type_.format is not None else '')

    def visit_TIME(self, type_, **kw):
        tz = ' WITH TIME ZONE' if type_.timezone else ''
        prec = self._get('precision', type_, kw)
        prec = '%s' % '('+str(prec)+')' if prec is not None else ''
        return 'TIME{}{}'.format(prec, tz)

    def visit_TIMESTAMP(self, type_, **kw):
        tz = ' WITH TIME ZONE' if type_.timezone else ''
        prec = self._get('precision', type_, kw)
        prec = '%s' % '('+str(prec)+')' if prec is not None else ''
        return 'TIMESTAMP{}{}'.format(prec, tz)

    def _string_process(self, type_, datatype, **kw):
        length = self._get('length', type_, kw)
        length = '(%s)' % length if length is not None  else ''

        charset = self._get('charset', type_, kw)
        charset = ' CHAR SET %s' % charset if charset is not None else ''

        res = '{}{}{}'.format(datatype, length, charset)
        return res

    def visit_CHAR(self, type_, **kw):
        return self._string_process(type_, 'CHAR', length=type_.length, **kw)

    def visit_VARCHAR(self, type_, **kw):
        if type_.length is None:
            return self._string_process(type_, 'LONG VARCHAR', **kw)
        else:
            return self._string_process(type_, 'VARCHAR', length=type_.length, **kw)

    def visit_CLOB(self, type_, **kw):
        multi = self._get('multiplier', type_, kw)
        if multi is not None and type_.length is not None:
            length = str(type_.length) + multi
            return self._string_process(type_, 'CLOB', length=length, **kw)

        return self._string_process(type_, 'CLOB', **kw)

    def visit_BYTEINT(self, type_, **kw):
        return 'BYTEINT'

    def visit_BYTE(self, type_, **kw):
        return 'BYTE{}'.format(
            '(' + str(type_.length) + ')' if type_.length is not None else '')

    def visit_VARBYTE(self, type_, **kw):
        return 'VARBYTE{}'.format(
            '(' + str(type_.length) + ')' if type_.length is not None else '')

    def visit_BLOB(self, type_, **kw):
        multiplier = self._get('multiplier', type_, kw)
        return 'BLOB{}'.format(
            '(' + str(type_.length) + \
                '{})'.format(multiplier if multiplier is not None else '')
            if type_.length is not None else '')

    def visit_NUMBER(self, type_, **kw):
        args = (str(type_.precision), '') if type_.scale is None \
               else (str(type_.precision), ', ' + str(type_.scale))
        return 'NUMBER{}'.format(
            '' if type_.precision is None else '({}{})'.format(*args))


class TeradataDialect(default.DefaultDialect):

    name = 'teradatasql'
    driver = 'teradatasql'
    paramstyle = 'qmark'
    default_paramstyle = 'qmark'
    poolclass = pool.SingletonThreadPool

    statement_compiler = TeradataCompiler
    ddl_compiler = TeradataDDLCompiler
    type_compiler = TeradataTypeCompiler
    preparer = TeradataIdentifierPreparer
    execution_ctx_cls = TeradataExecutionContext

    supports_native_boolean = False
    supports_native_decimal = True
    supports_unicode_statements = True
    supports_unicode_binds = True
    postfetch_lastrowid = False
    implicit_returning = False
    preexecute_autoincrement_sequences = False
    case_sensitive = False

    construct_arguments = [
      (Table, {
          "post_create": None,
          "suffixes": None
       }),

      (Index, {
          "order_by": None,
          "loading": None
       }),

      (Column, {
          "compress": None,
          "identity": None
      })
    ]

    def __init__(self, **kwargs):
        super(TeradataDialect, self).__init__(**kwargs)


    def create_connect_args(self, url):

        params = super(TeradataDialect, self).create_connect_args(url)[1]

        if 'username' in params:
            sUserName = params.pop ('username')
            if 'user' not in params: # user URL parameter has higher priority than username prefix before host
                params ['user'] = sUserName

        if 'port' in params:
          params['dbs_port'] = str(params['port'])
          del params['port']

        args = json.dumps(params), # single-element tuple
        kwargs = {}
        return (args, kwargs)



    @classmethod
    def dbapi(cls):

        """ Hook to the dbapi2.0 implementation's module"""
        import teradatasql
        return teradatasql

    def normalize_name(self, name, **kw):
        if name is not None:
            return name.strip()
        return name

    def _cast_name(self, name, **kw):
        if name is not None:
            return 'CAST(TRANSLATE({} USING UNICODE_TO_LATIN) as VARCHAR(128))'.format(name)
        return name

    def has_table(self, connection, table_name, schema=None):

        if schema is None:
            schema=self.default_schema_name

        stmt = select([column('tablename')],
                      from_obj=[text('dbc.tablesvx')]).where(
                        and_(text('DatabaseName (NOT CASESPECIFIC) = ' + self._cast_name(':schema') + ' (NOT CASESPECIFIC)'),
                             text('TableName=:table_name')))

        res = connection.execute(stmt, schema=schema, table_name=table_name).fetchone()
        return res is not None

    def _resolve_type(self, t, **kw):
        """
        Resolves the types for String, Numeric, Date/Time, etc. columns.
        """
        tc = self.normalize_name(t)
        if tc in ischema_names:
            type_ = ischema_names[tc]
            return TeradataTypeResolver().process(type_, typecode=tc, **kw)

        return sqltypes.NullType

    def _get_column_info(self, row):
        """
        Resolves the column information for get_columns given a row.
        """
        chartype = {
            0: None,
            1: 'LATIN',
            2: 'UNICODE',
            3: 'KANJISJIS',
            4: 'GRAPHIC'
        }

        # Handle unspecified characterset and disregard chartypes specified for
        # non-character types (e.g. binary, json)
        character_set = row['CharType'] if self.normalize_name(row['ColumnType']) in stringtypes else 0
        typ = self._resolve_type(row['ColumnType'],
                                  length=int(row['ColumnLength'] or 0),
                                  chartype=chartype[character_set],
                                  prec=int(row['DecimalTotalDigits'] or 0),
                                  scale=int(row['DecimalFractionalDigits'] or 0),
                                  fmt=row['ColumnFormat'])

        autoinc = row['IdColType'] in ('GA', 'GD')

        # attrs contains all the attributes queried from DBC.ColumnsV
        attrs    = {self.normalize_name(k): row[k] for k in row.keys()}
        col_info = {
            'name': self.normalize_name(row['ColumnName']),
            'type': typ,
            'nullable': row['Nullable'] == u'Y',
            'default': None,
            'autoincrement': autoinc
        }

        return dict(attrs, **col_info)

    def get_columns(self, connection, table_name, schema=None, **kw):

        if schema is None:
            schema = self.default_schema_name

        # TODO: consider using help schema.table.* statements
        # Check if the object is a view
        schema_name = self._cast_name(':schema')
        stmt = select([column('tablekind')], from_obj=text('dbc.tablesV')).where(
                    and_(text('DatabaseName (NOT CASESPECIFIC) = ' + schema_name + ' (NOT CASESPECIFIC)'),
                         text('TableName=:table_name'),
                         text("tablekind='V'")))

        res = connection.execute(stmt, schema=schema, table_name=table_name).rowcount
        isView = (res == 1)

        stmt = select(['*'], from_obj=text('dbc.ColumnsV')).where(
            and_(text('DatabaseName (NOT CASESPECIFIC) = ' + schema_name + ' (NOT CASESPECIFIC)'),
                 text('TableName=:table_name')))

        res = connection.execute(stmt, schema=schema, table_name=table_name).fetchall()

        # If this is a view, get types for individual columns (dbc.ColumnsV won't have types for view columns)
        if isView:
            res = [dict(r, **(self._get_column_help(
                connection, schema, table_name, r['ColumnName']))) for r in res]


        return [self._get_column_info(row) for row in res]


    def _get_default_schema_name(self, connection):
        res =  self.normalize_name(
               connection.execute('select database').scalar())
        return res

    def _get_column_help(self, connection, schema, table_name, column_name):

        prepared = preparer(dialect())
        stmt = 'help column ' + prepared.quote(schema) + '.' + prepared.quote(table_name) + '.' + prepared.quote(column_name)
        res  = connection.execute(stmt).fetchall()[0]

        return {
            'ColumnName': res['Column Name'],
            'ColumnType': res['Type'],
            'ColumnLength': res['Max Length'],
            'CharType': res['Char Type'],
            'DecimalTotalDigits': res['Decimal Total Digits'],
            'DecimalFractionalDigits': res['Decimal Fractional Digits'],
            'ColumnFormat': res['Format'],
            'Nullable': res['Nullable'],
            'DefaultValue': None,
            'IdColType': res['IdCol Type']
        }

    def get_table_names(self, connection, schema=None, **kw):

        if schema is None:
            schema = self.default_schema_name

        stmt = select([column('tablename')],
                      from_obj=[text('dbc.TablesVX')]).where(
                      and_(text('DatabaseName (NOT CASESPECIFIC) = ' + self._cast_name(':schema') + ' (NOT CASESPECIFIC)'),
                          or_(text('tablekind=\'T\''),
                              text('tablekind=\'O\''))))
        res = connection.execute(stmt, schema=schema).fetchall()
        return [self.normalize_name(name['tablename']) for name in res]

    def get_schema_names(self, connection, **kw):
        stmt = select([column('username')],
               from_obj=[text('dbc.UsersV')],
               order_by=[text('username')])
        res = connection.execute(stmt).fetchall()
        return [self.normalize_name(name['username']) for name in res]

    def get_view_definition(self, connection, view_name, schema=None, **kw):

        if schema is None:
             schema = self.default_schema_name

        res = connection.execute('show table {}.{}'.format(schema, view_name)).scalar()
        return self.normalize_name(res)

    def get_view_names(self, connection, schema=None, **kw):

        if schema is None:
            schema = self.default_schema_name

        stmt = select([column('tablename')],
                      from_obj=[text('dbc.TablesVX')]).where(
                      and_(text('DatabaseName (NOT CASESPECIFIC) = ' + self._cast_name(':schema') + ' (NOT CASESPECIFIC)'),
                           text('tablekind=\'V\'')))

        res = connection.execute(stmt, schema=schema).fetchall()
        return [self.normalize_name(name['tablename']) for name in res]

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        """
        Override
        TODO: Check if we need PRIMARY Indices or PRIMARY KEY Indices
        TODO: Check for border cases (No PK Indices)
        """

        if schema is None:
            schema = self.default_schema_name

        stmt = select([column('ColumnName'), column('IndexName')],
                      from_obj=[text('dbc.Indices')]).where(
                          and_(text('DatabaseName (NOT CASESPECIFIC) = ' + self._cast_name(':schema') + ' (NOT CASESPECIFIC)'),
                              text('TableName=:table'),
                              text('IndexType=:indextype'))
                      ).order_by(asc(column('IndexNumber')))

        # K for Primary Key
        res = connection.execute(stmt, schema=schema, table=table_name, indextype='K').fetchall()

        index_columns = list()
        index_name = None

        for index_column in res:
            index_columns.append(self.normalize_name(index_column['ColumnName']))
            index_name = self.normalize_name(index_column['IndexName']) # There should be just one IndexName

        return {
            "constrained_columns": index_columns,
            "name": index_name
        }

    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        """
        Overrides base class method
        """
        if schema is None:
            schema = self.default_schema_name

        stmt = select([column('ColumnName'), column('IndexName')], from_obj=[text('dbc.Indices')]) \
            .where(and_(text('DatabaseName (NOT CASESPECIFIC) = ' + self._cast_name(':schema') + ' (NOT CASESPECIFIC)'),
                        text('TableName=:table'),
                        text('IndexType=:indextype'))) \
            .order_by(asc(column('IndexName')))

        # U for Unique
        res = connection.execute(stmt, schema=schema, table=table_name, indextype='U').fetchall()

        def grouper(fk_row):
            return {
                'name': self.normalize_name(fk_row['IndexName']),
            }

        unique_constraints = list()
        for constraint_info, constraint_cols in groupby(res, grouper):
            unique_constraint = {
                'name': self.normalize_name(constraint_info['name']),
                'column_names': list()
            }

            for constraint_col in constraint_cols:
                unique_constraint['column_names'].append(self.normalize_name(constraint_col['ColumnName']))

            unique_constraints.append(unique_constraint)

        return unique_constraints

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        """
        Overrides base class method
        """

        if schema is None:
            schema = self.default_schema_name

        stmt = select([column('IndexID'), column('IndexName'), column('ChildKeyColumn'), column('ParentDB'),
                       column('ParentTable'), column('ParentKeyColumn')],
                      from_obj=[text('DBC.All_RI_ChildrenV')]) \
            .where(and_(text('ChildTable = :table'),
                        text('ChildDB = :schema'))) \
            .order_by(asc(column('IndexID')))

        res = connection.execute(stmt, schema=schema, table=table_name).fetchall()

        def grouper(fk_row):
            return {
                'name': fk_row.IndexName or fk_row.IndexID, #ID if IndexName is None
                'schema': fk_row.ParentDB,
                'table': fk_row.ParentTable
            }

        # TODO: Check if there's a better way
        fk_dicts = list()
        for constraint_info, constraint_cols in groupby(res, grouper):
            fk_dict = {
                'name': constraint_info['name'],
                'constrained_columns': list(),
                'referred_table': constraint_info['table'],
                'referred_schema': constraint_info['schema'],
                'referred_columns': list()
            }

            for constraint_col in constraint_cols:
                fk_dict['constrained_columns'].append(self.normalize_name(constraint_col['ChildKeyColumn']))
                fk_dict['referred_columns'].append(self.normalize_name(constraint_col['ParentKeyColumn']))

            fk_dicts.append(fk_dict)

        return fk_dicts

    def get_indexes(self, connection, table_name, schema=None, **kw):
        """
        Overrides base class method
        """

        if schema is None:
            schema = self.default_schema_name

        stmt = select(["*"], from_obj=[text('dbc.Indices')]) \
            .where(and_(text('DatabaseName (NOT CASESPECIFIC) = ' + self._cast_name(':schema') + ' (NOT CASESPECIFIC)'),
                        text('TableName=:table'))) \
            .order_by(asc(column('IndexName')))

        res = connection.execute(stmt, schema=schema, table=table_name).fetchall()

        def grouper(fk_row):
            return {
                'name': fk_row.IndexName or fk_row.IndexNumber, # If IndexName is None TODO: Check what to do
                'unique': True if fk_row.UniqueFlag == 'Y' else False
            }

        # TODO: Check if there's a better way
        indices = list()
        for index_info, index_cols in groupby(res, grouper):
            index_dict = {
                'name': index_info['name'],
                'column_names': list(),
                'unique': index_info['unique']
            }

            for index_col in index_cols:
                index_dict['column_names'].append(self.normalize_name(index_col['ColumnName']))

            indices.append(index_dict)

        return indices

    def get_transaction_mode(self, connection, **kw):
        """
        Returns the transaction mode set for the current session.
        T = TDBS
        A = ANSI
        """
        stmt = select([text('transaction_mode')],\
                from_obj=[text('dbc.sessioninfov')]).\
                where(text('sessionno=SESSION'))

        res = connection.execute(stmt).scalar()
        return res

    def _get_server_version_info(self, connection, **kw):
        """
        Returns the Teradata Database software version.
        """
        stmt = select([text('InfoData')],\
                from_obj=[text('dbc.dbcinfov')]).\
                where(text('InfoKey=\'VERSION\''))

        res = connection.execute(stmt).scalar()
        return res

    def conn_supports_autocommit(self, connection, **kw):
        """
        Returns True if autocommit is used for this connection (underlying Teradata session)
        else False
        """
        return self.get_transaction_mode(connection) == 'T'

dialect = TeradataDialect
preparer = TeradataIdentifierPreparer
compiler = TeradataCompiler

class TeradataOptions(object):
    """
    An abstract base class for various schema object options
    """
    _prepare = preparer(dialect())
    def _append(self, opts, val):
        _opts=opts.copy()
        _opts.update(val)
        return _opts

    def compile(self, **kw):
        """
        processes the argument options and returns a string representation
        """
        pass

    def format_cols(self, key, val, **kw):

        """
        key is a string
        val is a list of strings with an optional dict as the last element
            the dict values are appended at the end of the col list
        """
        res = ''
        col_expr = ', '.join([x for x in val if type(x) is str])

        res += key + '( ' + col_expr + ' )'
        if type(val[-1]) is dict:
            # process syntax elements (dict) after cols
            res += ' '.join( val[-1]['post'] )
        return res

class TDCreateTableSuffix(TeradataOptions):
    """
    A generative class for Teradata create table options
    specified in teradata_suffixes
    """
    def __init__(self, opts={}, **kw):
        """
        opts is a dictionary that can be pre-populated with key-value pairs
        that may be overidden if the keys conflict with those entered
        in the methods below. See the compile method to see how the dict
        gets processed.
        """
        self.opts = opts

    def compile(self):
        def process_opts(opts):
            return [key if opts[key] is None else '{}={}'.\
                            format(key, opts[key]) for key in opts]

        res = ',\n'.join(process_opts(self.opts))
        return res

    def fallback(self, enabled=True):
        res = 'fallback' if enabled else 'no fallback'
        return self.__class__(self._append(self.opts, {res:None}))

    def log(self, enabled=True):
        res = 'log' if enabled else 'no log'
        return self.__class__(self._append(self.opts, {res:None}))

    def with_journal_table(self, tablename=None):
        """
        tablename is the schema.tablename of a table.
        For example, if t1 is a SQLAlchemy:
                with_journal_table(t1.name)
        """
        return self.__class__(self._append(self.opts,\
                        {'with journal table':tablename}))

    def before_journal(self, prefix='dual'):
        """
        prefix is a string taking vaues of 'no' or 'dual'
        """
        assert prefix in ('no', 'dual')
        res = prefix+' '+'before journal'
        return self.__class__(self._append(self.opts, {res:None}))

    def after_journal(self, prefix='not local'):
        """
        prefix is a string taking vaues of 'no', 'dual', 'local',
        or 'not local'.
        """
        assert prefix in ('no', 'dual', 'local', 'not local')
        res = prefix+' '+'after journal'
        return self.__class__(self._append(self.opts, {res:None}))

    def checksum(self, integrity_checking='default'):
        """
        integrity_checking is a string taking vaues of 'on', 'off',
        or 'default'.
        """
        assert integrity_checking in ('on', 'off', 'default')
        return self.__class__(self._append(self.opts,\
                        {'checksum':integrity_checking}))

    def freespace(self, percentage=0):
        """
        percentage is an integer taking values from 0 to 75.
        """
        return self.__class__(self._append(self.opts,\
                        {'freespace':percentage}))

    def no_mergeblockratio(self):
        return self.__class__(self._append(self.opts,\
                        {'no mergeblockratio':None}))

    def mergeblockratio(self, integer=None):
        """
        integer takes values from 0 to 100 inclusive.
        """
        res = 'default mergeblockratio' if integer is None\
                                        else 'mergeblockratio'
        return self.__class__(self._append(self.opts, {res:integer}))

    def min_datablocksize(self):
            return self.__class__(self._append(self.opts,\
                            {'minimum datablocksize':None}))

    def max_datablocksize(self):
        return self.__class__(self._append(self.opts,\
                        {'maximum datablocksize':None}))

    def datablocksize(self, data_block_size=None):
        """
        data_block_size is an integer specifying the number of bytes
        """
        res = 'datablocksize' if data_block_size is not None\
                              else 'default datablocksize'
        return self.__class__(self._append(self.opts,\
                                           {res:data_block_size}))

    def blockcompression(self, opt='default'):
        """
        opt is a string that takes values 'autotemp',
        'default', 'manual', or 'never'
        """
        return self.__class__(self._append(self.opts,\
                        {'blockcompression':opt}))

    def with_no_isolated_loading(self, concurrent=False):
        res = 'with no ' +\
            ('concurrent ' if concurrent else '') +\
            'isolated loading'
        return self.__class__(self._append(self.opts, {res:None}))

    def with_isolated_loading(self, concurrent=False, opt=None):
        """
        opt is a string that takes values 'all', 'insert', 'none',
        or None
        """
        assert opt in ('all', 'insert', 'none', None)
        for_stmt = ' for ' + opt if opt is not None else ''
        res = 'with ' +\
            ('concurrent ' if concurrent else '') +\
            'isolated loading' + for_stmt
        return self.__class__(self._append(self.opts, {res:None}))


class TDCreateTablePost(TeradataOptions):
    """
    A generative class for building post create table options
    given in the teradata_post_create keyword for Table
    """
    def __init__(self, opts={}, **kw):
        self.opts = opts

    def compile(self, **kw):
        def process(opts):
            return [key.upper() if opts[key] is None\
                       else self.format_cols(key, opts[key], **kw)\
                       for key in opts]

        return ',\n'.join(process(self.opts))

    def no_primary_index(self):
        return self.__class__(self._append(self.opts, {'no primary index':None}))

    def primary_index(self, name=None, unique=False, cols=[]):
        """
        name is a string for the primary index
        if unique is true then unique primary index is specified
        cols is a list of column names
        """
        res = 'unique primary index' if unique else 'primary index'
        res += ' ' + name if name is not None else ''
        return self.__class__(self._append(self.opts, {res:[self._prepare.quote(c) for c in cols if c is not None]}))

    def primary_amp(self, name=None, cols=[]):

        """
        name is an optional string for the name of the amp index
        cols is a list of column names (strings)
        """
        res = 'primary amp index'
        res += ' ' + name if name is not None else ''
        return self.__class__(self._append(self.opts, {res:[self._prepare.quote(c) for c in cols if c is not None]}))


    def partition_by_col(self, all_but=False, cols={}, rows={}, const=None):

        """
        ex:

        Opts.partition_by_col(cols ={'c1': True, 'c2': False, 'c3': None},
                     rows ={'d1': True, 'd2':False, 'd3': None},
                     const = 1)
        will emit:

        partition by(
          column(
            column(c1) auto compress,
            column(c2) no auto compress,
            column(c3),
            row(d1) auto compress,
            row(d2) no auto compress,
            row(d3))
            add 1
            )

        cols is a dictionary whose key is the column name and value True or False
        specifying AUTO COMPRESS or NO AUTO COMPRESS respectively. The columns
        are stored with COLUMN format.

        rows is a dictionary similar to cols except the ROW format is used

        const is an unsigned BIGINT
        """
        res = 'partition by( column all but' if all_but else\
                        'partition by( column'
        c = self._visit_partition_by(cols, rows)
        c += [{'post': (['add %s' % str(const)]
            if const is not None
            else []) + [')']}]

        return self.__class__(self._append(self.opts, {res: c}))

    def _visit_partition_by(self, cols, rows):

        if cols:
            c = ['column('+ self._prepare.quote(k) +') auto compress '\
                            for k,v in cols.items() if v is True]

            c += ['column('+ self._prepare.quote(k) +') no auto compress'\
                            for k,v in cols.items() if v is False]

            c += ['column('+ self._prepare.quote(k) +')' for k,v in cols.items() if v is None]

        if rows:
            c += ['row('+ k +') auto compress'\
                            for k,v in rows.items() if v is True]

            c += ['row('+ k +') no auto compress'\
                            for k,v in rows.items() if v is False]

            c += ['row('+ k +')' for k,v in rows.items() if v is None]

        return c

    def partition_by_col_auto_compress(self, all_but=False, cols={},\
                                       rows={}, const=None):

        res = 'partition by( column auto compress all but' if all_but else\
                        'partition by( column auto compress'
        c = self._visit_partition_by(cols,rows)
        c += [{'post': (['add %s' % str(const)]
            if const is not None
            else []) + [')']}]

        return self.__class__(self._append(self.opts, {res: c}))


    def partition_by_col_no_auto_compress(self, all_but=False, cols={},\
                                          rows={}, const=None):

        res = 'partition by( column no auto compress all but' if all_but else\
                        'partition by( column no auto compression'
        c = self._visit_partition_by(cols,rows)
        c += [{'post': (['add %s' % str(const)]
            if const is not None
            else []) + [')']}]

        return self.__class__(self._append(self.opts, {res: c}))


    def index(self, index):
        """
        Index is created with dialect specific keywords to
        include loading and ordering syntax elements

        index is a sqlalchemy.sql.schema.Index object.
        """
        return self.__class__(self._append(self.opts, {res: c}))


    def unique_index(self, name=None, cols=[]):
        res = 'unique index ' + (name if name is not None else '')
        return self.__class__(self._append(self.opts, {res:[self._prepare.quote(c) for c in cols if c is not None] }))

#@compiles(Select, 'teradata')
#def compile_select(element, compiler, **kw):
#    """
#    """
#
#    if not getattr(element, '_window_visit', None):
#      if element._limit is not None or element._offset is not None:
#          limit, offset = element._limit, element._offset
#
#          orderby=compiler.process(element._order_by_clause)
#          if orderby:
#            element = element._generate()
#            element._window_visit=True
#            #element._limit = None
#            #element._offset = None  cant set to none...
#
#            # add a ROW NUMBER() OVER(ORDER BY) column
#            element = element.column(sql.literal_column('ROW NUMBER() OVER (ORDER BY %s)' % orderby).label('rownum')).order_by(None)
#
#            # wrap into a subquery
#            limitselect = sql.select([c for c in element.alias().c if c.key != 'rownum'])
#
#            limitselect._window_visit=True
#            limitselect._is_wrapper=True
#
#            if offset is not None:
#              limitselect.append_whereclause(sql.column('rownum') > offset)
#              if limit is not None:
#                  limitselect.append_whereclause(sql.column('rownum') <= (limit + offset))
#            else:
#              limitselect.append_whereclause(sql.column("rownum") <= limit)
#
#            element = limitselect
#
#    kw['iswrapper'] = getattr(element, '_is_wrapper', False)
#    return compiler.visit_select(element, **kw)

