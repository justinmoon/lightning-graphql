import config
import graphene
import lightning

from pprint import pprint


cl = lightning.LightningRpc(config.CLIGHTNING_SOCKET)


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

    all_invoices = graphene.List(Invoice)

    def resolve_all_invoices(self, info):
        invoices = cl.listinvoices()['invoices']
        invoices = [Invoice(**invoice) for invoice in invoices]
        return invoices


schema = graphene.Schema(query=Query)
query = """
    query queryInvoices {
      allInvoices {
        label
        bolt11
        paymentHash
        payIndex
        msatoshi
        amountMsat
        msatoshiReceived
        amountReceivedMsat
        status
        paidAt
        expiresAt
        description
      }
    }
"""


def test_query():
    result = schema.execute(query)
    return result


if __name__ == "__main__":
    result = schema.execute(query)
    if result.errors:
        print(f"Errors: {result.errors}")
    if result.data:
        invoices = result.data['allInvoices']
        print(f"First invoice (of {len(invoices)}):")
        pprint(invoices[0])
    else:
        print('No results')

