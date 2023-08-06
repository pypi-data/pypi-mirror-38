import csv
import datetime
import os
import sys
import sqlite3

from beem.account import Account
from beem.comment import Comment
from beem.exceptions import AccountDoesNotExistsException, ContentDoesNotExistsException
from beem.nodelist import NodeList
from beem.instance import set_shared_steem_instance
from beem import Steem

options = ['Incoming Downvotes To Account', 'Outgoing Downvotes from Account']
nodes = NodeList().get_nodes()
stm = Steem(node=nodes)
set_shared_steem_instance(stm)

db = sqlite3.connect('flag.db')
cursor = db.cursor()
#uncomment on first run
#cursor.execute('''CREATE TABLE downvoters
# (user TEXT, total_rshares TEXT, total_downvotes INT)''')
 
class RangeDict(dict):
    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
        else:
            return super().__getitem__(item)

#Shining Force Rank and Image Dictionaries
rank_dict = RangeDict({
                        range(0,999999): 'F0 Yogurt < 1 Mil',
                        range(1000000,999999): 'F1 Healer',
                        range(10000000,99999999): 'F2 Monk 10 Mil',
                        range(100000000,999999999): 'F3 Swordsman 100 Mil',
                        range(1000000000,9999999999): 'F4 Knight 1 Bil',
                        range(10000000000,99999999999): 'F5 BirdMan 10 Bil',
                        range(100000000000,999999999999): 'F6  Mage 100 Bil',
                        range(1000000000000,9999999999999): 'F7 Bow Master 1 Tril',
                        range(10000000000000,99999999999999): 'F8 Hero 10 Tril',
                        range(100000000000000,999999999999999): 'F9 Wizard 100 Tril',
                        range(1000000000000000,9999999999999999): 'F10 Great Dragon 1 Quad',
                        range(10000000000000000,99999999999999999): 'F11 Wolf Baron 10 Quad',
                        range(100000000000000000,999999999999999999): 'F12 Steem Knight 100 Quad'
                    }) 
