from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render 
from .models import Profile,User,InterventionRecord,Flag,Tag
from .serializers import ProfileSerializer,UserSerializer,UserRegSerializer,InterventionSerializer,FlagSerializer,TagSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser,JSONParser,FileUploadParser
import cloudinary.uploader
from django.http.response import JsonResponse
import jwt
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view,APIView,permission_classes
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .backends import JWTAuthentication
from rest_framework import generics



# Create your views here
class CreateUserAPIView(APIView):
    '''
    class to define view for the signup api endpoint
    '''
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,) 
    def post(self, request):
        # Validating our serializer from the UserRegSerializer
        serializer = UserRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Everything's valid, so send it to the UserSerializer
        model_serializer = UserSerializer(data=serializer.data)
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save()

        subject = 'welcome'
        body = '''
                Greetings from the I-reporter Team,
                Hello ''' + model_serializer.data['first_name'] + ''', we are glad having you as one of our entrusted clients to give news and update the different agencies on the country's development.
                We ensure that your voices will be heard!
                Cheers, 
                The I-reporter team. '''
        sender = settings.EMAIL_HOST_USER
        receiver = model_serializer.data['email']
        send_mail(subject,body,sender,[receiver])
        return Response(model_serializer.data, status=status.HTTP_201_CREATED)
        
