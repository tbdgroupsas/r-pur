# -*- coding: utf-8 -*-
{
    'name': "sbo_pivot_po_duedate",

    'summary': """
        sbo_pivot_po_duedate aim is to add a pivot clickable view
        accessible from purchase module
        this pivot view show all the billable purchase order, group by category and due_date""",

    'description': """
        SBO Solutions dev for r-pur
        pivot view show all the billable purchase order, group by category and due_date
        
        for the purpose of this developpement we add store field in account_move_line 
        not the best way but necessary for Odoo pivot view.
    """,

    'author': "SBO Solutions",
    'website': "https://www.sbosolutions.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'account'],

    # always loaded
    'data': [
        'views/account_move_line.xml',
    ],
}
