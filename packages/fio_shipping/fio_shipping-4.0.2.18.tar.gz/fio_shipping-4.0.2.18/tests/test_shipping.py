# -*- coding: utf-8 -*-
"""
    tests/test_shipping.py

"""
import unittest
from datetime import date
from decimal import Decimal

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER, with_transaction
from trytond.transaction import Transaction
from trytond.exceptions import UserError


class TestShipping(unittest.TestCase):
    '''
    Test views and depends
    '''

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        trytond.tests.test_tryton.install_module('shipping')
        trytond.tests.test_tryton.install_module('product_measurements')

        self.Party = POOL.get('party.party')
        self.PartyContact = POOL.get('party.contact_mechanism')
        self.Address = POOL.get('party.address')
        self.Category = POOL.get('product.category')
        self.Party = POOL.get('party.party')
        self.Payment_term = POOL.get('account.invoice.payment_term')
        self.Country = POOL.get('country.country')
        self.CountrySubdivision = POOL.get('country.subdivision')
        self.Sale = POOL.get('sale.sale')
        self.SaleConfiguration = POOL.get('sale.configuration')
        self.Currency = POOL.get('currency.currency')
        self.Company = POOL.get('company.company')
        self.Template = POOL.get('product.template')
        self.SaleLine = POOL.get('sale.line')
        self.Uom = POOL.get('product.uom')
        self.User = POOL.get('res.user')
        self.Account = POOL.get('account.account')
        self.Product = POOL.get('product.product')
        self.Carrier = POOL.get('carrier')
        self.PartyConf = POOL.get('party.configuration')
        self.LabelWizard = POOL.get('shipping.label', type='wizard')
        self.Attachment = POOL.get('ir.attachment')
        self.Shipment = POOL.get('stock.shipment.out')
        self.StockLocation = POOL.get('stock.location')
        self.Package = POOL.get('stock.package')
        self.PackageType = POOL.get('stock.package.type')
        self.Tracking = POOL.get('shipment.tracking')
        self.BoxType = POOL.get('carrier.box_type')

    def setup_defaults(self):
        """
        Setup defaults
        """
        # Create currency
        currency, = self.Currency.create([{
            'name': 'United Stated Dollar',
            'code': 'USD',
            'symbol': 'USD',
        }])

        company_party, carrier_party = self.Party.create([{
            'name': 'Test Party',
        }, {
            'name': 'Carrier Party',
        }])

        self.company, = self.Company.create([{
            'party': company_party.id,
            'currency': currency.id,
        }])
        self.PartyContact.create([{
            'type': 'phone',
            'value': '8005551212',
            'party': self.company.party.id
        }])
        country_us, = self.Country.create([{
            'name': 'United States',
            'code': 'US',
        }])

        subdivision_florida, = self.CountrySubdivision.create([{
            'name': 'Florida',
            'code': 'US-FL',
            'country': country_us.id,
            'type': 'state'
        }])

        self.User.write(
            [self.User(USER)], {
                'main_company': self.company.id,
                'company': self.company.id,
            }
        )

        self._create_coa_minimal(company=self.company)
        self.payment_term, = self._create_payment_term()

        self.uom_kg, = self.Uom.search([('symbol', '=', 'kg')])
        self.uom_pound, = self.Uom.search([('symbol', '=', 'lb')])
        self.uom_inch, = self.Uom.search([('symbol', '=', 'in')])

        self.sale_party, = self.Party.create([{
            'name': 'Test Sale Party',
            'addresses': [('create', [{
                'name': 'John Doe',
                'street': '250 NE 25th St',
                'zip': '33137',
                'city': 'Miami, Miami-Dade',
                'country': country_us.id,
                'subdivision': subdivision_florida.id,
            }])],
        }])
        self.PartyContact.create([{
            'type': 'phone',
            'value': '8005763279',
            'party': self.sale_party.id
        }])

        carrier_product = self.create_product(is_service=True)

        self.custom_box_type, = self.BoxType.create([{
            'name': "Custom Box Type",
            "code": "CODE_BOX",
            "length": 1,
            "width": 2,
            "height": 3,
            "distance_unit": self.uom_inch.id,
        }])
        self.carrier, = self.Carrier.create([{
            'party': carrier_party,
            'carrier_product': carrier_product,
            'currency': currency,
            'box_types': [('add', [self.custom_box_type.id])]
        }])

        warehouse_address, = self.Address.create([{
            'party': self.company.party.id,
            'name': 'Amine Khechfe',
            'street': '247 High Street',
            'zip': '32003',
            'city': 'Palo Alto',
            'country': country_us.id,
            'subdivision': subdivision_florida.id,
        }])

        warehouse = self.StockLocation.search([('type', '=', 'warehouse')])[0]
        warehouse.address = warehouse_address
        warehouse.save()

    def create_product(self, weight=None, weight_uom=None, is_service=False):
        """
        Create product
        """
        # Create product category
        category, = self.Category.create([{
            'name': 'Test Category',
        }])

        account_revenue, = self.Account.search([
            ('kind', '=', 'revenue')
        ])

        # Create product
        template, = self.Template.create([{
            'name': 'Test Product',
            'categories': [('add', [category.id])],
            'type': is_service and 'service' or 'goods',
            'sale_uom': self.uom_kg,
            'list_price': Decimal('10'),
            'cost_price': Decimal('5'),
            'default_uom': self.uom_kg,
            'salable': True,
            'account_revenue': account_revenue.id,
            'weight': weight,
            'weight_uom': weight_uom,
            'products': [
                ('create', [{
                    'code': 'Test Product',
                }])
            ]
        }])

        return template.products[0]

    def _create_coa_minimal(self, company):
        """Create a minimal chart of accounts
        """
        AccountTemplate = POOL.get('account.account.template')
        Account = POOL.get('account.account')

        account_create_chart = POOL.get(
            'account.create_chart', type="wizard"
        )

        account_template, = AccountTemplate.search([
            ('parent', '=', None),
            ('name', '=', 'Minimal Account Chart'),
        ])

        session_id, _, _ = account_create_chart.create()
        create_chart = account_create_chart(session_id)
        create_chart.account.account_template = account_template
        create_chart.account.company = company
        create_chart.transition_create_account()

        receivable, = Account.search([
            ('kind', '=', 'receivable'),
            ('company', '=', company),
        ])
        payable, = Account.search([
            ('kind', '=', 'payable'),
            ('company', '=', company),
        ])
        create_chart.properties.company = company
        create_chart.properties.account_receivable = receivable
        create_chart.properties.account_payable = payable
        create_chart.transition_create_properties()

    def _get_account_by_kind(self, kind, company=None, silent=True):
        """Returns an account with given spec

        :param kind: receivable/payable/expense/revenue
        :param silent: dont raise error if account is not found
        """
        Account = POOL.get('account.account')
        Company = POOL.get('company.company')

        if company is None:
            company, = Company.search([], limit=1)

        accounts = Account.search([
            ('kind', '=', kind),
            ('company', '=', company)
        ], limit=1)
        if not accounts and not silent:
            raise Exception("Account not found")
        return accounts[0] if accounts else None

    def _create_payment_term(self):
        """Create a simple payment term with all advance
        """
        PaymentTerm = POOL.get('account.invoice.payment_term')

        return PaymentTerm.create([{
            'name': 'Direct',
            'lines': [('create', [{'type': 'remainder'}])]
        }])

    @with_transaction()
    def test_0005_sale_line_weight(self):
        '''
        Check weight for product in sale line and total package weight
        for sale
        '''
        self.setup_defaults()

        # Create sale order
        with Transaction().set_context(company=self.company.id):
            sale, = self.Sale.create([{
                'reference': 'S-1001',
                'payment_term': self.payment_term.id,
                'party': self.sale_party.id,
                'invoice_address': self.sale_party.addresses[0].id,
                'shipment_address': self.sale_party.addresses[0].id,
            }])

        # Sale line without product
        sale_line1, = self.SaleLine.create([{
            'sale': sale.id,
            'type': 'line',
            'quantity': 1,
            'unit_price': Decimal('10.00'),
            'description': 'Test Description1',
            'unit': self.uom_kg,
        }])
        weight = sale_line1.get_weight(self.uom_kg)

        self.assertEqual(weight, 0)

        # Sale line with product but quantity as 0
        product = self.create_product(0.5, self.uom_kg)
        sale_line2, = self.SaleLine.create([{
            'sale': sale.id,
            'type': 'line',
            'quantity': 0,
            'product': product.id,
            'unit_price': Decimal('10.00'),
            'description': 'Test Description1',
            'unit': product.template.default_uom,
        }])
        weight = sale_line2.get_weight(self.uom_kg)

        self.assertEqual(weight, 0)

        # Sale line with service product and quantity > 0
        service_product = self.create_product(
            0.5, self.uom_kg, is_service=True
        )
        sale_line3, = self.SaleLine.create([{
            'sale': sale.id,
            'type': 'line',
            'quantity': 1,
            'product': service_product.id,
            'unit_price': Decimal('10.00'),
            'description': 'Test Description1',
            'unit': service_product.template.default_uom,
        }])

        weight = sale_line3.get_weight(self.uom_kg)

        self.assertEqual(weight, 0)

        # Sale line with product having no weight
        product = self.create_product()
        sale_line4, = self.SaleLine.create([{
            'sale': sale.id,
            'type': 'line',
            'quantity': 1,
            'product': product.id,
            'unit_price': Decimal('10.00'),
            'description': 'Test Description1',
            'unit': product.template.default_uom,
        }])

        with self.assertRaises(Exception):
            sale_line4.get_weight(self.uom_pound)

        # Sale line with uom different from product uom
        product = self.create_product(0.5, self.uom_kg)
        sale_line5, = self.SaleLine.create([{
            'sale': sale.id,
            'type': 'line',
            'quantity': 1,
            'product': product.id,
            'unit_price': Decimal('10.00'),
            'description': 'Test Description1',
            'unit': self.uom_pound,
        }])

        weight = sale_line5.get_weight(self.uom_pound)

        self.assertEqual(weight, 0.5)

        # Sale line with uom same as product uom
        product = self.create_product(3, self.uom_kg)
        sale_line6, = self.SaleLine.create([{
            'sale': sale.id,
            'type': 'line',
            'quantity': 1,
            'product': product,
            'unit_price': Decimal('10.00'),
            'description': 'Test Description1',
            'unit': product.template.default_uom,
        }])

        weight = sale_line6.get_weight(self.uom_kg)

        self.assertEqual(weight, 3)

        self.assertEqual(sale.weight_uom.name, 'Pound')

        # 0.5 kg + 3.0 kg = 3.5 kg = 7.11 pounds (approx.)
        self.assertAlmostEqual(
            sale.weight, 7.11, delta=0.001
        )

    @with_transaction()
    def test_0010_stock_move_weight(self):
        '''
        Check weight for shipment package
        '''
        self.setup_defaults()

        # Create sale order
        with Transaction().set_context(company=self.company.id):
            sale, = self.Sale.create([{
                'reference': 'S-1001',
                'payment_term': self.payment_term.id,
                'party': self.sale_party.id,
                'invoice_address': self.sale_party.addresses[0].id,
                'shipment_address': self.sale_party.addresses[0].id,
            }])

            # Sale line with service product and quantity > 0
            service_product = self.create_product(
                0.5, self.uom_kg, is_service=True
            )
            sale_line3, = self.SaleLine.create([{
                'sale': sale.id,
                'type': 'line',
                'quantity': 1,
                'product': service_product.id,
                'unit_price': Decimal('10.00'),
                'description': 'Test Description1',
                'unit': service_product.template.default_uom,
            }])

            weight = sale_line3.get_weight(self.uom_kg)

            self.assertEqual(weight, 0)

            # Sale line with uom different from product uom
            product = self.create_product(0.5, self.uom_kg)
            sale_line5, = self.SaleLine.create([{
                'sale': sale.id,
                'type': 'line',
                'quantity': 1,
                'product': product.id,
                'unit_price': Decimal('10.00'),
                'description': 'Test Description1',
                'unit': self.uom_pound,
            }])

            weight = sale_line5.get_weight(self.uom_pound)

            self.assertEqual(weight, 0.5)

            # Sale line with uom same as product uom
            product = self.create_product(3, self.uom_kg)
            sale_line6, = self.SaleLine.create([{
                'sale': sale.id,
                'type': 'line',
                'quantity': 1,
                'product': product,
                'unit_price': Decimal('10.00'),
                'description': 'Test Description1',
                'unit': product.template.default_uom,
            }])

            weight = sale_line6.get_weight(self.uom_kg)

            self.assertEqual(weight, 3)

            self.assertEqual(sale.weight_uom.name, 'Pound')

            # Sale package weight

            # 0.5 kg + 3.0 kg = 3.5 kg = 7.11 pounds (approx.)
            self.assertAlmostEqual(
                sale.weight, 7.11, delta=0.001
            )

            self.Sale.quote([sale])

            self.Sale.confirm([sale])

            self.Sale.process([sale])

            self.assertEqual(len(sale.shipments), 1)

            shipment, = sale.shipments

            self.assertTrue(shipment.outgoing_moves)

            # Assign and pack the shipment
            self.Shipment.assign(sale.shipments)
            self.Shipment.pack(sale.shipments)

            # Create a package for shipment products
            package_type, = self.PackageType.create([{
                'name': 'Box',
            }])
            package, = self.Package.create([{
                'code': 'ABC',
                'type': package_type.id,
                'shipment': (shipment.__name__, shipment.id),
                'moves': [('add', map(int, shipment.outgoing_moves))],
            }])

            self.assertEqual(package.weight_uom.name, 'Pound')

            # Shipment package weight
            # 0.5 kg + 3.0 kg = 7.7 pounds = 8 pounds (after round off)
            self.assertAlmostEqual(
                package.computed_weight, 7.11, delta=0.001
            )

            self.assertFalse(package.override_weight)

            # Since weight is not overridden, package weight will be
            # computed weight
            self.assertAlmostEqual(
                package.weight, 7.11, delta=0.001
            )

            package.override_weight = 20
            package.override_weight_uom = self.uom_pound.id
            package.save()

            # Since overridden weight is there, package weight will be
            # overridden weight
            self.assertEqual(package.weight, 20)

    @with_transaction()
    def test_0020_wizard_create(self):
        """
        Test creation of label generation wizard.
        """
        self.setup_defaults()

        session_id, start_state, end_state = self.LabelWizard.create()
        self.assertEqual(start_state, 'start')
        self.assertEqual(end_state, 'end')
        self.assert_(session_id)

    @with_transaction()
    def test_0025_wizard_delete(self):
        """
        Tests deletion of label generation wizard.
        """
        self.setup_defaults()

        session_id, start_state, end_state = self.LabelWizard.create()
        self.LabelWizard.delete(session_id)

    @with_transaction()
    def test_0030_wizard_execute(self):
        """
        Tests execution of label generation wizard.
        """
        self.setup_defaults()

        with Transaction().set_context(company=self.company.id):
            sale, = self.Sale.create([{
                'reference': 'S-1001',
                'payment_term': self.payment_term.id,
                'party': self.sale_party.id,
                'invoice_address': self.sale_party.addresses[0].id,
                'shipment_address': self.sale_party.addresses[0].id,
                'carrier': self.carrier,
            }])
            self.assertFalse(sale.is_international_shipping)

            # Sale line with uom same as product uom
            product = self.create_product(3, self.uom_kg)
            sale_line6, = self.SaleLine.create([{
                'sale': sale.id,
                'type': 'line',
                'quantity': 1,
                'product': product,
                'unit_price': Decimal('10.00'),
                'description': 'Test Description1',
                'unit': product.template.default_uom,
            }])

            self.Sale.quote([sale])
            self.Sale.confirm([sale])
            self.Sale.process([sale])

            self.assertEqual(len(sale.shipments), 1)

            self.Shipment.assign(sale.shipments)

            self.assertFalse(sale.shipments[0].is_international_shipping)

            shipment, = sale.shipments

        self.Shipment.pack(sale.shipments)
        # Create a package for shipment products
        shipment, = sale.shipments

        with Transaction().set_context(
                active_id=sale.shipments[0], company=self.company.id,
                active_model="stock.shipment.out"
        ):
            session_id, start_state, end_state = self.LabelWizard.create()

            result = self.LabelWizard.execute(session_id, {}, start_state)

            self.assertEqual(result.keys(), ['view'])
            self.assertEqual(len(self.Attachment.search([])), 0)

            data = {
                start_state: {
                    'carrier': self.carrier,
                    'override_weight': 9,
                    'carrier_service': shipment.carrier_service,
                    'cost_currency': shipment.cost_currency,
                    'box_type': self.custom_box_type,
                },
            }

            self.LabelWizard.execute(
                session_id, data, 'next'
            )
            # Test if a package was created for shipment
            self.assertTrue(shipment.packages)
            self.assertEqual(len(shipment.packages), 1)
            self.assertEqual(
                shipment.packages[0].moves, shipment.outgoing_moves)

    @with_transaction()
    def test_0035_wizard_button(self):
        """
        Test that the label wizard button works properly.
        """
        self.setup_defaults()

        # Pass empty list.
        # no_shipments error.
        with self.assertRaises(UserError):
            self.Shipment.label_wizard([])

        with Transaction().set_context({'company': self.company.id}):
            shipment1, = self.Shipment.create([{
                'planned_date': date.today(),
                'effective_date': date.today(),
                'customer': self.sale_party.id,
                'warehouse': self.StockLocation.search([
                    ('type', '=', 'warehouse')
                ])[0],
                'delivery_address': self.sale_party.addresses[0],
            }])
            shipment2, = self.Shipment.create([{
                'planned_date': date.today(),
                'effective_date': date.today(),
                'customer': self.sale_party.id,
                'warehouse': self.StockLocation.search([
                    ('type', '=', 'warehouse')
                ])[0],
                'delivery_address': self.sale_party.addresses[0],
            }])

        # Too many shipments.
        with self.assertRaises(UserError):
            self.Shipment.label_wizard([shipment1, shipment2])

        # One shipment works.
        self.Shipment.label_wizard([shipment1])

    @with_transaction()
    def test_0040_add_shipping_line(self):
        """
        Tests the add_shipping_line() method.
        """
        self.setup_defaults()

        # Create sale order
        with Transaction().set_context(company=self.company.id):
            sale, = self.Sale.create([{
                'reference': 'S-1001',
                'payment_term': self.payment_term.id,
                'party': self.sale_party.id,
                'invoice_address': self.sale_party.addresses[0].id,
                'shipment_address': self.sale_party.addresses[0].id,
                'carrier': self.carrier,
            }])
            product = self.create_product(3, self.uom_kg)
            sale_line, = self.SaleLine.create([{
                'sale': sale.id,
                'type': 'line',
                'quantity': 1,
                'product': product,
                'unit_price': Decimal('10.00'),
                'description': 'Test Description1',
                'unit': product.template.default_uom,
            }])

        # add a shipping line for 1
        sale.add_shipping_line(Decimal('1'), 'Rate 1')
        self.assertEqual(len(sale.lines), 2)
        self.assertEqual(sale.total_amount, Decimal('11'))

        # Appy again and the line should still be the same
        sale.add_shipping_line(Decimal('2'), 'Rate 2')
        self.assertEqual(len(sale.lines), 2)
        self.assertEqual(sale.total_amount, Decimal('12'))

        # Apply shipping in quote state
        self.Sale.quote([sale])
        self.assertEqual(len(sale.lines), 2)
        self.assertEqual(sale.total_amount, Decimal('20'))
        sale.add_shipping_line(Decimal('3'), 'Rate 3')
        self.assertEqual(len(sale.lines), 2)
        self.assertEqual(sale.total_amount, Decimal('13'))

        # Apply shipping in confirmed state
        self.Sale.confirm([sale])
        self.assertEqual(len(sale.lines), 2)
        self.assertEqual(sale.total_amount, Decimal('13'))
        sale.add_shipping_line(Decimal('4'), 'Rate 4')
        self.assertEqual(len(sale.lines), 2)
        self.assertEqual(sale.total_amount, Decimal('14'))

    @with_transaction()
    def test_0045_check_shipment_tracking_number_copy(self):
        """
        Test that tracking number is not copied while copying shipment
        """
        self.setup_defaults()

        with Transaction().set_context({'company': self.company.id}):
            package1, = self.Package.create([{
                'code': 'Package 1'
            }])
            # Master tracking number
            tracking_number1, = self.Tracking.create([{
                'carrier': self.carrier,
                'tracking_number': 'AA1234',
                'tracking_url': 'url',
                'origin': '%s,%d' % (package1.__name__, package1.id)
            }])
            shipment1, = self.Shipment.create([{
                'planned_date': date.today(),
                'effective_date': date.today(),
                'customer': self.sale_party.id,
                'warehouse': self.StockLocation.search([
                    ('type', '=', 'warehouse')
                ])[0],
                'delivery_address': self.sale_party.addresses[0],
                'tracking_number': self.Tracking.search([])[0].id
            }])

            shipment2, = self.Shipment.copy([shipment1])

            self.assertFalse(shipment2.tracking_number)

    @with_transaction()
    def test_0050_check_package_weight_redistribution(self):
        """
        Tests package weight redistribution in wizard.
        """
        self.setup_defaults()

        with Transaction().set_context(company=self.company.id):
            sale, = self.Sale.create([{
                'reference': 'S-1001',
                'payment_term': self.payment_term.id,
                'party': self.sale_party.id,
                'invoice_address': self.sale_party.addresses[0].id,
                'shipment_address': self.sale_party.addresses[0].id,
                'carrier': self.carrier,
            }])

            product_1 = self.create_product(3, self.uom_kg)
            product_2 = self.create_product(7, self.uom_kg)

            sale_line1, = self.SaleLine.create([{
                'sale': sale.id,
                'type': 'line',
                'quantity': 1,
                'product': product_2,
                'unit_price': Decimal('10.00'),
                'description': 'Test Description1',
                'unit': product_1.template.default_uom,
            }])
            sale_line2, = self.SaleLine.create([{
                'sale': sale.id,
                'type': 'line',
                'quantity': 1,
                'product': product_1,
                'unit_price': Decimal('10.00'),
                'description': 'Test Description1',
                'unit': product_2.template.default_uom,
            }])

            self.assertEqual(sale.weight, 22.04)
            self.assertEqual(sale.weight_uom.name, 'Pound')

            self.Sale.quote([sale])
            self.Sale.confirm([sale])
            self.Sale.process([sale])

            self.assertEqual(len(sale.shipments), 1)

            self.Shipment.assign(sale.shipments)

            self.assertFalse(sale.shipments[0].is_international_shipping)

        self.Shipment.pack(sale.shipments)
        shipment, = sale.shipments

        # Use the default package as first one and create new to get
        # second package
        package_type, = self.PackageType.search(
            [('name', '=', 'Shipment Package')])
        package1 = shipment.packages[0]
        package1.type = package_type.id
        package1.outgoing_moves = shipment.outgoing_moves[0]
        package1.override_weight = 3
        package1.override_weight_uom = self.uom_pound.id
        package1.save()

        package2, = self.Package.create([{
            'shipment': '%s,%d' % (shipment.__name__, shipment.id),
            'type': package_type.id,
            'moves': [('add', [shipment.outgoing_moves[1]])],
            'override_weight': 4,
            'override_weight_uom': self.uom_pound.id
        }])

        # Check weight of packages before execution
        # of wizard.
        self.assertEqual(package1.override_weight, 3.0)
        self.assertEqual(package1.weight_uom, self.uom_pound)
        self.assertEqual(package2.override_weight, 4.0)
        self.assertEqual(package2.weight_uom, self.uom_pound)

        # Also check total weight of shipment which must be sum
        # of weight of both packages. 3 + 4 = 7 pound
        self.assertEqual(shipment.weight, 7)
        self.assertEqual(shipment.weight_uom, self.uom_pound)

        # CASE 1: default override_weight = override_weight of wizard
        with Transaction().set_context(
                active_id=sale.shipments[0], company=self.company.id,
                active_model='stock.shipment.out',
        ):
            session_id, start_state, end_state = self.LabelWizard.create()

            data = {
                start_state: {
                    'carrier': self.carrier,
                    'override_weight': 7.0,
                    'carrier_service': None,
                    'box_type': None,
                },
            }

            self.LabelWizard.execute(
                session_id, data, 'next'
            )
            # Test if a package was created for shipment
            self.assertTrue(shipment.packages)
            self.assertEqual(len(shipment.packages), 2)

            # As total override weight is same as override weight of
            # wizard, both package weight should be same as before
            self.assertEqual(package1.override_weight, 3)
            self.assertEqual(package2.override_weight, 4)

        # CASE 2: default override_weight != override_weight of wizard
        with Transaction().set_context(
                active_id=sale.shipments[0], company=self.company.id,
                active_model="stock.shipment.out"
        ):
            session_id, start_state, end_state = self.LabelWizard.create()

            data = {
                start_state: {
                    'carrier': self.carrier,
                    'override_weight': 8.0,
                    'carrier_service': None,
                    'box_type': None,
                },
            }

            self.LabelWizard.execute(
                session_id, data, 'next'
            )
            # Test if a package was created for shipment
            self.assertTrue(shipment.packages)
            self.assertEqual(len(shipment.packages), 2)

            # As override weight is different from wizard's
            # override weight, it will be redistributed
            # equally
            self.assertEqual(package1.override_weight, 4.0)
            self.assertEqual(package2.override_weight, 4.0)

        # CASE 3: override_weight in wizard is None
        with Transaction().set_context(
                active_id=sale.shipments[0], company=self.company.id,
                active_model="stock.shipment.out"
        ):
            session_id, start_state, end_state = self.LabelWizard.create()

            data = {
                start_state: {
                    'carrier': self.carrier,
                    'override_weight': None,
                    'carrier_service': None,
                    'box_type': None,
                },
            }

            # As override weight in wizard is None, it shouldn't continue
            self.LabelWizard.execute(
                session_id, data, 'next'
            )

    @with_transaction()
    def test_0055_shipment_tracking_number(self):
        """
        Check tracking number for shipment and packages
        """
        self.setup_defaults()
        with Transaction().set_context({'company': self.company.id}):
            package1, = self.Package.create([{
                'code': 'Package 1'
            }])

            package2, = self.Package.create([{
                'code': 'Package 2'
            }])

            # Master tracking number
            tracking_number1, = self.Tracking.create([{
                'carrier': self.carrier,
                'tracking_number': 'AA1234',
                'tracking_url': 'url',
                'origin': '%s,%d' % (package1.__name__, package1.id)
            }])

            # Non master tracking number
            tracking_number2, = self.Tracking.create([{
                'carrier': self.carrier,
                'tracking_number': 'AA1234',
                'tracking_url': 'url',
                'origin': '%s,%d' % (package2.__name__, package2.id)
            }])

            shipment, = self.Shipment.create([{
                'planned_date': date.today(),
                'effective_date': date.today(),
                'customer': self.sale_party.id,
                'warehouse': self.StockLocation.search([
                    ('type', '=', 'warehouse')
                ])[0],
                'delivery_address': self.sale_party.addresses[0],
                'tracking_number': self.Tracking.search([])[0].id,
            }])

            for package in [package1, package2]:
                package.shipment = \
                    '%s,%d' % (shipment.__name__, shipment.id)
                package.save()

            self.assertEqual(
                package1.tracking_number, tracking_number1
            )

            self.assertEqual(
                package2.tracking_number, tracking_number2
            )

            self.assertEqual(
                self.Package.search([('tracking_number', '=', 'AA1234')]),
                [package1, package2]
            )
            self.assertEqual(
                self.Shipment.search([('tracking_number', '=', 'AA1234')]),
                [shipment]
            )


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestShipping)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
