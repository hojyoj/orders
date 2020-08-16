# -*- coding: utf-8 -*-

 ##############################################
 ##                                            ##
 ##                Orders Package               ##
 ##                                             ##
 ##                                             ##
 ##              from Basiq Series              ##
 ##           by Críptidos Digitales            ##
 ##                 GPL (c)2008                 ##
  ##                                            ##
    ##############################################

"""
"""

from __future__ import print_function

__version__ = "0.1"             ## Go to end for change log

import sys
from PyQt4 import QtCore, QtGui

import processes

import view
import model



class Controller(processes.Controller):

    _cast = 'order'
    _title = u"Pedidos"


    def __init__(self, *args, **kwds):
        """    orders.Controller.__init__()"""

        kwds['role'] = 'purchase'

        processes.Controller.__init__(self, *args, **kwds)

        self.initOrder = 3
        self.displayOrder = 2

        self.model = model.Model(self.app.model)

        if self.capture_mode is 1:
            self.master = view.Master(self.owner.master, cnt=self)


    def make_captureView(self, document, task):
        # print("         orders Controller.make_captureView()")

        captureView = view.CaptureView(master=self.master, document=document, task=task)
        self.connect(captureView, QtCore.SIGNAL("captureViewClosed()"), self.master.manager_update)
        self.master.ui.outerSplitter.insertWidget(1, captureView)

        # print("         orders Controller.make_captureView() - END")

        return captureView


    def entities(self, **kwds):
        kwds['kind'] = 'supplier'
        if 'goodKinds' in kwds:
            kwds['goodKinds'] = kwds['goodKinds'].replace(u'Mercancía', 'goods')
            kwds['goodKinds'] = kwds['goodKinds'].replace(u'Equipamiento', 'supplies')
            kwds['goodKinds'] = kwds['goodKinds'].replace(u'Gasto', 'services')

        return self.app.model.rols_full_pull(order='name', **kwds)

    def process(self, **kwds):
        if 'id' not in kwds.keys():
            kwds['kind_code'] = self.app.model.getAttribute(category='processKind', name=u'Mercancía', cast_=self.role)['code']

        dbProcess = self.app.model.getProcess(**kwds)

        process = self.process_new(**dbProcess)

        return process

    def order_erase(self, **kwds):
        return self.app.model.eraseProcess(id=kwds['id'])

    def order_exists(self, **kwds):
        # kwds['docs.kind_code'] = self.master.capture.documentKind_code
        kwds['docs.rstatus'] = 'active'
        return not not self.model.getOrder(**kwds)

    # def order_set(self, data):
        # return self.model.setOrder(**data)

    def process_save(self, **data):
        self.app.log2sys ( 'info', "    orders       Controller.process_save()" )

        try:

            if 'id' not in data.keys():
                kind = self.app.model.getAttribute(name=u'Mercancía', cast_='purchase')

                data['kind'] = {'code':kind['code']}

            self.app.model.startTransaction()

            process = self.app.model.setProcess(**data)

            ## POST PROCESSING

            """
            ## Update document last number
            documents = process.pop('documents', [])
            for document in documents:
                tmp = document.copy()
                kind_code = tmp.pop('kind_code', None)
                if not kind_code:
                    tmp = self.model.getDocument(id=document['id'])

                kind = self.model.setAttribute(cast_='purchase', category='documentKind', name='order') # Purchase order

                if tmp['kind_code'] in [kind['code']]:
                    number = tmp.pop('number', None)
                    if number:
                        self.model.setAttribute(code=kind['code'], value=number)
            """

            self.app.model.endTransaction()

            return process

        except:
        # else:
            print ("orders.Controller.process_save() :: ERROR - Could not register order")
            print ("puaaaaaaaaaaaaaaaaaaaaaj")
            print (sys.exc_info())

        self.app.log2sys ( 'info', "    orders       Controller.process_save() - END" )



if __name__ == "__main__":

    print ("Test not implemented")



"""
  ~~~~~~  To Do  ~~~~~~
    2012.12.18  Must subclass itemsTable to isolate local behaviour

  ~~~~~~  Known Issues  ~~~~~~

  ~~~~~~  Wish List  ~~~~~~

  ~~~~~~  Change Log  ~~~~~~
    2012.12.18  Quantity capture tooltip now shows current stock
                Quantity capture now shows suggested data, if
                changed color is set to yellow.


  ~~~~~~  Features  ~~~~~~
    Captura de pedido
    Cantidad
        Al solicitar la lista de los productos de un proveedor, se cargan los valores existencia, minimo, maximo, quota y sugerido.
        La existencia se muestra en el tooltip de la captura de cantidad.
        El sugerido se muestra en la captura.
        Si se modifica el sugerido, se muestra en color amarillo.

"""
