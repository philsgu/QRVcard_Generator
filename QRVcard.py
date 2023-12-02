import streamlit as st
import re 
from segno import helpers
import segno
import io

#create a session state for form validation
if "submitted" not in st.session_state:
    st.session_state['submitted'] = False
#Regex to catch validation errors
phone_format = r"^[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4}$"
zip_format = "^[0-9]{5}(?:-[0-9]{4})?$"
email_format = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
#url_format = "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
url_format = re.compile(
    r'^(?:http|ftp)s?://'  # scheme
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP address
    r'(?::\d+)?'  # port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


#US state list
states = ['', 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

st.markdown('## Create QR Business VCard for iPhone and Android Contact')
st.write('This will produce a QR code in VCard format')
st.write("Created by Phil Kim, MD (12/4/22)")
#title
profession_degree = ["DO", "MPH", "MD", "PhD"]

#create QR Function formation
def vcardmake (first=None, last= None, displayname=None, degree=None, title=None, org=None, email=None, phone=None, workphone=None, fax=None, street=None, city=None, region=None, zipcode=None, url=None):
    # n  = displayname.split(' ')
    # n.append(';')
    # n.insert(2, ' ')
    # n.insert(4, ' ')
    # name = ''.join(n[1:]) + n[0]
    # use a bitmap font
    #font = ImageFont.truetype("arial.ttf", 12)
    if degree:
        name = last.title() + " " + ", ".join(degree) + ";" + first.title()     
    else:
        name = last.title() + ";" + first.title()
    vcard = helpers.make_vcard(
        name=name,
        displayname=displayname,
        title=title,
        org=org,
        email=email,
        phone=phone,
        workphone=workphone,
        fax=fax,
        street=street,
        city=city,
        region=region,
        zipcode=zipcode,
        url=url
    )
    out = io.BytesIO()
    vcard.save(out, scale=3, border=10, kind='png') #save to buffer
    out.seek(0)
    
    #img = Image.open(out)
    #d1 = ImageDraw.Draw(img)
    #myfont = ImageFont.truetype("/System/Library/Fonts/Geneva.ttf", 12)
    #img_width, img_height = img.size
    #d1.text((img_width//2, 180), displayname, anchor='ms')
    return out


##################################################
def check_valid():
    st.session_state.submitted = True
   
    for k in st.session_state.keys():
        if k == 'Address':
            if st.session_state[k]:
                if not st.session_state['City']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: City")
                if not st.session_state['State']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: State")
                if not st.session_state['Zip']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: Zip")
                elif not re.match(zip_format, st.session_state['Zip']):
                    st.session_state.submitted = False
                    st.error(f"Incorrect Format: Zip")
                break         
        if k == 'City':
            if st.session_state[k]:
                if not st.session_state['Address']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: Address")
                if not st.session_state['State']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: State")
                if not st.session_state['Zip']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: Zip")
                elif not re.match(zip_format, st.session_state['Zip']):
                    st.session_state.submitted = False
                    st.error(f"Incorrect Format: Zip")
                break             
        if k == 'State':
            if st.session_state[k]:
                if not st.session_state['Address']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: Address")
                if not st.session_state['City']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: City")
                if not st.session_state['Zip']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: Zip")
                elif not re.match(zip_format, st.session_state['Zip']):
                    st.session_state.submitted = False
                    st.error(f"Incorrect Format: Zip")
                break
        if k == 'Zip':
            if st.session_state[k]: 
                if not re.match(zip_format, st.session_state[k]):
                    st.session_state.submitted = False
                    st.error(f"Incorrect Format: {k}")
                if not st.session_state['City']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: City")
                if not st.session_state['State']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: State")
                if not st.session_state['Address']:
                    st.session_state.submitted = False
                    st.error(f"Missing Address values: Address")
                break
    for k in st.session_state.keys():
        if k == 'Cell':
            if st.session_state[k]:
                if not re.match(phone_format, st.session_state[k]):
                    st.session_state.submitted = False
                    st.error(f"Incorrect Number Format: {k}")
        if k == 'Work':
            if st.session_state[k]:
                if not re.match(phone_format, st.session_state[k]):
                    st.session_state.submitted = False
                    st.error(f"Incorrect Number Format: {k}")
        if k == 'Fax':
            if st.session_state[k]:
                if not re.match(phone_format, st.session_state[k]):
                    st.session_state.submitted = False
                    st.error(f"Incorrect Number Format: {k}") 

    if not st.session_state['First']:
        st.session_state.submitted = False
        st.error(f"Missing Required Value: First")
    elif not re.match(r'^[a-zA-Z\s]+$', st.session_state['First'].strip()):
        st.session_state.submitted = False
        st.error(f"No numerics or special characters allowed: First")
        
    if not st.session_state['Last']:
        st.session_state.submitted = False
        st.error(f"Missing Required Value: Last")
    elif not re.match(r'^[a-zA-Z\s]+$', st.session_state['Last'].strip()):
        st.session_state.submitted = False
        st.error(f"No numerics or special characters allowed: Last")        
            
#     if not st.session_state['Email']:
#         st.session_state.submitted = False
#         st.error(f"Missing Required Value: Email")
    if st.session_state['Email']:
        if not re.match(email_format, st.session_state['Email']):
            st.session_state.submitted = False
            st.error(f"Incorrect Email Format")
  
    if st.session_state['Website']:
        if not re.match(url_format, st.session_state['Website']):
            st.session_state.submitted = False
            st.error(f"Incorrect URL Format")                            
###############################################            
with st.form('contact_info'):
    st.markdown("###### *Denotes Required")
    col1, bra, col2 = st.columns([3,1,3])

    with col1:
        first_name = st.text_input("First*", key="First").capitalize()
    with col2:
        last_name = st.text_input("Last*", key="Last").capitalize()
    
    degree = st.multiselect("Professional Degree(s)", options=profession_degree, key='Degree')
    title = st.text_input("Enter Occupation Title", key='Title')
    org = st.text_input("Organization", key='Organization')
    personal_cell = st.text_input("Cell Number (optional)", key='Cell', help='US Number Format (xxx)xxx-xxxxx')
    work_phone = st.text_input("Work Number", key='Work')
    work_fax = st.text_input("Work Fax", key='Fax')
    business_add = st.text_input("Business Address", key='Address')
    add1, add2, add3 = st.columns([4, 2, 4])

    with add1:
        city = st.text_input("City", key='City')
    with add2:
        state = st.selectbox("State", (states), key='State')
    with add3:
        zip_code = st.text_input("Zip", key='Zip')

    email = st.text_input("Email", key='Email')
    website = st.text_input("Website", key='Website')
    s1, s2, s3 = st.columns([4, 2, 4])
    with s2:
        submit = st.form_submit_button("Create VCard", on_click=check_valid)
    

    #execute QR generate code
    if st.session_state.submitted and submit:
        displayname = str()
        if degree:
            displayname = (" ").join([first_name.strip(), last_name.strip()]).title() + " " + ", ".join(degree)
            print (displayname)
        else:
            displayname = (' ').join([first_name.strip(), last_name.strip()]).title()
        #execute QR maker function
        col1, col2, col3 = st.columns([4, 4, 4])
        with col2:
            global qrcard
            qrcard = vcardmake(first=first_name.strip(), last=last_name.strip(), degree=degree, displayname=displayname, email=email, title=title.title(), org=org, phone=personal_cell, workphone=work_phone, fax=work_fax, street=business_add, city=city, region=state, zipcode=zip_code, url=website)

            st.image(qrcard, use_column_width='auto', output_format='PNG')
            

#Clear the values in all keys:
def clear_fields():
    st.session_state['Degree'] = []
    set_keys = ['Website',
                'Title',
                'Zip',
                'Last',
                'State',
                'First',
                'Address',
                'Cell',
                'Email',
                'Organization',
                'Work',
                'City',
                'Fax']
    for s in set_keys:
        st.session_state[s] = ''
                
try:
    d1, d2, d3, d4 = st.columns(4)
    with d2:
        st.download_button('Download Image', data=qrcard.read(), file_name=f'qr_card_{last_name.strip()}.png')
    with d3:
        st.button("Clear Fields", on_click=clear_fields, key='Clear')        
except NameError:
    print('Name ERROR on Global')


##Sample Write output          
# for item in st.session_state.items():
#     st.write(item)
