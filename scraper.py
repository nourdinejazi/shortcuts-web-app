import requests 
from bs4 import BeautifulSoup
from links_chich import * 

def fill(ref) :
    payload={
            'login': email_intern,
            'password':mdp_intern
            }
    if 'R' in ref : 
        ref=ref.replace('R','')
    with requests.session() as s : 
        s.post(login_intern_link,data=payload)
        r=s.get(site_link+'/cpanel_magazin/admin/ges_detail_bijou.php?coderef={}&bouton=Envoyer'.format(ref))
        soup=BeautifulSoup(r.content,'html.parser')
        long=len(soup.find_all('table'))
        if long==3: 
            tab=soup.find_all('table')[1]
            rows=tab.find_all('tr')
            for row in rows :
                if row.find('th') :
                    if row.find('th').text.strip()=="FAMILLE"  :
                        fam=row.find_all('td')[0].text.lower().strip()
                        if 'barcelet' in fam : 
                            fam=fam.replace('barcelet','Bracelet')
                    if row.find('th').text.strip()=="POIDS"  :
                        poids=row.find_all('td')[1].text
                        mat=row.find_all('td')[2].text.lower().replace('en','')
                    elif row.find('th').text.strip()=="P-V"  :
                        prix=int(float(row.find_all('td')[0].text.strip()))
            return {'prix' : prix , 'fam' : fam , 'poids' : poids, 'mat' : mat}
        else : 
            return "Référence invalide"

        
                                

def item_det(ref) :
    if (len(ref.split(' '))<2) :
        if fill(ref) == "Référence invalide":
            return ref
        else : 
            data=fill(ref)
            msg="bonsoir , suite a votre demande le prix est a {} TND / Poids : {} , {} en {}".format(data['prix'],data['poids'],data['fam'],data['mat'])
            return msg
    else :
        refs=ref.split(' ')
        msg='Bonsoir , suite a votre demande les prix sont : '
        i=0
        for r in refs : 
            if fill(r) != 'Référence invalide':
                data=fill(r)
                i=i+1
                if i==1 : 
                    msg=msg+"{}ére article a {} TND /Poids : {}  {} en {}      ".format(i,data['prix'],data['poids'],data['fam'],data['mat'])
                else : 
                    msg=msg+"{}éme article a {} TND /Poids : {}  {} en {}      ".format(i,data['prix'],data['poids'],data['fam'],data['mat'])

        return msg

def split_ref(ref) :
    refs=ref.split(' ')
    t=[]
    for r in refs :
        if r:
            r=r.replace('R','')
            r='R'+r
            t.append(r)
    return t 
