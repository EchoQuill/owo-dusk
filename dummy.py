import re
def clean(msg):
    return re.sub(r'[^a-zA-Z]', '', msg)

captcha = ["⚠️ **|** <@1180828954504990791>! Pl​ease co​mplete your c​aptcha to ve​rify that y​ou are human! (4/5)", """**⚠️ |** <@1180828954504990791>, are yo​u a real h​uman? Plea​se use th​e link b​elow so I can check!
<:blank:427371936482328596> **|** Pl​ease comple​te this within 10 minutes or it may result in a ban!""", """**⚠️ | .ylenavy**, Beep Boop. Please DM me with only the following **6 letter word** to check that you are a human!
:blank: **|** If you have trouble solving the c${invisible}aptcha, please ask us in our support guild!"""]

for i in captcha:
    t=clean(i)
    print()
    print(t)
    print()
    if "human" or "captcha" or "link" or "letterword" in clean(i).lower():
        print("passed")
    else:
        print("failed")