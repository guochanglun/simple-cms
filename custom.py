from flask import url_for, request
from flask_peewee.rest import UserAuthentication, RestResource
from flask_peewee.utils import PaginatedQuery


# 自定义权限，允许所有操作
class GclAuthentication(UserAuthentication):
    # 默认允许任何权限
    def authorize(self):
        return True


# 自定义RestResourc，返回layui table需要的数据格式
class GclRestResource(RestResource):

    def get_request_metadata(self, paginated_query):
        var = paginated_query.page_var
        request_arguments = request.args.copy()

        current_page = paginated_query.get_page()
        next = previous = ''

        if current_page > 1:
            request_arguments[var] = current_page - 1
            previous = url_for(self.get_url_name('api_list'), **request_arguments)
        if current_page < paginated_query.get_pages():
            request_arguments[var] = current_page + 1
            next = url_for(self.get_url_name('api_list'), **request_arguments)

        return {
            'model': self.get_api_name(),
            'page': current_page,
            'previous': previous,
            'next': next,
            'status': 200,
            'code': 0,
            'msg': "",
            'count': paginated_query.query.count(),
        }

    def paginated_object_list(self, filtered_query):
        paginate_by = self.get_paginate_by()
        pq = PaginatedQuery(filtered_query, paginate_by)
        meta_data = self.get_request_metadata(pq)

        query_dict = self.serialize_query(pq.get_list())
        meta_data['data'] = query_dict
        return self.response(meta_data)
