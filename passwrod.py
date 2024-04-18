import json
import re
from leak_api import LeakCheckAPI
from prettytable import PrettyTable




class GET_PASSWORD():
    def __init__(self, email):
        
        self.email = email
        
    def remove_ansi(self,text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)    
        
    def run(self):
        try:
            T = PrettyTable()
            api = LeakCheckAPI()
            with open('config.json', 'r') as f:
                json_data =  json.load(f)
                leak_check_api = json_data[0]['leak_check_api']
                api.set_key(leak_check_api)
                set_proxy = api.set_proxy(json_data[0]['leak_proxy'])
                s, m = set_proxy
                if s:
                    data = api.lookup(self.email, "email")
                    arr_data = []
                    count_result = 0
                    if len(data) > 0:
                        if data['success']:
                            for line in data['result']:
                                if line['line'].lower() != self.email.lower() or line['line'].upper() != self.email.upper():
                                    combo = line['line']
                                    if combo:
                                        password  = combo.split(':')[1]
                                        if len(password) >= 7:
                                            if all(char.isdigit() or char == '.' for char in password):
                                                pass
                                            elif ' ' not in password:
                                                
                                                arr_data.append(password.lower())
                                                arr_data.append(password.capitalize())
                                                arr_data.append(f'{password}!')
                                                arr_data.append(f'{password}!!')
                                                arr_data.append(f'{password.lower()}!')
                                                arr_data.append(f'{password.lower()}!!')
                                                arr_data.append(f'{password.capitalize()}!')
                                                arr_data.append(f'{password.capitalize()}!!')
                                            count_result+=1
                                
                            
                            value = {
                                "succes": True,
                                "result": count_result,
                                "modify_result": len(arr_data),
                                "item": arr_data
                            }
                            
                            
                            try:
                                T.add_row([f'[ {self.email} ]',f'[ SUCCES ]', f'[ {value} ]'])
                            except:
                                pass
                            return json.dumps(value) 
                        else:
                            T.add_row([f'[ {self.email} ]',f'[ API LEAKCHECKER ERROR ]', f'[ {value} ]'])
                            return 500, 'API LEAKCHECKER ERROR'
                    else:
                        value = {
                            "succes": True,
                            "result": 0,
                        }
                        T.add_row([f'[ {self.email} ]',f'[ API LEAKCHECKER ERROR ]', f'[ {value} ]'])
                        return json.dumps(value) 
                else:
                    value = {
                        "succes": False,
                        "result": 0,
                        "message": 'PROXY LEAK ERROR'
                    }
                    T.add_row([f'[ {self.email} ]',f'[ API LEAKCHECKER ERROR ]', f'[ {value} ]'])
                    return json.dumps(value)
        except Exception as e:
            print(e)
            T.add_row([f'[ {self.email} ]',f'[ ERROR ]' ,f'[ {e} ]'])
            value = {
                        "succes": False,
                        "result": 0,
                        "message": 'error'
                    }
            return json.dumps(value) 
        finally:
            table_text_with_colors = T.get_string(fields=["Field 1", "Field 2", "Field 3"], header=False)
            table_text_plain = self.remove_ansi(table_text_with_colors)
            with open('LOGS/raport_leak_checker.txt', 'a') as f:
                f.write(str(table_text_plain) + '\n')  
                
# x = GET_PASSWORD('xuithoi@gmail.com')
# aa = x.run()
# parsed_aa = json.loads(aa)
# print(parsed_aa)
