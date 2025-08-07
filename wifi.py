import subprocess

def get_wifi_profiles():
    """Fetch all Wi-Fi profiles and their passwords."""
    try:
        # Get the list of Wi-Fi profiles
        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        profiles = []
        for line in result.stdout.splitlines():
            if "All User Profile" in line:
                # Extract the profile name
                profile_name = line.split(":")[1].strip()
                profiles.append(profile_name)
        
        # Get the passwords for each profile
        wifi_data = []
        for profile in profiles:
            profile_result = subprocess.run(
                ["netsh", "wlan", "show", "profile", profile, "key=clear"],
                capture_output=True,
                text=True
            )
            password = None
            for line in profile_result.stdout.splitlines():
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
            wifi_data.append({"SSID": profile, "Password": password or "No password stored"})
        
        return wifi_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def display_wifi_profiles(profiles):
    """Display Wi-Fi profiles and their passwords."""
    print("\nSaved Wi-Fi Profiles and Passwords:")
    print("-" * 40)
    for profile in profiles:
        print(f"SSID: {profile['SSID']}")
        print(f"Password: {profile['Password']}")
        print("-" * 40)

if __name__ == "__main__":
    wifi_profiles = get_wifi_profiles()
    if wifi_profiles:
        display_wifi_profiles(wifi_profiles)
    else:
        print("No Wi-Fi profiles found or an error occurred.")
