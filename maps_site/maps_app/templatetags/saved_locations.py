from django import template
from maps_app.models import *
from django.template.loader import render_to_string

register  = template.Library()


@register.tag
def saved_location(parser,token):

	params = token.split_contents()
	if len(params) < 2 :
		raise template.TemplateSyntaxError('please provide id for the entry')

	return savedLocationNode((params[1]))

class savedLocationNode(template.Node):
	def __init__(self,entry_id):
		self.entry_id = template.Variable(entry_id)

	def render(self,context):
		try:
			sid = self.entry_id.resolve(context)
		except template.VariableDoesNotExist:
			return ''
		try:
			self.addr =  Address.objects.get(id=sid)
		except Address.DoesNotExist:
			#maybe there's a better error?
			raise template.TemplateSyntaxError('invalid id')


		return render_to_string('maps_app/saved_location_node.html',{'addr': self.addr })
