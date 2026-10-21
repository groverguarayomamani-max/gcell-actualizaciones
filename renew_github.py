import os,json,subprocess,tempfile,hashlib,datetime
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from refresh_metadata import renew
repo=os.environ['GITHUB_REPOSITORY']
assert repo=='groverguarayomamani-max/gcell-actualizaciones'
approved=json.loads(Path('approved-pilot.json').read_text())
with tempfile.TemporaryDirectory() as td:
 d=Path(td)
 subprocess.run(['gh','release','download','pilot','--repo',repo,'--pattern','release.*','--dir',str(d)],check=True)
 # Independently download the versioned approved asset and stream its hash.
 subprocess.run(['gh','release','download',approved['VersionTag'],'--repo',repo,'--pattern','piloto.zip','--dir',str(d)],check=True)
 h=hashlib.sha256();size=0
 with (d/'piloto.zip').open('rb') as f:
  while chunk:=f.read(1024*1024):h.update(chunk);size+=len(chunk)
 assert h.hexdigest()==approved['Sha256'] and size==approved['Bytes']
 key=serialization.load_pem_private_key(os.environ['GCELL_SIGNING_KEY_PEM'].encode(),None)
 data,sig=renew((d/'release.json').read_bytes(),(d/'release.sig').read_bytes(),Path('production-public.pem').read_bytes(),key,approved,datetime.datetime.now(datetime.timezone.utc))
 (d/'release.json').write_bytes(data);(d/'release.sig').write_bytes(sig)
 subprocess.run(['gh','release','upload','pilot',str(d/'release.json'),str(d/'release.sig'),'--clobber','--repo',repo],check=True)
 print('Same approved package: signed freshness renewed. No package promotion.')
