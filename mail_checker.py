#!/usr/bin/env python

##############################################
##                                          ##
##      MAIL_CHECKER by ZIRCONET (2020)     ##
##       cittadinoimperfetto@gmail.com      ##
##                                          ##
##############################################

import configparser
import imaplib
import os
import email


#lettura login.ini
config = configparser.ConfigParser()
config.read('login.ini')

#variabili
MY_ACCOUNT  = config.get('Credenziali', 'account')
MY_DOMAIN   = config.get('Credenziali', 'domain')
MY_PWD      = config.get('Credenziali', 'password')
MY_MAILBOX  = config.get('Credenziali', 'mailbox')
IMAP_SERVER = config.get('Credenziali', 'imap')
MY_DIR      = config.get('Controllo', 'directory')
MY_MESSAGE  = config.get('Controllo', 'print_text_message')
MY_ADDRESS  = config.get('Controllo', 'print_address')
MY_CHECK    = config.get('Controllo', 'check_directoy')
 
def check():
    if str(MY_CHECK) == 'Y':
        isdir = os.path.isdir(MY_DIR)  
        if isdir == False:
            os.mkdir(MY_DIR)
            print 'Creata directory: ' + MY_DIR
    else:
        isdir = os.path.isdir(MY_DIR)  
        if isdir == False:
            print 'Ci sono problemi con la directory impostata...'  


def main():
    try:
        #collegamento alla casella email
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(MY_ACCOUNT,MY_PWD)
        mail.select(MY_MAILBOX)
        #Parsing email    
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        status, response = mail.search(None, '(UNSEEN)')       
        id_list = response[0].split()
    except:
        print 'Errore lettura casella mail'
        return

    for e_id in id_list:
            control = 0
            e_id = e_id.decode('utf-8')
            typ, response = mail.fetch(e_id, '(RFC822)')
            email_message = email.message_from_string(response[0][1])
            email_subject = email_message['Subject']
            email_date = email_message['Date']
            email_from = email.utils.parseaddr(email_message['From'])
            email_response = str(email_from[1])
            riga1 = str('From : ' + str(email_from[0]))
            riga2 = str('Email : ' + str(email_response))
            riga3 = str('Data: ' + str(email_date))
            riga4 = str('Oggetto : ' + str(email_subject) + '\n')
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))

                    # skip any text/plain (txt) attachments
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        body = part.get_payload(decode=True)  # decode
                        break
            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
            else:
                body = email_message.get_payload(decode=True)
            messaggio = riga1 + '\n' + riga2 + '\n' + riga3 + '\n'+ riga4 + '\n'+ body
            
            data = email_date.replace(' ', '_')
            data = data.replace (',','')
            data = data.replace (':','_')
            data = data.replace ('+','')
            data = data[:-5]

            if str(MY_ADDRESS) == 'Y':
                data = str(email_response) + '__' + data 

            #Check if any attachments at all
            if email_message.get_content_maintype() != 'multipart':
                    continue

            for part in email_message.walk():
                    # multipart are just containers, so we skip them
                    if part.get_content_maintype() == 'multipart':
                            continue
                    # is this part an attachment ?
                    if part.get('Content-Disposition') is None:
                            continue

                    filename = part.get_filename()
                    filename = data + '_' + part.get_filename()
                    att_path = os.path.join(MY_DIR, filename)
                    try:
                        fp = open(att_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                        control = 1
                        print ('Salvato : ' + filename + '\n')
                    except:
                        print 'Errore Salvataggio ' + filename
                        continue

            if control == 1 and str(MY_MESSAGE) == "Y":
                print 'OK'
                filename_message = data
                att_path = os.path.join(MY_DIR, filename_message)
                try:
                    fp = open(att_path, 'wb')
                    fp.write(messaggio)
                    fp.close()
                    print ('Salvato : ' + filename_message + '\n')
                except:
                    print 'Errore Salvataggio file testo messaggio'
                    continue


if __name__== "__main__":
    check()
    main()