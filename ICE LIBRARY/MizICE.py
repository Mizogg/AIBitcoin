import secp256k1 as ice
import multiprocessing
import requests
import time
import random
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

console = Console()
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

filename = 'puzzle.txt'
with open(filename) as file:
    addfind = file.read().split()

def check_balance(address):
    try:
        response = session.get(f'https://btcbook.guarda.co/api/v2/address/{address}')
        if response.content:
            res = response.json()
            return res
        else:
            console.print('[red]Empty response from API[/red]')
    except json.JSONDecodeError:
        print('Error decoding JSON response from API')


def process_address(address, private_key, choice_start):
    if address in addfind:
        console.print(f'[purple]\nFOUND!! Private Key: {private_key}\tAddress: {address}\n[/purple]')
        with open('found.txt', 'a') as result:
            result.write(f'Private Key: {private_key}\tAddress: {address}\n')
    elif choice_start == '2':
        resload = check_balance(address)
        if resload:
            balance = resload['balance']
            txs = resload['txs']
            addressinfo = resload['address']
            if txs > 0:
                console.print(f'[purple]\nFOUND!! Private Key: {private_key}\tAddress: {addressinfo}\tBalance : {balance}\tTransactions : {txs}\n[/purple]')
                with open('found.txt', 'a') as result:
                    result.write(f'Private Key: {private_key}\tAddress: {addressinfo}\tBalance : {balance}\tTransactions : {txs}\n')

def generate_keys(start, end, order, choice_start, end_hex, num_cpus):
    keys_generated = 0
    total_keys_scanned = 0
    start_time = time.time()
    try:
        if num_cpus == 1:
            with Progress() as progress:
                task = progress.add_task("[cyan]Scanning...", total=(end - start))
                if order == '1':
                    for i in range(start, end):
                        private_key = i
                        address_compressed = ice.privatekey_to_address(0, True, private_key)
                        address_uncompressed = ice.privatekey_to_address(0, False, private_key)
                        if choice_start == '1':
                            process_address(address_compressed, private_key, choice_start)
                            process_address(address_uncompressed, private_key, choice_start)
                        elif choice_start == '2':
                            process_address(address_compressed, private_key, choice_start)
                            process_address(address_uncompressed, private_key, choice_start)
                        keys_generated += 1
                        total_keys_scanned += 1*num_cpus
                        if keys_generated % 1000 == 0:
                            save_progress('progress.txt', hex(private_key), end_hex)
                        if time.time() - start_time >= 1:
                            keys_per_second = keys_generated / (time.time() - start_time)
                            total_CPU_key = keys_per_second * num_cpus
                            description = f"[bold green]Keys/Sec: [/bold green]{round(keys_per_second)}[bold green] Total Keys: [/bold green]{total_keys_scanned}"
                            progress.update(task, completed=private_key - start, description=description)
                            keys_generated = 0
                            start_time = time.time()
                           
                elif order == '2':
                    while True:
                        private_key = random.randrange(start, end)
                        address_compressed = ice.privatekey_to_address(0, True, private_key)
                        address_uncompressed = ice.privatekey_to_address(0, False, private_key)
                        if choice_start == '1':
                            process_address(address_compressed, private_key, choice_start)
                            process_address(address_uncompressed, private_key, choice_start)
                        elif choice_start == '2':
                            process_address(address_compressed, private_key, choice_start)
                            process_address(address_uncompressed, private_key, choice_start)
                        keys_generated += 1
                        total_keys_scanned += 1*num_cpus
                        if time.time() - start_time >= 1:
                            keys_per_second = keys_generated / (time.time() - start_time)
                            total_CPU_key = keys_per_second * num_cpus
                            description = f"[bold green]Keys/Sec: [/bold green]{round(keys_per_second)}[bold green] Total Keys: [/bold green]{total_keys_scanned}"
                            progress.update(task, completed=private_key - start, description=description)
                            keys_generated = 0
                            start_time = time.time()

        else:
            console.print("[cyan]Scanning...")
            if order == '1':
                for i in range(start, end):
                    private_key = i
                    address_compressed = ice.privatekey_to_address(0, True, private_key)
                    address_uncompressed = ice.privatekey_to_address(0, False, private_key)
                    if choice_start == '1':
                        process_address(address_compressed, private_key, choice_start)
                        process_address(address_uncompressed, private_key, choice_start)
                    elif choice_start == '2':
                        process_address(address_compressed, private_key, choice_start)
                        process_address(address_uncompressed, private_key, choice_start)
                    keys_generated += 1
                    total_keys_scanned += 1*num_cpus
                    if keys_generated % 1000 == 0 and multiprocessing.current_process()._identity[0] == 1:
                        save_progress('progress.txt', hex(private_key), end_hex)
                    if time.time() - start_time >= 1 and multiprocessing.current_process()._identity[0] == 1:
                        keys_per_second = keys_generated / (time.time() - start_time)
                        total_CPU_key = keys_per_second * num_cpus
                        description = f"[bold green]Keys/Sec per CPU: [/bold green]{round(keys_per_second)}[bold green] Total Keys/Sec from[/bold green] {num_cpus} [bold green]CPU = [/bold green]{round(total_CPU_key)}[bold green] Total Keys: [/bold green]{total_keys_scanned}"
                        console.print(description, end='\r')
                        keys_generated = 0
                        start_time = time.time()
                           
            elif order == '2':
                while True:
                    private_key = random.randrange(start, end)
                    address_compressed = ice.privatekey_to_address(0, True, private_key)
                    address_uncompressed = ice.privatekey_to_address(0, False, private_key)
                    if choice_start == '1':
                        process_address(address_compressed, private_key, choice_start)
                        process_address(address_uncompressed, private_key, choice_start)
                    elif choice_start == '2':
                        process_address(address_compressed, private_key, choice_start)
                        process_address(address_uncompressed, private_key, choice_start)
                    keys_generated += 1
                    total_keys_scanned += 1*num_cpus
                    if time.time() - start_time >= 1 and multiprocessing.current_process()._identity[0] == 1:
                        keys_per_second = keys_generated / (time.time() - start_time)
                        total_CPU_key = keys_per_second * num_cpus
                        description = f"[bold green]Keys/Sec per CPU: [/bold green]{round(keys_per_second)}[bold green] Total Keys/Sec from[/bold green] {num_cpus} [bold green]CPU = [/bold green]{round(total_CPU_key)}[bold green] Total Keys: [/bold green]{total_keys_scanned}"
                        console.print(description, end='\r')
                        keys_generated = 0
                        start_time = time.time()
    except KeyboardInterrupt:
        console.print("[bold red]Program interrupted. Cleaning up...[/bold red]")
        if order == '1' and multiprocessing.current_process()._identity[0] == 1 and order == '1':
            save_progress('progress.txt', hex(private_key), end_hex)
        return False
    return True