class LoginApiView(APIView):
    '''
    class to define view for the login api endpoint
    '''
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']          
            user = authenticate(email=email, password=password)      
            if user:
                try:
                    token = user.generate_token()
                    #import pdb; pdb.set_trace()
                    user_details = {}
                    user_details['id'] = "%d" % (user.id)
                    user_details['name'] = "%s %s" % (
                        user.first_name, user.last_name)
                    user_details['token'] = token
              
                    return Response({'success':1,'msg': 'Login successful', 'user_details':user_details }, status=status.HTTP_200_OK)

                except:
                    return Response({'msg': 'Error while generating authenticating token.'}, status=status.HTTP_400_BAD_REQUEST)
            else:           
                return Response({'success':0,'msg': 'User with email and password is not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'msg': 'please provide a email and a password'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileList(APIView):
    '''
    class to define view for the profile api endpoint
    '''
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, format=None):
        all_profiles=Profile.objects.all()
        serializers=ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        def add_user_data(data,user):
            data['user']=user.id
            # import pdb; pdb.set_trace() 
            return data
           
        serializers = ProfileSerializer(data=add_user_data(request.data,request.user))
        
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    

class SingleProfile(APIView):
    '''
    class to define view for returning one profile
    '''
    permission_classes = (IsAuthenticated,)
 
    def get(self,request,pk):
        try:
            profile=Profile.objects.get(pk=pk)
            profile_serializer=ProfileSerializer(profile)
            return Response(profile_serializer.data)
        except Profile.DoesNotExist:
            return JsonResponse({'Message':"object does not exist"}, status=status.HTTP_404_NOT_FOUND)    
             
    def put(self,request,pk):
        parser_classes=[JSONParser,FileUploadParser,MultiPartParser]
        try:
            profile=Profile.objects.get(pk=pk)
            def add_user_data(data,user):
                request.data_mutable=True
                data['user']=user.id
                return data
            profile_serializer=ProfileSerializer(profile,data=add_user_data(request.data,request.user))
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.data)
            return Response(profile_serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
        except Profile.DoesNotExist:
            return JsonResponse({'Message':"object does not exist"}, status=status.HTTP_404_NOT_FOUND) 
    
    # *****GETTING ALL INTERVENTION RECORDS****

class CreateInterventionRecord(APIView):
    '''
    class to define view for the intervention record api endpoint
    '''
    permission_classes = (IsAuthenticated,) 
    def post(self,request): 
        current_user=request.user   
        data=request.data
        data._mutable=True
        data['user']=1
        data._mutable=False
            
        intervention_serializer = InterventionSerializer(data=data)
        print(intervention_serializer)
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return Response(intervention_serializer.data, status=status.HTTP_201_CREATED)
        return Response(intervention_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllInterventionRecords(APIView):
    '''
    class to define view for the api endpoint of all interventions records
    ''' 
    permission_classes = (IsAuthenticated,)   
    def get(self,request):
     
        intervention =InterventionRecord.objects.all()
        current_user=self.request.user
        
        title = request.GET.get('title', None)
        if title is not None:
            intervention = InterventionRecord.filter(title__icontains=title)
        
        intervention_serializers = InterventionSerializer(intervention, many=True)
        return JsonResponse(intervention_serializers.data, safe=False)


class InterventionList(APIView):
    '''
    class to define view for the api endpoint that gets record by searched title 
    '''
    permission_classes = (IsAuthenticated,)
    def get(self,request,title):
        # GET LIST OF INTERVENTION RECORDS,POST A NEW INTERVENTION,DELETE ALL INTERVENTIONS...

        interventions = InterventionRecord.objects.filter(title__icontains=title)
        if interventions.exists():
            interventions_serializer = InterventionSerializer(interventions, many=True)
            return Response(interventions_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'this title was not found.'}, status=status.HTTP_404_NOT_FOUND)


class InterventionDetail(APIView):
    '''
    class to define view for the api endpoint that gets,updates and deletes specific intervention records 
    '''
    permission_classes = (IsAuthenticated,)
    def get(self,request,pk):
    
        try:
            intervention=InterventionRecord.objects.get(pk=pk)
        
            intervention_serializer=InterventionSerializer(intervention)
            return Response(intervention_serializer.data)
        except InterventionRecord.DoesNotExist:
            return Response({'detail': 'The Intervention Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 

    def put (self,request,pk):
        intervention=InterventionRecord.objects.get(id=pk)  
        # tutorial_data = JSONParser().parse(request)
        def add_user_data(data,user):
            data._mutable=True
            data['user']=1
            data._mutable=False
            return data

        intervention_serializer=InterventionSerializer(intervention,data=add_user_data(request.data,request.user))
        print(intervention_serializer)
        data={}
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return Response(intervention_serializer.data, status=status.HTTP_200_OK)
        return Response(intervention_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
         

    def delete(self,request,pk):
        # DELETE A CERTAIN INTERVENTION RECORD
        try:
            intervention=InterventionRecord.objects.get(id=pk)
            intervention.delete()
            return Response({'detail': 'Intervention Record was deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except InterventionRecord.DoesNotExist:
            return Response({'detail': 'The Intervention Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 
          

class InterventionListStatus(APIView):
    '''
    class to define view for the api endpoint that gets records' status 
    '''
    permission_classes = (IsAuthenticated,)
    def get(self,request,intervention_status):
        # Get all record items using the ntervention_status
        interventions = InterventionRecord.objects.filter(status = intervention_status)
        if interventions.exists():
            interventions_serializer = InterventionSerializer(interventions, many=True)
            return Response(interventions_serializer.data, status=status.HTTP_200_OK)
        return Response({'detail' : 'The status was not found.'}, status=status.HTTP_404_NOT_FOUND)
    
class CreateFlag(APIView):
    '''
    class to define view api endpoint for creating the red flag record 
    ''' 
    permission_classes = (IsAuthenticated,)
    def post(self,request): 
        current_user=request.user   
        data=request.data
        data._mutable=True
        data['user']=1
        data._mutable=False
        flag_serializer = FlagSerializer(data=data)
        print(flag_serializer)
        if flag_serializer.is_valid():
            flag_serializer.save()
            return Response(flag_serializer.data, status=status.HTTP_201_CREATED)
        return Response(flag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FlagList(APIView):
    '''
    class to define view for the api endpoint that gets record by searched title 
    '''
    def get(self,request,title):
        #function to fetch all flag records data

        flags_obj = Flag.objects.filter(title__icontains=title)
        if flags_obj.exists():
            flag_serializer = FlagSerializer(flags_obj, many=True)
            return Response(flag_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'this title was not found.'}, status=status.HTTP_404_NOT_FOUND)

class AllFlagRecords(APIView):
    """
    class that view the end point for all red flags
    """
    permission_classes = (IsAuthenticated,)
    def get(self,request):
    
        flag_obj =Flag.objects.all()
        current_user=self.request.user
        # print(current_user)
        title = request.GET.get('title', None)
        if title is not None:
            flag_obj = Flag.filter(title__icontains=title)
        
        flag_serializers = FlagSerializer(flag_obj, many=True)
        return JsonResponse(flag_serializers.data, safe=False)

    #create and save flag record
    # def post(self,request,format=None):        
    #     def add_user_data(data,user):
    #             data['profile']=user.id
    #             return data
    #     flag_serializer = FlagSerializer(data=add_user_data(request.data,request.user))
    #     if flag_serializer.is_valid():
    #         flag_serializer.save()
    #         return Response(flag_serializer.data, status=status.HTTP_201_CREATED) 
    #     return Response(flag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FlagDetail(APIView):
    '''
    class to define view for the api endpoint that gets,updates and deletes specific red flag records 
    '''
    permission_classes = (IsAuthenticated,)
    def get(self,request,pk):
    #retreive flag record by ID

        try:
            flag_obj=Flag.objects.get(pk=pk)
        
            flag_serializer=FlagSerializer(flag_obj)
            return Response(flag_serializer.data, status= status.HTTP_200_OK)
        except Flag.DoesNotExist:
            return Response({'detail': 'Flag Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 
        
    def put (self,request,pk):
        flag_obj=Flag.objects.get(id=pk)  
        def add_user_data(data,user):
            data._mutable=True
            data['user']=1
            data._mutable=False
            return data

        flag_serializer=FlagSerializer(flag_obj,data=add_user_data(request.data,request.user))
        print(flag_serializer)
        data={}
        if flag_serializer.is_valid():
            flag_serializer.save()
            return Response(flag_serializer.data, status=status.HTTP_200_OK)
        return Response(flag_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
         
    def delete(self,request,pk):
        # delete a flag by ID
        try:
            flag_obj=Flag.objects.get(id=pk)
            flag_obj.delete()
            return Response({'detail': 'Flag  was deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Flag.DoesNotExist:
            return Response({'detail': 'Flag does not exist.'}, status=status.HTTP_404_NOT_FOUND)   

class TagList(generics.ListCreateAPIView):
    """
    Create tag and list all tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update and delete tag
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,) 
        




