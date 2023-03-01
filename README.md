# FireWall-Watcher
Monitors firewall for changes

This program is designed to periodically check the status of the Windows Firewall and log any changes in status to a file. It uses the PowerShell command "Get-NetFirewallProfile" to retrieve the current status of the Windows Firewall and parses the output to extract the relevant information.

At the beginning of the program, it takes a snapshot of the current status of the firewall and writes it to a file called "Firewall-snapshot.txt". Then it initializes the previous status to None.

It then enters a loop where it repeatedly checks the status of the firewall at a defined interval (5 seconds in this case) using the get_firewall_status() function. If the status has changed since the last check, it logs the changes to a file called "Firewall.txt". The program also prints the changes to the console.

The log file includes a timestamp for each change in status, along with the specific change that occurred (e.g. a rule was added or removed). The program handles keyboard interrupts (CTRL+C) gracefully, allowing the user to exit the loop and terminate the program.
