from kivy.utils import platform
import os, json, datetime
import traceback

# Global variables for debugging
LOG_DIR = None
LOG_FILE = None
INIT_SUCCESS = False
INIT_ERROR = None

print("[SIEM DEBUG] Starting initialization...")

try:
    print(f"[SIEM DEBUG] Platform detected: {platform}")
    
    if platform == "android":
        print("[SIEM DEBUG] Android platform - attempting to import android.storage...")
        try:
            from android.storage import app_storage_path
            LOG_DIR = app_storage_path()
            print(f"[SIEM DEBUG] Android storage path: {LOG_DIR}")
        except ImportError as e:
            print(f"[SIEM DEBUG] Android storage import failed: {e}")
            # Fallback for Android
            LOG_DIR = "/sdcard/sentinelit_mobile/logs"
            print(f"[SIEM DEBUG] Using fallback Android path: {LOG_DIR}")
    else:
        LOG_DIR = os.path.join(os.path.expanduser("~"), "sentinelit_mobile", "logs")
        print(f"[SIEM DEBUG] Desktop/other platform path: {LOG_DIR}")

    print(f"[SIEM DEBUG] Creating directory: {LOG_DIR}")
    os.makedirs(LOG_DIR, exist_ok=True)
    
    LOG_FILE = os.path.join(LOG_DIR, "siem_scan_log.json")
    print(f"[SIEM DEBUG] Log file will be: {LOG_FILE}")
    
    # Test if we can write to the directory
    test_file = os.path.join(LOG_DIR, "test_write.txt")
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
    print("[SIEM DEBUG] Write test successful")
    
    INIT_SUCCESS = True
    print("[SIEM DEBUG] Initialization completed successfully")

except Exception as e:
    INIT_ERROR = str(e)
    LOG_FILE = None
    print(f"[SIEM INIT ERROR]: {e}")
    print(f"[SIEM INIT ERROR] Full traceback:")
    traceback.print_exc()

def get_siem_status():
    """Return the initialization status for debugging"""
    return {
        "init_success": INIT_SUCCESS,
        "init_error": INIT_ERROR,
        "platform": platform,
        "log_dir": LOG_DIR,
        "log_file": LOG_FILE
    }

def run_siem_scan():
    """Main SIEM scan function with extensive debugging"""
    print("\n" + "="*50)
    print("[SIEM SCAN] Starting comprehensive scan...")
    print("="*50)
    
    try:
        # Check initialization status
        if not INIT_SUCCESS:
            raise Exception(f"SIEM not properly initialized: {INIT_ERROR}")
        
        print("[SIEM SCAN] Generating threat data...")
        threats = [
            {
                "id": 1,
                "type": "Suspicious Connection",
                "port": 8080,
                "severity": "medium",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "active"
            },
            {
                "id": 2,
                "type": "Root Access Attempt",
                "source": "unknown",
                "severity": "high",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "blocked"
            },
            {
                "id": 3,
                "type": "Unusual Network Traffic",
                "port": 443,
                "severity": "low",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "monitoring"
            }
        ]

        print(f"[SIEM SCAN] Generated {len(threats)} threat entries")

        # Try to log the results
        if LOG_FILE:
            print(f"[SIEM SCAN] Attempting to write to: {LOG_FILE}")
            try:
                scan_data = {
                    "scan_timestamp": datetime.datetime.now().isoformat(),
                    "scan_id": f"scan_{int(datetime.datetime.now().timestamp())}",
                    "threats_found": len(threats),
                    "threats": threats,
                    "scan_status": "completed"
                }
                
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    json.dump(scan_data, f, indent=2)
                
                print(f"[SIEM SCAN] Successfully wrote {len(json.dumps(scan_data))} bytes to log file")
                
                # Verify the file was written
                if os.path.exists(LOG_FILE):
                    file_size = os.path.getsize(LOG_FILE)
                    print(f"[SIEM SCAN] Log file confirmed, size: {file_size} bytes")
                else:
                    print("[SIEM SCAN] WARNING: Log file doesn't exist after writing!")
                    
            except Exception as write_error:
                print(f"[SIEM SCAN] File write error: {write_error}")
                traceback.print_exc()
        else:
            print("[SIEM SCAN] Warning: No log file available (LOG_FILE is None)")

        print("[SIEM SCAN] Scan completed successfully!")
        print(f"[SIEM SCAN] Returning {len(threats)} threats")
        print("="*50)
        
        return {
            "success": True,
            "threats": threats,
            "scan_timestamp": datetime.datetime.now().isoformat(),
            "threats_count": len(threats)
        }

    except Exception as e:
        error_msg = f"SIEM scan failed: {str(e)}"
        print(f"[SIEM SCAN ERROR] {error_msg}")
        print("[SIEM SCAN ERROR] Full traceback:")
        traceback.print_exc()
        
        return {
            "success": False,
            "error": error_msg,
            "threats": [],
            "scan_timestamp": datetime.datetime.now().isoformat(),
            "threats_count": 0
        }

def test_siem_complete():
    """Complete test function"""
    print("\n" + "#"*60)
    print("# SIEM COMPLETE TEST")
    print("#"*60)
    
    # Show status
    status = get_siem_status()
    print("\n[TEST] SIEM Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Run scan
    print("\n[TEST] Running scan...")
    result = run_siem_scan()
    
    print("\n[TEST] Scan Result:")
    for key, value in result.items():
        if key == "threats":
            print(f"  {key}: {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    print("\n[TEST] Test completed!")
    return result

# Auto-run test if executed directly
if __name__ == "__main__":
    test_siem_complete()
