import time
import subprocess
import os

def get_firewall_status():
    # Define the PowerShell command to get Windows Firewall status
    powershell_command = 'Get-NetFirewallProfile'

    # Run the PowerShell command and capture the output
    result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True)

    # Check the return code of the PowerShell command to see if it was successful
    if result.returncode != 0:
        print(f"Error running PowerShell command: {result.stderr.decode('utf-8').strip()}")
        return None
    else:
        # Parse the output of the PowerShell command to get the Windows Firewall status
        output = result.stdout.decode('utf-8').strip()
        status = {}
        lines = output.split('\n')
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                status[key] = value

        return status


if __name__ == "__main__":
    # Define the number of seconds between status checks
    check_interval = 5

    # Take a snapshot of the current firewall status on startup and write it to Firewall-snapshot.txt
    snapshot = get_firewall_status()
    if snapshot is not None:
        with open("Firewall-snapshot.txt", "w") as f:
            for key, value in snapshot.items():
                f.write(f"{key}: {value}\n")
                print(f"{key}: {value}")


        # Print out the initial snapshot to the console
        print(f"Initial Windows Firewall status:\n{snapshot}\n")

    # Initialize the previous status to None
    prev_status = snapshot

    try:
        with open(os.path.join(os.getcwd(), "Firewall.txt"), "a") as f:
            while True:
                # Get the current status of Windows Firewall
                status = get_firewall_status()

                # If the status has changed, print out a message
                if status is not None and status != prev_status:
                    label = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]"
                    print(label, "Windows Firewall status changed:")
                    f.write(label + " Windows Firewall status changed:\n")
                    for key, value in status.items():
                        if prev_status is None or status.get(key) != prev_status.get(key):
                            message = f"{key}: {value}"
                            print(label, message)
                            f.write(label + " " + message + "\n")
                    prev_status = status

                # Wait for the check interval before checking again
                time.sleep(check_interval)

    except KeyboardInterrupt:
        pass
