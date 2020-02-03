# SaveGmailAttachments
Python script to automatically save attachments received from a gmail box.

Credential gmail login and program settings are in login.ini file.

The program accesses the gmail box, checks the messages that are still to be read and for those that contain one or more attachments, it saves the files in the indicated directory, together with a text file that contains the email message (in case it does not matter, you can disable saving the message text by putting N in the print_text_message line in the login.ini file). The files are saved with the time reference of the received email + the name of the attachment received (by placing Y in the print_address line, the files are saved indicating the sender's email address in the name). Once the inbox has been processed, it will be 'read' and therefore the program will no longer process them.
