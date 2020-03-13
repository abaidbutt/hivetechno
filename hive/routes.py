from flask import render_template, redirect, url_for, request, flash, abort, send_file, jsonify, make_response
import datetime
import secrets
import os

from flask_admin.contrib.fileadmin import FileAdmin
from hive import db, app, admin, login_manager, mail
from flask_admin.contrib.sqla import ModelView
from hive.forms import RegisterForm, CheckForm, LoginForm, FeeSubmitForm, PasswordForm, EnrollmentForm
from hive.models import User, Courses, Promo, Enrollments, Invoices
from werkzeug.utils import secure_filename
from flask_admin import BaseView, expose
from markupsafe import Markup
from flask_admin.menu import MenuLink
from flask_login import login_user, logout_user, current_user, UserMixin
from flask_mail import Message


class Logger(UserMixin):
    def __init__(self, id, active=True):
        self.id = id
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


@login_manager.user_loader
def load_user(user_id):
    return Logger(user_id, True)


class UserModelView(ModelView):
    can_create = False
    can_view_details = True
    column_searchable_list = ['s_name', 'email']
    column_filters = ['roll_no']
    column_editable_list = ['c_nic']
    # edit_modal=True
    can_export = True
    

    
    def profiler(view, context, model, name):
        if not model.image_file:
            return ''
        return Markup(f'''<img src="{url_for('static', filename='images/profile_pic/'+model.image_file)}" width="50" height="50" />''')

    def fronter(view, context, model, name):
        if not model.image_file:
            return ''
        return Markup(f'''<img src="{url_for('static', filename='images/cnic_front/'+model.cnic_front)}" width="50" height="50" />''')

    def backer(view, context, model, name):
        if not model.image_file:
            return ''
        return Markup(f'''<img src="{url_for('static', filename='images/cnic_back/'+model.cnic_back)}" width="50" height="50" />''')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'
    column_list = ['id', 's_name', 'f_name', 'dob', 'c_nic', 'gender', 'status', 'roll_no','password', 'pp_no', 'parent_no', 'email', 'address',
                   'degree', 'semester', 'institute', 'marks', 'start_year', 'end_year', 'image_file', 'cnic_front', 'cnic_back']
    form_choices = {
        'gender': [
            ('M', 'male'),
            ('F', 'female'),
            ('O', 'other')
        ]
    }
    column_formatters = {'image_file': profiler,
                         'cnic_front': fronter, 'cnic_back': backer}


