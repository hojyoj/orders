# -*- coding: utf-8 -*-

 ##############################################
 ##                                            ##
 ##                Orders Package               ##
 ##                  Data Model                 ##
 ##                                             ##
 ##              from Basiq Series              ##
 ##           by Críptidos Digitales            ##
 ##                 GPL (c)2008                 ##
  ##                                            ##
    ##############################################

"""
"""

from __future__ import print_function

import logging

import sys
import datetime

# from basiq.baseModel import Model

import processes.model as processes


class Model(processes.Model):

    def __init__(self, *args, **kwds):
        self.model = args[0]

        processes.Model.__init__(self, *args, **kwds)

        self.plug()


    def plug(self):
        # print("""    orders.model.plug()""")
        
        self.model.getOrder = self.getOrder
        self.model.getOrders = self.getOrders
        self.model.getOrdersCount = self.getOrdersCount
        
        # print("""    orders.model.plug() - END""")


    def getOrder(self, **filters):
        
        documents = filters.pop('documents', [])
        for document in documents:
            for item in document:
                filters['docs.{}'.format(item)] = document[item]
        
        command = """SELECT processes.id, processes.status,
        array_agg(docs.id) AS docs_id,
        array_agg(docs.kind_code) AS docs_kind_code,
        array_agg(docs.number) AS docs_number,
        array_agg(docs.date)   AS docs_date,
        array_agg(docs.rol_id) AS docs_rol_id,
        array_agg(docs.subtotal) AS docs_subtotal,
        array_agg(docs.discount) AS docs_discount,
        array_agg(docs.discountpercent) AS docs_discountpercent,
        array_agg(docs.tax)    AS docs_tax,
        array_agg(docs.taxpercent) AS docs_taxpercent,
        array_agg(docs.total)  AS docs_total,
        array_agg(docs.status) AS docs_status,
        array_agg(docs.relation) AS docs_relation,
        array_agg(docs.reference) AS docs_reference,
        array_agg(persons.name) AS rol_name,
        array_agg(persons.name2) AS rol_name2
        FROM
        (
        SELECT processes.id, processes.status, docs.date
        FROM processes
        JOIN processes_documents AS link ON (processes.id=link.process_id)
        JOIN documents AS docs ON (link.document_id=docs.id)
        WHERE X
        ) AS processes

        JOIN processes_documents AS link ON (processes.id=link.process_id)
        JOIN documents AS docs ON (link.document_id=docs.id)
        JOIN rols ON (docs.rol_id=rols.id)
        JOIN persons ON (rols.person_id=persons.id)

        GROUP BY processes.id, processes.status, processes.date
        ORDER BY processes.date DESC
        LIMIT 100 """

        filtersText = ""
        for key in filters.keys():
            if key == 'sinCompra':
                filtersText += """status != 'closed' AND """
            elif key == 'rol_id':
                filtersText += """docs.%s=%s AND """ % (key, filters[key])
            elif key == 'id':
                filtersText += """processes.%s=%s AND """ % (key, filters[key])
            elif type(filters[key]) in (str, datetime.datetime):
                filtersText += "%s='%s' AND " % (key, filters[key])
            elif type(filters[key]) in (list,):
                temp = ("%s" % filters[key]).replace("[", "(").replace("]",")")
                filtersText += "%s IN %s AND " % (key, temp)
            else:
                try:
                    if type(filters[key]) in [unicode]:
                        filtersText += "%s='%s' AND " % (key, filters[key])
                    else:
                        filtersText += "%s=%s AND " % (key, filters[key])
                except:
                    filtersText += "%s=%s AND " % (key, filters[key])

        if filtersText:
            command = command.replace("WHERE X", "WHERE %s " % filtersText.rstrip("AND "))
        else:
            command = command.replace("WHERE X", "")
        # print "\n", filters
        # print "\n", command
        cursor = self.model.execute(command, giveCursor=True)
        order = cursor.fetchone()
        cursor.close()

        # print order

        if order:
            order['documents'] = [{'id':id,
                       'kind':{'code':order['docs_kind_code'][index]},
                       'number' :order['docs_number'][index],
                       'date'   :order['docs_date'][index],
                       'rol_id' :order['docs_rol_id'][index],
                       'rol'    :{'id':order['docs_rol_id'][index], 'person':{'name': order['rol_name'][index], 'name2': order['rol_name2'][index]}},
                       'subtotal':order['docs_subtotal'][index],
                       'discount':order['docs_discount'][index],
                       'discountpercent':order['docs_discountpercent'][index],
                       'tax'    :order['docs_tax'][index],
                       'taxpercent':order['docs_taxpercent'][index],
                       'total'  :order['docs_total'][index],
                       'status' :order['docs_status'][index],
                       'relation':order['docs_relation'][index],
                       'reference':order['docs_reference'][index],
                } for index, id in enumerate(order['docs_id'])]

            order.pop('docs_id')
            order.pop('docs_kind_code')
            order.pop('docs_number')
            order.pop('docs_date')
            order.pop('docs_rol_id')
            order.pop('docs_subtotal')
            order.pop('docs_discount')
            order.pop('docs_discountpercent')
            order.pop('docs_tax')
            order.pop('docs_taxpercent')
            order.pop('docs_total')
            order.pop('docs_status')
            order.pop('docs_relation')
            order.pop('docs_reference')
            order.pop('rol_name')
            order.pop('rol_name2')
        # else:
            # print ("orders.model.getOrder({}) Not Found".format(filters))

        return order



    def getOrders(self, **filters):
        f=g
        command = """SELECT processes.id, processes.status,
        array_agg(docs.id) AS docs_id,
        array_agg(docs.kind_code) AS docs_kind_code,
        array_agg(docs.number) AS docs_number,
        array_agg(docs.date)   AS docs_date,
        array_agg(docs.rol_id) AS docs_rol_id,
        array_agg(docs.subtotal) AS docs_subtotal,
        array_agg(docs.discount) AS docs_discount,
        array_agg(docs.discountpercent) AS docs_discountpercent,
        array_agg(docs.tax)    AS docs_tax,
        array_agg(docs.taxpercent) AS docs_taxpercent,
        array_agg(docs.total)  AS docs_total,
        array_agg(docs.status) AS docs_status,
        array_agg(docs.relation) AS docs_relation,
        array_agg(docs.reference) AS docs_reference,
        array_agg(persons.name) AS rol_name,
        array_agg(persons.name2) AS rol_name2,
        array_agg(persons.rfc) AS rol_rfc,
        array_agg(addresses.street) AS rol_address_street,
        array_agg(addresses.site_number) AS rol_address_number,
        array_agg(addresses.areaname) As rol_address_areaname,
        array_agg(addresses.postalcode) AS rol_address_postalcode,
        array_agg(places.name) AS rol_address_placename
        FROM
        (
        SELECT processes.id, processes.status
        FROM processes
        JOIN processes_documents AS link ON (processes.id=link.process_id)
        JOIN (SELECT id, date, rol_id FROM documents WHERE kind_code in (12513)) AS docs ON (link.document_id=docs.id)
        WHERE X
        ) AS processes

        JOIN processes_documents AS link ON (processes.id=link.process_id)
        JOIN documents AS docs ON (link.document_id=docs.id)
        JOIN rols ON (docs.rol_id=rols.id)
        JOIN persons ON (rols.person_id=persons.id)
        
        LEFT JOIN addresses ON (rols.id=addresses.rol_id)
        
        LEFT JOIN attributes AS places ON (places.code=addresses.place_code)

        GROUP BY processes.id, processes.status
        LIMIT 100 """

        filtersText = ""
        for key in filters.keys():
            if key == 'rol_id':
                filtersText += """docs.%s=%s AND """ % (key, filters[key])
            elif type(filters[key]) in (str, datetime.datetime):
                filtersText += "%s='%s' AND " % (key, filters[key])
            elif type(filters[key]) in (list,):
                temp = ("%s" % filters[key]).replace("[", "(").replace("]",")")
                filtersText += "%s IN %s AND " % (key, temp)
            else:
                try:
                    if type(filters[key]) in [unicode]:
                        filtersText += "%s='%s' AND " % (key, filters[key])
                    else:
                        filtersText += "%s=%s AND " % (key, filters[key])
                except:
                    filtersText += "%s=%s AND " % (key, filters[key])

        if filtersText:
            command = command.replace("WHERE X", "WHERE %s " % filtersText.rstrip("AND "))
        else:
            command = command.replace("WHERE X", "")

        # print  "\n101 ", filters
        # print  "\n102 ", command

        cursor = self.model.execute(command, giveCursor=True)
        items = cursor.fetchall()
        cursor.close()

        orders = []
        
        for item in items:
            order = {}
            
            order['documents'] = [
                {   'id':id,
                    'kind':{'code':item['docs_kind_code'][index]},
                    'number' :item['docs_number'][index],
                    'date'   :item['docs_date'][index],
                    'rol'    :{
                        'id':item['docs_rol_id'][index],
                        'person':{
                            'name': item['rol_name'][index],
                            'name2': item['rol_name2'][index],
                            'rfc': item['rol_rfc'][index]
                            },
                        'address': {
                            'street': item['rol_address_street'],
                            'areaname': item['rol_address_areaname'],
                            'postalcode': item['rol_address_postalcode'],
                            'place': {'name':item['rol_address_placename']},
                            'number': item['rol_address_number']
                            }
                        },
                    'subtotal':item['docs_subtotal'][index],
                    'discount':item['docs_discount'][index],
                    'discountpercent':item['docs_discountpercent'][index],
                    'tax'    :item['docs_tax'][index],
                    'taxpercent':item['docs_taxpercent'][index],
                    'total'  :item['docs_total'][index],
                    'status' :item['docs_status'][index],
                    'relation':item['docs_relation'][index],
                    'reference':item['docs_reference'][index],
                } for index, id in enumerate(item['docs_id'])
            ]

            item.pop('docs_id')
            item.pop('docs_kind_code')
            item.pop('docs_number')
            item.pop('docs_date')
            item.pop('docs_rol_id')
            item.pop('docs_subtotal')
            item.pop('docs_discount')
            item.pop('docs_discountpercent')
            item.pop('docs_tax')
            item.pop('docs_taxpercent')
            item.pop('docs_total')
            item.pop('docs_status')
            item.pop('docs_relation')
            item.pop('docs_reference')
            item.pop('rol_name')
            item.pop('rol_name2')
            item.pop('rol_rfc')
            item.pop('rol_address_street')
            item.pop('rol_address_areaname')
            item.pop('rol_address_postalcode')
            item.pop('rol_address_placename')
            item.pop('rol_address_number')
            
            # print item
            
            order['id'] = item['id']
            order['status'] = item['status']
            
            orders.append(order)

        return orders


    def getOrdersCount(self):
        documentKind = self.model.getAttribute(category=u'documentKind', name=u'Order')
        cursor = self.model.execute("SELECT count(*) FROM documents WHERE kind_code=%s" % documentKind['code'], giveCursor=True)
        count = cursor.fetchone()
        return count['count']



    def initDb(self):
        # print("""\n    orders.model.initDb()""")
        
        processes.Model.initDb(self)

        # print("""    orders.model.initDb() - END""")



def elimina(**filtros):
    f=g
    registro = man.session().query(Documento).filter(Documento.documento_id==filtros['id']).one()
    man.session().delete(registro)
    man.session().commit()

