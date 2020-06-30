import json
import os


class SimpleDataBase:
    def __init__(self, databasename, encryption_key):
        self.dbname = databasename
        self.encryption_key = encryption_key
        try:
            if os.path.exists(str(self.dbname)):
                self.db = json.load(open(self.dbname))
                if self.encrypt_key(self.encryption_key, self.encryption_key) != self.db['encryption_key']:
                    raise Exception('Encryption keys do not match')
            else:
                self.db = {}
                self.set_encryption_key(self.encryption_key)
        except Exception as e:
            print(e)
            exit()

        self.save()

    def save(self):
        try:
            json.dump(self.db, open(str(self.dbname), 'w'), indent=4, sort_keys=len)
            return True
        except Exception as e:
            return False

    def set_key(self, key, value):
        self.db[key] = value
        self.save()

    def get_key(self, key):
        if key in self.db:
            return self.db[key]
        return None

    def get_all_keys(self):
        without_encrypt = []
        for key in self.db:
            if key != 'encryption_key':
                without_encrypt.append(key)

        return without_encrypt

    def remove_key(self, key):
        if key in self.db:
            del self.db[key]
            self.save()
            return True
        return False

    def exists(self, key):
        return True if key in self.db else False

    def set_encryption_key(self, encryption_key):
        if not self.exists(encryption_key):
            self.set_key('encryption_key', self.encrypt_key(encryption_key, encryption_key))

    def encrypt_key(self, value, encrypt_key=None):
        if not encrypt_key:
            encrypt_key = self.encryption_key
        encoded_value = []
        for i in range(len(value)):
            key_chr = encrypt_key[i % len(encrypt_key)]
            encoded_chr = chr(ord(value[i]) + ord(key_chr) % 256)
            encoded_value.append(encoded_chr)
        return ''.join(encoded_value)

    def decrypt_key(self, value, encrypt_key=None):
        if not encrypt_key:
            encrypt_key = self.encryption_key
        decoded_value = []
        for i in range(len(value)):
            key_chr = encrypt_key[i % len(encrypt_key)]
            decoded_chr = chr(ord(value[i]) - ord(key_chr) % 256)
            decoded_value.append(decoded_chr)
        return ''.join(decoded_value)