class NewModelView(ModelView):
    can_create = False
    def profiler(view, context, model, name):
        if not model.image_file:
            return ''
        return Markup(f'''<img src="{url_for('static', filename='images/profile_pic/'+model.image_file)}" width="50" height="50" />''')

    def fronter(view, context, model, name):
        if not model.image_file:
            return ''
        return Markup(f'''<img src="{url_for('static', filename='images/cnic_front/'+model.cnic_front)}" width="50" height="50" />''')

    def backer(view, context, model, name):
        if not model.image_file:
            return ''
        return Markup(f'''<img src="{url_for('static', filename='images/cnic_back/'+model.cnic_back)}" width="50" height="50" />''')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'
    form_choices = {
        'gender': [
            ('M', 'male'),
            ('F', 'female'),
            ('O', 'other')
        ]
    }
    column_list = ['id', 's_name', 'f_name', 'dob', 'c_nic', 'gender', 'status', 'roll_no', 'pp_no', 'parent_no', 'email', 'address',
                   'degree', 'semester', 'institute', 'marks', 'start_year', 'end_year', 'image_file', 'cnic_front', 'cnic_back', 'approve', 'cancel']

    def _approve(view, context, model, name):
        _html = ''
        user = User.query.filter_by(
            status='new').order_by(User.id.asc()).first()
        if user.id == model.id:
            _html = f'''<button type="button" onclick="approval.user_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">approve</button>
            <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Approve User & Send Mail</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
            </div>
            <div class="modal-body">
            <form action='/approve' method='POST' name='approval'>
            <input type="hidden" name="user_id">
            <textarea name="approve_mail" class='form-control'>Congratulation! <br/>Your request has been approved. </textarea>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary">Send Mail</button>
            </form></div></div></div></div>'''
        else:
            _html = f'''<button type="button" onclick="approval.user_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">approve</button>'''

        return Markup(_html)

    def _cancel(view, context, model, name):
        _html = ''
        user = User.query.filter_by(
            status='new').order_by(User.id.asc()).first()
        if user.id == model.id:
            _html = f'''<button type="button" onclick="canceled.user_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal2">Cancel</button>
            <div class="modal fade" id="exampleModal2" tabindex="-1" role="dialog" aria-labelledby="exampleModal2Label" aria-hidden="true">
            <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title" id="exampleModal2Label">Cancel User & Send Mail</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
            </div>
            <div class="modal-body">
            <form action='/cancel' method='POST' name='canceled'>
            <input type="hidden" name="user_id">
            <textarea name="canceled_mail" class='form-control'>We regret to inform you that you have disapproved. Again register on our website <a href="www.hivetech.com/register">HiveTechnology</a> </textarea>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary">Send Mail</button>
            </form></div></div></div></div>'''
        else:
            _html = f'''<button type="button" onclick="canceled.user_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal2">Cancel</button>'''

        # _html=f''' <form action="/cancel" method="POST">
        #         <input name="user_id"  type="hidden" value="{model.id}">
        #         <button type='submit'>Cancel</button>
        #     </form>'''

        return Markup(_html)

    column_formatters = {'approve': _approve, 'cancel': _cancel,
                         'image_file': profiler, 'cnic_front': fronter, 'cnic_back': backer}

    def get_query(self):
        return self.session.query(self.model).filter(self.model.status == 'new')


class EnrollmentModelView(ModelView):
    can_create = False
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'
    column_list = ['id', 'admission_date', ' paid_installments', 'promo_code', 'paid_fee',
                   'installment', 'batch', 'time', 'total_fee', 'user_id', 'course_id']


class NewEnrollmentModelView(ModelView):
    can_create = False
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'
    column_list = ['id', 'admission_date', ' paid_installments', 'promo_code', 'paid_fee',
                   'installment', 'batch', 'time', 'total_fee', 'user_id', 'course_id', 'approve', 'cancel']

    def enroll_approve(view, context, model, name):
        _html = ''
        enroll = Enrollments.query.filter_by(
            paid_installments=-1).order_by(Enrollments.id.asc()).first()
        if enroll.id == model.id:
            _html = f'''<button type="button" onclick="enroll_approval.enroll_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">approve</button>
            <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Approve Enrollment & Send Mail</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span></button></div>
            <div class="modal-body">
            <form action='/enroll_approve' method='POST' name='enroll_approval'>
            <input type="hidden" name="enroll_id">
            <textarea name="enroll_approve_mail" class='form-control'>Congratulation! Your request has been approved. </textarea>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary">Send Mail</button>
            </form></div></div></div></div>'''
        else:
            _html = f'''<button type="button" onclick="enroll_approval.enroll_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">approve</button>'''

        return Markup(_html)

    def enroll_cancel(view, context, model, name):
        _html = ''
        enroll = Enrollments.query.filter_by(
            paid_installments=-1).order_by(Enrollments.id.asc()).first()
        if enroll.id == model.id:
            _html = f'''<button type="button" onclick="enroll_cancel.enroll_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal2">Cancel</button>
            <div class="modal fade" id="exampleModal2" tabindex="-1" role="dialog" aria-labelledby="exampleModal2Label" aria-hidden="true">
            <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title" id="exampleModal2Label">Cancel Enrollment & Send Mail</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
            </div>
            <div class="modal-body">
            <form action='/enroll_cancel' method='POST' name='enroll_cancel'>
            <input type="hidden" name="enroll_id">
            <textarea name="enroll_cancel_mail" class='form-control'>We regret to inform you that you have disapproved Enrollement. Again Enroll <a href="www.hivetech.com/register">HiveTechnology</a> </textarea>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary">Send Mail</button>
            </form></div></div></div></div>'''
        else:
            _html = f'''<button type="button" onclick="enroll_cancel.enroll_id.value={model.id}" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal2">Cancel</button>'''

        return Markup(_html)

    column_formatters = {'approve': enroll_approve, 'cancel': enroll_cancel}

    def get_query(self):
        return self.session.query(self.model).filter(self.model. paid_installments == -1)


class CourseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'
    column_list = ['id', 'course_name', 'course_fee', 'course_status']

class PromoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'
    column_list = ['id', 'code', 'discount', 'status', 'count']
    


class InvoiceModelView(ModelView):
    can_create = False
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'
    column_list = ['id', 'date', 'enroll_id', 'preview']

    def _preview(view, context, model, name):
        enroll = Enrollments.query.filter_by(id=model.enroll_id).first()
        invoicer = Invoices.query.filter_by(id=model.id).first()
        _html = f'''<a href="/pdf/{model.id}"><button type="button" class="btn btn-block btn-primary">Preview</button></a>'''

        return Markup(_html)

    column_formatters = {'preview': _preview}

    def get_query(self):
        return self.session.query(self.model).order_by(self.model.id.desc())


admin.add_view(InvoiceModelView(Invoices, db.session))

admin.add_view(CourseModelView(Courses, db.session,
                               menu_icon_type='glyph', menu_icon_value='glyphicon-home'))
admin.add_view(UserModelView(User, db.session, endpoint='user',
                             name='User', menu_icon_type='glyph', menu_icon_value='glyphicon-user'))
admin.add_view(NewModelView(User, db.session, endpoint='new',
                            name='New User', menu_icon_type='glyph', menu_icon_value='glyphicon-ok'))
admin.add_view(PromoModelView(Promo, db.session))
admin.add_view(EnrollmentModelView(Enrollments, db.session,
                                   endpoint='enroll', name='Enrollments'))
admin.add_view(NewEnrollmentModelView(Enrollments, db.session,
                                      endpoint='newenroll', name='New Enrollments'))


