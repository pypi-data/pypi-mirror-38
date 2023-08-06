```sh
$ git clone https://bitbucket.org/rstm-sf/pykmqc.git
$ cd pykmqc
$ pip3 install virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

```python
import kmqc

from kmqc import Qubit, gates, Program


qubit = Qubit(0)
p = Program()
p.append_instruction(gates.H(qubit))

endpoint = 'http://httpbin.org/post'
user_id, api_key = 'user_id', 'api_key'
conn = kmqc.connect(endpoint, user_id, api_key)
r = conn.execute(p)
print(r)
```

```
[qvm_conn]
endpoint = http://httpbin.org/post
user_id  = user_id
api_key  = api_key
```

```python
import kmqc

from kmqc import gates, Program


p = Program(
    gates.X(1),
    gates.H(0),
    gates.H(1),
    gates.CNOT(0, 1),
    gates.H(0)
)
conn = kmqc.connect(**kmqc.config('qvm_conn.ini', 'qvm_conn'))
r = conn.execute(p)
print(r)
```
