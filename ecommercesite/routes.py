def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/home')
    config.add_route('index','/index')
    config.add_route('shop','/shop');
    config.add_route('contact','/contact');
    config.add_route('faq','/faq');
    config.add_route('cart','/cart');
