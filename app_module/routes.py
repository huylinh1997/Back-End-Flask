from app_module import app, db, bcrypt
from app_module.models import Student, User 
from app_module.schemas import  user_schema, list_user_schema, student_schema, list_student_schema
from flask import request, jsonify
from flask_login import login_user, current_user
from flask_cors import cross_origin
from datetime import timedelta
from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity
from app_module import jwt


#Home 
@app.route('/')
def home():
    return 'Server is Running'


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'msg': 'The access token has expired'
    }), 401


#POST register
@app.route('/api/register',methods = ['POST'])
@cross_origin()
def register():
    username = request.json['username'],                        #lấy dữ liệu từ file json vừa nhận
    email = request.json['email'],
    password = request.json['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')       #hash password
    
    if User.query.filter_by(email = email).first():
        return jsonify({"msg" : "Email already existed"}),409
    if User.query.filter_by(username = username).first():
        return jsonify({"msg" : "UserName already existed"}),409
    else:
        new_user = User(username =username, email = email, password = hashed_password)   
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)             #serialization


#Post login
@app.route('/api/login',methods = ['POST'])    
@cross_origin()                                             # đối với login, ta dùng http POST
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email = email).first() 

    if user:                            #giống email và pass thì mới return true. 
        isTruePassword = bcrypt.check_password_hash( user.password , password)
        if not isTruePassword:
            return jsonify({"msg": "password is wrong"}), 401
    else: 
        return jsonify({"msg": "email is not existed"}), 401          #ép kiểu sang jsonify


    expires = timedelta(hours=8)
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=email,expires_delta=expires)
    return jsonify(access_token=access_token), 200



@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
 

#get all student
@app.route('/api/student',methods = ['GET'])
@jwt_required
@cross_origin()
def get_all_student():
    students = Student.query.all()
    list_students = list_student_schema.dump(students)      # đổ cái students vừa query được vào thằng list_schema.
    return jsonify(list_students)                           # ép kiểu sang jsonify, rồi truyền đi


#Post student 
@app.route('/api/student',methods = ['POST'])
@jwt_required
@cross_origin()
def post_student():
    name = request.json['name'],
    date_of_birth = request.json['date_of_birth'],
    classname = request.json['classname'],
    email = request.json['email']

    if Student.query.filter_by(email = email).first():
        return jsonify({"msg" : "email student already existed"}),409
    else:
        student = Student(name = name, date_of_birth = date_of_birth, classname = classname, email = email)
        db.session.add(student)
        db.session.commit()
        return student_schema.jsonify(student)


#Get 1 student by id
@app.route('/api/student/<id>',methods = ['GET'])             #<id> : biến id.  
@jwt_required
@cross_origin()
def get_student_by_id(id):
    student = Student.query.get_or_404(id)
    return student_schema.jsonify(student)


#Put student
@app.route('/api/student/<id>',methods = ['PUT'])
@jwt_required
@cross_origin()
def put_student(id):
    student = Student.query.get_or_404(id)
    if Student.query.filter_by(email = request.json['email']).first() and student.email != request.json['email']:
        return jsonify({"msg" : "email already existed"}),409
    else:
        student.name = request.json['name'],
        student.date_of_birth = request.json['date_of_birth'],
        student.classname = request.json['classname'],
        student.email = request.json['email']
        db.session.commit()
        return student_schema.jsonify(student)


#delete student
@app.route('/api/student/<id>',methods = ['DELETE'])
@jwt_required
@cross_origin()
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return student_schema.jsonify(student)


#Get islogin
@app.route('/api/islogin',methods = ['GET'])                 # đối với login, ta dùng http POST
@cross_origin()
def islogin():
    return jsonify({'status' : True  })