class FeeSubmit(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == '0'

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = FeeSubmitForm()
        first_user = User.query.filter_by(
            status='approved').order_by(User.id.asc()).first()
        if first_user:
            form.rollNo.choices = [(i.id, i.roll_no) for i in User.query.filter_by(
                status='approved').order_by(User.id.asc()).all()]
            first_enroll = db.session.query(Enrollments).filter(Enrollments.user_id == first_user.id if request.method == 'GET' else Enrollments.id ==
                                                                form.enrollments.data, Enrollments.paid_installments < Enrollments.installment, Enrollments.paid_installments > -1).first()
            if first_enroll:
                form.enrollments.choices = [(i.id, i.courses.course_name) for i in db.session.query(Enrollments).filter(Enrollments.user_id == first_user.id if request.method ==
                                                                                                                        'GET' else Enrollments.user_id == form.rollNo.data, Enrollments.paid_installments < Enrollments.installment, Enrollments.paid_installments > -1).all()]
                form.total_fee.data = first_enroll.total_fee
                form.paid_fee.data = first_enroll.paid_fee
                form.total_installments.data = first_enroll.installment
                form.paid_installments.data = first_enroll.paid_installments
                form.perinsta.data = (
                    first_enroll.total_fee / first_enroll.installment) if request.method == 'GET' else form.perinsta.data

        if request.method == 'POST' and form.validate_on_submit():
            print('ta ka pta chal sky')
            pay_enroll = Enrollments.query.filter_by(
                id=form.enrollments.data).first()
            pay_enroll.paid_installments = pay_enroll.paid_installments+1
            pay_enroll.paid_fee = pay_enroll.paid_fee + \
                int(float(form.perinsta.data))
            invoice_id = 1
            invoices = Invoices.query.order_by(Invoices.id.desc()).first()
            if invoices:
                invoice_id += 1
            invoicer = Invoices(enroll_id=pay_enroll.id, paid_fee=pay_enroll.paid_fee,
                                paid_installments=pay_enroll.paid_installments)

            db.session.add(pay_enroll)
            db.session.add(invoicer)
            db.session.commit()
            return self.render('pdf_template.html', enroll=pay_enroll, invoice=invoicer)
        return self.render('admin/notify.html', form=form)


@app.route('/pdf/<_id>')
def pdf(_id):
    invoicer = Invoices.query.filter_by(id=_id).first()
    enroll = Enrollments.query.filter_by(id=invoicer.enroll_id).first()

    return render_template('pdf_template.html', enroll=enroll, invoice=invoicer)


# admin.add_view(NotificationView(name='Notification', endpoint='notify'))
admin.add_link(MenuLink(name='Logout', url='/log_out', category='Admin'))
root = os.path.join(app.root_path, 'static')
admin.add_view(FileAdmin(root, '/static/', name='Files'))
admin.add_view(FeeSubmit(name='feeSubmit', endpoint='submission'))


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex+f_ext
#     picture_path = os.path.join(
#         app.root_path, 'static/images/profile_pic', picture_fn)
#     form_picture.save(picture_path)
#     return picture_fn


def photo_save(form_pics, _type):
    file_name = secure_filename(form_pics.filename)
    form_pics.save(os.path.join(
        app.root_path, 'static', 'images', _type, file_name))
    return form_pics.filename


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    fil = RegisterForm(request.files)
    form.course_name.choices = [(str(i.id), str(i.course_name))
                                for i in Courses.query.filter_by(course_status=True).all()]
    form.course_fee.choices = [(str(i.id), str(i.course_fee))
                               for i in Courses.query.filter_by(course_status=True).all()]
    if request.method == 'POST':
        print('heeloo', form.validate_on_submit())
        if form.validate_on_submit():
            print('kcuh')
            # print(form.user_name.data)
            # print(form.father_name.data)
            # print(form.dob.data)
            # print(form.cnic.data)
            # print(form.gender.data)
            # print(form.admit_date.data)
            # print(form.course_name.data)
            # print(form.course_fee.data)
            # print(form.course_installments.data)
            # print(form.course_promo.data)
            # print(form.discount.data)
            # print(form.total_fee.data)
            # print(form.personal_no.data)
            # print(form.parent_no.data)
            # print(form.email.data)
            # print(form.address.data)
            # print(form.degree.data)
            # print(form.sem.data)
            # print(form.institute.data)
            # print(form.marks.data)
            # print(form.start_year.data)
            # print(form.end_year.data)
            # user=User(s_name=form.user_name.data, f_name=form.father_name.data, dob=datetime.datetime.strptime(str(form.dob.data), '%Y-%m-%d'), c_nic=form.cnic.data, gender=form.gender.data, admission_date=datetime.datetime.strptime(str(form.admit_date.data), '%Y-%m-%d'), course_name=form.course_name.data, batch=form.batch_no.data, time=str(form.time.data), pp_no=form.personal_no.data, parent_no=form.parent_no.data, email=form.email.data, address=form.address.data, degree=form.degree.data, semester=form.sem.data, institute=form.institute.data, marks=form.marks.data, year=str(form.year.data), image_file=pic_file, cnic_file=cnic_file)
            if fil.cnic_front.data and fil.profile_picture.data and fil.cnic_back.data:
                pic_file = photo_save(fil.profile_picture.data, 'profile_pic')
                cnic_front = photo_save(fil.cnic_front.data, 'cnic_front')
                cnic_back = photo_save(fil.cnic_back.data, 'cnic_back')
                course = Courses.query.filter_by(
                    id=form.course_name.data).first()
                promo = Promo.query.filter(
                    Promo.code == form.course_promo.data, Promo.status == True, Promo.count > 0).first()
                d_user = User.query.order_by(User.id.desc()).first()
                rollNo = 1000
                if d_user:
                    rollNo = int(d_user.roll_no)+1

                totalfee = course.course_fee
                if promo:
                    totalfee -= ((totalfee*promo.discount)/100)

                user = User(s_name=form.user_name.data, f_name=form.father_name.data, dob=datetime.datetime.strptime(str(form.dob.data), '%Y-%m-%d'), c_nic=form.cnic.data, gender=form.gender.data, status='new', roll_no=rollNo, password=rollNo, pp_no=form.personal_no.data, parent_no=form.parent_no.data, email=form.email.data,
                            address=form.address.data, degree=form.degree.data, semester=form.semester.data, institute=form.institute.data, marks=form.marks.data, start_year=int(form.start_year.data), end_year=int(form.end_year.data), image_file=pic_file, cnic_front=cnic_front, cnic_back=cnic_back)
                db.session.add(user)
                # db.session.commit()
                user = User.query.filter_by(c_nic=form.cnic.data).first()

                enroll = Enrollments(admission_date=form.admit_date.data,  paid_installments=-1, promo_code=promo.id if promo else '0', paid_fee=0,
                                     installment=form.course_installments.data, batch='morning', time='Y-m-d', total_fee=totalfee, user_id=user.id, course_id=form.course_name.data)
                db.session.add(enroll)
                # db.session.commit()
                if promo:
                    promo.count = promo.count-1
                    db.session.add(promo)
                
                db.session.commit()

                flash(f'Adccount has been created!', 'success')
                return redirect(url_for('home'))

    return render_template('registeration.html', form=form)


@app.route('/verify_course_promo/<_code>')
def verify_course_promo(_code):

    # codes=Promo.query.filter_by(code=_code, status=True).first()
    counter = Promo.query.filter(
        Promo.count > 0, Promo.status == True, Promo.code == _code).first()
    # print(counter)
    if counter:
        return jsonify({'count': counter.discount})

    return jsonify({'count': 0})


@app.route('/get_course_admin/<_code>')
def get_course_admin(_code):
    # , 'total_fee': i.total_fee, 'paid_installment': i.paid_installments, 'total_installment': i.installment, 'paid_fee': i.paid_fee
    enroll = [{'enroll_id': i.id, 'course_name': i.courses.course_name} for i in db.session.query(Enrollments).filter(
        Enrollments.user_id == _code, Enrollments.paid_installments < Enrollments.installment, Enrollments.paid_installments > -1).all()]
    if enroll:
        return jsonify({'count': enroll})
    return jsonify({'count': [{'enroll_id': 0, 'course_name': ''}]})


@app.route('/enroll_change/<_code>')
def enroll_change(_code):
    enroll = Enrollments.query.filter_by(id=_code).first()
    if enroll:
        return jsonify({'count': {'t_fee': enroll.total_fee, 'p_fee': enroll.paid_fee, 't_install': enroll.installment, 'p_install': enroll.paid_installments}})
    return jsonify({'count': {'t_fee': '', 'p_fee': '', 't_install': '', 'p_install': ''}})


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    form.course_name.choices = [(str(i.id), str(i.course_name))
                                for i in Courses.query.filter_by(course_status=True).all()]
    form.course_fee.choices = [(str(i.id), str(i.course_fee))
                               for i in Courses.query.filter_by(course_status=True).all()]
    if form.validate_on_submit():
        course = Courses.query.filter_by(id=form.course_name.data).first()
        promo = Promo.query.filter_by(code=form.course_promo.data).first()
        d_user = User.query.order_by(User.id.desc()).first()
        rollNo = 1000
        if d_user:
            rollNo = int(d_user.roll_no)+1
        totalfee = course.course_fee
        if promo:
            totalfee -= ((totalfee*promo.discount)/100)
        pic_file = photo_save(form.profile_picture.data, 'profile_pic')
        cnic_front = photo_save(form.cnic_front.data, 'cnic_front')
        cnic_back = photo_save(form.cnic_back.data, 'cnic_back')
        user = User(s_name=form.user_name.data, f_name=form.father_name.data, dob=datetime.datetime.strptime(str(form.dob.data), '%Y-%m-%d'), c_nic=form.cnic.data, gender=form.gender.data, status='new', roll_no=rollNo, password=rollNo, pp_no=form.personal_no.data, parent_no=form.parent_no.data,
                    email=form.email.data, address=form.address.data, degree=form.degree.data, semester=form.semester.data, institute=form.institute.data, marks=form.marks.data, start_year=int(form.start_year.data), end_year=int(form.end_year.data), image_file=pic_file, cnic_front=cnic_front, cnic_back=cnic_back)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(c_nic=form.cnic.data).first()
        enroll = Enrollments(admission_date=form.admit_date.data,  paid_installments=-1, promo_code=promo.id if promo else '0', paid_fee=0,
                             installment=form.course_installments.data, batch='morning', time='Y-m-d', total_fee=totalfee, user_id=user.id, course_id=form.course_name.data)
        db.session.add(enroll)
        db.session.commit()
        flash(f'Adccount has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', form=form)
# def send_email(user):
#     msg = Message('HiveTechnology', recipients=[user.email])
#     msg.body = f'''{url_for('register', token=token, _external=True)}
#     If you did not make this request then simply ignore this email and no changes will be made.
#     '''
#     mail.send(msg)


# admin approve & cancell User
@app.route('/approve', methods=['POST'])
def approve():
    user = User.query.filter_by(id=int(request.form['user_id'])).first()
    user.status = 'approved'
    db.session.add(user)
    msg = Message('HiveTechnology',
                  sender="bestabaidullahbutt@gmail.com", recipients=[user.email])
    msg.body = f''' {request.form["approve_mail"]} <br /> Roll No: {user.roll_no} '''
    mail.send(msg)
    db.session.commit()

    flash(f'User has been approved', 'success')
    return redirect('admin/new/')


@app.route('/cancel', methods=['POST'])
def cancel():
    user = User.query.filter_by(id=int(request.form['user_id'])).first()
    enroll = Enrollments.query.filter_by(user_id=user.id).all()
    if os.path.isfile(os.path.join(app.root_path, 'static', 'images', 'profile_pic', user.image_file)):
        os.remove(os.path.join(app.root_path, 'static',
                               'images', 'profile_pic', user.image_file))

    if os.path.isfile(os.path.join(app.root_path, 'static', 'images', 'cnic_front', user.cnic_front)):
        os.remove(os.path.join(app.root_path, 'static',
                               'images', 'cnic_front', user.cnic_front))

    if os.path.isfile(os.path.join(app.root_path, 'static', 'images', 'cnic_back', user.cnic_back)):
        os.remove(os.path.join(app.root_path, 'static',
                               'images', 'cnic_back', user.cnic_back))

    for en in enroll:
        db.session.delete(en)
    # db.session.commit()

    db.session.delete(user)
    msg = Message('HiveTechnology',
                  sender="bestabaidullahbutt@gmail.com", recipients=[user.email])
    msg.body = f''' {request.form["canceled_mail"]} '''
    mail.send(msg)
    db.session.commit()
    flash(f'User has been deleted {user.image_file}', 'success')
    return redirect('admin/new/')


# admin approve & cancell enrollemnts
@app.route('/enroll_approve', methods=['POST'])
def enroll_approve():
    enroll = Enrollments.query.filter_by(
        id=int(request.form['enroll_id'])).first()
    enroll. paid_installments = 0
    db.session.add(enroll)
    msg = Message('HiveTechnology', sender="bestabaidullahbutt@gmail.com",
                  recipients=[enroll.user.email])
    msg.body = f''' {request.form["enroll_approve_mail"]} <br /> Roll No: {enroll.user.roll_no} '''
    mail.send(msg)
    db.session.commit()

    flash(f'Enrollemtns of User  has been approved', 'success')
    return redirect('admin/newenroll/')


@app.route('/enroll_cancel', methods=['POST'])
def enroll_cancel():
    print(request.form['enroll_id'])
    enroll = Enrollments.query.filter_by(
        id=int(request.form['enroll_id'])).first()
    db.session.delete(enroll)
    msg = Message('HiveTechnology', sender="bestabaidullahbutt@gmail.com",
                  recipients=[enroll.user.email])
    msg.body = f'''{request.form["enroll_cancel_mail"]}'''
    mail.send(msg)
    db.session.commit()
    flash(f'Enrollements of User has been deleted', 'success')
    return redirect('admin/newenroll/')




@app.route('/xyz', methods=['POST', 'GET'])
def xyz():
    if current_user.is_authenticated and (current_user.id == '0'):
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.username.data == 'admin@blog.com' and form.password.data == 'admin':
            user = load_user(0)
            login_user(user, form.remember.data)
            return redirect(url_for('admin.index'))

    return render_template('login.html', form=form)


@app.route('/log_out')
def log_out():
    out = False
    if current_user.id == '0':
        out = True
    logout_user()
    if out:
        return redirect(url_for('xyz'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated and current_user.id != '0':
        return redirect(url_for('profile'))
    form = LoginForm()

    if request.method == 'POST':
        user = User.query.filter_by(roll_no=form.username.data).first()
        if not(user):
            form.username.errors = ['Please Check your username']
        else:
            if user.password == form.password.data:
                if user.status =='new':
                    return f'<h3>Welcome {user.s_name} ! Your request has been pending.</h3>'
                login_user(load_user(user.id), form.remember.data)
                flash('You are logged in ', 'success')
                return redirect(url_for('profile'))
            else:
                form.password.errors = ['Please Check your password']

    return render_template('login.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    
    if current_user.is_authenticated and current_user.id != 0:
        act='home'
        pass_form = PasswordForm()
        enroll_form = EnrollmentForm()
        user_details = User.query.filter_by(id=current_user.id).first()
        enroll = Enrollments.query.filter_by(user_id=current_user.id).all()
        choice_name = [(i.id, i.course_name)
                       for i in Courses.query.filter_by(course_status=True).all()]
        choice_fee = [(i.id, i.course_fee)
                      for i in Courses.query.filter_by(course_status=True).all()]

        for en in enroll:
            if (en.course_id, en.courses.course_name) in choice_name:
                choice_name.remove((en.course_id, en.courses.course_name))
                choice_fee.remove((en.course_id, en.courses.course_fee))

        enroll_form.course_name.choices = choice_name
        enroll_form.course_fee.choices = choice_fee

        if pass_form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            user.password = pass_form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash(f'Your password has been updated', 'success')
            act='password'
            # return render_template('profile.html', enroll=enroll, user_details=user_details, act=act, pass_form=pass_form, enroll_form=enroll_form)

        if enroll_form.validate_on_submit():
            course = Courses.query.filter_by(
                id=enroll_form.course_name.data).first()
            promo = Promo.query.filter(
                Promo.code == enroll_form.course_promo.data, Promo.status == True, Promo.count > 0).first()

            totalfee = course.course_fee
            if promo:
                totalfee -= ((totalfee*promo.discount)/100)

            enroller = Enrollments(paid_installments=-1, promo_code=promo.id if promo else '0', paid_fee=0, installment=enroll_form.course_installments.data,
                                   batch='morning', time='Y-m-d', total_fee=totalfee, user_id=current_user.id, course_id=enroll_form.course_name.data)
            db.session.add(enroller)
            # db.session.commit()
            if promo:
                promo.count = promo.count-1
                db.session.add(promo)
            db.session.commit()
            enroll = Enrollments.query.filter_by(user_id=current_user.id).all()
            for en in enroll:
                if (en.course_id, en.courses.course_name) in choice_name:
                    choice_name.remove((en.course_id, en.courses.course_name))
                    choice_fee.remove((en.course_id, en.courses.course_fee))
            enroll_form.course_name.choices = choice_name
            enroll_form.course_fee.choices = choice_fee
            act='menu1'
            flash(f'Your enrollment has been completed ', 'success')
            # return render_template('profile.html', enroll=enroll, user_detail=user_details, act=act, enroll_form=enroll_form, pass_form=pass_form)

        return render_template('profile.html', enroll=enroll, user_details=user_details, pass_form=pass_form, act=act, enroll_form=enroll_form)
    return redirect(url_for('login'))
