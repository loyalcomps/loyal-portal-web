# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.helpdesk.controllers.portal import CustomerPortal
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


class CustomerPortal(CustomerPortal):

    @http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    def my_helpdesk_tickets(self, page=1, date_begin=None, date_end=None, sortby=None, search=None, search_in='content',
                            groupby='none', **kw):
        res = super(CustomerPortal, self).my_helpdesk_tickets(page=page, date_begin=date_begin, date_end=date_end,
                                                              sortby=sortby, search=search, search_in=search_in,
                                                              groupby=groupby, **kw)

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'stage': {'input': 'stage', 'label': _('Stage')},
        }
        res.qcontext['searchbar_groupby']=searchbar_groupby
        if groupby == 'stage':
            grouped_tickets = [request.env['helpdesk.ticket'].concat(*g) for k, g in
                             groupbyelem(res.qcontext['tickets'], itemgetter('stage_id'))]
        else:
            grouped_tickets = [res.qcontext['tickets']]
        res.qcontext['grouped_tickets'] = grouped_tickets
        res.qcontext['groupby'] = groupby
        return res
