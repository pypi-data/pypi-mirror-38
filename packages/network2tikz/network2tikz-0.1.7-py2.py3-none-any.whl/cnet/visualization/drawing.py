#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : drawing.py 
# Creation  : 08 May 2018
# Time-stamp: <Mon 2018-05-21 10:40 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$ 
#
# Description : Module to draw the network
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
# =============================================================================

import numpy as np
from collections import OrderedDict

from cnet import logger
from cnet.utils.exceptions import CnetError
from cnet.visualization.units import UnitConverter
from cnet.visualization.canvas import Canvas
log = logger(__name__)

# TODO: move this to the config file
DIGITS = 3

class TikzNetworkDrawer(object):
    """Class which handles the drawing of the network.

    The default visualization of a network draws the nodes on a 2D plane
    according to a given Layout, then draws a straight or curved edge between
    nodes connected by edges. This is the visualization used when one invokes
    the :py:meth:`plot` function on a Network object.

    Parameters
    ----------
    network : network object
        Network to be drawn. The network can be a 'cnet', 'networkx', 'igraph',
        'pathpy' object, or a tuple of a node list and edge list.

    kwds : keyword arguments, optional (default= no attributes)
        Attributes to add to the drawer as key=value pairs.
        See also :py:meth:`plot`

    See Also
    --------
    plot

    """
    def __init__(self,network,**kwds):
        """Initialize the network drawer.

        Parameters
        ----------
        network : network object
            Network to be drawn. The network can be a 'cnet', 'networkx',
            'igraph', 'pathpy' object, or a tuple of a node list and edge list.

        kwds : keyword arguments, optional (default= no attributes)
            Attributes to add to the drawer as key=value pairs.
            See also :py:meth:`plot`

        """
        # initialize variables
        self.edges = OrderedDict()
        self.nodes = None
        self.directed = False
        self.digits = DIGITS

        self.node_attributes = {}
        self.edge_attributes = {}
        self.general_attributes = {}

        # check type of network
        if 'cnet' in str(type(network)):
            log.debug('The network is of type "cnet".')
            for e,n in network.edges(nodes=True):
                self.edges[e] = n
            self.nodes = list(network.nodes)
            self.directed = network.directed

        elif 'networkx' in str(type(network)):
            log.debug('The network is of type "networkx".')
            for e in network.edges():
                self.edges[e] = e
            self.nodes = list(network.nodes())
            self.directed = network.is_directed()

        elif 'igraph' in str(type(network)):
            log.debug('The network is of type "igraph".')
            for i in range(len(network.es)):
                self.edges[i] = network.es[i].tuple
            self.nodes = list(range(len(network.vs)))
            self.directed = network.is_directed()

        elif 'pathpy' in str(type(network)):
            log.debug('The network is of type "pathpy".')
            for e in network.edges:
                self.edges[e] = e
            self.nodes = list(network.nodes)
            self.directed = network.directed

        elif isinstance(network,tuple):
            log.debug('The network is of type "list".')
            self.nodes = network[0]
            self.edges = {e:e for e in network[1]}
        else:
            log.error('Type of the network could not be determined.'
                      ' Currently only "cnet", "networkx","igraph", "pathpy"'
                      ' and "node/edge list" is supported!')

        # assign attributes to the class
        self.attributes = kwds
        # draw the network in the memory
        self.draw()

    @staticmethod
    def rename_attributes(**kwds):
        """Rename node and edge attributes.

        In the style dictionary multiple keywords can be used to address
        attributes. These keywords will be converted to an unique key word,
        used in the remaining code. This allows to keep the keywords used in
        'igrap'.

        ======= =================
        keys    other valid keys
        ======= =================
        node    vertex, v, n
        edge    link, l, e
        margins margin
        canvas  bbox, figure_size
        units   unit
        ======= =================

        """
        names = {'node_':['vertex_','v_','n_'],
                 'edge_':['edge_','link_','l_','e_'],
                 'margins':['margin'],
                 'canvas':['bbox','figure_size'],
                 'units':['units','unit']
        }
        _kwds = {}
        del_keys = []
        for key,value in kwds.items():
            for attr,name_list in names.items():
                for name in name_list:
                    if name in key and name[0] == key[0]:
                        _kwds[key.replace(name,attr)] = value
                        del_keys.append(key)
                        break
        # remove the replaced keys from the dict
        for key in del_keys:
            del kwds[key]

        return {**_kwds, **kwds}

    def draw(self):
        """Function to draw a virtual network."""
        # rename the attributes
        kwds = self.rename_attributes(**self.attributes)

        # go through all attributes and assign them to nodes, edges or the
        # general dictionary
        for key,value in kwds.items():
            if 'node_' in key:
                self.node_attributes[key] = self.format_node_value(value)
            elif 'edge_' in key:
                self.edge_attributes[key] = self.format_edge_value(value)
            else:
                self.general_attributes[key] = value

        # check if network is directed and nothing other is defined
        if self.directed and \
           self.edge_attributes.get('edge_directed',None) is None:
            self.edge_attributes['edge_directed'] = self.format_edge_value(True)

        # convert the units
        self.convert_units()

        # create canvas
        _canvas = self.general_attributes.get('canvas',(None,None))
        _margins = self.general_attributes.get('margins',None)
        _node_sizes = self.node_attributes.get('node_size',None)
        self.canvas = Canvas(_canvas[0],_canvas[1],_margins,_node_sizes)

        # configure the layout
        # check if a layout is defined
        if self.attributes.get('layout', None) is not None:
            self.layout = self.format_node_value(self.attributes['layout'])
        else:
            log.warn('No layout was assigned! '
                     'Hence a random layout was chosen!')
            self.layout = {}
            for node in self.nodes:
                self.layout[node] = (np.random.rand(),np.random.rand())

        # fit the node position to the chosen canvas
        k_a_r = self.general_attributes.get('keep_aspect_ratio',True)
        self.layout = self.canvas.fit(self.layout,keep_aspect_ratio=k_a_r)

        # assign layout to the nodes
        self.node_attributes['layout'] = self.layout

        # bend the edges if enabled
        if self.edge_attributes.get('edge_curved',None) is not None:
            self.edge_attributes['edge_curved'] = self.curve()

        # initialize vertices
        self.node_drawer = []
        for node in self.nodes:
            _attr = {}
            for key in self.node_attributes:
                _attr[key] = self.node_attributes[key][node]
            self.node_drawer.append(TikzNodeDrawer(node,**_attr))

        # initialize edges
        self.edge_drawer = []
        for edge,(u,v) in self.edges.items():
            _attr = {}
            for key in self.edge_attributes:
                _attr[key] = self.edge_attributes[key][edge]
            self.edge_drawer.append(TikzEdgeDrawer(edge,u,v,**_attr))


    def convert_units(self):
        """Function to convert the units used."""
        # get unit converter
        _units = self.general_attributes.get('units',('cm','pt'))
        if isinstance(_units,tuple):
            self.unit2cm = UnitConverter(_units[0],'cm')
            self.unit2pt = UnitConverter(_units[1],'pt')
        else:
            self.unit2cm = UnitConverter(_units,'cm')
            self.unit2pt = UnitConverter(_units,'pt')

        # TODO: Fix this ugly code!
        for key in ['node_size','node_label_distance']:
            if  key in self.node_attributes:
                _attr = {}
                for k,v in self.node_attributes[key].items():
                    if isinstance(v,int) or isinstance(v,float):
                        _attr[k] = self.unit2cm(v)
                    else:
                        _attr[k] = v
                self.node_attributes[key] = _attr

        for key in ['node_label_size']:
            if  key in self.node_attributes:
                _attr = {}
                for k,v in self.node_attributes[key].items():
                    if isinstance(v,int) or isinstance(v,float):
                        _attr[k] = round(self.unit2pt(v)/7,self.digits)
                    else:
                        _attr[k] = v
                self.node_attributes[key] = _attr

        for key in ['edge_arrow_size','edge_arrow_width']:
            if  key in self.edge_attributes:
                _attr = {}
                for k,v in self.edge_attributes[key].items():
                    if isinstance(v,int) or isinstance(v,float):
                        _attr[k] = self.unit2cm(v)
                    else:
                        _attr[k] = v
                self.edge_attributes[key] = _attr

        for key in ['edge_width']:
            if  key in self.edge_attributes:
                _attr = {}
                for k,v in self.edge_attributes[key].items():
                    if isinstance(v,int) or isinstance(v,float):
                        _attr[k] = self.unit2pt(v)
                    else:
                        _attr[k] = v
                self.edge_attributes[key] = _attr

        for key in ['edge_loop_size']:
            if  key in self.edge_attributes:
                _attr = {}
                for k,v in self.edge_attributes[key].items():
                    if isinstance(v,int) or isinstance(v,float):
                        _attr[k] = str(self.unit2cm(v))+'cm'
                    else:
                        _attr[k] = v
                self.edge_attributes[key] = _attr

        for key in ['edge_label_size']:
            if  key in self.edge_attributes:
                _attr = {}
                for k,v in self.edge_attributes[key].items():
                    if isinstance(v,int) or isinstance(v,float):
                        _attr[k] = round(self.unit2pt(v)/7,self.digits)
                    else:
                        _attr[k] = v
                self.edge_attributes[key] = _attr

        if 'canvas' in self.general_attributes:
            w,h = self.general_attributes['canvas']
            self.general_attributes['canvas'] = (self.unit2cm(w),self.unit2cm(h))

        if 'margins' in self.general_attributes:
            _margins = self.general_attributes['margins']
            if isinstance(_margins,int) or isinstance(_margins,float):
                value = self.unit2cm(_margins)
            else:
                value = {'top':self.unit2cm(_margins.get('top',0)),
                         'left':self.unit2cm(_margins.get('left',0)),
                         'bottom':self.unit2cm(_margins.get('bottom',0)),
                         'right':self.unit2cm(_margins.get('right',0))}
            self.general_attributes['margins'] = value

    def format_node_value(self,value):
        """Returns a dict with node ids and assigned values."""
        # check if value is string, list or dict
        _values = {}
        if isinstance(value,str) or isinstance(value,int) or \
           isinstance(value,float):
            for n in self.nodes:
                _values[n] = value
        elif isinstance(value,list):
            for i,n in enumerate(self.nodes):
                try:
                    _values[n] = value[i]
                except:
                    _values[n] = None
        elif isinstance(value,dict):
            for n in self.nodes:
                try:
                    _values[n] = value[n]
                except:
                    _values[n] = None
        else:
            log.error('Something went wrong, by formatting the node values!')
            raise CnetError
        return _values

    def format_edge_value(self,value):
        """Returns a dict with edge ids and assigned values."""
        # check if value is string, list or dict
        _values = {}
        if isinstance(value,str) or isinstance(value,int) or \
           isinstance(value,float) or isinstance(value,bool):
            for n in self.edges:
                _values[n] = value
        elif isinstance(value,list):
            for i,n in enumerate(self.edges):
                try:
                    _values[n] = value[i]
                except:
                    _values[n] = None
        elif isinstance(value,dict):
            for n in self.edges:
                try:
                    _values[n] = value[n]
                except:
                    _values[n] = None
        else:
            log.error('Something went wrong, by formatting the edge values!')
            raise CnetError
        return _values

    def curve(self):
        """Calculate the bend factor for curved edges."""
        if 'edge_curved' in self.edge_attributes:
            _curved = {}
            for key,value in self.edge_attributes['edge_curved'].items():
                curved = value

                if curved == 0:
                    _curved[key] = 0
                else:
                    v1 = np.array([0,0])
                    v2 = np.array([1,1])
                    v3 = np.array([(2*v1[0]+v2[0]) / 3.0 - curved * 0.5 * (v2[1]-v1[1]),
                                   (2*v1[1]+v2[1]) / 3.0 + curved * 0.5 * (v2[0]-v1[0])
                    ])
                    vec1 = v2-v1
                    vec2 = v3 -v1
                    angle = np.rad2deg(np.arccos(np.dot(vec1,vec2) / np.sqrt((vec1*vec1).sum()) / np.sqrt((vec2*vec2).sum())))
                    _curved[key] = np.round(np.sign(curved) * angle * -1,self.digits)
        return _curved

