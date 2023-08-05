from shutterstock.endpoint import EndPoint, EndPointParam, ChoicesParam,\
    IntegerParam
from shutterstock.resource import Resource, ResourceObjectMethod, \
    ResourceCollectionMethod


class ImageEndPoint(EndPoint):
    """Endpoint for Shutterstock images"""
    MINIMAL = 'minimal'
    FULL = 'full'
    VIEW_CHOICES = (MINIMAL, FULL, )

    id = EndPointParam(required=True,
                       help_text='Required. The ID of the image.')
    view = ChoicesParam(required=True, default=MINIMAL, choices=VIEW_CHOICES,
                        help_text='Required. Minimal view does not return licensing options, categories, keywords')


class Contributor(Resource):
    LIST = EndPoint('/contributors')
    GET = EndPoint('/contributors/{id}')


class Image(Resource):
    LIST = ImageEndPoint('/images')
    GET = ImageEndPoint('/images/{id}')


class ImageCollectionListEndPoint(EndPoint):
    id = EndPointParam()


class ImageCollectionItemsEndPoint(EndPoint):
    id = EndPointParam()
    per_page = IntegerParam(min=1, max=150)
    page = IntegerParam(default=1, min=1)


class ImageCollection(Resource):
    LIST = ImageCollectionListEndPoint('/images/collections')
    GET = EndPoint('/images/collections/{id}')
    ITEMS = ImageCollectionItemsEndPoint('/images/collections/{id}/items')

    @ResourceCollectionMethod(resource=Image, id='id')
    def items(cls, **params):
        detail = cls.API.get(cls.GET, id=params.get('id'))
        item_count = detail['total_item_count']
        per_page = params.get('per_page', 150)
        ids = []
        for page in range(0, math.ceil(item_count / per_page)):
            response = cls.API.get(cls.ITEMS, page=page + 1, **params)
            page_ids = [item['id'] for item in response['data']]
            ids.extend(page_ids)

        results = {'data': []}
        for page in range(0, math.ceil(len(ids) / 100)):
            page_ids = ids[page * 100:page * 100 + 100]
            if len(page_ids):
                images_to_add = cls.API.get(Image.LIST, id=page_ids,
                                            view=params.get('view', 'minimal'))
                results['data'].extend(images_to_add['data'])
        return results


class ImageLicense(Resource):
    LIST = EndPoint('/images/licenses')
    DOWNLOAD = EndPoint('/images/licenses/{id}/downloads')
    LICENSE = EndPoint('/images/licenses?subscription_id={subscription_id}', params=['images'])

    @ResourceObjectMethod(id='id')
    def download(cls, **params):
        return cls.API.post(cls.DOWNLOAD, **params)

    @ResourceCollectionMethod(id='id')
    def license(cls, **params):
        return cls.API.post(cls.LICENSE, **params)


class ImageContributor(Resource):
    GET = EndPoint('/contributors/{contributor_id}')
