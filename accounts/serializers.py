import re
import phonenumbers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from.models import UserAccount,CourseCategory,Course,TeacherProfile,StudentProfile,Module,Chapter,Assignment,Quiz,Questions,Order,StudentCourse,StudentAssignment,StudentQuiz,Masterclass,Shedule,Room,Message,StudentChapter,StudentCertificate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True) 
    profile_pic = serializers.ImageField(required=False)
    years_of_experience = serializers.IntegerField(required=False)
    company_name = serializers.CharField(required=False)
    about = serializers.CharField(required=False)
    job_role = serializers.CharField(required=False)
    highest_education = serializers.CharField(required=False)
    specialization = serializers.CharField(required=False)
    mother_name = serializers.CharField(required=False)
    father_name = serializers.CharField(required=False)
    house_name = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    pin = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['email','password', 'password2','full_name','phone_number','role','profile_pic','about','years_of_experience','company_name','about','job_role','highest_education','specialization','mother_name','father_name','house_name','street','city','state','country','pin']
        extra_kwargs = {'profile_pic': {'required': False}}  # Include password2 field in fields

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        

        phone_number = attrs.get('phone_number', None)
        phone_number_pattern = r'^\+\d{1,3}\s?\d{3,14}$'

        if phone_number:
           if not re.match(phone_number_pattern, phone_number):
                raise serializers.ValidationError({"phone_number": "Invalid phone number format."})
        role = attrs.get('role')
        if role:
            role_mapping = {
            '1': 1,  # ADMIN
            '2': 2,  # STUDENT
            '3': 3,  # TEACHER
            }
            attrs['role'] = role_mapping.get(str(role), role)

        return attrs
    def create(self, validated_data):
        role = validated_data['role'] 
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role']
           
        )
        user.set_password(validated_data['password'])
        print(user)
        profile_pic=validated_data.get('profile_pic') 
        if profile_pic:
            user.profile_pic=profile_pic
        user.save()
        if role == 3:  # Assuming '3' is the role code for TEACHER
            TeacherProfile.objects.create(
                user=user,
                years_of_experience=validated_data.get('years_of_experience', 0),
                company_name=validated_data.get('company_name', ''),
                job_role=validated_data.get('job_role',''),
                about=validated_data.get('about', '')
            )
        if role == 2:  # Assuming '3' is the role code for TEACHER
            StudentProfile.objects.create(
                user=user,
                highest_education=validated_data.get('highest_education', ''),  # Adjust as needed
                specialization=validated_data.get('specialization', ''),
                mother_name=validated_data.get('mother_name', ''),
                father_name=validated_data.get('father_name', ''),
                house_name=validated_data.get('house_name', ''),
                street=validated_data.get('street', ''),
                city=validated_data.get('city', ''),
                country=validated_data.get('country',''),
                state=validated_data.get('state', ''),
                pin=validated_data.get('pin', 0),
            )    

        return user
#<----------------------------------------------------------------------------------------------------------------->
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
#<-------------------------------------------------------------------------------------------------------------------->
        

class TeacherSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number=serializers.CharField(source='user.phone_number',read_only=True)
    is_active = serializers.BooleanField(source='user.is_active')
    profile_pic=serializers.ImageField(source='user.profile_pic')
    
    class Meta:
        model = TeacherProfile
        fields = ['user_id','full_name','email','phone_number','profile_pic','is_active','years_of_experience','company_name','job_role','about','account']      

#<---------------------------------------------------------------------------------------------------------------------->
class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number=serializers.CharField(source='user.phone_number',read_only=True)
    is_active = serializers.BooleanField(source='user.is_active')
    profile_pic=serializers.ImageField(source='user.profile_pic')

    class Meta:
        model=StudentProfile
        fields=['user_id','full_name','email','phone_number','profile_pic','is_active','highest_education','specialization','father_name','mother_name','house_name','city','street','state','pin']
#<-------------------------------------------------------------------------------------------------------------->
class CourseSerializer(serializers.ModelSerializer):
     class Meta:
        model = Course
        fields = '__all__'

#<------------------------------------------------------------------------------------------------------------->
class TeacherCourseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)
    class Meta:
        model=Course
        fields=['id','title','is_active','created_at','about','category_name']
#<-------------------------------------------------------------------------------------------------------------->
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Module
        fields = '__all__'      
#<---------------------------------------------------------------------------------------------------------------->
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter  
        fields = '__all__'
#<------------------------------------------------------------------------------------------------------------------>
class AssignmentSerializer(serializers.ModelSerializer):
     class Meta:
        model = Assignment  
        fields = '__all__'
#<------------------------------------------------------------------------------------------------------------------>
class QuizSerializer(serializers.ModelSerializer):
     class Meta:
        model = Quiz  
        fields = '__all__'        
#<----------------------------------------------------------------------------------------------------------------->
class QuestionSerializer(serializers.ModelSerializer):
     class Meta:
        model = Questions 
        fields = '__all__'   
#<------------------------------------------------------------------------------------------------------------------>           
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
#<----------------------------------------------------------------------------------------------------------------->
class MasterclassSerializer(serializers.ModelSerializer):
     class Meta:
        model = Masterclass
        fields = '__all__'   
class SheduleSerializer(serializers.ModelSerializer):
     class Meta:
        model = Shedule
        fields = '__all__'           
#<---------------------------------------------------------------------------------------------------------------------->        
class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = '__all__'                
#<-------------------------------------------------------------------------------------------------------------------->                       
class StudentAssignmentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='student.user.full_name', read_only=True)
    profile_pic=serializers.ImageField(source='student.user.profile_pic')

    class Meta:
        model = StudentAssignment
        fields = ['full_name','profile_pic','submitted_at','answer','verified']
#<---------------------------------------------------------------------------------------------------------------------------------->
class StudentQuizSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='student.user.full_name', read_only=True)
    profile_pic=serializers.ImageField(source='student.user.profile_pic')

    class Meta:
        model = StudentQuiz
        fields = ['full_name','profile_pic','submitted_at','mark']
        
class StudentQuizsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentQuiz
        fields = ['student', 'quiz', 'submitted_at', 'mark', 'response']
        
                 
                                               
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields=['full_name','profile_pic']
                 
  
class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'    

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'            
class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields=['profile_pic']        


class StudentChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentChapter
        fields = '__all__'         

        
class StudentCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCertificate
        fields = '__all__'     
        
class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6)
    confirmpassword = serializers.CharField(min_length=6)

    def validate(self, data):
        if data['password'] != data['password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
