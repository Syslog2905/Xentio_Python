import imaplib
import email
import time
import re

EMAIL = "email.auto.blippar.hub@gmail.com"
PASSWORD = "dduqicyqpqferfdo"

PATTERN_UID = re.compile('\d+ \(UID (?P<uid>\d+)\)')


class gmail_client:
    def __init__(self, email, password, mailbox='inbox'):
        self.email = email
        self.password = password
        self.mailbox = mailbox
        self.session = self._connect_to_gmail(mailbox=self.mailbox)

    def _connect_to_gmail(self, mailbox):
        session = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        session.login(EMAIL, PASSWORD)

        session.select(mailbox, readonly=False)
        return session

    def _parse_uid(self, data):
        match = PATTERN_UID.match(data)
        return match.group('uid')

    def close_session(self):
        self.session.close()
        self.session.logout()

    def _process_search_result(self, data):
        emails = []
        for num in data[0].split():
            typ, data = self.session.fetch(num, '(RFC822)')
            email_body = data[0][1]
            try:#TODO : fix this using a better approach. This quickly fixes the tests
                mail = email.message_from_string(email_body).get_payload()[0].get_payload(decode=True)
            except:
                mail = email.message_from_string(email_body).get_payload(decode=True)
            emails.append(mail)
        if data == ['']:
            return None
        else:
            return emails

    def find_string_in_body(self, email_body, regexp):
        r = re.compile(regexp)
        search = r.search(email_body)
        if search:
            string_found = search.group(1)
            return string_found
        else:
            return None

    def find_text_in_body(self, email_body, text):
        if text in email_body:
            return True
        else:
            return False

    def get_all_emails(self):
        typ, data = self.session.search(None, 'ALL')
        return self._process_search_result(data)

    def move_all_emails(self, destination_mailbox):
        resp, items = self.session.search(None, 'ALL')
        email_ids = items[0].split()
        for email_id in email_ids:
            resp, data = self.session.fetch(email_id, "(UID)")
            time.sleep(0.5)
            msg_uid = self._parse_uid(data[0])
            result = self.session.uid('COPY', msg_uid, destination_mailbox)
            if result[0] == 'OK':
                mov, data = self.session.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
                self.session.expunge()

    def get_unseen_emails(self):
        typ, data = self.session.search(None, '(UNSEEN)')
        return self._process_search_result(data)

    def get_emails_by_subject(self, subject):
        typ, data = self.session.search(None, 'SUBJECT', subject)
        return self._process_search_result(data)

    def get_emails_by_sender(self, sender):
        typ, data = self.session.search(None, 'FROM', sender)
        return self._process_search_result(data)

    def get_last_email(self, retries=5):
        while retries > 0:
            emails = self.get_all_emails()
            if emails == None:
                retries -= 1
                time.sleep(1)
            else:
                return emails[-1]
        print("No emails received. Inbox is empty")

    def get_activation_link_from_email_body(self, email):
        #print(email)
        #For self managed accounts
        regexp = "To confirm this is correct, go to (.*)"
        link_self_managed = self.find_string_in_body(email, regexp)
        if link_self_managed != None:
            return link_self_managed
        #For managed accounts (Need better regexp or a different approach using beautifulsoup)
        regexp = """<td align="center" style="-webkit-border-radius: 2px; -moz-border-radius: 2px; border-radius: 2px;" bgcolor="#FCB93E"><a href="(.*)" target"""
        link_managed = self.find_string_in_body(email, regexp)
        return link_managed

    def get_reset_password_link_from_email_body(self, email):
        regexp = "Click the link below to reset your password.\n\n(.*)"
        return self.find_string_in_body(email, regexp)

    def get_user_email_from_email_body(self, email):
        regexp = "You're receiving this e-mail because user (.*) at"
        return self.find_string_in_body(email, regexp)

    def delete_all_emails(self):
        result, emails_id = self.session.uid('search', None, 'ALL')    #Searching all mails in folder
        if len(emails_id) == 0:
            print("No emails in inbox, not deleting anything.")
        else:
            emails_id = emails_id[0].split()
            for email_id in emails_id:
                type,resp = self.session.uid('store', email_id, '+FLAGS', r'(\Deleted)')
            expungeResult, response = self.session.expunge() #Actual deletion of emails
            print("Mails Deleted???  ", expungeResult)

#USAGE EXAMPLE:
#gm = gmail_client(EMAIL,PASSWORD)
#email = gm.get_last_email()
#gm.delete_all_emails()
#print gm.find_text_in_body(email, "some_text")
#print gm.get_activation_link_from_email_body(email)
#print gm.get_user_email_from_email_body(email)
#print gm.get_reset_password_link_from_email_body(email)
#gm.close_session()

# gm = gmail_client(EMAIL, PASSWORD, mailbox='[Gmail]/Spam')
# gm.move_all_emails('inbox')
# gm.close_session()