class TikzEdgeDrawer(object):
    """Class which handles the drawing of the edges.

    Parameters
    ----------
    id : edge id
        This parameter is the identifier (id) for the edge. Every edge should
        have a unique id.

    u : node id
        This parameter defines the origin of the edge (if directed), i.e. u->v.

    v : node id
        This parameter defines the destination of the edge (if directed)
        i.e. u->v.

    attr : keyword arguments, optional (default = no attributes)
        Attributes to add to edge as key=value pairs.
        See also :py:meth:`plot`

    See Also
    --------
    plot

    """
    def __init__(self,id,u,v,**attr):
        """Initialize the edge drawer.

        Parameters
        ----------
        id : edge id
            This parameter is the identifier (id) for the edge. Every edge
            should have a unique id.

        u : node id
            This parameter defines the origin of the edge (if directed).

        v : node id
            This parameter defines the destination of the edge (if directed).

        attr : keyword arguments, optional (default = no attributes)
            Attributes to add to edge as key=value pairs.
            See also :py:meth:`plot`
        """
        self.id = id
        self.u = u
        self.v = v
        self.attributes = attr
        self.digits = DIGITS
        # all options from the tikz-network library
        self.tikz_kwds =  OrderedDict()
        self.tikz_kwds["edge_width"] = 'lw'
        self.tikz_kwds["edge_color"] = 'color'
        self.tikz_kwds["edge_opacity"] = 'opacity'
        self.tikz_kwds["edge_curved"] = 'bend'
        self.tikz_kwds["edge_label"] = 'label'
        self.tikz_kwds["edge_label_position"] = 'position'
        self.tikz_kwds["edge_label_distance"] = 'distance'
        self.tikz_kwds["edge_label_color"] = 'fontcolor'
        self.tikz_kwds["edge_label_size"] = 'fontscale'
        self.tikz_kwds["edge_style"] = 'style'
        # self.tikz_kwds["edge_arrow_size"] = 'length'
        # self.tikz_kwds["edge_arrow_width"] = 'width'
        # self.tikz_kwds["edge_path"] = 'path'
        self.tikz_kwds["edge_loop_size"] = 'loopsize'
        self.tikz_kwds["edge_loop_position"] = 'loopposition'
        self.tikz_kwds["edge_loop_shape"] = 'loopshape'

        self.tikz_args = OrderedDict()
        self.tikz_args['edge_directed'] = 'Direct'
        self.tikz_args['edge_math_mode'] = 'Math'
        #self.tikz_args['edge_rgb'] = 'RGB'
        self.tikz_args['edge_not_in_bg'] = 'NotInBG'

    def _format_style(self):
        """Format the style attribute for the edge.

        In order to change the arrow shape, the style attribute of the edge has
        to be changed. This option is only available for 'pdf' and 'tex'
        files. 'csv' files do not have this option.

        """
        if 'edge_arrow_size' in self.attributes:
            arrow_size = 'length=' + str(15*self.attributes['edge_arrow_size'])+'cm,'
        else:
            arrow_size = ''

        if 'edge_arrow_size' in self.attributes:
            arrow_width = 'width=' + str(10*self.attributes['edge_arrow_width'])+'cm'
        else:
            arrow_width = ''

        if (arrow_size != '' or arrow_width != '') and\
           self.attributes.get('edge_directed',False) == True:
            self.attributes['edge_style'] = '{{-{{Latex[{}{}]}}, {} }}'.format(arrow_size,arrow_width,self.attributes.get('edge_style',''))

    def draw(self,mode='tex'):
        """Function to draw an virtual edge.

        Parameters
        ----------
        mode : str, optional (default = 'tex')
            The mode defines which kind of result should be returned. Currently
            a string for a tex file or a string for a csv file can be returned.

        Returns
        -------
        string : str
            Returns a string defining the edge. If 'tex' mode is enabled, a
            tikz-network code is returned. If 'csv' mode is enabled, a row
            element for the edge list is returned.

        """
        if mode == 'tex':
            self._format_style()
            string = '\\Edge['

            for k in self.tikz_kwds:
                if k in self.attributes and \
                   self.attributes.get(k,None) is not None:
                    string += ',{}={}'.format(self.tikz_kwds[k],
                                              self.attributes[k])
            for k in self.tikz_args:
                if k in self.attributes:
                    if self.attributes[k] == True:
                        string += ',{}'.format(self.tikz_args[k])

            string += ']({})({})'.format(self.u,self.v)

        elif mode == 'csv':
            string = '{},{}'.format(self.u,self.v)

            for k in self.tikz_kwds:
                if k in self.attributes:
                    string += ',{}'.format(self.attributes[k])

            for k in self.tikz_args:
                if k in self.attributes:
                    if self.attributes[k] == True:
                        string += ',true'
                    else:
                        string += ',false'

        return string + '\n'

    def head(self):
        """Function to draw the header of an virtual edge.

        Returns
        -------
        string : str
            Returns a string with the attributes defined for the edge. This
            string can be used as header for the 'csv' file.

        """
        string = 'u,v'
        for k in self.tikz_kwds:
            if k in self.attributes:
                string += ',{}'.format(self.tikz_kwds[k])
        for k in self.tikz_args:
            if k in self.attributes:
                string += ',{}'.format(self.tikz_args[k])

        return string + '\n'

