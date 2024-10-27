from odoo import http
from odoo.http import request
import base64

class IdApplicationController(http.Controller):

    @http.route('/national_id/application', type='http', auth='public', website=True)
    def id_application_form(self, **kwargs):
        return http.request.render('id_application.national_id_application_form',{})

    @http.route('/national_id/application/submit', type='http', auth='none', methods=['POST'], csrf=True)
    def submit_application(self, **post):
        try:
            lc_letter_file = post.get('lc_letter')
            photo_file = post.get('photo')
            lc_letter = base64.b64encode(lc_letter_file.read()) if lc_letter_file else False
            photo = base64.b64encode(photo_file.read()) if photo_file else False
            vals = {
                    'name': post.get('name'),
                    'date_of_birth': post.get('date_of_birth'),
                    'sex': post.get('sex'),
                    'country_of_origin': post.get('country_of_origin'),
                    'parent_nin': post.get('parent_nin'),
                    'lc_letter': lc_letter,
                    'photo': photo,

                    }
            application = request.env['id.application'].sudo().create(vals)
            return request.render('id_application.thank_you', {'application': application})
        except Exception as e:
            return request.render('id_application.error', {'error': str(e)})
