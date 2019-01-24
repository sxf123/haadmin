from jinja2 import Environment,PackageLoader

def render_frontend(templatefile,frontend,file):
    env = Environment(loader=PackageLoader('haproxy.config'))
    template = env.get_template(templatefile)
    content = template.render(frontends=frontend)
    with open(file,'w') as f:
        f.write(content)
        f.close()

def render_backend(templatefile,backend,file):
    env = Environment(loader=PackageLoader('haproxy.config'))
    template = env.get_template(templatefile)
    content = template.render(backends=backend)
    with open(file,'w') as f:
        f.write(content)
        f.close()