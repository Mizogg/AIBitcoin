import secp256k1 as ice
import multiprocessing
import requests
import time
import random
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from bloomfilter import BloomFilter
console = Console()
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

import os, sys, platform
is_windows = True if platform.system() == "Windows" else False

if is_windows:
    os.system("title Mizogg @ github.com/Mizogg")

def red(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 250
        for character in line:
            green -= 5
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded


def win_colour(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 20
        for character in line:
            green += 3
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded
    
def blue(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 0
        for character in line:
            green += 3
            if green > 255:
                green = 255
            faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        faded += "\n"
    return faded

def water(text):
    os.system(""); faded = ""
    green = 10
    for line in text.splitlines():
        faded += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded

def purple(text):
    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
    return faded
    
try:
    with open('btc.bf', "rb") as fp:
        addfind = BloomFilter.load(fp)
except FileNotFoundError:
    filename = 'btc.txt'
    with open(filename) as file:
        addfind = file.read().split()

def check_balance(address):
    try:
        response = session.get(f'https://btcbook.guarda.co/api/v2/address/{address}')
        if response.content:
            res = response.json()
            return res
        else:
            print(red('Empty response from API'), end="")
    except json.JSONDecodeError:
        print(red('Error decoding JSON response from API'), end="")

def convert_int(num: int): 
    dict_suffix = {0: 'key', 1: 'Kkey/s', 2: 'Mkey/s', 3: 'Gkey/s', 4: 'Tkey/s', 5: 'Pkey/s', 6: 'Ekeys/s'} 
    num *= 1.0 
    idx = 0 
    for ii in range(len(dict_suffix) - 1): 
        if int(num / 1000) > 0: 
            idx += 1 
            num /= 1000 
        else: 
            break 
    return f"{num:.2f}", dict_suffix[idx]
    
def process_address(address, private_key, choice_start):
    if choice_start == '1':
        if address in addfind:
            print(win_colour(f'\nFOUND!! Private Key: {hex(private_key)}\tAddress: {address}\n') + "")
            with open('found.txt', 'a') as result:
                result.write(f'Private Key: {hex(private_key)}\tAddress: {address}\n')
    elif choice_start == '2':
        resload = check_balance(address)
        if resload:
            balance = resload['balance']
            txs = resload['txs']
            addressinfo = resload['address']
            if txs > 0:
                print(purple(f'\nFOUND!! Private Key: {hex(private_key)}\tAddress: {addressinfo}\tBalance : {balance}\tTransactions : {txs}\n') + "\033[38;2;148;0;230m")
                with open('found.txt', 'a') as result:
                    result.write(f'Private Key: {hex(private_key)}\tAddress: {addressinfo}\tBalance : {balance}\tTransactions : {txs}\n')

def generate_keys(cpu_start, cpu_end, order, choice_start, end_hex, num_cpus):
    keys_generated = 0
    total_keys_scanned = 0
    total_keys_scanned1 = 0
    start_time = time.time()
    group_size = 1000000
    try:
        if num_cpus == 1:
            with Progress() as progress:
                task = progress.add_task("[cyan]Scanning...", total=(cpu_end - cpu_start))
                if order == '1':
                    private_key = cpu_start
                    P = ice.scalar_multiplication(private_key)
                    current_pvk = private_key + 1
                    for i in range(cpu_start, cpu_end, group_size):
                        Pv = ice.point_sequential_increment(group_size, P)
                        for t in range(group_size):
                            this_btc = ice.pubkey_to_address(0, True, Pv[t*65:t*65+65])
                            process_address(this_btc, current_pvk+t, choice_start)
                            keys_generated += 1
                            total_keys_scanned += 1
                            if keys_generated % group_size == 0:
                                save_progress('progress.txt',  current_pvk+t, end_hex)
                            if time.time() - start_time >= 1:
                                elapsed_time = time.time() - start_time
                                speed = keys_generated / elapsed_time if elapsed_time > 0 else 0
                                formatted_speed = convert_int(speed)
                                description = print(red(f" {formatted_speed}  Total Keys: {total_keys_scanned}"), end="")
                                progress.update(task, completed=current_pvk+t - cpu_start, description=description)
                                keys_generated = 0
                                start_time = time.time()
                        P = Pv[-65:]
                        current_pvk += group_size

                elif order == '2':
                    while True:
                        private_key = random.randrange(cpu_start, cpu_end, group_size)
                        P = ice.scalar_multiplication(private_key)
                        current_pvk = private_key + 1
                        Pv = ice.point_sequential_increment(group_size, P)
                        for t in range(group_size):
                            this_btc = ice.pubkey_to_address(0, True, Pv[t*65:t*65+65])
                            process_address(this_btc, current_pvk+t, choice_start)
                            keys_generated += 1
                            total_keys_scanned += 1
                            if time.time() - start_time >= 1:
                                elapsed_time = time.time() - start_time
                                speed = keys_generated / elapsed_time if elapsed_time > 0 else 0
                                formatted_speed = convert_int(speed)
                                description = print(red(f"{formatted_speed}  Total Keys: {total_keys_scanned}"), end="")
                                progress.update(task, completed=current_pvk+t - cpu_start, description=description)
                                keys_generated = 0
                                start_time = time.time()
                        P = Pv[-65:]
                        current_pvk += group_size

        else:
            print(water("Scanning..."), end="")
            if order == '1':
                private_key = cpu_start
                P = ice.scalar_multiplication(private_key)
                current_pvk = private_key + 1
                for i in range(cpu_start, cpu_end, group_size):
                    Pv = ice.point_sequential_increment(group_size, P)
                    for t in range(group_size):
                        this_btc = ice.pubkey_to_address(0, True, Pv[t*65:t*65+65])
                        process_address(this_btc, current_pvk+t, choice_start)
                        keys_generated += 1
                        total_keys_scanned += keys_generated*num_cpus
                        total_keys_scanned1 += keys_generated*num_cpus
                        if keys_generated % group_size == 0 and multiprocessing.current_process()._identity[0] == 1:
                            save_progress('progress.txt', current_pvk+t, end_hex)
                        if time.time() - start_time >= 1 and multiprocessing.current_process()._identity[0] == 1:
                            elapsed_time = time.time() - start_time
                            speed = keys_generated / elapsed_time if elapsed_time > 0 else 0
                            formatted_speed = convert_int(speed)
                            speed1 = total_keys_scanned / elapsed_time if elapsed_time > 0 else 0
                            formatted_speed1 = convert_int(speed1)
                            description = f"{formatted_speed} Total Keys/Sec from {num_cpus}  CPU = {formatted_speed1} Total Keys: {total_keys_scanned1}"
                            print(red(description), end="")
                            keys_generated = 0
                            total_keys_scanned = 0
                            start_time = time.time()
                    P = Pv[-65:]
                    current_pvk += group_size

            elif order == '2':
                while True:
                    private_key = random.randrange(cpu_start, cpu_end)
                    P = ice.scalar_multiplication(private_key)
                    current_pvk = private_key + 1
                    for i in range(cpu_start, cpu_end, group_size):
                        Pv = ice.point_sequential_increment(group_size, P)
                        for t in range(group_size):
                            this_btc = ice.pubkey_to_address(0, True, Pv[t*65:t*65+65])
                            process_address(this_btc, current_pvk+t, choice_start)
                            keys_generated += 1
                            total_keys_scanned += keys_generated*num_cpus
                            total_keys_scanned1 += keys_generated*num_cpus
                            if time.time() - start_time >= 1 and multiprocessing.current_process()._identity[0] == 1:
                                elapsed_time = time.time() - start_time
                                speed = keys_generated / elapsed_time if elapsed_time > 0 else 0
                                formatted_speed = convert_int(speed)
                                speed1 = total_keys_scanned / elapsed_time if elapsed_time > 0 else 0
                                formatted_speed1 = convert_int(speed1)
                                description = f"{formatted_speed} Total Keys/Sec from {num_cpus}  CPU = {formatted_speed1} Total Keys: {total_keys_scanned1}"
                                print(red(description), end="")
                                keys_generated = 0
                                total_keys_scanned = 0
                                start_time = time.time()

                        P = Pv[-65:]
                        current_pvk += group_size
    except KeyboardInterrupt:
        print(purple("Program interrupted. Cleaning up...")+ "\033[38;2;148;0;230m")
        if order == '1' and multiprocessing.current_process()._identity[0] == 1 and order == '1':
            save_progress('progress.txt', current_pvk+t, end_hex)
        return False
    return True

def save_progress(filename, start_hex, end_hex):
    with open(filename, 'w') as file:
        file.write(f'{hex(start_hex)}\n{end_hex}')

def load_progress(filename):
    try:
        with open(filename, 'r') as file:
            start_hex = file.readline().strip()
            end_hex = file.readline().strip()
            return start_hex, end_hex
    except FileNotFoundError:
        return None, None

if __name__ == '__main__':
    mizogg= f'''
                      ___            ___
                     (o o)          (o o)
                    (  V  ) MIZOGG (  V  )
                    --m-m------------m-m--
                  © mizogg.co.uk 2018 - 2023
                   MizICE.py CryptoHunter

                     VIP PROJECT Mizogg
                 
                {red(f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")}


'''
    print(water(mizogg), end="")
    CPU_AMOUNT = multiprocessing.cpu_count()
    num_cpus = int(Prompt.ask(f'[bold yellow]You have [/bold yellow]{CPU_AMOUNT}[bold yellow] CPUs. How many would you like to use? [/bold yellow](1-{CPU_AMOUNT})'))
    choice_start = Prompt.ask('[bold yellow]Do you want to run the scan[/bold yellow] Offline or Online?[bold yellow] ([/bold yellow]1 - Offline 2 - Online[bold yellow]) [/bold yellow]')

    start_hex, end_hex = load_progress('progress.txt')
    if start_hex and end_hex:
        choice = Prompt.ask('[bold cyan]Do you want to resume from the last scan results? [/bold cyan] (Y/N) ').lower()
        resume = choice == 'y'
    else:
        resume = False

    if not resume:
        start_hex = Prompt.ask("[bold cyan]Enter the starting hex value [/bold cyan](Example: 66 for 20000000000000000): ")
        end_hex = Prompt.ask("[bold cyan]Enter the ending hex value [/bold cyan](Example: 66 for 3ffffffffffffffff): ")
    order = Prompt.ask("[bold cyan]Enter the scanning order ([/bold cyan] 1 - Sequential, 2 - Random): ")
    start = int(start_hex, 16)
    end = int(end_hex, 16)
    chunk_size = (end - start) // num_cpus
    console.print("[bold yellow]===== Scanning Configuration =====[/bold yellow]")
    console.print(f"[bold yellow]Start Hex:[/bold yellow] {start_hex}")
    console.print(f"[bold yellow]End Hex:[/bold yellow] {end_hex}")
    console.print(f"[bold yellow]Scan Order:[/bold yellow] {'Sequential' if order == '1' else 'Random'}")
    console.print(f"[bold yellow]Number of CPUs:[/bold yellow] {num_cpus}")
    console.print("[bold yellow]=================================[/bold yellow]")

    if order == '1':
        ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size) for i in range(num_cpus)]
    elif order == '2':
        range_list = [(start + i * chunk_size, start + (i + 1) * chunk_size) for i in range(num_cpus)]
        random.shuffle(range_list)
        ranges = range_list
    else:
        print('Invalid order selected. Using sequential order.')
        ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size) for i in range(num_cpus)]

    if resume:
        start_index = int(start_hex, 16)
        if start_index < int(start_hex, 16):
            print(f'Resuming from {hex(start_index)}...')
        else:
            print('Resuming from the last scan results...')
    else:
        start_index = start

    for i in range(num_cpus - 1, -1, -1):
        cpu_start = ranges[i][0]
        cpu_end = ranges[i][1]
        if start_index >= cpu_start and start_index < cpu_end:
            console.print(f'[bold yellow]CPU {i + 1}:\t{hex(cpu_start)} - {hex(cpu_end)}\t<<-- Current CPU[/bold yellow]')
        else:
            console.print(f'[bold yellow]CPU {i + 1}:\t{hex(cpu_start)} - {hex(cpu_end)}[/bold yellow]')
    Prompt.ask('[green]Press Enter to continue...[/green]')
    console.print('[green]\nStarting key generation...\n[/green]')
    processes = []
    for i in range(num_cpus):
        cpu_start = ranges[i][0]
        cpu_end = ranges[i][1]
        p = multiprocessing.Process(target=generate_keys, args=(cpu_start, cpu_end, order, choice_start, end_hex, num_cpus))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
