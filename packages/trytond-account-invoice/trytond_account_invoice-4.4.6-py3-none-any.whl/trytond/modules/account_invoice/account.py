# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from sql import Literal
from sql.conditionals import Coalesce

from trytond.model import (fields, ModelView, ModelSQL, MatchMixin,
    sequence_ordered)
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond import backend

__all__ = ['FiscalYear',
    'Period', 'Move', 'Reconciliation', 'InvoiceSequence']


class FiscalYear(metaclass=PoolMeta):
    __name__ = 'account.fiscalyear'
    invoice_sequences = fields.One2Many(
        'account.fiscalyear.invoice_sequence', 'fiscalyear',
        "Invoice Sequences",
        domain=[
            ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        pool = Pool()
        Sequence = pool.get('account.fiscalyear.invoice_sequence')
        sequence = Sequence.__table__()
        sql_table = cls.__table__()

        super(FiscalYear, cls).__register__(module_name)
        cursor = Transaction().connection.cursor()
        table = TableHandler(cls, module_name)

        # Migration from 4.2: Use Match pattern for sequences
        if (table.column_exist('in_invoice_sequence')
                and table.column_exist('in_credit_note_sequence')
                and table.column_exist('out_invoice_sequence')
                and table.column_exist('out_credit_note_sequence')):
            cursor.execute(*sequence.insert(columns=[
                        sequence.sequence, sequence.fiscalyear,
                        sequence.company,
                        sequence.out_invoice_sequence,
                        sequence.out_credit_note_sequence,
                        sequence.in_invoice_sequence,
                        sequence.in_credit_note_sequence],
                    values=sql_table.select(
                        Literal(20), sql_table.id,
                        sql_table.company,
                        sql_table.out_invoice_sequence,
                        sql_table.out_credit_note_sequence,
                        sql_table.in_invoice_sequence,
                        sql_table.in_credit_note_sequence)))
            table.drop_column('out_invoice_sequence')
            table.drop_column('out_credit_note_sequence')
            table.drop_column('in_invoice_sequence')
            table.drop_column('in_credit_note_sequence')

    @staticmethod
    def default_invoice_sequences():
        if Transaction().user == 0:
            return []
        return [{}]


class Period(metaclass=PoolMeta):
    __name__ = 'account.period'

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        pool = Pool()
        Sequence = pool.get('account.fiscalyear.invoice_sequence')
        FiscalYear = pool.get('account.fiscalyear')
        sequence = Sequence.__table__()
        fiscalyear = FiscalYear.__table__()
        sql_table = cls.__table__()

        super(Period, cls).__register__(module_name)
        cursor = Transaction().connection.cursor()
        table = TableHandler(cls, module_name)

        # Migration from 4.2: Use Match pattern for sequences
        if (table.column_exist('in_invoice_sequence')
                and table.column_exist('in_credit_note_sequence')
                and table.column_exist('out_invoice_sequence')
                and table.column_exist('out_credit_note_sequence')):
            cursor.execute(*sequence.insert(columns=[
                        sequence.sequence, sequence.fiscalyear,
                        sequence.company, sequence.period,
                        sequence.out_invoice_sequence,
                        sequence.out_credit_note_sequence,
                        sequence.in_invoice_sequence,
                        sequence.in_credit_note_sequence],
                    values=sql_table.join(fiscalyear,
                            condition=(fiscalyear.id == sql_table.fiscalyear)
                        ).select(
                        Literal(10), sql_table.fiscalyear,
                        fiscalyear.company, sql_table.id,
                        Coalesce(sql_table.out_invoice_sequence,
                            fiscalyear.out_invoice_sequence),
                        Coalesce(sql_table.out_credit_note_sequence,
                            fiscalyear.out_credit_note_sequence),
                        Coalesce(sql_table.in_invoice_sequence,
                            fiscalyear.in_invoice_sequence),
                        Coalesce(sql_table.in_credit_note_sequence,
                            fiscalyear.in_credit_note_sequence))))
            table.drop_column('out_invoice_sequence')
            table.drop_column('out_credit_note_sequence')
            table.drop_column('in_invoice_sequence')
            table.drop_column('in_credit_note_sequence')


class InvoiceSequence(sequence_ordered(), ModelSQL, ModelView, MatchMixin):
    'Invoice Sequence'
    __name__ = 'account.fiscalyear.invoice_sequence'
    company = fields.Many2One('company.company', "Company", required=True)
    fiscalyear = fields.Many2One(
        'account.fiscalyear', "Fiscal Year", required=True, ondelete='CASCADE',
        domain=[
            ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])
    period = fields.Many2One('account.period', 'Period',
        domain=[
            ('fiscalyear', '=', Eval('fiscalyear')),
            ('type', '=', 'standard'),
            ],
        depends=['fiscalyear'])
    in_invoice_sequence = fields.Many2One('ir.sequence.strict',
        'Supplier Invoice Sequence', required=True,
        domain=[
            ('code', '=', 'account.invoice'),
            ['OR',
                ('company', '=', Eval('company')),
                ('company', '=', None),
                ],
            ],
        depends=['company'])
    in_credit_note_sequence = fields.Many2One('ir.sequence.strict',
        'Supplier Credit Note Sequence', required=True,
        domain=[
            ('code', '=', 'account.invoice'),
            ['OR',
                ('company', '=', Eval('company')),
                ('company', '=', None),
                ],
            ],
        depends=['company'])
    out_invoice_sequence = fields.Many2One('ir.sequence.strict',
        'Customer Invoice Sequence', required=True,
        domain=[
            ('code', '=', 'account.invoice'),
            ['OR',
                ('company', '=', Eval('company')),
                ('company', '=', None),
                ],
            ],
        depends=['company'])
    out_credit_note_sequence = fields.Many2One('ir.sequence.strict',
        'Customer Credit Note Sequence', required=True,
        domain=[
            ('code', '=', 'account.invoice'),
            ['OR',
                ('company', '=', Eval('company')),
                ('company', '=', None),
                ],
            ],
        depends=['company'])

    @classmethod
    def __setup__(cls):
        super(InvoiceSequence, cls).__setup__()
        cls._order.insert(0, ('fiscalyear', 'ASC'))

    @classmethod
    def default_company(cls):
        return Transaction().context.get('company')


class Move(metaclass=PoolMeta):
    __name__ = 'account.move'

    @classmethod
    def _get_origin(cls):
        return super(Move, cls)._get_origin() + ['account.invoice']


class Reconciliation(metaclass=PoolMeta):
    __name__ = 'account.move.reconciliation'

    @classmethod
    def create(cls, vlist):
        Invoice = Pool().get('account.invoice')
        reconciliations = super(Reconciliation, cls).create(vlist)
        move_ids = set()
        account_ids = set()
        for reconciliation in reconciliations:
            move_ids |= {l.move.id for l in reconciliation.lines}
            account_ids |= {l.account.id for l in reconciliation.lines}
        invoices = Invoice.search([
                ('move', 'in', list(move_ids)),
                ('account', 'in', list(account_ids)),
                ])
        Invoice.process(invoices)
        return reconciliations

    @classmethod
    def delete(cls, reconciliations):
        Invoice = Pool().get('account.invoice')

        move_ids = set(l.move.id for r in reconciliations for l in r.lines)
        invoices = Invoice.search([
                ('move', 'in', list(move_ids)),
                ])
        super(Reconciliation, cls).delete(reconciliations)
        Invoice.process(invoices)
