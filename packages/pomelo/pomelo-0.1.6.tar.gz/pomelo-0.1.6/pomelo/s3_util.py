from boto.s3.key import Key
from boto.s3.connection import S3Connection
import os
import boto3

class S3Store(object):
    def __init__(self,key_id,key_secret,host,port,bucket_name):
        self.conn = S3Connection(
            aws_access_key_id = key_id,
            aws_secret_access_key = key_secret,
            host = host,
            port = port,
            is_secure = False,
            calling_format='boto.s3.connection.OrdinaryCallingFormat'
        )
        self.bucket_name = bucket_name
        try:
            self.bucket = self.conn.get_bucket(self.bucket_name)
        except:
            pass
            #self.bucket = self.conn.create_bucket(self.bucket_name)
    
    def upload(self,local_path,remote_path):
        package_name = os.path.basename(local_path)
        package_key = Key(self.bucket, remote_path)
        packege_key.set_contents_from_filename(local_path)
        return True
    
    def download(self,remote_path,local_path):
        package_key = Key(self.bucket, remote_path)
        package_key.get_contents_to_filename(local_path)

    def dir(self,opath):
        rt = []
        path = ''.strip()
        if (path.startswith("/")):
            path = path[1:]
        for k in self.bucket.list(prefix = path,delimiter = "/"):
            rt.append(k.name)
        return rt
    
    def rename(self,old_name,new_name):
        package_old_key = Key(self.bucket, old_name)
        package_new_key = Key(self.bucket, new_name)
        if package_old_key.exists() and (not package_new_key.exists()):
            package_old_key.copy(self.bucket, package_new_key)
        if package_new_key.exists():
            package_old_key.delete()
        return True
    
    def delete_packetage(self, package_name):
        package_key = Key(self.bucket, package_name)
        if package_key.exists():
            package_key.delete()
        else:
            raise ValueError('package:%s are not exist' % package_name)
        return True