class TikzNodeDrawer(object):
    """Class which handles the drawing of the nodes

    Parameters
    ----------
    id : node id
        This parameter is the identifier (id) for the node. Every node should
        have a unique id.

    attr : keyword arguments, optional (default = no attributes)
        Attributes to add to node as key=value pairs.
        See also :py:meth:`plot`

    See Also
    --------
    plot

    """
    def __init__(self,id,**attr):
        """Initialize the node drawer.

        Parameters
        ----------
        id : node id
            This parameter is the identifier (id) for the node. Every node
            should have a unique id.

        attr : keyword arguments, optional (default = no attributes)
            Attributes to add to node as key=value pairs.
            See also :py:meth:`plot`

        """
        self.id = id
        self.x = attr.get('layout',(0,0))[0]
        self.y = attr.get('layout',(0,0))[1]
        self.attributes = attr
        self.digits = DIGITS
        # all options from the tikz-network library
        self.tikz_kwds = OrderedDict()
        self.tikz_kwds['node_size'] = 'size'
        self.tikz_kwds['node_color'] = 'color'
        self.tikz_kwds['node_opacity'] = 'opacity'
        self.tikz_kwds['node_label'] = 'label'
        self.tikz_kwds['node_label_position'] = 'position'
        self.tikz_kwds['node_label_distance'] = 'distance'
        self.tikz_kwds['node_label_color'] = 'fontcolor'
        self.tikz_kwds['node_label_size'] = 'fontscale'
        self.tikz_kwds['node_shape'] = 'shape'
        self.tikz_kwds['node_style'] = 'style'
        self.tikz_kwds['node_layer'] = 'layer'

        self.tikz_args = OrderedDict()
        self.tikz_args['node_label_off'] = 'NoLabel'
        self.tikz_args['node_label_as_id'] = 'IdAsLabel'
        self.tikz_args['node_math_mode'] = 'Math'
        #self.tikz_args['node_rgb'] = 'RGB'
        self.tikz_args['node_pseudo'] = 'Pseudo'

    def draw(self,mode='tex'):
        """Function to draw a virtual node.

        Parameters
        ----------
        mode : str, optional (default = 'tex')
            The mode defines which kind of result should be returned. Currently
            a string for a tex file or a string for a csv file can be returned.

        Returns
        -------
        string : str
            Returns a string defining the node. If 'tex' mode is enabled, a
            tikz-network code is returned. If 'csv' mode is enabled, a row
            element for the node list is returned.

        """
        if mode == 'tex':
            string = '\\Vertex[x={x:.{n}f},y={y:.{n}f}'\
                     ''.format(x=self.x,y=self.y,n=self.digits)

            for k in self.tikz_kwds:
                if k in self.attributes and \
                   self.attributes.get(k,None) is not None:
                    string += ',{}={}'.format(self.tikz_kwds[k],
                                              self.attributes[k])
            for k in self.tikz_args:
                if k in self.attributes:
                    if self.attributes[k] == True:
                        string += ',{}'.format(self.tikz_args[k])

            string += ']{{{}}}'.format(self.id)

        elif mode == 'csv':
            string = '{id},{x:.{n}f},{y:.{n}f}'\
                     ''.format(id=self.id,x=self.x,y=self.y,n=self.digits)

            for k in self.tikz_kwds:
                if k in self.attributes:
                    string += ',{}'.format(self.attributes[k])

            for k in self.tikz_args:
                if k in self.attributes:
                    if self.attributes[k] == True:
                        string += ',true'
                    else:
                        string += ',false'

        return string + '\n'

    def head(self):
        """Function to draw the header of a virtual node.

        Returns
        -------
        string : str
            Returns a string with the attributes defined for the node. This
            string can be used as header for the 'csv' file.

        """
        string = 'id,x,y'
        for k in self.tikz_kwds:
            if k in self.attributes:
                string += ',{}'.format(self.tikz_kwds[k])
        for k in self.tikz_args:
            if k in self.attributes:
                string += ',{}'.format(self.tikz_args[k])

        return string + '\n'

# =============================================================================
# eof
#
# Local Variables: 
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:  
