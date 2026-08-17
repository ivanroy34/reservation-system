import urllib.request

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/customers/',
    'http://127.0.0.1:8000/customers/1/',
    'http://127.0.0.1:8000/table-categories/',
    'http://127.0.0.1:8000/table-categories/1/',
    'http://127.0.0.1:8000/tables/',
    'http://127.0.0.1:8000/tables/1/',
    'http://127.0.0.1:8000/reservation-statuses/',
    'http://127.0.0.1:8000/reservations/',
    'http://127.0.0.1:8000/reservations/1/',
    'http://127.0.0.1:8000/payments/',
    'http://127.0.0.1:8000/payments/1/',
    'http://127.0.0.1:8000/audit-logs/',
    'http://127.0.0.1:8000/audit-logs/1/',
]

print("Testing all system endpoints...")
all_passed = True
for url in urls:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            status = resp.getcode()
            content = resp.read().decode('utf-8')
            if status == 200 and len(content) > 0:
                print(f"[OK 200] {url} ({len(content)} bytes)")
            else:
                print(f"[FAIL] {url} - Status: {status}")
                all_passed = False
    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        all_passed = False

if all_passed:
    print("\nALL ENDPOINTS PASSED PERFECTLY WITH 200 OK STATUS!")
else:
    print("\nSOME ENDPOINTS FAILED.")
