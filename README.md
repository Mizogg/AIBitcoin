# AIBitcoin



![image](https://github.com/Mizogg/AIBitcoin/assets/88630056/99f4917d-26c6-4796-a863-ec69e00081d2)


Just another Bitcoin Script from Mizogg but with a little help from ChatGPT AI systems. Here is what AI thought of the finished product.

Python script that generates Bitcoin private keys and checks their corresponding addresses for balances or matches in a given list of addresses.

The script utilizes the following libraries:

   *multiprocessing: Provides support for executing tasks in parallel using multiple processes.
  *bit: A Python Bitcoin library for working with Bitcoin data structures, such as keys and addresses.
  *requests: A library for making HTTP requests.
  
Here's a breakdown of the main parts of the script:

1.Importing the required libraries.

2. Defining a function check_balance that queries the balance information of a Bitcoin address using an API.

3.Reading a list of addresses from a file named puzzle.txt.

4.Defining the main function generate_keys, which generates private keys within a given range and performs actions based on user input.

5.The generate_keys function creates instances of bit.Key using the generated private keys and derives compressed and uncompressed addresses from them.

6.If the user chooses offline mode (choice_start == '1'), the script checks if the generated addresses match any of the addresses from the puzzle.txt file. If a match is found, it is printed and appended to a file named found.txt.

7.If the user chooses online mode (choice_start == '2'), the script calls the check_balance function to retrieve balance information for the generated addresses. If the address has a non-zero balance, the information is printed, and the result is appended to found.txt.
Progress is saved after every 1000 keys in a file named progress.txt.

8.The script supports resuming from the last scan results if the progress file exists and the user chooses to resume.
The script handles interruptions, such as keyboard interrupts, and provides an option to resume or start a new scan.

9.The main program flow sets up the multiprocessing pool, divides the key generation range among the available CPUs, and starts generating keys in parallel.

To run the script, you would need to have the required dependencies installed (bit, requests) and provide a valid puzzle.txt file with the Bitcoin addresses to search for. You can customize the script's behavior by providing input when prompted, such as choosing between offline and online mode, scanning order, and resuming previous scans.

Please note that using this script for Bitcoin key generation or scanning addresses without proper authorization or legal rights may be against the terms of service of Bitcoin services and could potentially violate applicable laws and regulations. It's important to use such tools responsibly and for legitimate purposes.


![image](https://github.com/Mizogg/AIBitcoin/assets/88630056/22843c0e-6119-460f-9b5f-b08898a68e94)


Puzzle66 = 20000000000000000 3ffffffffffffffff 
