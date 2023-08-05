# -*- coding: utf-8 -*-
from collections import defaultdict
from flask import Response, render_template
from flask_paginate import Pagination
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD
from rdflib.term import Identifier
import json
from pyldapi.renderer import Renderer
from pyldapi.view import View
from pyldapi.exceptions import ViewsFormatsException, RegOfRegTtlError


class RegisterRenderer(Renderer):
    """
    Specific implementation of the abstract Renderer for displaying Register information
    """
    def __init__(self, request, uri, label, comment, register_items,
                 contained_item_classes, register_total_count, *args,
                 views=None, default_view_token=None, super_register=None,
                 page_size_max=1000, register_template=None, **kwargs):
        """
        Init function for class
        :param request: the Flask request triggering this class object creation
        :type request: Flask request
        :param uri: the URI requested
        :type uri: string
        :param label: the label of the Register
        :type label: string
        :param comment: a description of the Register
        :type comment: string
        :param register_items: items within this register
        :type register_items: list of URIs (strings) or tuples like (URI, label) of (string, string) or tuples like (URI, URI, label) if you want to manually specify an item's Class.
        :param contained_item_classes: list of URIs of each distinct class of item contained in this register
        :type contained_item_classes: list (of strings)
        :param register_total_count: total number of items in this Register (not of a page but the register as a whole)
        :type register_total_count: int
        :param views: a list of views available for this Register, apart from 'reg' which is auto-created
        :type views: list (of Views)
        :param default_view_token: the ID of the default view (key of a view in the list of Views)
        :type default_view_token: string (key in views)
        :param super_register: a super-register URI for this register. Can be within this API or external
        :type super_register: string
        :param register_template: the jinja template to use for rendering the HTML view of the register
        :type register_template: string | None
        """
        if views is None:
            self.views = self._add_standard_reg_view()
        if default_view_token is None:
            self.default_view_token = 'reg'
        super().__init__(request, uri, self.views,
                         self.default_view_token, **kwargs)
        self.label = label
        self.comment = comment
        if register_items is not None:
            self.register_items = register_items
        else:
            self.register_items = []
        self.contained_item_classes = contained_item_classes
        self.register_total_count = register_total_count
        self.per_page = request.args.get('per_page', type=int, default=20)
        self.page = request.args.get('page', type=int, default=1)
        self.super_register = super_register
        self.page_size_max = page_size_max
        self.register_template = register_template
        self.paging_error = self._paging()

        try:
            self.format = self._get_requested_format()
        except ViewsFormatsException as e:
            self.vf_error = str(e)

    def _paging(self):
        # calculate last page
        self.last_page = int(round(self.register_total_count / self.per_page, 0)) + 1  # same as math.ceil()

        # if we've gotten the last page value successfully, we can choke if someone enters a larger value
        if self.page > self.last_page:
            return 'You must enter either no value for page or an integer <= {} which is the last page number.'\
                .format(self.last_page)

        if self.per_page > self.page_size_max:
            return 'You must choose a page size >= {}'.format(self.page_size_max)

        # set up Link headers
        links = list()
        # signalling this is an LDP Resource
        links.append('<http://www.w3.org/ns/ldp#Resource>; rel="type"')
        # signalling that this is, in fact, a Resource described in pages
        links.append('<http://www.w3.org/ns/ldp#Page>; rel="type"')

        # always add a link to first
        self.first_page = 1
        links.append('<{}?per_page={}&page={}>; rel="first"'
                     .format(self.uri, self.per_page, self.first_page))

        # if this isn't the first page, add a link to "prev"
        if self.page > 1:
            self.prev_page = self.page - 1
            links.append('<{}?per_page={}&page={}>; rel="prev"'.format(
                self.uri,
                self.per_page,
                self.prev_page
            ))
        else:
            self.prev_page = None

        # if this isn't the last page, add a link to next
        if self.page < self.last_page:
            self.next_page = self.page + 1
            links.append('<{}?per_page={}&page={}>; rel="next"'.format(
                self.uri,
                self.per_page,
                self.next_page
            ))
        else:
            self.next_page = None

        # always add a link to last
        links.append('<{}?per_page={}&page={}>; rel="last"'
                     .format(self.uri, self.per_page, self.last_page))

        self.headers = {
            'Link': ', '.join(links)
        }

        return None

    def render(self):
        if self.view == 'alternates':
            return self._render_alternates_view()
        elif self.view == 'reg':
            if self.paging_error is None:
                self.headers['Profile'] = str(self.views['reg'].namespace)
                return self._render_reg_view()
            else:  # there is a paging error (e.g. page > last_page)
                return Response(self.paging_error, status=400, mimetype='text/plain')

    def _render_reg_view(self):
        # add link headers for all formats of reg view
        if self.format == '_internal':
            return self
        elif self.format == 'text/html':
            return self._render_reg_view_html()
        elif self.format in Renderer.RDF_MIMETYPES:
            return self._render_reg_view_rdf()
        else:
            return self._render_reg_view_json()

    def _render_reg_view_html(self):
        pagination = Pagination(page=self.page, per_page=self.per_page,
                                total=self.register_total_count,
                                page_parameter='page', per_page_parameter='per_page')
        return Response(
            render_template(
                self.register_template or 'register.html',
                uri=self.uri,
                label=self.label,
                comment=self.comment,
                contained_item_classes=self.contained_item_classes,
                register_items=self.register_items,
                page=self.page,
                per_page=self.per_page,
                first_page=self.first_page,
                prev_page=self.prev_page,
                next_page=self.next_page,
                last_page=self.last_page,
                super_register=self.super_register,
                pagination=pagination
            ),
            headers=self.headers
        )

    def _generate_reg_view_rdf(self):
        g = Graph()

        REG = Namespace('http://purl.org/linked-data/registry#')
        g.bind('reg', REG)

        LDP = Namespace('http://www.w3.org/ns/ldp#')
        g.bind('ldp', LDP)

        XHV = Namespace('https://www.w3.org/1999/xhtml/vocab#')
        g.bind('xhv', XHV)

        EREG = Namespace('https://promsns.org/def/eregistry#')
        g.bind('ereg', EREG)

        register_uri = URIRef(self.uri)
        g.add((register_uri, RDF.type, REG.Register))
        g.add((register_uri, RDFS.label, Literal(self.label, datatype=XSD.string)))
        g.add((register_uri, RDFS.comment, Literal(self.comment, datatype=XSD.string)))
        for cic in self.contained_item_classes:
            g.add((register_uri, REG.containedItemClass, URIRef(cic)))
        if self.super_register is not None:
            g.add((register_uri, EREG.superregister, URIRef(self.super_register)))

        page_uri_str = self.uri + '?per_page=' + str(self.per_page) + '&page=' + str(self.page)
        page_uri_str_nonum = self.uri + '?per_page=' + str(self.per_page) + '&page='
        page_uri = URIRef(page_uri_str)

        # pagination
        # this page
        g.add((page_uri, RDF.type, LDP.Page))
        g.add((page_uri, LDP.pageOf, register_uri))

        # links to other pages
        g.add((page_uri, XHV.first, URIRef(page_uri_str_nonum + '1')))
        g.add((page_uri, XHV.last, URIRef(page_uri_str_nonum + str(self.last_page))))

        if self.page != 1:
            g.add((page_uri, XHV.prev, URIRef(page_uri_str_nonum + str(self.page - 1))))

        if self.page != self.last_page:
            g.add((page_uri, XHV.next, URIRef(page_uri_str_nonum + str(self.page + 1))))

        if len(self.contained_item_classes) == 1:
            contained_item_class = URIRef(self.contained_item_classes[0])
        else:
            contained_item_class = None

        # add all the items
        for item in self.register_items:
            if isinstance(item, tuple):  # if it's a tuple, add in the type
                if len(item) < 2:
                    raise ValueError("Not enough items in register_item tuple.")
                item_uri = URIRef(item[0])
                if item[1] and isinstance(item[1], (str, bytes, Literal)):
                    g.add((item_uri, RDFS.label,
                           Literal(item[1], datatype=XSD.string)))
                    if len(item) > 2 and isinstance(item[2], Identifier):
                        g.add((item_uri, RDF.type, item[2]))
                    elif contained_item_class:
                        g.add((item_uri, RDF.type, contained_item_class))
                elif item[1] and isinstance(item[1], Identifier):
                    g.add((item_uri, RDF.type, item[1]))
                    if len(item) > 2:
                        g.add((item_uri, RDFS.label,
                               Literal(item[2], datatype=XSD.string)))
                g.add((item_uri, REG.register, register_uri))
            else:  # just URIs
                item_uri = URIRef(item)
                if contained_item_class:
                    g.add((item_uri, RDF.type, contained_item_class))
                g.add((item_uri, REG.register, register_uri))

        return g

    def _render_reg_view_rdf(self):
        g = self._generate_reg_view_rdf()
        return self._make_rdf_response(g)

    def _render_reg_view_json(self):
        return Response(
            json.dumps({
                'uri': self.uri,
                'label': self.label,
                'comment': self.comment,
                'views': list(self.views.keys()),
                'default_view': self.default_view_token,
                'contained_item_classes': self.contained_item_classes,
                'register_items': self.register_items
            }),
            mimetype='application/json',
            headers=self.headers
        )

    def _add_standard_reg_view(self):
        return {
            'reg': View(
                'Registry Ontology',
                'A simple list-of-items view taken from the Registry Ontology',
                ['text/html', 'application/json', '_internal'] + self.RDF_MIMETYPES,
                'text/html',
                languages=['en'],  # default 'en' only for now
                namespace='http://purl.org/linked-data/registry'
            )
        }


