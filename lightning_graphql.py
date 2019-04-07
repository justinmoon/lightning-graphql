import sys
import config
import graphene
import lightning

from pprint import pprint


cl = lightning.LightningRpc(sys.argv[2])


class Invoice(graphene.ObjectType):
    label = graphene.String()
    bolt11 = graphene.String()
    payment_hash = graphene.String()
    pay_index = graphene.Int()
    msatoshi = graphene.Int()
    amount_msat = graphene.String()
    msatoshi_received = graphene.Int()
    amount_received_msat = graphene.String()
    status = graphene.String()
    paid_at = graphene.Int()
    expires_at = graphene.Int()
    description = graphene.String()




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
        print("cl.invoice() args: ", msatoshi, label, description)
        cl_invoice = cl.invoice(msatoshi, label, description)
        invoices = cl.listinvoices(label)['invoices']
        assert len(invoices) == 1
        ok = True
        invoice = Invoice(**invoices[0])
        return CreateInvoice(invoice=invoice, ok=ok)


class Mutations(graphene.ObjectType):
    create_invoice = CreateInvoice.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