def save_progress(filename, start_hex, end_hex):
    with open(filename, 'w') as file:
        file.write(f'{start_hex}\n{end_hex}')

def load_progress(filename):
    try:
        with open(filename, 'r') as file:
            start_hex = file.readline().strip()
            end_hex = file.readline().strip()
            return start_hex, end_hex
    except FileNotFoundError:
        return None, None

if __name__ == '__main__':
    mizogg= '''[red]
                      ___            ___  
                     (o o)          (o o) 
                    (  V  ) MIZOGG (  V  )
                    --m-m------------m-m--
                  © mizogg.co.uk 2018 - 2023
                    MizICE.py CryptoHunter
[/red]'''
    console.print(mizogg)
    CPU_AMOUNT = multiprocessing.cpu_count()
    num_cpus = int(Prompt.ask(f'[bold yellow]You have [/bold yellow]{CPU_AMOUNT}[bold yellow] CPUs. How many would you like to use? [/bold yellow](1-{CPU_AMOUNT})'))
    choice_start = Prompt.ask('[bold yellow]Do you want to run the scan[/bold yellow][bold green] Offline [/bold green]or [bold red]Online?[/bold red][bold yellow] ([/bold yellow][bold green]1 - Offline[/bold green] [bold red]2 - Online[/bold red][bold yellow]) [/bold yellow]')
    if choice_start == '1':
        console.print('[bold green] Starting Offline Scan[/bold green]')
        addfind = set(addfind)
    elif choice_start == '2':
        console.print('[bold red]Starting Online Scan[/bold red]')
    else:
        choice_start = '1'
        print('Invalid option selected. Using Offline Scan.')
        console.print('[bold green] Starting Offline Scan[/bold green]')
        addfind = set(addfind)

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
