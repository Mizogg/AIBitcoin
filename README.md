# AIBitcoin

AIBitcoin
GUI PyQT5 Version Coming SOON! But CMD Version already here down below the discription.

This is a Bitcoin key generation and scanning application built using PyQt5 and secp256k1 libraries.

Features
---------
Utilizes multiprocessing for faster key generation and scanning
Supports sequential and random order scanning
Displays the current key being checked in hexadecimal format
Shows the corresponding Bitcoin address for the checked key
Detects and saves found private keys and their associated addresses
Provides information on the total keys scanned and keys per second

![image](https://github.com/Mizogg/AIBitcoin/assets/88630056/cdb08042-d616-40d1-adbb-aceda0c5fd15)

Screenshot 1
Description: The application's main interface, allowing users to start and stop the scanning process.

![image](https://github.com/Mizogg/AIBitcoin/assets/88630056/3100e111-f76a-4aa8-a514-c08b4d2f2e62)

Screenshot 2
Description: An example of a found private key and its corresponding Bitcoin address.

Installation
Clone the repository:
---------

```
git clone https://github.com/Mizogg/AIBitcoin.git
```
Install the required dependencies:
---------

```
pip install PyQt5 bloomfilter
```
---------
## Usage
Choose the scanning order (sequential or random) and the number of CPUs to utilize.
Specify the start and end hexadecimal values for the puzzle 66.
Click the "Start" button to begin the scanning process.
As the application scans keys, it will display the current key being checked, the corresponding Bitcoin address, and the total keys scanned.
If a private key matches one of the Bitcoin addresses in the puzzle.txt file, it will be saved in the found.txt file.

https://github.com/Mizogg/AIBitcoin/assets/88630056/52b521c8-d7ad-49d7-8360-ee7901c6a559

---------
## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

![image](https://github.com/Mizogg/AIBitcoin/assets/88630056/b520d696-494f-4cad-b7dd-488bc14a13ae)

## AIBitcoin

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

## Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them.
Push your changes to your forked repository.
Open a pull request, describing your changes in detail.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Disclaimer
Please note that using this script for Bitcoin key generation or scanning addresses without proper authorization or legal rights may be against the terms of service of Bitcoin services and could potentially violate applicable laws and regulations. Use this tool responsibly and for legitimate purposes.



![image](https://github.com/Mizogg/AIBitcoin/assets/88630056/22843c0e-6119-460f-9b5f-b08898a68e94)

```
Puzzle66 = 20000000000000000 3ffffffffffffffff 
```
