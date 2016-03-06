{% extends "b64.tpl" %}
{% block shellcode %}{{obfs.set_wrap('shellcode', obfs.add_comment(obfs.shellcode,'php'))}}{% endblock %}
