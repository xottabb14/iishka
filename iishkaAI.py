#pip3 install g4f

import config
import g4f


def gpt_message(text):
    answ = ""
    try:
        response = g4f.ChatCompletion.create(model="gpt-4o-mini", provider=config.prov_name,\
                    messages=[{"role": "user", "content": text}],\
                    stream=config.prov_name.supports_stream)

        
        for message in response:
            answ = answ+str(message)
            
    except Exception as err:
        answ = "Error: "+str(err)

    return(answ)

print(gpt_message("Как на cisco 881 настроить DHCP-пул?"))
