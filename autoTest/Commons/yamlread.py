import yaml


from Base.basepage import BasePage


def read_yaml(name):
    with open(name, encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return data

def generate_yaml(driver,name,index=1):
    page=BasePage(driver)
    labelelement=page.get_elements("xpath",f"(//form[starts-with(@class,'el-form')])[{index}]//label")
    label= {}
    for x in labelelement:
       label[x.text]=" "
    with open("./"+name+".yaml", "a",encoding='utf-8') as f:  # 写文件
        yaml.safe_dump(data=label, stream=f,allow_unicode=True)

def generate_yaml_gtos(driver,name,index=1):
    page=BasePage(driver)
    labelelement=page.get_elements("xpath",f"(//form[starts-with(@class,'el-form')])[{index}]//label")
    label= {}
    for x in labelelement:
       label[x.get_attribute("textContent")]=" "
    with open("./"+name+".yaml", "a",encoding='utf-8') as f:  # 写文件
        yaml.safe_dump(data=label, stream=f,allow_unicode=True)

def get_api_info(api_name, file_path=''):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.SafeLoader)[api_name]
        return data

