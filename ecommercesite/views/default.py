from pyramid.session import SignedCookieSessionFactory
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render
from sqlalchemy.exc import DBAPIError
from ..models import Cart
import transaction
from ..models import Register
from sqlalchemy.orm import Query
from sqlalchemy import and_

@view_config(route_name='home',renderer='../templates/home.jinja2')
def home(request):
	session = request.session
	if 'cartcnt' in session:
		cartcnt = session['cartcnt']
	else:
		cartcnt = 0
	return Response(render('../templates/home.jinja2',{'cartcnt':cartcnt},request=request))

@view_config(route_name='shop',renderer='../templates/shop.jinja2')
def shop(request):
	ses = request.session
	if 'lstat' in ses:
		stat = ses['lstat']
	else:
		ses['lstat'] = 'false'
		stat = ses['lstat']
	if 'cartcnt' in ses:
		cartcnt = ses['cartcnt']
	else:
		ses['cartcnt'] = 0
		cartcnt = 0
	if request.POST.get('reg'):
		cartcnt = ses['cartcnt']
		email = request.params['email']
		pwd = request.params['pwd']
		q = request.dbsession.query(Register)
		for i in q:
			if i.email == email:
				return Response(render('../templates/shop.jinja2',{'result':'User already exists !','stat':stat,'cartcnt':cartcnt},request = request))
		p = Register(email,pwd)
		request.dbsession.add(p)
		transaction.commit()
		return Response(render('../templates/shop.jinja2',{'result':'Registration Successfuly !','cartcnt':cartcnt},request=request))
	if request.POST.get('outsub'):
		cartcnt = ses['cartcnt']
		print('hello')
		ses['lstat'] = "false"
		stat = 'false'
		return Response(render('../templates/shop.jinja2',{'result':'Logout Successful !','stat':stat,'cartcnt':cartcnt},request=request))
	if request.POST.get('log'):
		cartcnt = ses['cartcnt']
		if stat == 'true':
			return Response(render('../templates/shop.jinja2',{'result':'Already Logged in !','stat':stat,'cartcnt':cartcnt},request=request))
		else:
			lemail = request.params['lemail']
			lpwd = request.params['lpwd']
			q =request.dbsession.query(Register).filter(and_(Register.email == lemail,Register.password == lpwd))
			if q.count() > 0:
				ses['lstat'] = "true"
				stat = 'true'
				return Response(render('../templates/shop.jinja2',{'result':'Login Successful !','stat':stat,'cartcnt':cartcnt},request=request))
			else:
				return Response(render('../templates/shop.jinja2',{'result':'Invalid Username/Password !','stat':stat,'cartcnt':cartcnt},request=request))
	if request.POST.get('sub'):
		name = request.params['pname']
		desc = request.params['pdesc']
		price = request.params['pprice']
		img = request.params['pimg']
		cartcnt = request.params['cartcnt']
		ses['cartcnt'] = cartcnt
		q = request.dbsession.query(Cart)
		p = Cart(name,desc,price,img)
		request.dbsession.add(p)
		transaction.commit()
		return Response(render('../templates/shop.jinja2',{'stat':stat,'cartcnt':cartcnt},request=request))
	return {'stat':stat,'cartcnt':cartcnt}

@view_config(route_name='faq',renderer='../templates/faq.jinja2')
def faq(request):
	session = request.session
	if 'cartcnt' in session:
		cartcnt = session['cartcnt']
	else:
		cartcnt = 0
	return Response(render('../templates/faq.jinja2',{'cartcnt':cartcnt},request=request))

@view_config(route_name='cart',renderer='../templates/cart.jinja2')
def cart(request):
	session = request.session
	if 'cartcnt' in session:
		cartcnt = session['cartcnt']
	else:
		cartcnt = 0
	if request.POST.get('del'):
		q = request.dbsession.query(Cart)
		id = request.params['delitem']
		request.dbsession.query(Cart).filter(Cart.id == id).delete()
		session['cartcnt'] = int(session['cartcnt']) -1
		cartcnt = session['cartcnt']
		return Response(render('../templates/cart.jinja2',{'result':q,'cartcnt':cartcnt},request=request))
	print('yov')
	q = request.dbsession.query(Cart)
	return Response(render('../templates/cart.jinja2',{'result':q,'cartcnt':cartcnt},request=request))

@view_config(route_name='contact',renderer='../templates/contact.jinja2')

def contact(request):
	session = request.session
	if 'cartcnt' in session:
		cartcnt = session['cartcnt']
	else:
		cartcnt = 0
	return Response(render('../templates/contact.jinja2',{'cartcnt':cartcnt},request=request))

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_EcommerceSite_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
