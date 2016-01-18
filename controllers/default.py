@auth.requires_login()
def index():
    form = FORM(INPUT(_name='vmid', _id='vmid'),
                INPUT(_class='task-button', _type='button', _id='start', _name='start', _value='start'),
                INPUT(_class='task-button', _type='button', _name='pause', _value='pause'),
                INPUT(_class='task-button', _type='button', _name='shutdown', _value='shutdown'),
                INPUT(_class='task-button', _type='button', _name='resume', _value='resume'),
                )
    script = """
    <script>
    (function(){
            var $buttons = $('.task-button');
            $buttons.each(function(){
              var $this = $(this);
              $this.on('click', function(){
                $.ajax({
                    type : 'POST',
                    url : 'baadal/action/'+ this.name + '.json',
                    data : {
                        vmid : $('#vmid').val()
                    },
                    success : function (response) {
                        console.log(response);
                    }
                });
              });
              console.log(this.name);
            });
        })();
        </script>
        """
    response.script = script
    return dict(form=form)


@auth.requires_login()
def home():
    return dict()

def user():
    if request.vars._formname == 'login':
        session.username = request.vars.username
        session.password = request.vars.password
    if request.args(0) == 'not_authorized':
        raise HTTP(403, 'forbidden')
    else:
        if auth.user and request.args(0) in ('login', None):
            redirect('/baadal/user')
        from gluon.html import INPUT, H2
        form = auth()
        el = list()
        el.append(H2('Please log in')) 
        label = LABEL('Email address')
        label.attributes['_for'] = 'auth_user_username'
        label.add_class('sr-only')
        el.append(label)
        for i in form.elements():
            if isinstance(i, INPUT):
                if i.attributes['_type'] in ('text','password'):
                    i.add_class('form-control')
                if i.attributes['_type'] == 'submit':
                    i.add_class('btn btn-primary btn-lg btn-block')
                el.append(i)
        form.components = el
        form.add_class('form-signin')
        return dict(form=form)
