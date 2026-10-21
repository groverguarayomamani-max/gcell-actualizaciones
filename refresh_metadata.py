"""Renew freshness for the SAME approved signed target; never promote a new package."""
import json,datetime,hashlib
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding,rsa
TARGET=('Schema','Channel','Sequence','Archive','Sha256','Bytes')
def renew(current_bytes,current_signature,pinned_public_pem,private_key,approved_target,now):
 public=serialization.load_pem_public_key(pinned_public_pem)
 if not isinstance(public,rsa.RSAPublicKey) or public.key_size<3072:raise ValueError('Production RSA key required')
 public.verify(current_signature,current_bytes,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=32),hashes.SHA256())
 current=json.loads(current_bytes)
 if set(current)!=set(TARGET)|{'IssuedUtc','ExpiresUtc'}:raise ValueError('Unexpected metadata fields')
 if any(current[k]!=approved_target[k] for k in TARGET):raise ValueError('Target differs from manually approved immutable release')
 if current['Schema']!=1 or current['Channel'] not in ('gcell-ventas-pilot','gcell-ventas-stable') or current['Sequence']<1 or current['Archive']!='piloto.zip' or not 1<=current['Bytes']<=1024**3 or len(current['Sha256'])!=64 or any(c not in '0123456789abcdefABCDEF' for c in current['Sha256']):raise ValueError('Invalid target')
 if private_key.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)!=public.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo):raise ValueError('Unapproved signing-key change')
 if now.tzinfo is None:raise ValueError('UTC time required')
 # Expired metadata can be renewed by its authorized signer, after verifying the
 # approved immutable target. The client still must never install expired metadata.
 result={k:current[k] for k in TARGET};result.update(IssuedUtc=now.isoformat(),ExpiresUtc=(now+datetime.timedelta(days=7)).isoformat())
 data=json.dumps(result,indent=2).encode('utf-8')
 signature=private_key.sign(data,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=32),hashes.SHA256())
 return data,signature
