from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item with name '{}' already exists".format(name)}, 400 # bad request

        payload_data = Item.parser.parse_args()  # This line only gets the price from the payload

        item = ItemModel(name, **payload_data)

        try:
            item.save_to_db()
        except:
            return {"message":"An error ocurred inserting the item"}, 500 #internal server error

        return item.json(), 201 #No need to jsonify as long as you return a dictionary

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item deleted'}

    def put(self,name):

        data = Item.parser.parse_args() # This line only gets the price from the payload

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
