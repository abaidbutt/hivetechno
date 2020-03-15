import datetime
from hive import db, app

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(30), nullable=False, unique=True)
    course_fee = db.Column(db.Integer, nullable=False)
    course_status  = db.Column(db.Boolean)
    enrollment=db.relationship('Enrollments', backref='courses')
    def __init__(self, course_name, course_fee, course_status):
        self.course_name=course_name
        self.course_fee=course_fee
        self.course_status=course_status
    def __repr__(self):
        # return self.course_name + '-' + ('Enabled' if self.course_status else 'Disabled')
        return self.course_name if self.course_status else ''

class Promo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    discount = db.Column(db.Integer)
    # discount = db.Column(db.Numeric)
    status = db.Column(db.Boolean)
    # status = db.Column(db.Unicode(100))
    count=db.Column(db.Integer)
    # count=db.Column(db.Text)
    enrollment=db.relationship('Enrollments', backref='promo')
    def __init__(self, code, discount, status, count):
        self.code=code
        self.discount=discount
        self.status=status
        self.count=count
    def __repr__(self):
        return self.code

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(30), nullable=False)
    f_name = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    c_nic = db.Column(db.String(30), unique=True, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    status=db.Column(db.String(30), nullable=True)
    roll_no=db.Column(db.String(30), nullable=False, unique=True)
    password=db.Column(db.String(30), nullable=False)
    # conatact
    pp_no = db.Column(db.String(20), nullable=True)
    parent_no = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    address = db.Column(db.String(120), nullable=False)
    # academic details
    degree = db.Column(db.String(30), nullable=True)
    semester = db.Column(db.String(20), nullable=True)
    institute = db.Column(db.String(50), nullable=True)
    marks = db.Column(db.Float, nullable=True)
    start_year = db.Column(db.Integer, nullable=True)
    end_year = db.Column(db.Integer, nullable=True)
    # image_details
    image_file = db.Column(db.String(100), nullable=True)
    cnic_front = db.Column(db.String(100), nullable=True)
    cnic_back = db.Column(db.String(100), nullable=True)
    enrollment=db.relationship('Enrollments', backref='user')
    def __init__(self, s_name, f_name, dob, c_nic, gender, roll_no, status, password, pp_no, parent_no, email, address, degree, semester, institute, marks, start_year, end_year, image_file, cnic_front, cnic_back):
        self.s_name = s_name
        self.f_name = f_name
        self.dob = dob
        self.c_nic = c_nic
        self.gender = gender
        self.roll_no = roll_no
        self.status = status
        self.password=password
        # contact detail
        self.pp_no = pp_no
        self.parent_no = parent_no
        self.email = email
        self.address = address
        # qualification detail
        self.degree = degree
        self.semester = semester
        self.institute = institute
        self.marks = marks
        self.start_year = start_year
        self.end_year = end_year
        # images
        self.image_file = image_file
        self.cnic_front = cnic_front
        self.cnic_back = cnic_back
    def __repr__(self):
        return self.roll_no

class Enrollments(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    admission_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    promo_code = db.Column(db.Integer, db.ForeignKey('promo.id'), nullable=True)
    paid_fee = db.Column(db.Integer, nullable=False)
    paid_installments=db.Column(db.Integer, nullable=True)
    installment = db.Column(db.Integer, nullable=False)
    total_fee=db.Column(db.Integer, nullable=False)
    batch = db.Column(db.String(30), nullable=True)
    time = db.Column(db.String(30), nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id=db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    invoice=db.relationship('Invoices', backref='enrollment')
    def __init__(self, paid_installments,  promo_code, paid_fee, installment, batch, time,total_fee, user_id, course_id, admission_date=datetime.datetime.now()):
        self.admission_date = admission_date
        self.paid_installments=paid_installments
        # promocode
        self.promo_code = promo_code
        self.paid_fee = paid_fee
        self.installment = installment
        self.batch = batch
        self.time = time
        self.total_fee=total_fee
        self.user_id=user_id
        self.course_id=course_id

class Invoices(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    enroll_id=db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    paid_fee = db.Column(db.Integer, nullable=False)
    paid_installments=db.Column(db.Integer, nullable=True)
    
    def __init__(self, enroll_id,  paid_fee, paid_installments, date=datetime.datetime.now()):
        self.date=date
        self.enroll_id=enroll_id
        self.paid_fee=paid_fee
        self.paid_installments=paid_installments
        
        
class Abc(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30), nullable=False)
    
    def __init__(self, name):
        self.name=name
        
        
        
