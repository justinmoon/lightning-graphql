from flask import Flask
from flask_graphql import GraphQLView

from lightning_graphql import schema

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(port=9000)
