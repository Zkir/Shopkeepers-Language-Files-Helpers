# *********************************************************************
# simple script to reformat translation file created by poeditor
# for some unknown reason, the format of Shopkeepers plugin language files
# is not compartible with popular translation tools.
# see https://github.com/Shopkeepers/Language-Files
# (c) Zkir 2024
# *********************************************************************
import yaml
import re

def check_placeholders_v(value, orig_value):
    
    placeholders = [".","{","}"]
    r=re.findall("(&.)", orig_value)
    if r:
        for q in r:
            if q not in placeholders:
                placeholders.append(q)
    
    r=re.findall("({\w+})", orig_value)
    if r:
        for q in r:
            if q not in placeholders:
                placeholders.append(q)
    
        #print(placeholders)   
        
    for placeholder in placeholders:    
        a=value.count(placeholder) 
        b=orig_value.count(placeholder)
        if a!=b:
          print()
          print("Количество вхождений '"+placeholder+"' отличается")
          print("    " +value+ "\n    "+ orig_value)
      

def check_placeholders(source_file_name, translated_file_name):
    with open(source_file_name, "r",encoding='utf-8') as stream:
        orig_strings = yaml.safe_load(stream)    
        
    with open(translated_file_name, "r",encoding='utf-8') as stream:
        translated_strings = yaml.safe_load(stream)    
        
    for key in translated_strings:
        value= translated_strings[key]
        orig_value = orig_strings[key]
        
        if value is None:
            value = ""        
            
        if orig_value is None:
            orig_value = ""        
            
        #if (value=="" and orig_value!="") or (value!="" and orig_value==""):
        #    print(key)
        #    print(value)
        #    print(orig_value)
        #    print("")        
        
        check_placeholders_v(value, orig_value)   
      

def reformat(s):
    if s[0] in ("#", " "):
        return s
    else:
        tokens = s.strip('\n').split(":",1)

        key = tokens[0]
        value =  tokens[1]        
        if value.strip() == "NULL":
            value = ""
        
      
        if key.isnumeric():
            key = "-"

        if key == "-":
            return key +  value + '\n'
        else:
            return key + ":" + value + '\n'

def main():
        
    check_placeholders("Shopkeepers_English.yml", "Shopkeepers_Russian.yml")    
    
    f1 = open("Shopkeepers_Russian.yml", "r",encoding='utf-8')
    f2 = open("language-ru.yml", "w",encoding='utf-8')
    for x in f1:
        s=reformat(x)
        f2.write(s)

    f1.close()
    

if __name__ == '__main__':
    main()
    

