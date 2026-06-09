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

def create_medication_list(meds_input):
    """
    Tao list thuoc tu chuoi nhap vao.
    - Tach theo dau phay.
    - Xoa khoang trang thua.
    """
    if not meds_input:
        return []
    # Tach chuoi
    raw_meds = meds_input.split(',')
    # Xoa khoang trang thua cho tung thuoc
    clean_meds = [m.strip() for m in raw_meds if m.strip()]
    return clean_meds

def copy_medication_list(original_list):
    """
    Tao ban sao moi cua list thuoc.
    - Su dung slicing [:] de tao shallow copy.
    """
    return original_list[:]

def add_patient(patient_list, p_id, p_name, meds_str):
    """
    Them benh nhan moi voi don thuoc da sao chep.
    """
    print(f"\n--- Them benh nhan: {p_id} ---")
    
    # Tao list thuoc tu chuoi
    raw_meds = create_medication_list(meds_str)
    
    # QUAN TRONG: Tao ban sao de tranh loi tham chieu
    # Neu khong copy: patient_list se tham chieu den cung list voi bien raw_meds
    # va cac benh nhan khac neu chung cung gan tu cung bien nay.
    safe_meds = copy_medication_list(raw_meds)
    
    new_patient = [p_id, p_name, safe_meds]
    patient_list.append(new_patient)
    print(f"Da them benh nhan {p_name}. Don thuoc: {safe_meds}")
    print(f"Dia chi bo nho don thuoc: {id(safe_meds)}")

def update_medication(patient_list, p_id, new_meds_str):
    """
    Cap nhat don thuoc cho benh nhan.
    - Tao list moi va sao chep truoc khi gan.
    """
    print(f"\n--- Cap nhat don thuoc cho benh nhan: {p_id} ---")
    
    index = -1
    for i, p in enumerate(patient_list):
        if p == p_id:
            index = i
            break
    
    if index == -1:
        print(f"Khong tim thay benh nhan {p_id}!")
        return

    # Tao list thuoc moi
    new_meds_list = create_medication_list(new_meds_str)
    
    # QUAN TRONG: Tao ban sao moi cho benh nhan nay
    safe_new_meds = copy_medication_list(new_meds_list)
    
    # Cap nhat vao benh nhan
    patient_list[index] = safe_new_meds
    
    print(f"Da cap nhat don thuoc cho {patient_list[index]}: {safe_new_meds}")
    print(f"Dia chi bo nho moi: {id(safe_new_meds)}")

def display_patients(patient_list):
    """
    Hien thi danh sach benh nhan va dia chi bo nho.
    """
    print("\n----- DANH SACH BENH NHAN (CO ID BO NHO) -----")
    if not patient_list:
        print("Khong co du lieu.")
        return

    for i, p in enumerate(patient_list, 1):
        meds = p
        print(f"{i}. ID: {p} | Ten: {p} | Don thuoc: {meds} | ID List: {id(meds)}")

def main():
    """
    Ham chinh minh hoa loi va cach sua.
    """
    patients = []

    # 1. Them benh nhan 1 voi don thuoc "Aspirin, Paracetamol"
    add_patient(patients, "P001", "Nguyen Van A", "Aspirin, Paracetamol")

    # 2. Them benh nhan 2 voi cung don thuoc "Aspirin, Paracetamol"
    # Neu khong copy, P001 va P002 se chung mot list.
    add_patient(patients, "P002", "Tran Thi B", "Aspirin, Paracetamol")

    print("\n--- Hien tai, hai benh nhan co cung don thuoc (nhung list khac nhau) ---")
    display_patients(patients)

    # 3. Cap nhat don thuoc cho P001: them "Amoxicillin"
    # Neu khong copy, P002 cung se co Amoxicillin (loi tham chieu).
    # Code nay da copy nen P002 khong bi thay doi.
    update_medication(patients, "P001", "Aspirin, Paracetamol, Amoxicillin")

    print("\n--- Sau khi cap nhat P001 ---")
    print("Neu dung: P001 co Amoxicillin, P002 khong co.")
    print("Neu loi: P002 cung co Amoxicillin.")
    display_patients(patients)

    # Kiem tra ket qua
    p1_meds = patients
    p2_meds = patients
    
    if "Amoxicillin" in p1_meds and "Amoxicillin" not in p2_meds:
        print("\n[THANH CONG] Loi tham chieu da duoc giai quyet!")
    else:
        print("\n[LOI] Loi tham chieu van con ton tai!")

if __name__ == "__main__":
    main()