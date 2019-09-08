# -*- coding: utf-8 -*-

 ##############################################
 ##                                            ##
 ##                Orders Package               ##
 ##                     View                    ##
 ##                                             ##
 ##              from Basiq Series              ##
 ##           by Críptidos Digitales            ##
 ##                 GPL (c)2008                 ##
  ##                                            ##
    ##############################################

"""
"""

from __future__ import print_function

__version__ = "0.1"

import sys
import os
import logging

from decimal import Decimal
import datetime

try:
    import xlwt
except:
    import xlwt3 as xlwt

from PyQt4 import QtCore, QtGui
from basiq import utilities
from cdWidgets import cdFrame, cdNumberEdit
from cdWidgets import cdTableWidgetItem

from orders import manager_ui
from orders import capture_ui
from orders import details_ui




from basiq import itemsTable
from products import selector as productSelector

from processes import view


# DATAROLE_ROL = 1032


class Master(view.Master):


    DATAROLE_PRODUCT  = 1030
    DATAROLE_ROL = 1032


    def __init__(self, *args, **kwds):
        # print("""    orders.view.Master.__init__()""")

        view.Master.__init__(self, *args, **kwds)

        self.theme['text']['color'] = '#C0C000'
        self.theme['background']['color'] = '#F0E040'
        self.theme['background']['color2'] = '#FDFFB0'

        ## Details
        self.details = Details(self)
        self.details.hide()        
        
        self.ui.innerSplitter.insertWidget(0, self.details)
        
        self.connect(self.details, QtCore.SIGNAL('doubleClicked()'), self.details_toggle)
        
        self.connect(self.eventRouter, QtCore.SIGNAL("suppliersChanged()"), self.loadSuppliers)
        self.connect(self.eventRouter, QtCore.SIGNAL("customersChanged()"), self.loadCustomers)

        # print("""    orders.view.Master.__init__() - END""")

    
    def add(self):
        f=k
        document_kind = self.cnt.documentKinds_pull(category='documentKind', name='Order', cast_=self.cnt.role)[0]
        view.Master.add(self, document_kind)
    
    
    '''
    def captureView_new(self, *args, **kwds):
        # print("    orders.view.Master.capture_new()")
        
        captureView = CaptureView(self, *args, **kwds)
        self.connect(captureView, QtCore.SIGNAL("captureViewClosed()"), self.captureView_close)
        self.ui.outerSplitter.insertWidget(1, captureView)
        
        # print("    orders.view.Master.capture_new() - END")
        
        return captureView
    '''
    
    
    def init(self, duty='purchase'):
        # print("""    orders.view.Master.init()""")

        view.Master.init(self)  
    
        
        
        # self.capture.init()
        
        if duty is 'sale':
            self.duty = u'sale'
            self.captureView.documentKind_code = 13513      ## sale order
            self.captureView.rolKind_code = 13215           ## sale customer
        else:
            self.duty = u'purchase'
            # self.capture.documentKind_code = 12513      ## purchase order
            # self.capture.rolKind_code = 12215           ## purchase supplier

        self.loadSuppliers()
        self.loadCustomers()

        # print("""    orders.view.Master.init() - END""")


    def edit(self):
        self.setCursor(QtCore.Qt.WaitCursor)

        # order = self.data()[index]
        order = self.ui.listTA.item(self.ui.listTA.currentRow(),0).data(1001)        
        
        self.cnt.app.master.titleWidget.setText(u"Modificación de Pedido")
        
        self.captureView.edit(order)
        
        self.setCursor(QtCore.Qt.ArrowCursor)
        
    '''
    def innerHandlePressed(self):
        """orders.view.Master.innerHandlePressed()"""
        self.details_toggle()
    '''

    def loadCustomers(self):
        """orders.view.Master.loadCustomers()"""
        pass
        # self.capture.entities_load()

        """

        if self.capture.kind == 'sale':

            self.capture.state = self.cnt.BUSY

            customers = self.cnt.customers()

            oldAtCapture = self.capture.ui.entityCB.currentData().toInt()[0]
            self.capture.ui.entityCB.clear()
            self.capture.ui.entityCB.addItem(u"", self.cnt.app.holder['id'])
            self.capture.ui.entityCB.setItemData(self.capture.ui.entityCB.count()-1, self.cnt.app.holder, self.DATAROLE_ROL)

            if customers:
                for entity in customers:
                    self.capture.ui.entityCB.addItem("%s %s" % (entity['person']['name'], rntity['person']['name2']), entity['id'])
                    self.capture.ui.entityCB.setItemData(self.capture.ui.entityCB.count()-1, entity, self.DATAROLE_ROL)
            else:
                self.capture.ui.entityCB.addItem("Debe dar de alta al cliente", self.cnt.app.holder)
                self.capture.ui.entityCB.setItemData(self.capture.ui.entityCB.count()-1, self.cnt.app.holder, self.DATAROLE_ROL)

            if oldAtManager > 0:
                self.capture.ui.entityCB.setCurrentData(oldAtCapture)
            else:
                self.capture.ui.entityCB.setCurrentIndex(0)

            self.capture.state_reset()
        """


    def loadSuppliers(self):
        """orders.view.Master.loadSuppliers()"""
        
        suppliers = self.cnt.suppliers()

        # self.capture.entities_load(suppliers)

        oldAtManager = self.manager.ui.cbProveedor.currentData()

        self.manager.ui.cbProveedor.clear()

        if suppliers:
            # 2015.01.18 self.manager.ui.cbProveedor.addItem(u"", self.cnt.app.holder['id'])
            self.manager.ui.cbProveedor.addItem(u"", -1)
            for supplier in suppliers:
                self.manager.ui.cbProveedor.addItem(u"{} {}".format(supplier['person']['name'], supplier['person']['name2']), supplier['id'])

        else:
            # 2015.01.18 self.manager.ui.cbProveedor.addItem("No hay proveedores", self.cnt.app.holder['id'])
            self.manager.ui.cbProveedor.addItem("No hay proveedores", -1)
            self.manager.ui.frProveedor.setToolTip(u"No hay proveedores capturados")

        self.manager.ui.cbProveedor.setCurrentData(oldAtManager)


    def manager_new(self):
        # print("""    orders.Master.manager_new()""")
        
        self.manager = Manager(self)

        self.connect(self.manager, QtCore.SIGNAL('doubleClicked()'), self.details_toggle)
        
        self.ui.innerSplitter.insertWidget(0, self.manager)
        
        self.connect(self.eventRouter, QtCore.SIGNAL("ordersChanged()"), self.manager.data_update)

        # print("""    orders.Master.manager_new() - END""")

    
    def outerHandlePressed(self):
        """orders.view.Master.outerHandlePressed()"""
        if self.ui.outerSplitter.sizes()[0] == 0:
            self.setInnerStatus('visible')
        else:
            self.setInnerStatus('hidden')


