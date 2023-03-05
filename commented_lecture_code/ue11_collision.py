import hashlib

prefix='255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe01'
# %PDF-1.3%âãÏÓ1 0 obj<</Width 2 0 R/Height 3 0 R/Type 4 0 R/Subtype 5 0 R/Filter 6 0 R/ColorSpace 7 0 R/Length
# 8 0 R/BitsPerComponent 8>>streamÿØÿþ$SHA-1 is dead!!!!!/ì	#9u9±¡Æ<Láÿþ

m1= '7f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df614f86db1690901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe9d41398abe12ef5bc942be33542a4802d98b5d70f2a332ec37fac3514e74ddc0f2cc1a874cd0c78305a21566461309789606bd0bf3f98cda8044629a1'
# FÜ¦¶~;ª²VEÊgÖÇøKLyà+=öøm±i	ÅkEÁS
# þß·`8érr/ç­rIàFÂ0WéÔ«á.õ¼+ã5B¤-µ×*3.Ã
# ¬5çMÜ,Á¨tÍx0Z!Vda0`kÐ¿?Í¨F)¡

m2= '7346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a90901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570feb141398bb552ef5a0a82be331fea48037b8b5d71f0e332edf93ac3500eb4ddc0decc1a864790c782c76215660dd309791d06bd0af3f98cda4bc4629b1'
# sFÜf¶~¶!²VùÊgÌ¨Çø[¨Ly+=âøm³©	ÕßEÁO&þß³Ü8éjÂ
# /ç½rE¼àFÒ<Wë»U.õ ¨+ã1þ¤7¸µ×3.ß¬5ëMÜ
# ìÁ¨dyx,v!V`Ý0ÐkÐ¯?Í¤¼F)±

h1 = hashlib.sha1()
h1.update (bytes.fromhex(prefix+m1))
print(f'SHA1 hash of first message:  {h1.hexdigest()}') # SHA1 hash of first message:  f92d74e3874587aaf443d1db961d4e26dde13e9c
h2 = hashlib.sha1()
h2.update (bytes.fromhex( prefix+m2))
print(f'SHA1 hash of second message: {h2.hexdigest()}') # SHA1 hash of second message: f92d74e3874587aaf443d1db961d4e26dde13e9c

print(f'SHA1 hashes are equal: {h1.hexdigest() == h2.hexdigest()}') # ADDED BY ME; yields 'True'

#print(bytes.fromhex(prefix))
print(bytes.fromhex(prefix+m1))
#print(bytes.fromhex(prefix+m2))



"""
kendrick@Kendricks-MacBook-Pro-M2 commented_lecture_code % shasum m1.pdf
f92d74e3874587aaf443d1db961d4e26dde13e9c  m1.pdf
kendrick@Kendricks-MacBook-Pro-M2 commented_lecture_code % shasum m2.pdf
f92d74e3874587aaf443d1db961d4e26dde13e9c  m2.pdf
"""
