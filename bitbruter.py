#!/usr/bin/python3

import hashlib
import random
import os
import binascii
import ecdsa
import base58
import datetime
import PySimpleGUI as sg




sg.ChangeLookAndFeel('Black')
layout =  [
            [sg.Text('Bitcoin bruteforcer - Bitbruter', size=(30,1), font=('Comic sans ms', 13), text_color='red')],
            [sg.Text('This program has been running for... ', size=(30,1), font=('Comic sans ms', 10)),sg.Text('', size=(30,1), font=('Comic sans ms', 10), key='_DATE_')],
            [sg.Image('sco.png', size=(225, 225))],
            [sg.Text('Address: ', size=(12,1), font=('Comic sans ms', 10)), sg.Text('', size=(80,1), font=('Comic sans ms', 10),  key='address')],
            [sg.Text('Privatekey: ', size=(12,1), font=('Comic sans ms', 10)), sg.Text('', size=(90,1), font=('Comic sans ms', 10), key= 'privatekey')],
            [sg.Text('WIF: ', size=(12,1), font=('Comic sans ms', 10)), sg.Text('', size=(80,1), font=('Comic sans ms', 10), key= 'wif')],
            [sg.Text('Address \nwith balance: ',size=(12,2), font=('Comic sans ms', 10)), sg.Text('',size=(8,1), font=('Comic sans ms', 10), key='found')],
            [sg.Button('Exit', button_color=('white', 'red'), font=('Comic sans ms', 10) )]
          ]

window = sg.Window('Bitbruter',
                  layout=layout,
                   default_element_size=(9,1),
                   font='Helvetica 18',
                   )

start_time = datetime.datetime.now()

def secret():
    return binascii.hexlify(os.urandom(32)).decode('utf-8').upper()

def pubkey(secret_exponent):
    privatekey = binascii.unhexlify(secret_exponent)
    s = ecdsa.SigningKey.from_string(privatekey, curve = ecdsa.SECP256k1)
    return '04' + binascii.hexlify(s.verifying_key.to_string()).decode('utf-8')

def addr(public_key):
    output = []; alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    var = '00' + var.hexdigest() + hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()[0:8]
    count = [char != '0' for char in var].index(True) // 2
    n = int(var, 16)
    while n > 0:
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    for i in range(count): output.append(alphabet[0])
    return ''.join(output[::-1])

def wif(secret_exponent):
    var80 = "80"+secret_exponent
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')

def database(address):
    with open("data-base", "r") as m:
        add = m.read().split()
        for ad in add:
            continue
        if address in add:
            data = open("Win.txt","a")
            data.write("Bingo " + str(sect)+"\n" +str(address)+"\n"+str(WIF)+"\n"+"\n")
            data.close()
            return 'Bingo'
        else:
            i = 'No luck'
            return i


def main():
    while True:
        secret_exponent = secret()
        public_key = pubkey(secret_exponent)
        address = addr(public_key)
        WIF = wif(secret_exponent)
        data_base = database(address)
        event, values = window.Read(timeout=10)
        if event in (None, 'Exit'):
            break
        window.Element('_DATE_').Update(str(datetime.datetime.now()-start_time))
        window.Element('address').Update(str(address))
        window.Element('privatekey').Update(str(secret_exponent))
        window.Element('wif').Update(str(WIF))
        window.Element('found').Update(str(data_base))
    
    window.Close()
    
main()

