import sys
import config
import graphene
import lightning

from pprint import pprint


cl = lightning.LightningRpc(sys.argv[1])


class Invoice(graphene.ObjectType):
    id = graphene.String()
    label = graphene.String()
    bolt11 = graphene.String()
    payment_hash = graphene.String()
    pay_index = graphene.Int()
    msatoshi = graphene.Int()
    amount_msat = graphene.String()
    msatoshi_received = graphene.Int()
    amount_sent_msat = graphene.String()
    msatoshi_sent = graphene.Int()
    amount_received_msat = graphene.String()
    status = graphene.String()
    paid_at = graphene.Int()
    expires_at = graphene.Int()
    created_at = graphene.Int()
    expiry = graphene.Int()
    description = graphene.String()
    payment_preimage = graphene.String()
    destination = graphene.String()
    # WTF
    warning_capacity = graphene.String()


class Query(graphene.ObjectType):

    all_invoices = graphene.List(Invoice, 
            maxSat=graphene.Int(),
            minSat=graphene.Int(),
            status=graphene.String())

    def resolve_all_invoices(self, info, maxSat=None, minSat=None,
            status=None):
        invoices = cl.listinvoices()['invoices']

        if maxSat:
            invoices = [i for i in invoices if i['msatoshi'] < maxSat]
        if minSat:
            invoices = [i for i in invoices if i['msatoshi'] > minSat]
        if status:
            invoices = [i for i in invoices if i['status'] == status]

        return [Invoice(**invoice) for invoice in invoices]


class CreateInvoice(graphene.Mutation):
    class Arguments:
        msatoshi = graphene.Int()
        label = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    invoice = graphene.Field(lambda: Invoice)

    def mutate(self, info, msatoshi, label, description):
        cl_invoice = cl.invoice(msatoshi, label, description)
        # FIXME: should we look invoice up to get more fields?
        # invoices = cl.listinvoices(label)['invoices']
        # assert len(invoices) == 1
        # invoice = Invoice(**invoices[0])
        invoice = Invoice(**cl_invoice)
        ok = True
        return CreateInvoice(invoice=invoice, ok=ok)


class PayInvoice(graphene.Mutation):
    class Arguments:
        bolt11 = graphene.String()

    ok = graphene.Boolean()
    invoice = graphene.Field(lambda: Invoice)

    def mutate(self, info, bolt11):
        result = cl.pay(bolt11)
        ok = True
        return PayInvoice(ok=ok, invoice=Invoice(**result))


class Mutations(graphene.ObjectType):
    create_invoice = CreateInvoice.Field()
    pay_invoice = PayInvoice.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