class RegisterOfRegistersRenderer(RegisterRenderer):
    """
    Specialised implementation of the RegisterRenderer for displaying Register of Register information

    This subclass just auto-fills many of the RegisterRenderer options
    """
    def __init__(self, request, uri, label, comment, rofr_file_path, *args,
                 super_register=None, **kwargs):
        """
        Init function for class
        :param request: the Flask request triggering this class object creation
        :type request: Flask request
        :param uri: the URI requested
        :type uri: string
        :param label: the label of the Register
        :type label: string
        :param comment: a description of the Register
        :type comment: string
        :param rofr_file_path: the path to the Register of Register RDF file (used in API setup)
        :type rofr_file_path: path (string)
        :param super_register: a super-register URI for this register. Can be within this API or external
        :type super_register: string
        """
        super(RegisterOfRegistersRenderer, self).__init__(request, uri, label,
              comment, None, ['http://purl.org/linked-data/registry#Register'],
              0, super_register=super_register, **kwargs)
        self.subregister_cics = defaultdict(lambda: set())

        # find subregisters from rofr.ttl
        try:
            with open(rofr_file_path, 'rb') as file:
                g = Graph().parse(file=file, format='turtle')
            assert g, "Could not parse the RofR TTL file."
        except FileNotFoundError:
            raise RegOfRegTtlError()
        except AssertionError:
            raise RegOfRegTtlError()
        q = '''
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX reg: <http://purl.org/linked-data/registry#>
            SELECT ?uri ?label ?rofr ?cic
            WHERE {
                ?uri a reg:Register ;
                rdfs:label ?label ;
                reg:containedItemClass ?cic .
                ?rofr reg:subregister ?uri .
            }
            '''
        found_subregisters = set()
        for r in g.query(q):
            target_rofr = r['rofr']
            # TODO filter so we only add subregisters which
            # match this rofr to target_rofr
            subregister_uri = r['uri']
            subregister_cic = r['cic']
            if subregister_cic:
                self.subregister_cics[subregister_uri].add(subregister_cic)
            if subregister_uri in found_subregisters:
                # don't add subregister to register_items more than once
                continue
            self.register_items.append((subregister_uri, r['label']))
            found_subregisters.add(subregister_uri)

    def _generate_reg_view_rdf(self):
        g = super(RegisterOfRegistersRenderer, self)._generate_reg_view_rdf()
        REG = Namespace('http://purl.org/linked-data/registry#')
        for uri_str, cics in self.subregister_cics.items():
            uri = URIRef(uri_str)
            for cic in cics:
                g.add((uri, REG.containedItemClass, cic))
        return g
