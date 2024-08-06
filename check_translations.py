# ********************************************************************************
# A very simple script to find existing translations and check their completeness
# see https://github.com/Shopkeepers/Language-Files
# and discussion https://github.com/Shopkeepers/Language-Files/issues/68
# (c) Zkir 2024
# ********************************************************************************

import os
import sys
import yaml
from git import Repo
import re

LANGUAGE_FILES_FOLDER="../Shopkeepers-Language-Files"
ORIGNAL_EN_DEFAULT="language-en-default.yml"
ORIGNAL_EN="language-en.yml" #in older versions original lang file is called just language-en 

LINK_TEMPLATE = "https://github.com/Shopkeepers/Language-Files/blob/{}/lang/{}"

def get_lang_code(filename):
    r=re.findall(r"language\-(.*)\.yml", filename)
    return r[0]


def compare_translations(original_strings, translated_strings,original_strings_of_version):
    
    missing_translations  = 0
    obsolete_translations = 0  
    extra_translations    = 0
    
    for key in original_strings:
        
        orig_value = original_strings[key]
        if isinstance(orig_value, list):
            orig_value = "\n".join(orig_value)
            
        value = translated_strings.get(key,"")
        if isinstance(value, list):
            value = "\n".join(value)        
            
        orig_value_of_version = original_strings_of_version.get(key,"")
        if isinstance(orig_value_of_version, list):
            orig_value_of_version = "\n".join(orig_value_of_version)
      
        
        if orig_value != "" and value == "":
            missing_translations += 1   
            
        if orig_value != "" and value != "" and orig_value_of_version != orig_value:
            obsolete_translations += 1

    for key in translated_strings:
           
        if key not in original_strings:
            extra_translations += 1                  
        
        
    return missing_translations, obsolete_translations, extra_translations    
        

def sort_versions(head):
     
    v = head.name.split(".")
     
    return str(v[0]) +"{:04.0f}".format(int(v[1])) + "{:04.0f}".format(int(v[2]))
        
def main(blnMakeMD):
    
    translations=[]
    if not os.path.exists(LANGUAGE_FILES_FOLDER):
        print(f"ERROR: path to Language-Files repository {LANGUAGE_FILES_FOLDER} is not found")
        print("if your path is different, please change LANGUAGE_FILES_FOLDER constant")
        exit()
    
    
    
    repo = Repo(LANGUAGE_FILES_FOLDER)    
    sorted_heads = sorted(repo.heads, key= sort_versions, reverse=True)
    
    # We start with the most latest version, 
    # because we need to compare to the most recent language file
    sorted_heads[0].checkout()    
    print("Current branch is: ", sorted_heads[0].name)
    if blnMakeMD:
        print()
    
    # get current english orignal
    with open(LANGUAGE_FILES_FOLDER+"/lang/" +ORIGNAL_EN_DEFAULT , "r",encoding='utf-8') as f:
        original_strings = yaml.safe_load(f)    

    total_translations =  len(original_strings)       
    print(ORIGNAL_EN_DEFAULT + " contains " + str(total_translations) + " keys")    
    print()
    print(f"|{'Language':10}|{'Version':7}| {'Completeness':>12}|{'Missing':>8}|{'Obsolete':>8}|{'Extra':>6}| Link" )
    print( "|----------|-------|-------------|--------|--------|------|-----------")
        
    for head in sorted_heads:
        head.checkout()    
    
        files = os.listdir(LANGUAGE_FILES_FOLDER+"/lang")
        for file in files:
            if file not in (ORIGNAL_EN_DEFAULT,ORIGNAL_EN) and file.lower() not in translations:
                with open(LANGUAGE_FILES_FOLDER+"/lang/" + file, "r",encoding='utf-8') as f:
                    translated_strings = yaml.safe_load(f) 

                original_en_of_version = LANGUAGE_FILES_FOLDER+"/lang/" + ORIGNAL_EN_DEFAULT
                if not os.path.isfile(original_en_of_version):
                    original_en_of_version = LANGUAGE_FILES_FOLDER+"/lang/" + ORIGNAL_EN
                
                if not os.path.isfile(original_en_of_version):
                    print("ERROR: version "+ head.name + " lacks english language file")                    
    
                    
                with open(original_en_of_version, "r",encoding='utf-8') as f:
                    original_strings_of_version = yaml.safe_load(f)     
                
                #Compare translation                
                missing_translations, obsolete_translations, extra_translations = compare_translations(original_strings, translated_strings,original_strings_of_version)
                
                completeness = int((total_translations - missing_translations - obsolete_translations) / total_translations *100)
                #print(file, head.name, missing_translations, obsolete_translations, extra_translations)
                lang_code = get_lang_code(file)
                if blnMakeMD:
                    link = LINK_TEMPLATE.format(head.name, file)
                    link=f"[{file}]({link})"
                else: 
                    link = file                  
                print(f"|{lang_code:10}|{head.name:7}|{completeness:12}%|{missing_translations:8}|{obsolete_translations:8}|{extra_translations:6}|{link}")
                
                translations.append(file.lower())                
    

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == "--MD":
        blnMakeMD = True
    else:     
        blnMakeMD = False 
    main(blnMakeMD)
        