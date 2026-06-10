"""

phan tich va thiet ke giai phap: loi tham chieu bo nho va cap nhat don thuoc


MO TAI BAI TOAN:
He thong hien tai bi loi khi cap nhat don thuoc cho mot benh nhan.
Khi thay doi don thuoc cua benh nhan A, don thuoc cua benh nhan B (co cung don cuoi cung)
cung bi thay doi theo.
Nguyen nhan: Su dung gan nhan (assignment) thay vi tao ban sao (shallow copy) khi 
luu don thuoc vao danh sach benh nhan.

1. NGUYEN NEN LOI (ROOT CAUSE)

 Trong Python, khi thuc hien:
    new_list  old_list
  > new_list va old_list truong cung mot dia chi bo nho (cung mot doi tuong).
   Neu su dung new_list.append(...) hoac sua phan tu, old_list cung bi thay doi.
 Trong bai nay:
     Don thuoc la mot list (vi du: ['Aspirin', 'Paracetamol']).
     Khi gan don thuoc vao benh nhan: patient['don_thuoc']  don_thuoc
     Neu don_thuoc duoc tao chung cho nhieu benh nhan hoac gan truc tiep,
      thay doi benh nhan A se lam thay doi benh nhan B.

2. CHIEN LUOC SUA LOI (SOLUTION STRATEGY)

 Tao ban sao (Copy) moi khi gan don thuoc vao benh nhan:
   Su dung slicing: new_list  old_list[:]
   Hoac ham builtin: new_list  list(old_list)
   Hoac phuong thuc: new_list  old_list.copy()
 Van dung:
   Khi nhap don thuoc moi, tao list moi.
   Khi gan vao benh nhan, tao ban sao cua list do.
   Khi cap nhat don thuoc, thao tac tren ban sao, khong tac dong len list goc.

3. PHAN TICH INPUT/OUTPUT (FUNCTION SPECIFICATION)


A. HAM HELPER: create_medication_list(meds_input: str) > list
    Input: Chuoi thuoc (vi du: 'Aspirin,Paracetamol').
    Logic:
     1. Tach chuoi theo dau phay: .split(',')
     2. Loai bo khoang trang cho moi thuoc: [m.strip() for m in list]
     3. Tra ve list moi da tao.
    Output: List chuoi thuoc.

B. HAM HELPER: copy_medication_list(original_list: list) > list
    Input: List thuoc goc.
    Logic:
     1. Tao ban sao moi bang slicing [:] hoac .copy().
     2. Tra ve list moi.
    Output: List moi (khong cung dia chi voi list goc).

C. CHUC NANG: add_patient_with_meds(patient_list, patient_id, name, meds_str) > None
    Input: Danh sach benh nhan, Ma, Ten, Chuoi thuoc.
    Logic:
     1. Tao list thuoc tu chuoi.
     2. Tao ban sao cua list thuoc (de phong loi tham chieu khi nhap sau).
     3. Tao benh nhan moi: [id, name, copy_of_meds].
     4. Them vao danh sach.
    Output: None.

D. CHUC NANG: update_medication(patient_list, patient_id, new_meds_str) > None
    Input: Danh sach, Ma benh nhan, Chuoi thuoc moi.
    Logic:
     1. Tim benh nhan.
     2. Tao list thuoc moi tu chuoi.
     3. Tao ban sao cua list moi.
     4. Gan vao benh nhan: patient  copy_of_new_meds.
     5. In ra thong bao.
    Output: None.

E. CHUC NANG: check_medication(patient_list, patient_id) > None
    Input: Danh sach, Ma benh nhan.
    Logic:
     1. Tim benh nhan.
     2. In ra don thuoc hien tai.
     3. In dia chi bo nho (id()) de minh hoa su khac biet.
    Output: None.

4. MINH HOA LOI (DEMO THE BUG)

 Truong hop loi:
  patient_list  []
  base_meds  ['Thuoc A']
  # Loi: Gan truc tiep, khong copy
  patient1  ['P1', 'A', base_meds]
  patient2  ['P2', 'B', base_meds] 
  
  # Cap nhat patient1
  patient1.append('Thuoc B') 
  
  # Ket qua sai: patient2 cung co 'Thuoc B' vi cung list.

 Truong hop dung:
  patient1  ['P1', 'A', base_meds.copy()]
  patient2  ['P2', 'B', base_meds.copy()]
  
  # Cap nhat patient1
  patient1.append('Thuoc B')
  
  # Ket qua dung: patient2 khong co 'Thuoc B'.


"""

# Hệ thống lưu trữ tập trung
emergency_registry = {}

def admit_patient(p_id, name):
    """Thêm bệnh nhân mới vào hệ thống."""
    if p_id in emergency_registry:
        print(f"Lỗi: ID {p_id} đã tồn tại.")
        return
    
    # Khởi tạo dict mới cho mỗi bệnh nhân
    emergency_registry[p_id] = {
        'name': name,
        'heart_rate': 0,
        'spo2': 0,
        'meds': [] # Danh sách thuốc rỗng
    }
    print(f"Đã nhập viện: {name} (ID: {p_id})")

def update_vitals(p_id, heart_rate, spo2):
    """Cập nhật sinh hiệu."""
    if p_id in emergency_registry:
        emergency_registry[p_id]['heart_rate'] = heart_rate
        emergency_registry[p_id]['spo2'] = spo2
        print(f"Đã cập nhật sinh hiệu cho {emergency_registry[p_id]['name']}")
        
        # Kiểm tra ngưỡng cảnh báo
        if spo2 < 90:
            print(f"!!! CẢNH BÁO: Bệnh nhân {emergency_registry[p_id]['name']} SpO2 thấp ({spo2}%) !!!")
    else:
        print("Không tìm thấy bệnh nhân.")

def update_medication(p_id, new_meds_list):
    """Cập nhật danh sách thuốc bằng cách sao chép thủ công."""
    if p_id in emergency_registry:
        # Sử dụng [:] để tạo bản sao mới của list, tránh tham chiếu bộ nhớ
        emergency_registry[p_id]['meds'] = new_meds_list[:]
        print(f"Đã cập nhật đơn thuốc cho {emergency_registry[p_id]['name']}")

def display_dashboard():
    """Hiển thị bảng điều khiển."""
    print("\n--- BẢNG ĐIỀU KHIỂN CẤP CỨU ---")
    for p_id, info in emergency_registry.items():
        print(f"ID: {p_id} | Tên: {info['name']} | SpO2: {info['spo2']}% | Thuốc: {info['meds']}")

# --- CHẠY CHƯƠNG TRÌNH ---
def main():
    admit_patient("P001", "Nguyen Van A")
    admit_patient("P002", "Tran Thi B")
    
    # Cập nhật cho P001
    update_medication("P001", ["Aspirin", "Paracetamol"])
    update_vitals("P001", 80, 85) # Kích hoạt cảnh báo
    
    # Cập nhật cho P002
    update_medication("P002", ["Amoxicillin"])
    
    display_dashboard()

if __name__ == "__main__":
    main()