img_dict = RangeDict({
                        range(0,999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/jogurt_face.gif',
                        range(1000000,999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/lowe_heal_icon.gif',
                        range(10000000,99999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/gong_monk_icon.gif',
                        range(100000000,999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/max_sdmn_icon.gif',
                        range(1000000000,9999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/mae_knte_icon.gif',
                        range(10000000000,99999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/balbaroy_bdmn_icon.gif',
                        range(100000000000,999999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/tao_mage_icon.gif',
                        range(1000000000000,9999999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/diane_bwms_icon.gif',
                        range(10000000000000,99999999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/max_sdmn_icon.gif',
                        range(100000000000000,999999999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/tao_wizd_icon.gif',
                        range(1000000000000000,9999999999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/bleu_grdr_icon.gif',
                        range(10000000000000000,99999999999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/zylo_wfbn_icon.gif',
                        range(100000000000000000,999999999999999999): 'http://shrines.rpgclassics.com/genesis/shiningforce/images/characters/guntz_sknt_icon.gif'
                    }) 


def export_csv(name,votelist):
    cwd = os.getcwd()
    filename=datetime.datetime.now().strftime(name+"%Y%m%d-%H%M%S.csv")
    keys = votelist[0].keys()
    outfile=open(cwd+'/'+filename,'w')
    writer=csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(votelist)

def option_select(options):
    'https://stackoverflow.com/questions/34927479/command-line-show-list-of-options-and-let-user-choose'
    print("Please choose:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)
    except:
        pass
    return 

def get_rank(vote_list):
    total = 0
    flags_total = 0
    players = []
    rank = []
    for i in vote_list:
        total += int(i['rshares'])
        players.append(i['Downvoter'])
    players = set(players)
    for p in players:
        player_rshares = 0
        for i in vote_list:
            if i['Downvoter'] == p:
                flags_total += 1
                player_rshares += int(i['rshares'])
        downvote_sbd_amount = round(stm.rshares_to_sbd(player_rshares),3)
        rank.append({
                        'Downvoter': p,
                        'Total Flags': flags_total,
                        'SBD amount': str(downvote_sbd_amount),
                        'rshares': total,
                        'Rank': rank_dict[abs(player_rshares)],
                        'Image': img_dict[abs(player_rshares)]
                    })
    export_csv('ranklist',rank)
    return rank

class DownvoteReport:
    'Common base class for all reports'

    def __init__(self, account=None, stop_date=None, start_date=None, vote_list=None):
       self.account = account
       self.stop_date = stop_date
       self.start_date = start_date
       self.vote_list = vote_list
                                        
    def incoming_to_account(self):
        nodes = NodeList().get_nodes()
        stm = Steem(node=nodes)
        set_shared_steem_instance(stm)
        #list to store dictionary variables
        self.vote_list = []
        account=(self.account or input("Downvoted User Account? "))
        try:
            downvoted_account = Account(account)
        except AccountDoesNotExistsException:
            print('The specified account does not exist on the Steem blockchain.')
            sys.exit(1)
        #prompts to be used for datetime variable in format.
        if(self.stop_date==None):
            #input option to enable input of self.start_date
            stop_option = input("Would you like to specify stop date? y/n ")
            if(stop_option == 'y'):
                self.stop_date = self.prompt_start_stop_time()
            else:
                self.stop_date = None
        if(self.start_date==None):
            #input option to enable input of self.start_date
            start_option = input("Would you like to specify start date? y/n ")
            #start date prompts
            if(start_option == 'y'):
                self.start_date = self.prompt_start_stop_time()
            else:
                self.start_date= None
        try:
            if type(self.start_date) is not datetime.datetime and self.start_date != None:
                raise TypeError("Improper start_date format!")
        except TypeError as e:
            print(e)
            sys.exit(1)
        try:
            if type(self.stop_date) is not datetime.datetime and self.stop_date != None:
                raise TypeError("Improper stop_date format!")
        except TypeError as e:
            print(e)
            sys.exit(1)
        #estimated number of operations between stop and start to assess if limit is breached
        start_v_ops = downvoted_account.estimate_virtual_op_num(self.start_date or datetime.datetime.utcnow())
        stop_v_ops = downvoted_account.estimate_virtual_op_num(self.stop_date or datetime.datetime(1969,12,31,23,59,59))
        start_stop_op_dif = start_v_ops - stop_v_ops
        if(start_stop_op_dif > 10000):
            print("Operations Scope exceeds Get_Account_History limit. Splitting into multiple calls with index.")
            hist_index = 10000
            while hist_index <= start_stop_op_dif:
                for vote in (downvoted_account.get_account_history(hist_index,10000,start=self.start_date,stop=self.stop_date,only_ops=['vote'])):
                    if vote['voter'] != downvoted_account.name and vote['weight'] < 0:
                        downvoter = Account(vote['voter'])
                        try:
                            downvote = downvoter.get_vote(downvoted_account.name+'/'+vote['permlink'])
                            downvoted_post = Comment(downvoted_account.name+'/'+vote['permlink'])
                        except ContentDoesNotExistsException:
                            print(vote['permlink']+"Does Not Exist! Skipping.")
                            continue
                        pending_payout_value = downvoted_post['pending_payout_value']
                        downvote_sbd_amount = round(stm.rshares_to_sbd(downvote['rshares']),3)
                        link = '[Comment](https://steemit.com/@'+downvoted_post.identifier+')'
                        report_dict = {
                                           'Downvoter': '@'+vote['voter'],
                                           'Comment': link,
                                           'SBD amount': str(downvote_sbd_amount),
                                           'rshares': downvote['rshares'],
                                           'Remaining Rewards': str(pending_payout_value),
                                           'Timestamp': vote['timestamp'],
                                           'ID': vote['_id']}
                        self.vote_list.append(report_dict)
                hist_index += 10000
        else:
            for vote in (downvoted_account.get_account_history(-1,10000,start=self.start_date,stop=self.stop_date,only_ops=['vote'])):
                if vote['voter'] != downvoted_account.name and vote['weight'] < 0:
                    downvoter = Account(vote['voter'])
                    try:
                        downvote = downvoter.get_vote(downvoted_account.name+'/'+vote['permlink'])
                        downvoted_post = Comment(downvoted_account.name+'/'+vote['permlink'])
                    except ContentDoesNotExistsException:
                        print(vote['permlink']+"Does Not Exist! Skipping.")
                        continue
                    pending_payout_value = downvoted_post['pending_payout_value']
                    downvote_sbd_amount = round(stm.rshares_to_sbd(downvote['rshares']),3)
                    link = '[Comment](https://steemit.com/@'+downvoted_post.identifier+')'
                    report_dict = {
                                       'Downvoter': '@'+vote['voter'],
                                       'Comment': link,
                                       'SBD amount': str(downvote_sbd_amount),
                                       'rshares': downvote['rshares'],
                                       'Remaining Rewards': str(pending_payout_value),
                                       'Timestamp': vote['timestamp'],
                                       'ID': vote['_id']
                                  }
                    self.vote_list.append(report_dict)
        #remove duplicates
        self.vote_list = [dict(t) for t in {tuple(d.items()) for d in self.vote_list}]
        export_csv('incoming_downvote_report',self.vote_list)
        return self.vote_list

    def outgoing_from_account(self):
        nodes = NodeList().get_nodes()
        stm = Steem(node=nodes)
        set_shared_steem_instance(stm)
        #list to store dictionary variables
        self.vote_list = []
        account=(self.account or input("Downvoter User Account? "))
        try:
            downvoter_account = Account(account)
        except AccountDoesNotExistsException:
            print('The specified account does not exist on the Steem blockchain.')
            sys.exit(1)
        #prompts to be used for datetime variable in format.
        if(self.stop_date==None):
            #input option to enable input of self.start_date
            stop_option = input("Would you like to specify stop date? y/n ")
            if(stop_option == 'y'):
                self.stop_date = self.prompt_start_stop_time()
            else:
                self.stop_date = None
        if(self.start_date==None):
            #input option to enable input of self.start_date
            start_option = input("Would you like to specify start date? y/n ")
            #start date prompts
            if(start_option == 'y'):
                self.start_date = self.prompt_start_stop_time()
            else:
                self.start_date= None
        try:
            if type(self.start_date) is not datetime.datetime and self.start_date !=None:
                raise TypeError("Improper start_date format!")
        except TypeError as e:
            print(e)
            sys.exit(1)
        try:
            if type(self.stop_date) is not datetime.datetime and self.stop_date != None:
                raise TypeError("Improper stop_date format!")
        except TypeError as e:
            print(e)
            sys.exit(1)
        #estimated number of operations between stop and start to assess if limit is breached
        start_v_ops = downvoter_account.estimate_virtual_op_num(self.start_date or datetime.datetime.utcnow())
        stop_v_ops = downvoter_account.estimate_virtual_op_num(self.stop_date or datetime.datetime(1969,12,31,23,59,59))
        start_stop_op_dif = start_v_ops - stop_v_ops
        if(start_stop_op_dif > 10000):
            print("Operations Scope exceeds Get_Account_History limit. Splitting into multiple calls with index.")
            hist_index = 10000
            while hist_index <= start_stop_op_dif:
                for vote in (downvoter_account.get_account_history(hist_index,10000,start=self.start_date,stop=self.stop_date,only_ops=['vote'])):
                    if vote['voter'] == downvoter_account.name and vote['weight'] < 0:
                        try:
                            downvote = downvoter_account.get_vote(vote['author']+'/'+vote['permlink'])
                            downvoted_post = Comment(vote['author']+'/'+vote['permlink'])
                        except ContentDoesNotExistsException:
                            print(vote['permlink']+"Does Not Exist! Skipping.")
                            continue
                        pending_payout_value = downvoted_post['pending_payout_value']
                        downvote_sbd_amount = round(stm.rshares_to_sbd(downvote['rshares']),3)
                        link = '[Comment](https://steemit.com/@'+downvoted_post.identifier+')'
                        report_dict = {
                                          'Downvoter': '@'+vote['voter'],
                                          'Comment': link,
                                          'SBD amount': str(downvote_sbd_amount),
                                          'rshares': downvote['rshares'],
                                          'Remaining Rewards': str(pending_payout_value),
                                          'Timestamp': vote['timestamp'],
                                          'ID': vote['_id']
                                          }
                        self.vote_list.append(report_dict)
                hist_index += 1000
        else:
            for vote in (downvoter_account.get_account_history(-1,10000,start=self.start_date,stop=self.stop_date,only_ops=['vote'])):
                if vote['voter'] == downvoter_account.name and vote['weight'] < 0:
                    try:
                        downvote = downvoter_account.get_vote(vote['author']+'/'+vote['permlink'])
                        downvoted_post = Comment(vote['author']+'/'+vote['permlink'])
                    except ContentDoesNotExistsException:
                        print(vote['permlink']+"Does Not Exist! Skipping.")
                        continue
                    pending_payout_value = downvoted_post['pending_payout_value']
                    downvote_sbd_amount = round(stm.rshares_to_sbd(downvote['rshares']),3)
                    link = '[Comment](https://steemit.com/@'+downvoted_post.identifier+')'
                    report_dict = {
                                    'Downvoter': '@'+vote['voter'],
                                    'Comment': link, 
                                    'SBD amount': str(downvote_sbd_amount),
                                    'rshares': downvote['rshares'],
                                    'Remaining Rewards': str(pending_payout_value),
                                    'Timestamp': vote['timestamp'],
                                    'ID': vote['_id']
                                  }
                    self.vote_list.append(report_dict)
        #remove duplicates
        self.vote_list = [dict(t) for t in {tuple(d.items()) for d in self.vote_list}]
        export_csv('outgoing_downvote_report',self.vote_list)
        return self.vote_list      

    def prompt_start_stop_time(self):
        year = int(input("Until Year Value? "))
        month = int(input("Until Month Value? "))
        day = int(input("Until Day Value? "))
        s_date = datetime.datetime(int(year), int(month), int(day),0,0,0)
        return s_date

def main():
    user_option = option_select(options)
    if(user_option == 1):
        dreport = DownvoteReport()
        report = dreport.incoming_to_account()
    elif(user_option == 2):
        dreport = DownvoteReport()
        report = dreport.outgoing_from_account()
    else:
        print("Invalid Option Selected")
        sys.exit(1)
    get_rank(report)

if __name__== "__main__":
    main()