class Manager(view.Manager):

    def __init__(self, *args, **kwds):

        view.Manager.__init__(self, *args, **kwds)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(9)

        ## FILTROS

        self.connect(self.ui.ch1, QtCore.SIGNAL('stateChanged(int)'), self.data_update)
        self.connect(self.ui.ch2, QtCore.SIGNAL('stateChanged(int)'), self.data_update)
        self.connect(self.ui.ch3, QtCore.SIGNAL('stateChanged(int)'), self.data_update)

        self.ui.cbProveedor.setMaxVisibleItems(15)
        self.ui.cbProveedor.setFont(font)
        self.connect(self.ui.cbProveedor, QtCore.SIGNAL("currentIndexChanged(int)"), self.data_update)

        ## TABLA DE CONSULTA
        # self.ui.listTA = self.ui.tablaConsulta
        
        self.labels = [u"Proveedor", u"Folio", u"Fecha", u"Status", u"Monto", u""]
        self.ui.listTA.setColumnCount(len(self.labels))
        self.ui.listTA.setHorizontalHeaderLabels(self.labels)
        
        # self.ui.listTA.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.ui.listTA.horizontalHeader().setResizeMode(5, QtGui.QHeaderView.Stretch)
        
        # self.ui.listTA.setToolTip(u"ALT+D muestra detalles de la Orden seleccionada")


        ## Details
        self.aDetails = QtGui.QAction("Detalles", self)
        self.aDetails.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_D))
        #~ self.connect(self.aDetails, QtCore.SIGNAL("triggered()"), self.detailsTriggered)

        ## BUTTONS
        iconTextLayout = QtCore.Qt.ToolButtonTextBesideIcon

        font = QtGui.QFont()
        font.setPointSize(10 * self.mst.layoutZoom)
        font.setBold(True)
        
        self.ui.toAgregar.setFont(font)
        self.ui.toAgregar.setDefaultAction(self.aAdd)
        self.ui.toAgregar.setIconSize(QtCore.QSize(44, 40))
        self.ui.toAgregar.setToolButtonStyle(iconTextLayout)
        
        ## Edit
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aModificar = QtGui.QAction(icon1, u"&Modificar", self)
        self.aModificar.setCheckable(True)
        self.aModificar.setIconText(u"&Modificar")
        self.connect(self.aModificar, QtCore.SIGNAL("triggered()"), self.edit)

        self.ui.toModificar.setFont(font)
        self.ui.toModificar.setDefaultAction(self.aModificar)
        self.ui.toModificar.setIconSize(QtCore.QSize(44, 40))
        self.ui.toModificar.setToolButtonStyle(iconTextLayout)

        ## Delete
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aRemove = QtGui.QAction(icon2, u"&Eliminar", self)
        self.aRemove.setCheckable(True)
        self.aRemove.setIconText(u"&Eliminar")
        self.connect(self.aRemove, QtCore.SIGNAL("triggered()"), self.elimina)

        self.ui.toEliminar.setFont(font)
        self.ui.toEliminar.setDefaultAction(self.aRemove)
        self.ui.toEliminar.setIconSize(QtCore.QSize(44, 40))
        self.ui.toEliminar.setToolButtonStyle(iconTextLayout)

        self.aCancel = QtGui.QAction(icon2, u"Cancelar proceso", self)
        self.aCancel.setCheckable(True)
        self.aCancel.setIconText(u'Cancelar')
        self.connect(self.aCancel, QtCore.SIGNAL('triggered()'), self.cancelProcess)

        ## Print
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/Print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.aImprimir = QtGui.QAction(icon, u"Imprimir", self)
        # self.aImprimir.setIconText(u"&Imprimir")
        # self.connect(self.aImprimir, QtCore.SIGNAL("triggered()"), self.imprime)

        self.ui.toImprimir.setFont(font)
        self.ui.toImprimir.setDefaultAction(self.aPrint)
        self.ui.toImprimir.setIconSize(QtCore.QSize(44, 40))
        self.ui.toImprimir.setToolButtonStyle(iconTextLayout)
        self.ui.toImprimir.setToolTip(u"Se imprime sólo los renglones mostrados en la lista")

        self.impresor = QtGui.QPrinter()


        ## Menu
        font = QtGui.QFont()
        font.setPointSize(10 * self.mst.layoutZoom)
        font.setBold(True)

        self.listMN = QtGui.QMenu(self)
        self.listMN.setFont(font)
        self.listMN.addAction(self.aAdd)
        self.listMN.addAction(self.aModificar)
        self.listMN.addAction(self.aCancel)
        self.listMN.addAction(self.aRemove)

        self.connect(self.mst.eventRouter, QtCore.SIGNAL('ordersChanged()'), self.data_update)
        self.connect(self.mst.eventRouter, QtCore.SIGNAL('productosChanged()'), self.updateButtons)

        '''  
        # self.upToDate = False

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.connect(self, QtCore.SIGNAL('showed()'), self.showed)
        '''


    def ui_load(self):
        ## Methods like this that access personalized modules must replace not inherit
        self.ui = manager_ui.Ui_Form()
        self.ui.setupUi(self)
        

    def cancelProcess(self):
        if self.ui.listTA.currentRow() < 0:
            result = QtGui.QMessageBox.information(self, u"Empresa Básica - Orden de compra", u"Selecciona la ORDEN DE COMPRA que quieres CANCELAR", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        else:
            self.setCursor(QtCore.Qt.WaitCursor)

            index = self.ui.listTA.item(self.ui.listTA.currentRow(),0).data(1001)
            orderTmp = self.data()[index]

            documentTmp = [x for x in orderTmp['documents'] if x['kind']['code']==12513][0]

            document = {'id':documentTmp['id'], 'status':u'cancelado'}

            order = {'id':orderTmp['id'], 'status':u'cancelado'}
            order['documents'] = [document]

            self.cnt.process_save(order)

            self.data_update()

            self.setCursor(QtCore.Qt.ArrowCursor)


    def currentId(self):
        if self.ui.listTA.currentRow() != -1:
            item = self.ui.listTA.item(self.ui.listTA.currentRow(), 0)
            id = item.data(self.ui.listTA.DOCUMENT_ID)
        else:
            id = None
        return id


    def editt(self):
        """orders.view.Manager.edit()"""
        f=h
        if self.ui.listTA.currentRow() < 0:
            result = QtGui.QMessageBox.information(self, u"Empresa Básica - Modificar Orden de compra", u"Selecciona la ORDEN DE COMPRA que quieres MODIFICAR", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        else:
            self.setCursor(QtCore.Qt.WaitCursor)

            index = self.ui.listTA.item(self.ui.listTA.currentRow(),0).data(1001)
            
            # order = self.data()[index]
            
            self.mst.process_edit(order)

            self.setCursor(QtCore.Qt.ArrowCursor)


    def elimina(self):
        item = self.ui.listTA.item(self.ui.listTA.currentRow(), 0)
        process = eval('{}'.format(item.data(self.ui.listTA.DOCUMENT_ID).toString()))

        document = [x for x in process['documents'] if x['kind']['code'] in [12513, 13513]][0]

        if document['status'] == u"pending":
            result = QtGui.QMessageBox.warning(self, u"Empresa Básica - Eliminar Orden de compra", u"¿Realmente quieres ELIMINAR la ORDEN DE COMPRA {} {}?".format(document['number'], document['date'].strftime('%d %b %Y')), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.Yes:
                result = self.cnt.order_erase(id=process['id'])
                if result:
                    self.mst.eventRouter.emit(QtCore.SIGNAL("ordersChanged()"))
                else:
                    print ("No pude borrar pedido")
        else:
            result = QtGui.QMessageBox.information(self, u"Empresa Básica - Eliminar Orden de compra", u"Lo siento, esta orden de compra ya ha sido procesada, NO SE PUEDE ELIMINAR", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        self.updateButtons()


    def findData(self, data):
        index = -1
        for row in range(self.ui.listTA.rowCount()):
            item = self.ui.listTA.item(row, 0)
            if item.data(self.ui.listTA.DOCUMENT_ID) == data:
                index = row
        return index

    # def hideInfo(self):
        # self.frame.hide()


    def imprime(self):
        dialogoImpresora = QtGui.QPrintDialog(self.impresor)
        if dialogoImpresora.exec_() == QtGui.QDialog.Accepted:
            painter = QtGui.QPainter(self.impresor)
            margenHorizontal, margenVertical = [10, 10]

            font1 = QtGui.QFont("courier", 10)
            font1.setBold(True)
            font2 = QtGui.QFont("courier", 9)
            font3 = QtGui.QFont("Courier", 12)
            font3.setBold(True)

            margenX, margenY = [25, 75]
            pageWidth, pageHeight = (self.impresor.paperRect().width(), self.impresor.paperRect().height())
            pageNo = 1

            ## HEADER
            header = []
            x, y = [25, 0]
            header.append([pageWidth/2-100, margenY+y, u"Catálogo de Empleados", font3])
            x, y = [400, 25]
            header.append([pageWidth-200, margenY+y, u"Fecha: {}".format(QtCore.QDate().currentDate().toString('dd MMM yyyy')), font1])

            # x, y = [0, 100]
            # header.append([margenX+x, margenY+y, u"    Nombre                                     RFC            Teléfonos", font1])

            tabla = self.ui.listTA

            x, y = [0, 75]
            contenido = []
            footer = []
            offset = 0
            for row in range(tabla.rowCount()):
                if offset == 0:
                    contenido.extend(header)
                posX, posY = (margenX + x, margenY + y + offset)
                contenido.append([posX    , posY, str(row+1), font2])
                contenido.append([posX+40 , posY, tabla.item(row, 0).text(), font2])    # Nombre
                contenido.append([posX+90 , posY+18, tabla.item(row, 4).text(), font2]) # Domicilio
                contenido.append([posX+90 , posY+36, tabla.item(row, 3).text(), font2]) # Lugar
                contenido.append([posX+90 , posY+54, u"RFC: {}   Teléfonos: {}".format(tabla.item(row, 1).text(), tabla.item(row, 2).text()), font2]) # RFC, Teléfono
                # if tabla.item(row, 5):
                    # contenido.append([posX+690, posY, tabla.item(row, 5).text(), font2])# Importe
                offset += 80
                if posY+190 >= pageHeight:
                    contenido.append([pageWidth/2-50, pageHeight-50, "Hoja {}".format(pageNo), font2])
                    for item in contenido:
                        painter.setFont(item[3])
                        painter.drawText(QtCore.QPoint(margenHorizontal + item[0], margenVertical + item[1]), item[2])
                    offset = 0
                    contenido = []
                    footer = []
                    pageNo += 1
                    self.impresor.newPage()

            contenido.append([pageWidth/2-50, pageHeight-50, "Hoja {}".format( pageNo), font2])
            for item in contenido:
                painter.setFont(item[3])
                painter.drawText(QtCore.QPoint(margenHorizontal + item[0], margenVertical + item[1]), item[2])


    def init(self):
        
        self.data_update()


    def showListMenu(self, pos):
        pos = self.ui.listTA.mapToGlobal(pos)
        self.listMN.popup(pos)


    def listResized(self, event):
        """pedidos.igu.Manager.listResized()"""
        headerWidth = self.ui.listTA.width()-self.ui.listTA.verticalHeader().width()-self.ui.listTA.verticalScrollBar().width()
        self.ui.listTA.horizontalHeader().setMinimumWidth(headerWidth)

        porcentajes = [0, 10, 15, 15, 15]
        overflow = 0

        for index in range(self.ui.listTA.horizontalHeader().count()-1):

            if not self.ui.listTA.isColumnHidden(index):
                self.ui.listTA.resizeColumnToContents(index)

                porContenido = self.ui.listTA.columnWidth(index)
                calculado = headerWidth * porcentajes[index] / 100

                if porContenido < calculado:
                    if overflow:
                        offset = calculado - porContenido
                        if offset > overflow:
                            calculado = calculado - overflow
                            overflow = 0
                        else:
                            overflow -= offset
                            calculado = porContenido
                    self.ui.listTA.setColumnWidth(index, calculado)
                else:
                    overflow += porContenido - calculado


    # def selectionChanged(self):
        # if self.ui.listTA.currentRow() != -1:
            # item = self.ui.listTA.item(self.ui.listTA.currentRow(), 0)
            # process = item.data(self.ui.listTA.PROCESS)
            # id = item.data(self.ui.listTA.DOCUMENT_ID)
            
            # self.mst.current_set(process, id)
            
        # self.updateButtons()


    def setCurrentId(self, id):
        self.ui.listTA.setCurrentItem(self.ui.listTA.item(self.findData(id), 0))


    def showed(self):
        self.cnt.information_set(u"")
        self.data_update()


    def theme_update(self):

        buttonsStyle = "border:2px outset #908878; border-top:0px; border-top-left-radius:0px; border-top-right-radius:0px; border-bottom-left-radius:12px; border-bottom-right-radius:12px; background-color:qradialgradient(cx:.5, cy:.75, radius:1.5,fx:.5, fy:.75, stop:0 {}, stop:1 {});".format(self.mst.theme['background']['color'], self.mst.theme['background']['color2'])
        
        self.ui.toAgregar.setStyleSheet(buttonsStyle)
        self.ui.toModificar.setStyleSheet(buttonsStyle)
        self.ui.toEliminar.setStyleSheet(buttonsStyle)
        self.ui.toImprimir.setStyleSheet(buttonsStyle)        
        
        self.listMN.setStyleSheet("QMenu{background-color:QRadialGradient(cx:.5, cy:.5, radius:1, fx:.5, fy:.5, stop:0 #FFFFFF, stop:1 #FFD040);} QMenu::item{color:#202020;} QMenu::item:selected{color:#000000; background-color:#F0C038;}")


    def updateButtons(self):

        # view.Manager.updateButtons(self, count)
        
        message4New = u""
        message4Filter = u""
        message4Edit = u""
        message4Remove = u""
        message4Print = u""
        self.message4Info = u""
        
        if self.mst.duty == 'purchase' and not self.cnt.supplier():
            message4New += u"No hay proveedores registrados\n"
            message4Filter += u"No hay proveedores registrados\n"
            self.message4Info += u"Debe registrar proveedores\n"

        if self.mst.duty == 'sale' and self.cnt.customersCount() == 0:
            message4New += u"No hay clientes registrados\n"
            message4Filter += u"No hay clientes registrados\n"
            self.message4Info += u"Debe registrar clientes\n"

        if not self.cnt.order_exists():
            message4Filter += u"No hay órdenes de compra registradas\n"
            message4Edit += u"No hay órdenes de compra registradas\n"
            message4Remove += u"No hay órdenes de compra registradas\n"
            message4Print += u"No hay órdenes de compra para imprimir\n"

        elif self.ui.listTA.rowCount() == 0:
            message4Edit += u"No hay órdenes de compra desplegadas\n"
            message4Remove += u"No hay órdenes de compra desplegadas\n"
            message4Print += u"No hay órdenes de compra desplegadas\n"

        elif self.ui.listTA.rowCount() > 0:
            if self.ui.listTA.currentRow() == -1:
                message4Edit += u"Selecciona la Orden de Compra que quieres Modificar"
                message4Remove += u"Selecciona la Orden de Compra que quieres Eliminar"

        if message4Filter:
            self.ui.frFiltros.setToolTip(message4Filter.rstrip("\n"))
            self.ui.frFiltros.setEnabled(False)
            self.ui.frProveedor.setToolTip(u"")
            self.ui.frFiltros.setToolTip(message4Filter.rstrip("\n"))
        else:
            self.ui.frFiltros.setEnabled(True)
            self.ui.frFiltros.setToolTip(u"")

        if message4New:
            self.aAdd.setEnabled(False)
            self.aAdd.setToolTip(message4New.rstrip("\n"))
        else:
            self.aAdd.setEnabled(True)
            self.aAdd.setToolTip(u"Presiona para registrar una Orden de Compra nueva")

        # self.aModificar.setEnabled(False)
        # self.aModificar.setToolTip(u"La modificación de Órden de compra no está implementada")
        if message4Edit:
            self.aModificar.setEnabled(False)
            self.aModificar.setToolTip(message4Edit.rstrip("\n"))
        else:
            self.aModificar.setEnabled(True)
            self.aModificar.setToolTip(u"Presiona para modificar los datos de la Orden de Compra seleccionada")

        if message4Remove:
            self.aRemove.setEnabled(False)
            self.aRemove.setToolTip(message4Remove.rstrip("\n"))
        else:
            self.aRemove.setEnabled(True)
            self.aRemove.setToolTip(u"Presiona para eliminar la Orden de compra seleccionada")

        if message4Print:
            self.aPrint.setEnabled(False)
            self.aPrint.setToolTip(message4Print.rstrip("\n"))
        else:
            self.aPrint.setEnabled(True)
            self.aPrint.setToolTip(u"Presiona para Imprimir las compras mostradas")

        if self.message4Info:
            self.cnt.information_set(self.message4Info)
        else:
            self.cnt.information_set(u"")



    def data_update(self, *args):
        """orders.view.Manager.data_update()"""

        # if self.isVisible() and not self.upToDate:
        if self.isVisible():

            self.mst.appCursor_set(QtCore.Qt.WaitCursor)

            filtros = {}

            if self.ui.cbProveedor.currentIndex() > 0:
                filtros['rol_id'] = self.ui.cbProveedor.currentData()

            old = self.currentId()

            all = 0
            status = []
            if self.ui.ch1.isChecked():
                status.append('open')
                all += 1
            if self.ui.ch2.isChecked():
                status.append('closed')
                all += 1
            if self.ui.ch3.isChecked():
                status.append('cancelado')
                all += 1

            if not all == 3:
                filtros['status'] = status

            filtros['document kind_code'] = 12513

            orders = self.cnt.get_processes_using(**filtros)

            # self.ui.listTA.setSortingEnabled(False)
            self.ui.listTA.setRowCount(0)
            
            for indexProceso, process in enumerate(orders):
                
                self.ui.listTA.insertRow(indexProceso)
                #~ try:
                if True:
                    
                    document = [doc for doc in process.documents if doc.kind['code'] == 12513][0]
                    
                    item = cdTableWidgetItem.CDTableWidgetItem(u"{} {}".format(document.rol['person']['name'], document.rol['person']['name2']))
                    item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
                    item.setData(self.ui.listTA.DOCUMENT, document)
                    item.setData(self.ui.listTA.DOCUMENT_ID, process.id)
                    item.setData(1001, indexProceso)
                    item.setData(self.ui.listTA.PROCESS, process)
                    self.ui.listTA.setItem(indexProceso, 0, item)

                    item = QtGui.QTableWidgetItem("{}".format(document.number))
                    item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.listTA.setItem(indexProceso, 1, item)

                    item = QtGui.QTableWidgetItem(document.date.strftime("%d %b %Y"))
                    item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.listTA.setItem(indexProceso, 2, item)

                    item = QtGui.QTableWidgetItem(document.status.capitalize())
                    item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.listTA.setItem(indexProceso, 3, item)

                    item = QtGui.QTableWidgetItem("%.2f" % document.total)
                    item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
                    item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                    self.ui.listTA.setItem(indexProceso, 4, item)

                    item = QtGui.QTableWidgetItem("")
                    self.ui.listTA.setItem(indexProceso, 5, item)

                #~ except:
                else:
                    print ("Error at orders.view.Manager.data_update()")
                    print (sys.exc_info())


            self.ui.listTA.resizeColumnToContents(0)

            self.setCurrentId(old)

            self.updateButtons()

            # self.upToDate = True

            # self.ui.listTA.setSortingEnabled(True)
            self.ui.listTA.horizontalHeader().setSortIndicator(1, QtCore.Qt.DescendingOrder)

            self.mst.appCursor_set(QtCore.Qt.ArrowCursor)



class CaptureView(view.CaptureView):

    def __init__(self, *args, **kwds):
        
        view.CaptureView.__init__(self, *args, **kwds)

        # oldLevel = self.cnt.app.stdoutLog.level
        # self.cnt.app.stdoutLog.setLevel(logging.INFO)
        self.cnt.app.stdoutLog.info("    orders view     CaptureView.__init__()")
        
        
        # self.connect(self.ui.frame, QtCore.SIGNAL('returnPressed()'), self.returnPressed)

        # frameFont = QtGui.QFont()
        # frameFont.setBold(True)
        # frameFont.setPointSize(12 * self.mst.layoutZoom)

        # self.ui.titulo.setFont(font)
        # self.ui.titulo.hide()
        
        

        self.ui.searchFR.hide()

        ## Document Status
        self.connect(self.ui.statusSL, QtCore.SIGNAL("changed()"), self.update_status)

        ## ENTITY
        self.connect(self.ui.entityCB, QtCore.SIGNAL("currentIndexChanged(int)"), self.entity_update)

        ## Fecha
        self.ui.dateED.setMaximumDate(QtCore.QDate().currentDate())

        # self.impuestoGeneralFactor = (self.cnt.app.generalTax + Decimal('100')) / Decimal('100')
        
        ## PRODUCT SELECTOR
        # self.ui.productSelector = productSelector.Form(self)
        self.ui.productSelector.setStyleColor("#E4D460")
        # self.ui.captureLY.addWidget(self.ui.productSelector)

        # self.connect(self.ui.productSelector, QtCore.SIGNAL('originChanged()'), self.origin_update)
        # self.connect(self.ui.productSelector, QtCore.SIGNAL('productSelected()'), self.setItem)

        # self.connect(self.ui.productSelector, QtCore.SIGNAL('addProduct()'), self.addProduct)


        ## Tabla partidas
        # self.ui.itemsTA = itemsTable.Form(self, self.ui.captureFR, cnt=self.cnt, task=self.task)

        self.ui.captureLY.addWidget(self.ui.itemsTA)

        self.connect(self.ui.itemsTA, QtCore.SIGNAL('editingFinished()'), self.partidaCapturada)

        ## Cargar Lista
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.boCargarLista.setIcon(icon)
        self.ui.boCargarLista.setToolTip(u"Presione para cargar la lista de todos los productos del proveedor")
        self.connect(self.ui.boCargarLista, QtCore.SIGNAL("clicked()"), self.loadList)


        ## Linea

        ## Subtotal

        ## Discount

        ## Discount Factor

        ## Tax

        ## Tax Factor
        # impuesto = self.cnt.app.generalTax
        # self.ui.taxFactorED.setText("%s" % impuesto)

        ## Total


        ####  BUTTONS  ####

        ## Guardar
        self.ui.saveBU.setIconSize(QtCore.QSize(32,32))

        ## Cancelar
        self.ui.cancelBU.setIconSize(QtCore.QSize(32,32))


        self.connect(self, QtCore.SIGNAL('showed()'), self.showed)

        # self.impuestoGeneralFactor = (self.cnt.app.generalTax + Decimal('100')) / Decimal('100')

        # self._rangoPrecioActual = 0

        # self.origin_set(self.cnt.app.holder)
        
        self.cnt.app.stdoutLog.info("    orders view     CaptureView.__init__() - END")
        # self.cnt.app.stdoutLog.setLevel(oldLevel)



    # _modificationMessages = u''
    # def get_modificationMessages(self):
        # return self._modificationMessages
    # def set_modificationMessages(self, value):
        # self._modificationMessages = value
    # modificationMessages = property(get_modificationMessages, set_modificationMessages)


    __rolKind_code = None
    def getRolKind_code(self):
        return self.__rolKind_code
    def setRolKind_code(self, value):
        f=t
        self.__rolKind_code = value
        self.entities_load()
    rolKind_code = property(getRolKind_code, setRolKind_code)

    __rolKind = None
    def getRolKind(self):
        return self.__rolKind
    def setRolKind(self, value):
        self.__rolKind = value
        kind = self.cnt.rolKind(name=self.__rolKind)
        self.__rolKind_code = kind['code']
    rolKind = property(getRolKind, setRolKind)

    def clear(self):
        # print("""    orders.view.Capture.clear()""")
        self.state_set(self.cnt.BUSY)

        self.ui.statusSL.setCurrentData(11203, initialToo=True)

        self.ui.entityCB.setCurrentIndex(0)

        self.ui.boCargarLista.setEnabled(False)


        self.ui.productSelector.clear()

        self.ui.itemsTA.setRowCount(0)

        self.ui.subtotalED.clear()
        self.ui.discountED.clear()

        self.impuestoIncluido_set(False)
        
        self.ui.taxED.clear()

        self.ui.totalED.clear()


        self.ui.textTotalLA.clear()

        self.initialDocument = None

        self.state_reset()

        # print("""    orders.view.Capture.clear() - END""")

    '''
    def codigoProductoSeleccionado(self, completerModelIndex):
        completerRow = completerModelIndex.row()

        model = self.ui.codeED.completer().completionModel()

        exec("product = {}".format(model.data(model.index(completerRow, 0), self.mst.DATAROLE_PRODUCT).toString()))

        # ! checar el costo

        # self.ui.itemsTA.setDatosRenglon(rowIndex=-1, product=product, cantidad=Decimal('0.0'), precio=acepcionRol['cost'])
        self.ui.itemsTA.setDatosRenglon(rowIndex=-1, product=product)

        self.ui.codeED.setText("")
        self.ui.nameED.setText("")
        self.ui.lineCB.setCurrentIndex(0)

        self.ui.nameFR.setEnabled(True)
        self.ui.nameFR.setToolTip("")
        self.ui.lineFR.setEnabled(True)

        self.ui.itemsTA.setCurrentCell(self.ui.itemsTA.rowCount()-1, self.ui.itemsTA.QUANTITY)
        self.ui.itemsTA.editItem(self.ui.itemsTA.item(self.ui.itemsTA.rowCount()-1, self.ui.itemsTA.QUANTITY))

        self.update_status()
    '''

    def set_data(self, document):
        # oldLevel = self.cnt.app.stdoutLog.level
        # self.cnt.app.stdoutLog.setLevel(logging.INFO)
        self.cnt.app.stdoutLog.info("    orders view     CaptureView.set_data()")
        
        self.state_set(self.cnt.BUSY)

        view.CaptureView.set_data(self, document)

        ## Pedido
        
        if document.status is None:
            self.ui.statusSL.setCurrentData(11203, initialToo=True)
        elif document.status == 'pendiente':
            self.ui.statusSL.setCurrentData(11203, initialToo=True)
        elif document.status == 'cancelado':
            self.ui.statusSL.setCurrentData(11217, initialToo=True)
        elif document.status == 'entregado':
            self.ui.statusSL.setCurrentData(11215, initialToo=True)
        elif document.status == 'closed':
            self.ui.statusSL.setCurrentData(11219, initialToo=True)

        try:
            self.ui.numberED.setText("{}".format(document.number))
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document number\n""")
            raise

        try:
            self.ui.dateED.setDate(QtCore.QDate().fromString(document.date.strftime("%Y-%m-%d"), QtCore.Qt.ISODate), initialToo=True)
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document date\n""")
            raise

        try:
            if document.rol:
                entity = document.rol
                self.entity_set(entity, initialToo=True)
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document rol\n""")
            raise

        ## Partidas
        try:
            items = document.items
            if not document.items:
                if document.id:
                    items = self.cnt.documentItems(document_id=document.id)
            if items:
                self.ui.itemsTA.setDatos(items)
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document items\n""")
            raise
        
        try:
            self.ui.subtotalED.setValue(document.subtotal, initialToo=True)
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document subtotal\n""")
            raise
            
        try:
            if document.discounts:
                self.ui.discountED.setValue(document.discounts[0].value, initialToo=True)
                # self.ui.discountED.setText("%.2f" % document['discount'])
                if document.discounts[0].factor:
                    discountPercent = document.discounts[0].factor
                else:
                    discountPercent = Decimal('0')
                    
                self.ui.discountFactorED.setValue(discountPercent, initialToo=True)
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document discounts\n""")
            raise                        

        try:
            if document.taxes:
                tax = document.taxes['general']
                
                # 2015.01.22 self.ui.taxED.setValue(document['tax'], initialToo=True)
                self.ui.taxED.setValue(tax['amount'], initialToo=True)
                
                # 2015.01.22 if document['taxpercent']:
                if tax['factor']:
                    taxPercent = tax['factor']
                else:
                    taxPercent = Decimal('0')
                self.ui.taxFactorED.setValue(taxPercent, initialToo=True)
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document taxes\n""")
            raise
        
        try:
            self.ui.totalED.setValue(document.total, initialToo=True)
        except:
            print (""">>> Error @ orders.CaptureView.set_data()""")
            print ("""    Could not set document total\n""")
            raise
    
        self.state_reset()

        self.cnt.app.stdoutLog.info("    orders view     CaptureView.set_data() - END")
        # self.cnt.app.stdoutLog.setLevel(oldLevel)


    def modifiedData(self):
        data = {}
        messages = u""

        documents = []

        document = {}
        
        if self.ui.statusSL.isModified() or self.task == self.ADD:
            if unicode(self.ui.statusSL.text()) == 'Pendiente':
                document['status'] = u'pendiente'
            elif unicode(self.ui.statusSL.text()) == 'Entregado':
                document['status'] = u'entregado'
            elif unicode(self.ui.statusSL.text()) == 'Cancelado':
                document['status'] = u'cancelado'
            elif unicode(self.ui.statusSL.text()) == 'Cerrado':
                document['status'] = u'closed'
            messages += u"Status modificado\n"

        if self.ui.numberED.isModified() or self.task == self.ADD:
            document['number'] = unicode(self.ui.numberED.text())
            messages += u"Folio modificado\n"

        if self.ui.dateED.isModified():
            document['date'] = self.ui.dateED.dateTime().toPyDateTime()
            messages += u"Fecha Modificada\n"

        if self.ui.entityCB.isModified():
            document['rol_id'] = self.ui.entityCB.currentData()
            messages += u"Proveedor cambiado\n"

        if self.ui.subtotalED.isModified():
            document['subtotal'] = self.ui.subtotalED.value()
            messages += u"Subtotal modificado\n"

        if self.ui.discountED.isModified():
            document['discount'] = self.ui.discountED.value()
            messages += u"Descuento modificado\n"

        if self.ui.discountFactorED.isModified():
            document['discountpercent'] = self.ui.discountFactorED.value()
            messages += u"Porcentaje de descuento modificado\n"

        if self.ui.taxED.isModified():
            document['tax'] = self.ui.taxED.value()
            messages += u"Impuesto modificado\n"

        if self.ui.taxFactorED.isModified():
            document['taxpercent'] = self.ui.taxFactorED.value()
            messages += u"Porcentaje de impuesto modificado\n"

        if self.ui.totalED.isModified():
            document['total'] = self.ui.totalED.value()
            messages += u"Total modificado\n"

        if self.task == self.ADD or self.ui.itemsTA.isModified():
            # items = self.ui.itemsTA.modifiedData()
            # if items:
                # document['items'] = items
                # messages += self.ui.itemsTA.modificationMessages
            
            items = []
            for item in self.document.items:                
                items.append(item.data)
            
            document['items'] = items
            
        if document:
            if self.task == self.EDIT:
                document['id'] = self.initialDocument.id

            elif self.task == self.ADD:
                document['status'] = u"pending"
                document['kind'] = {'code':12513}

            # document_ = self.Document(self.cnt, document)

            documents.append(document)

        if documents:
            data['documents'] = documents
            if self.task == self.EDIT:
                data['id'] = self.processId

        self.modificationMessages = messages.rstrip("\n")

        return data


    def load_documentKinds(self, processFase):
        # print("    processes view CaptureView.load_documentKinds()")
        
        self.ui.documentKindLA.clear()
        self.ui.documentKindLA.references = []

        kinds = self.cnt.documentKinds_pull(reference=processFase, cast_=self.cnt.cast)
        
        for index, kind in enumerate(kinds):
            self.ui.documentKindLA.setItemText(index, kind['name'].capitalize())
            self.ui.documentKindLA.setItemData(index, kind['code'])
            self.ui.documentKindLA.setItemData(index, kind, role=1001)
            self.ui.documentKindLA.references.append(kind['value'])
        
        # self.ui.documentKindLA.current_setByData(int(self.cnt.documentKinds_pull(name='default', reference=processFase, cast_=self.cnt.cast)[0]['value']))

        # print("    processes view CaptureView.load_documentKinds() - END")


    def documentStatuss_load(self):
        # print("""   orders.view.Capture.documentStatuss_load()""")
        
        statuss = self.cnt.documentStatuss()
        for status in statuss:
            self.ui.statusSL.addItem(status['name'], status['code'])

        # print("""   orders.view.Capture.documentStatuss_load() - END""")


    def editt(self, order):
        f=g
        self.task = self.EDIT
        self.taxMode = self.NO_TAX

        self.ui.titulo.setText(QtGui.QApplication.translate("Empresa Básica", "ORDEN DE COMPRA - MODIFICACIÓN", None, QtGui.QApplication.UnicodeUTF8))

        self.clear()

        self.processId = order.id
        self.setData(order)
        # order = self.cnt.process(id=id)

        self.ui.entityCB.setEnabled(False)

        self.ui.codeED.setEnabled(True)
        self.ui.nameED.setEnabled(True)
        self.ui.lineCB.setEnabled(True)

        self.update_status()

        self.cnt.information_set(u"Para capturar partidas debe localizar el producto, por medio de su código o de su nombre")

        self.mst.setInnerStatus('hidden')

        self.show()


    def init(self, *args, **kwds):
        self.cnt.app.stdoutLog.info("    orders view     CaptureView.init()")

        view.CaptureView.init(self, *args, **kwds)

        '''
        ## Tipo de documento
        try:
            self.ui.numberED.setText(document.number)
        except:
            print (""">>> Error @ sales.CaptureView.set_data()""")
            print ("""    Could not set document number\n""")
            raise
        '''

        ## ENTITY
        self.ui.entityCB.setMaxVisibleItems(15)
        
        self.entities_load()

        # self.impuestoGeneralFactor = (self.cnt.app.generalTax + Decimal('100')) / Decimal('100')
        self.loadPaymentConditions()
        self.loadLines()
        self.documentStatuss_load()

        self.load_documentKinds('order')

        # impuesto = self.cnt.app.generalTax
        # self.ui.taxFactorED.setText("{}".format(impuesto))
        
        self.ui.productSelector.init()
        
        self.taxMode = self.txSTRIPPED
        
        self.ui.itemsTA.init()

        self.cnt.app.stdoutLog.info("    orders view     CaptureView.init() - END")


    def isModified(self):
        if self.modifiedData():
            return True
        else:
            return False


    def isValid(self):
        isValid = True
        self.mensajes = ""

        if not self.ui.dateED.lineEdit().text():
            isValid = False
            self.mensajes += u"Falta la fecha\n"

        if not self.ui.entityCB.currentIndex() > 0:
            isValid = False
            self.mensajes += u"Debe seleccionar un proveedor\n"

        partidasValidas = self.ui.itemsTA.isValid()
        if not partidasValidas:
            isValid = False
            self.mensajes += self.ui.itemsTA.validityMessages

        if not self.ui.subtotalED.isValid():
            isValid = False
            self.mensajes += u"Subtotal fuera de rango\n"

        if not self.ui.discountFactorED.isValid():
            isValid = False
            self.mensajes += u"Porcentaje de descuento no válido\n"

        if not self.ui.discountED.isValid():
            isValid = False
            self.mensajes += u"Descuento fuera de rango\n"

        if not self.ui.taxFactorED.isValid():
            isValid = False
            self.mensajes += u"Porcentaje de impuesto no válido\n"

        if not self.ui.taxED.isValid():
            isValid = False
            self.mensajes += u"Impuesto fuera de rango\n"

        if not self.ui.totalED.isValid():
            isValid = False
            self.mensajes += u"Total fuera de rango\n"
            
        ## Search matching saved document
        if self.task == self.EDIT and self.cnt.order_exists(documents=[{'number':unicode(self.ui.numberED.text()), 'rol_id':self.ui.entityCB.currentData()}]):
            isValid = False
            self.mensajes += u"Ya existe un pedido con este Folio para este proveedor\n"

        self.mensajes = self.mensajes.rstrip("\n")

        return isValid


    @property
    def impuestoIncluido(self):
        return self._impuestoIncluido
    def impuestoIncluido_set(self, value):
        
        if self.state is self.cnt.IDLE:
        
            if value:
                self._impuestoIncluido = True
            else:
                self._impuestoIncluido = False

            self.update_total()
            # self.ui.itemsTA.subtotal_update()


    def loadLines(self):
        lines = self.cnt.productLines()
        self.ui.lineCB.clear()
        self.ui.lineCB.addItem("", -1)
        for line in lines:
            self.ui.lineCB.addItem(line['name'], line['id'])


    def loadList(self):
        # print("""    orders.CaptureView.loadList()""")
        
        self.setCursor(QtCore.Qt.WaitCursor)

        products = self.cnt.products(rol_id=self.ui.entityCB.currentData(), status=[40161, 40163])

        self.ui.itemsTA.setRowCount(0)
        # self.ui.itemsTA.setSortingEnabled(False)
        
        self.ui.itemsTA.state_set(self.cnt.BUSY)
        
        for index, product in enumerate(products):
            item = self.document.item_insert(index, product=product)
            
            self.ui.itemsTA.insertRow(index)
            self.ui.itemsTA.setDatosRenglon(index, instance=item)
            
        self.ui.itemsTA.state_reset()

        #! What's this!!!   update_total()  should be called aparte
        # self.ui.itemsTA.subtotal_update()

        # self.ui.itemsTA.setSortingEnabled(True)

        self.ui.boCargarLista.setEnabled(False)
        self.ui.itemsTA.setFocus()

        self.update_total()

        self.setCursor(QtCore.Qt.ArrowCursor)

        # print("""    orders.CaptureView.loadList() - END""")
        

    def loadPaymentConditions(self):
        conditions = self.cnt.paymentConditions()
        for condition in conditions:
            self.ui.cbCondiciones.addItem(condition['name'], condition['code'])
        self.ui.cbCondiciones.setCurrentIndex(-1)


    def new(self):
        f=g
        self.task = self.ADD
        self.taxMode = self.NO_TAX

        self.ui.titulo.setText("ORDEN DE COMPRA NUEVA")

        self.clear()

        self.ui.numberED.setText(self.cnt.documentNumber(cast_=self.mst.cast)[1])

        self.ui.dateED.setDate(QtCore.QDate().currentDate())

        self.ui.entityCB.setEnabled(True)

        self.ui.codeED.setEnabled(True)
        self.ui.nameED.setEnabled(True)
        self.ui.lineCB.setEnabled(True)

        self.ui.nameED.setFocus()

        self.cnt.information_set(u"Para capturar partidas debe localizar el producto, por medio de su código o de su nombre")

        self.update_status()

        self.mst.setInnerStatus('hidden')

        self.show()


    def nombreProductoSeleccionado(self, completerModelIndex=None):
        """orders.view.Capture.nombreProductoSeleccionado()"""
        completerRow = completerModelIndex.row()

        model = self.ui.nameED.completer().completionModel()

        product = eval( "{}".format( model.data( model.index(completerRow, 0), self.mst.DATAROLE_PRODUCT ).toString() ) )


        # ! checar el costo

        self.ui.itemsTA.setDatosRenglon(rowIndex=-1, product=product)

        self.ui.codeED.setText("")
        self.ui.nameED.setText("")
        self.ui.lineCB.setCurrentIndex(0)

        self.ui.itemsTA.setCurrentCell(self.ui.itemsTA.rowCount()-1, itemsTable.COL_QUANTITY)
        self.ui.itemsTA.editItem(self.ui.itemsTA.item(self.ui.itemsTA.rowCount()-1, itemsTable.COL_QUANTITY))

        self.update_status()


    def partidaCapturada(self):
        """pedidos.igu.Capture.partidaCapturada()"""
        self.ui.itemsTA.clearSelection()
        self.ui.nameED.setFocus()

    # @property
    # def rangoPrecioActual(self):
        # return self._rangoPrecioActual


    def returnPressed(self):
        m = "pedidos.igu.Capture.returnPressed()"
        if self.ui.saveBU.isEnabled():
            self.save()
        

    def save(self):
        #! This should call Process instance's method save
        #! Process data must be well hooked to data edition widgets
        
        ## No se revisa validez de datos, para llegar aquí se tuvo que haber hecho

        # oldLevel = self.cnt.app.stdoutLog.level
        # self.cnt.app.stdoutLog.setLevel(logging.INFO)
        self.cnt.app.stdoutLog.info("    orders view     CaptureView.save()")
        
        # data = self.modifiedData()

        if self.task == self.ADD:
            # order_id = self.cnt.process_save(**data)
            
            self.document.status_set('open')

            status = self.document.process.push()
            
            #! ReThink this
            # if status == 'acepcion changed':
                # self.mst.eventRouter.emit(QtCore.SIGNAL('productosChanged()'))
        else:
            order_id = data['id']
            self.cnt.process_save(data)
        
        # process = self.cnt.process(id=order_id)
                
        # self.mst.details.setData(process)


        self.hide()


        # document = self.cnt.create_process()
        # document.new()
        
        self.mst.eventRouter.emit(QtCore.SIGNAL("ordersChanged()"))

        self.emit(QtCore.SIGNAL('captureViewClosed()'))

        self.cnt.app.stdoutLog.info("    orders view     CaptureView.save() - END")
        # self.cnt.app.stdoutLog.setLevel(oldLevel)

        # self.close()


    '''
    def setItem(self):
        # print("""\n    orders.view.Capture.setItem()""")
        
        # product = eval("{}".format(item))
        product = self.sender().data
        
        self.ui.itemsTA.insertRow()

        self.ui.itemsTA.setDatosRenglon(rowIndex=-1, product=product)
        
        self.ui.itemsTA.setCurrentCell(self.ui.itemsTA.rowCount()-1, itemsTable.COL_QUANTITY)
        self.ui.itemsTA.editItem(self.ui.itemsTA.item(self.ui.itemsTA.rowCount()-1, itemsTable.COL_QUANTITY))

        self.update_status()

        # print("""    orders.view.Capture.setItem() - END""")
    '''

    def get_task(self):
        return self._task
    def set_task(self, value):
        # print("""    orders.view.Capture.set_task()""")
        
        self._task = value
        
        self.ui.itemsTA.task = value

        self.taxMode = self.NO_TAX

        self.ui.titulo.setText("ORDEN DE COMPRA NUEVA")

        # self.clear()

        self.ui.numberED.setText(self.cnt.documentNumber(name="order", cast_=self.mst.duty)[1])

        self.ui.dateED.setDate(QtCore.QDate().currentDate())
        self.document.date_set(self.ui.dateED.dateTime().toPyDateTime())

        self.ui.entityCB.setEnabled(True)

        self.ui.codeED.setEnabled(True)
        self.ui.nameED.setEnabled(True)
        self.ui.lineCB.setEnabled(True)

        self.ui.nameED.setFocus()

        self.cnt.information_set(u"Para capturar partidas debe localizar el producto, por medio de su código o de su nombre")

        self.update_status()

        self.mst.setInnerStatus('hidden')

        self.show()
        
        # print("""    orders.view.Capture.set_task()""")
    task = property(get_task, set_task)


    def entity_update(self):
        """orders.view.Capture.entity_update()"""
        if self.state is self.cnt.IDLE:
            
            self.setCursor(QtCore.Qt.WaitCursor)

            origin = eval("{}".format(self.ui.entityCB.currentData(self.mst.DATAROLE_ROL)))
            
            self.document.rol_set(origin)
            
            self.ui.productSelector.dealer_set(origin)

            self.ui.itemsTA.origin_set(origin)

            self.update_total()
            # self.ui.itemsTA.subtotal_update()

            self.ui.boCargarLista.setEnabled(True)

            self.setCursor(QtCore.Qt.ArrowCursor)


    def entity_set(self, entity, initialToo=False):
        """orders.view.Capture.entity_set()"""
        self.ui.entityCB.setCurrentData(entity['id'], initialToo=initialToo)
        self.ui.productSelector.origin_set(entity)
        self.ui.itemsTA.origin_set(entity)


    def entities_load(self, entities=None):
        """orders.view.Capture.entities_load()"""
        
        self.state_set(self.cnt.BUSY)
        
        if not entities:
            entities = self.cnt.entities()

        oldAtCapture = self.ui.entityCB.currentData()

        self.ui.entityCB.clear()
        # 2015.01.18 self.ui.entityCB.addItem(u"", self.cnt.app.holder['id'])
        self.ui.entityCB.addItem(u"", -1)
        # 2015.01.18 self.ui.entityCB.setItemData(0, repr(self.cnt.app.holder), self.mst.DATAROLE_ROL)

        if entities:
            for entity in entities:
                self.ui.entityCB.addItem(u"{} {}".format(entity['person']['name'], entity['person']['name2']), entity['id'])
                self.ui.entityCB.setItemData(self.ui.entityCB.count()-1, repr(entity), self.mst.DATAROLE_ROL)
        else:
            # self.ui.entityCB.addItem("Debe dar de alta al proveedor", self.cnt.app.holder)
            self.ui.entityCB.addItem("Debe dar de alta al proveedor", -1)
            # self.ui.entityCB.setItemData(self.ui.entityCB.count()-1, self.cnt.app.holder, self.mst.DATAROLE_ROL)
            self.ui.entityCB.setItemData(self.ui.entityCB.count()-1, "", self.mst.DATAROLE_ROL)

        if oldAtCapture:
            if oldAtCapture >= 0:
                self.ui.entityCB.setCurrentData(oldAtCapture)
            else:
                self.ui.entityCB.setCurrentIndex(0)
        else:
            self.ui.entityCB.setCurrentIndex(0)

        self.state_reset()


    def origin_update(self):
        """orders.view.Capture.origin_update()"""
        self.ui.itemsTA.origin_set(self.ui.productSelector.origin())


    # def state_get(self):
        # return self._state[-1]
    # def state_set(self, value):
        # self._state.append(value)
    # state = property(state_get, state_set)
    # def state_reset(self):
        # self._state.pop()


    def showed(self):
        self.cnt.information_set(u"Para capturar partidas debe localizar el producto, por medio de su código o de su nombre")


    def update_total(self):
        # print("    orders view    Capture.update_total()")
        
        subtotal = self.ui.itemsTA.subtotal()

        if self.ui.discountFactorED.value():
            descuento = subtotal * self.ui.discountFactorED.value() / Decimal("100")
        else:
            descuento = Decimal("0.00")

        total = subtotal - descuento
        
        if self.ui.taxFactorED.text():
            impuesto = total * self.ui.taxFactorED.value() / Decimal("100")
        else:
            impuesto = Decimal("0.00")

        total += impuesto
        self.ui.subtotalED.setValue(subtotal)
        self.ui.discountED.setValue(descuento)
        self.ui.taxED.setValue(impuesto)
        self.ui.totalED.setValue(total)
        
        self.document.subtotal_set(subtotal)
        self.document.discounts_set([{'amount':descuento, 'factor':self.ui.discountFactorED.value()}])
        
        self.document.taxes_set({'general':{'name':self.ui.taxFactorED.name, 'amount':impuesto, 'factor':self.ui.taxFactorED.value()}})
        self.document.total_set(total)
        
        if total:
            self.ui.textTotalLA.setText("Son {}".format(utilities.moneyToText(Decimal(str(total)))))
        
        self.update_status()

        # print("    orders view    Capture.update_total() - END")


    def ui_set(self):
        self.ui = capture_ui.Ui_Form()
        self.ui.setupUi(self)



class Details(view.Details):

    # @property
    # def state(self):
        # return self._state[-1]
    # def state_set(self, value):
        # self._state.append(value)
    # def state_reset(self):
        # self._state.pop()

    def __init__(self, *args, **kwds):
        
        
        # self.mst = args[0]
        # self.cnt = self.mst.cnt

        view.Details.__init__(self, *args)

        self.ui = details_ui.Ui_Form()
        self.ui.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.toImprimir.setIcon(icon)
        self.connect(self.ui.toImprimir, QtCore.SIGNAL("clicked()"), self.imprimir)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Recycle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.toExportar.setIcon(icon)
        self.ui.toExportar.setToolTip(u"Exportar a formato xls")
        self.connect(self.ui.toExportar, QtCore.SIGNAL("clicked()"), self.exportarDetails)

        
        
        
        
        
        # self.connect(self.mst.eventRouter, QtCore.SIGNAL('pedidosChanged()'), self.update)
        self.impresor = QtGui.QPrinter()
        # self._state = [self.cnt.IDLE]
        
    
    def exportarDetails(self):
        
        try:
            path = self.cnt.path()
            
            # order = [x for x in self.data.documents if x.kind['code']==12513][0]
            
            order = self.data
            
            items = self.cnt.documentItems(document_id=order.id)
            
            filename = QtGui.QFileDialog.getSaveFileName(self, u"{} - Selecciona la ubicación del documento".format(self.cnt.app.name), os.path.join(path, "OrdComp{}.xls".format("{}-{}".format(order.number, (u"{}{}".format(order.rol['person']['name'], order.rol['person']['name2'])).replace(u'á', 'a').replace(u'é', 'e').replace(u'í', 'i').replace(u'ó', 'o').replace(u'ú', 'u').replace(u'ñ','n').replace('\n', '_')).replace(" ", "").replace(".", "").replace(",", "_"), "Orders (*.pdf)")))
            
            if filename:
            
                self.setCursor(QtCore.Qt.WaitCursor)
                
                mainTitleStyle = xlwt.easyxf('font:name Arial, color-index red, bold on', num_format_str='#,##0.00')
                style1 =         xlwt.easyxf(num_format_str='D-MMM-YY')
                fieldStyle =     xlwt.easyxf('pattern:pattern solid, fore-color gray25; font:height 160; align:horiz center')
                headerStyle =    xlwt.easyxf('pattern:pattern solid, fore-color gray25; font:height 160, color-index black; align:horiz center')

                wb = xlwt.Workbook()
                ws = wb.add_sheet('Hoja 1')

                index = 0
                ws.write(index, 0, "ORDEN DE COMPRA", mainTitleStyle)
                ws.write(index, 2, "Folio", fieldStyle)
                ws.write(index, 4, "Fecha", fieldStyle)

                index += 1
                ws.write(index, 2, order.number, xlwt.easyxf('font:color-index red; align: horiz center'))
                ws.write(index, 4, order.date.strftime("%d %b %Y"), xlwt.easyxf('align: horiz center', num_format_str='D-MMM-YY'))

                index += 1
                ws.write(index, 0, "Emisor", fieldStyle)
                ws.write(index, 1, "", fieldStyle)
                ws.write(index, 2, "", fieldStyle)
                ws.write(index, 3, "Proveedor", fieldStyle)
                ws.write(index, 4, "", fieldStyle)

                index += 1
                ws.write(index, 0, u"{} {}".format(self.cnt.app.holder['person']['name'], self.cnt.app.holder['person']['name2']))
                ws.write(index, 2, u"{} {}".format(order.rol['person']['name'], order.rol['person']['name2']))

                index += 1
                ws.write(index, 0, u"{} Num.{} {}".format(self.cnt.app.holder['addresses'][0]['street'], self.cnt.app.holder['addresses'][0]['site_number'], self.cnt.app.holder['addresses'][0]['areaname']))
                ws.write(index, 2, u"{} Num.{} {}".format(order.rol['addresses'][0]['street'], order.rol['addresses'][0]['site_number'], order.rol['addresses'][0]['areaname']))

                index += 1
                ws.write(index, 0, u"{} {}, {}".format(self.cnt.app.holder['addresses'][0]['postalcode'], self.cnt.app.holder['addresses'][0]['place']['name'], self.cnt.app.holder['addresses'][0]['state']['shortname']))
                ws.write(index, 2, u"{} {}, {}".format(order.rol['addresses'][0]['postalcode'], order.rol['addresses'][0]['place']['name'], order.rol['addresses'][0]['state']['shortname']))

                index += 1
                ws.write(index, 0, u"{}".format(self.cnt.app.holder['person']['rfc']))
                ws.write(index, 2, u"{}".format(order.rol['person']['rfc']))

                index += 2
                ws.write(index, 0, u"CÓDIGO", headerStyle)
                ws.write(index, 1, u"NOMBRE", headerStyle)
                ws.write(index, 2, u"CANTIDAD", headerStyle)
                ws.write(index, 3, u"COSTO", headerStyle)
                ws.write(index, 4, u"IMPORTE", headerStyle)

                index += 1
                for row, item in enumerate(items):
                    aception = [x for x in item['product']['aceptions'] if x['rol_id']==order.rol['id']][0]

                    ws.write(index+row, 0, aception['code'])
                    ws.write(index+row, 1, aception['name'])
                    ws.write(index+row, 2, item['quantity'], xlwt.easyxf('align: horiz center'))
                    ws.write(index+row, 3, item['price'], xlwt.easyxf(num_format_str='#,##0.00'))
                    ws.write(index+row, 4, item['quantity'] * item['price'], xlwt.easyxf(num_format_str='#,##0.00'))

                index += row + 2
                ws.write(index, 3, "Subtotal", fieldStyle)
                ws.write(index, 4, order.subtotal, xlwt.easyxf(num_format_str='#,##0.00'))

                index += 1
                ws.write(index, 3, "Descuentos", fieldStyle)
                if order.discounts:
                    ws.write(index, 4, order.discounts[0]['amount'], xlwt.easyxf(num_format_str='#,##0.00'))

                index += 1
                ws.write(index, 3, "Impuestos", fieldStyle)
                ws.write(index, 4, order.taxes['general']['amount'], xlwt.easyxf(num_format_str='#,##0.00'))

                index += 1
                ws.write(index, 3, "Total", fieldStyle)
                ws.write(index, 4, order.total, xlwt.easyxf(num_format_str='#,##0.00'))

                ws.col(1).width = ws.col(1).width * 3

                wb.save(filename)

                self.setCursor(QtCore.Qt.ArrowCursor)
                
                result = QtGui.QMessageBox.information(self, u"Empresa Básica - Exportación de pedido", u"Archivo {} creado".format(filename, QtGui.QMessageBox.Ok), QtGui.QMessageBox.Ok)

        except:
            raise
            print (sys.exc_info())
            result = QtGui.QMessageBox.warning(self, u"Empresa Básica - Exportación de pedido", u"No se realizó la exportación".format(filename), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if sys.exc_info()[1][0]==13:
                print (sys.exc_info()[1][0])
                


    def imprimir(self):
        margenHorizontal, margenVertical = [10, 10]
        pageNo = 1

        dialogoImpresora = QtGui.QPrintDialog(self.impresor)
        if dialogoImpresora.exec_() == QtGui.QDialog.Accepted:
            # result = QtGui.QMessageBox.information(self, u"Empresa Básica - Impresión de pedido", u"Imprimiendo ...", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

            painter = QtGui.QPainter(self.impresor)
            painter.setFont(QtGui.QFont("courier", 10))

            order = [x for x in self.data.documents if x.kind['code']==12513][0]
            items = self.cnt.documentItems(document_id=order.id)

            # pedido = self.cnt.app.model.getOne("pedidos", {'pedido_id':self.selectedId})
            # proveedor = self.cnt.app.model.getOne("proveedores", {'proveedor_id':pedido['proveedor']})
            # partidas = self.cnt.app.model.getAll("partidasPedido", {'pedido_id':pedido['pedido_id']})

            contenido = []

            margenX, margenY = [25, 75]

            x, y = [25, 0];   contenido.append([margenX + x, margenY + y, u"ORDEN DE COMPRA"])
            x, y = [200, 50]; contenido.append([margenX + x, margenY + y, u"Folio: {}".format(order['number'])])
            x, y = [400, 50]; contenido.append([margenX + x, margenY + y, u"Fecha: {}".format(order['date'])])
            x, y = [0, 100];  contenido.append([margenX + x, margenY + y, u"{} {}".format(order.rol['person']['name'], order['rol']['person']['name2'])])
            x, y = [0, 120];  contenido.append([margenX + x, margenY + y, u"{} {}".format(order.rol['address']['street'], order['rol']['address']['areaname'])])
            x, y = [0, 140];  contenido.append([margenX + x, margenY + y, u"{} {}".format(order.rol['address']['postalcode'], order['rol']['address']['placename'])])
            x, y = [0, 160];  contenido.append([margenX + x, margenY + y, u"RFC {}".format(order.rol['person']['rfc'])])
            x, y = [0, 200];  contenido.append([margenX + x, margenY + y, u"Código        Nombre                       Clasificación       Cantidad  Precio    Importe"])
            x, y = [0, 225]
            offset = 0
            for item in items:
                aception = [aception for aception in item['product']['aceptions'] if item['rol']['id']==order['rol']['id']][0]
                contenido.append([margenX + x      , margenY + y + offset, "{}".format(aception['code'])])
                contenido.append([margenX + x + 100, margenY + y + offset, aception['name']])
                contenido.append([margenX + x + 325, margenY + y + offset, item['product']['lines'][0]['name']])
                contenido.append([margenX + x + 525, margenY + y + offset, item['quantity']])
                contenido.append([margenX + x + 600, margenY + y + offset, item['cost']])
                contenido.append([margenX + x + 650, margenY + y + offset, unicode(Decimal(item['quantity']) * Decimal(item['cost']))])
                offset += 20
            x, y = [500, 240]
            contenido.append([margenX + x, margenY + y + offset, u"Subtotal"])
            x, y = [625, 240]
            contenido.append([margenX + x, margenY + y + offset, order['subtotal']])
            x, y = [500, 265]
            contenido.append([margenX + x, margenY + y + offset, u"Descuentos"])
            x, y = [625, 265]
            contenido.append([margenX + x, margenY + y + offset, order['discount']])
            x, y = [500, 290]
            contenido.append([margenX + x, margenY + y + offset, u"IVA"])
            x, y = [625, 290]
            contenido.append([margenX + x, margenY + y + offset, order['tax']])
            x, y = [500, 315]
            contenido.append([margenX + x, margenY + y + offset, u"Total"])
            x, y = [625, 315]
            contenido.append([margenX + x, margenY + y + offset, order['total']])


            for item in contenido:
                painter.drawText(QtCore.QPoint(margenHorizontal + item[0], margenVertical + item[1]), item[2])


            # y = 0
            # fm = p.fontMetrics()
            # metrics = QtGui.QPaintDevice.PaintDeviceMetric(self.impresor)

            # for i in range(view.numLines()):
                # if margin + y > metrics.height() - margin:
                    # pageNo = pageNo + 1
                    # self.impresor.newPage()
                    # y = 0

                # p.drawText(margin,
                           # margin + y,
                           # metrics.width(),
                           # fm.lineSpacing(),
                           # QtCore.Qt.ExpandTabs | QtCore.Qt.DontClip,
                           # view.textLine(i))
                # y = y + fm.lineSpacing()


            # self.statusBar().message('Impresión terminada',2000)
        # else:
            # pass
            # self.statusBar().message('Impresión abortada',2000)


    def setData(self, document):
        self.cnt.app.stdoutLog.info("    orders view         Details.setData()")
    
        self.data = document
        
        document.items_set(self.cnt.documentItems(document_id=document.id))
        
        self.clear()
        
        self.ui.numberLA.setText("{}".format(document.number))
        self.ui.laFecha.setText(document.date.strftime("%d %b %Y"))
        self.ui.laOrigen.setText(u"{} {}".format(document.rol['person']['name'], document.rol['person']['name2']))
        
        self.ui.laSubtotal.setText("%.2f" % document.subtotal)
        
        if document.discounts:
            self.ui.laDescuentos.setText("%.2f" % document.discounts[0]['amount'])
        
        ## Join taxes
        
        self.ui.laImpuestos.setText("%.2f" % document.taxes['general']['amount'])
        
        self.ui.laTotal.setText("%.2f" % document.total)

        labels = [u"Código", u"Nombre", u"Clasificación", u"Cantidad", u"Precio", u"Importe"]
        self.ui.itemsTA.setColumnCount(len(labels))
        self.ui.itemsTA.setHorizontalHeaderLabels(labels)

        self.ui.itemsTA.setRowCount(0)
        
        for itemIndex, item in enumerate(document.items):
            
            self.ui.itemsTA.insertRow(itemIndex)

            self.ui.itemsTA.setRowHeight(itemIndex, 20)

            product = self.cnt.product(id=item.product['id'])
            
            aception = [x for x in product['aceptions'] if x['rol_id']==document.rol['id']][0]

            tableItem = QtGui.QTableWidgetItem("{}".format(aception['code']))
            tableItem.setFlags(tableItem.flags().__xor__(QtCore.Qt.ItemIsEditable))
            self.ui.itemsTA.setItem(itemIndex, 0, tableItem)

            tableItem = QtGui.QTableWidgetItem(u"{}".format(aception['name']))
            tableItem.setFlags(tableItem.flags().__xor__(QtCore.Qt.ItemIsEditable))
            self.ui.itemsTA.setItem(itemIndex, 1, tableItem)

            tableItem = QtGui.QTableWidgetItem(u"{}".format(product['lines'][0]['name']))
            tableItem.setFlags(tableItem.flags().__xor__(QtCore.Qt.ItemIsEditable))
            self.ui.itemsTA.setItem(itemIndex, 2, tableItem)

            tableItem = QtGui.QTableWidgetItem("{}".format(item.quantity))
            tableItem.setFlags(tableItem.flags().__xor__(QtCore.Qt.ItemIsEditable))
            tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.itemsTA.setItem(itemIndex, 3, tableItem)

            tableItem = QtGui.QTableWidgetItem("{}".format(item.cost))
            tableItem.setFlags(tableItem.flags().__xor__(QtCore.Qt.ItemIsEditable))
            tableItem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.ui.itemsTA.setItem(itemIndex, 4, tableItem)

            tableItem = QtGui.QTableWidgetItem("{}".format((item.quantity * item.price).quantize(Decimal('0.01'))))
            tableItem.setFlags(tableItem.flags().__xor__(QtCore.Qt.ItemIsEditable))
            tableItem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.ui.itemsTA.setItem(itemIndex, 5, tableItem)

        # self.ui.itemsTA.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
        
        self.ui.itemsTA.resizeColumnToContents(0)
        self.ui.itemsTA.resizeColumnToContents(1)
        self.ui.itemsTA.resizeColumnToContents(2)
        self.ui.itemsTA.resizeColumnToContents(3)
        self.ui.itemsTA.resizeColumnToContents(4)
        self.ui.itemsTA.resizeColumnToContents(5)

        self.cnt.app.stdoutLog.info("    orders view         Details.setData() - END")


class Splitter(QtGui.QSplitter):

    def __init__(self, *args):
        self.orientation = args[0]
        QtGui.QSplitter.__init__(self, *args)

    def createHandle(self):
        return Handle(self.orientation, self)



class Handle(QtGui.QSplitterHandle):

    def __init__(self, *args):
        QtGui.QSplitterHandle.__init__(self, *args)

    def mouseDoubleClickEvent(self, event):
        self.emit(QtCore.SIGNAL("handlePressed"))


class Modell(QtCore.QAbstractListModel):

    DATAROLE_PRODUCT  = 1030

    def __init__(self, *args):
        QtCore.QAbstractListModel.__init__(self, *args)
        self.__data = []
        self.aceptionIndex = 1004
        self.productIdRole = 1003


    def clear(self):
        # self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        self.__data = []
        self.reset()
        # self.endRemoveRows()


    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            return self.__data[index.row()][index.column()]
        elif role == QtCore.Qt.TextAlignmentRole:
            # if index.column() == CANTIDAD:
                # return int(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            # if index.column() in [PRECIO, IMPORTE]:
                # return int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            return int(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        elif role == 1001:
            return self.__data[index.row()][1]
        elif role == self.DATAROLE_PRODUCT:
            return self.__data[index.row()][5]
        else:
            return


    def insertRow(self, row, parent=QtCore.QModelIndex()):
        self.__data.insert(row, [u"", u""])
        return True


    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__data)


    def setData(self, row, valor, role=QtCore.Qt.DisplayRole):
        """ No se usa la porquería de modelIndex """
        if row >= len(self.__data):
            self.__data.append([None, None, None, None, None, None])

        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            self.__data[row][0] = valor
        elif role == 1001:
            self.__data[row][1] = valor
        elif role == 1003:
            self.__data[row][3] = valor
        elif role == 1004:
            self.__data[row][4] = valor
        elif role == self.DATAROLE_PRODUCT:
            self.__data[row][5] = valor
        else:
            print ("puaje")
            f=g
        return True



"""
    Estados de Pedidos
        pendiente
        autorizada
        remitida
        aceptada
        surtida

    Si el estado de un pedido no es "pendiente", será imposible modificarlo o
        eliminarlo

"""

# background-color:qlineargradient(x1: 0, y1: 0, x2:1, y2:.1, stop: 0 #E0E0E0, stop:0.4#F8F8F8, stop:1 #B0B0B0); border-top-left-radius: 3px; border-top-right-radius: 3px;

if __name__ == "__main__":
    print ('yep')

