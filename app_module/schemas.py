from app_module import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username','email')	   #đây là cái response format gửi lại frontend
						   #thành ra nó không nên có password 

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','date_of_birth','classname')      # output format 

user_schema =  UserSchema()                         # 1 schema
list_user_schema = UserSchema(many = True)          # cho phép serialization nhiều schema

student_schema = StudentSchema()
list_student_schema = StudentSchema(many = True)



