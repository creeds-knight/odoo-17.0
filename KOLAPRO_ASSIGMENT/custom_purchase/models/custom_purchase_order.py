from odoo import models, fields
from odoo.exceptions import UserError

class CustomPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_ids = fields.Many2many('res.partner', string='Vendors',
                                   domain=[('supplier_rank', '>', 0)])

    def action_rfq_send(self):
        if not self.vendor_ids:
            # Fallback to the original method if no vendors are selected
            return super(CustomPurchaseOrder, self).action_rfq_send()

        template_id = self.env.ref('purchase.email_template_edi_purchase').id
        mail_template = self.env['mail.template'].browse(template_id)

        for vendor in self.vendor_ids:
            # Create a copy of the RFQ for each vendor
            rfq_copy = self.copy(default={
                'partner_id': vendor.id,
                'state': 'draft',
            })

            # Confirm the RFQ
            rfq_copy.button_confirm()

            # Send the email to the vendor
            mail_template.with_context(email_to=vendor.email).send_mail(rfq_copy.id, force_send=True)

        res = super(CustomPurchaseOrder, self).action_rfq_send()
        # Ensure the response contains 'context' before modifying it
        if 'context' in res:
            res['context'] = dict(res['context'])  # Ensure it's a mutable dictionary
            res['context']['vendor_ids'] = [v.id for v in self.vendor_ids]

        return res
