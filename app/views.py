from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail


# Create your views here.

def index(request):
    # tourPlaces.objects.all().delete()
    # addHotelsModel.objects.all().delete()
    return render(request, 'index.html')

def home(request):
    login = request.session.get('login')  
    places_list = tourPlaces.objects.all()
    print(places_list)  
    paginator = Paginator(places_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'login': login,
        'places': page_obj,       
        'page_obj': page_obj,
    }
    return render(request, 'home.html', context)

def userRegistration(request):
    if request.method == 'POST':
        userName = request.POST.get('userName')
        userEmail = request.POST.get('userEmail')
        password = request.POST.get('password')
        confirmPass = request.POST.get('confirmPass')
        addresh = request.POST.get('addresh')
        contact = request.POST.get('contact')
        profilePic = request.FILES.get('profilePic')

        # Basic server-side validation
        if password != confirmPass:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')
        
        checkMail = userModel.objects.filter(userEmail=userEmail).exists()
        if checkMail:
           messages.error(request, "Mail alredy in use")
           return redirect('userRegistration') 


        # Create user
        user = userModel(
            userName=userName,
            userEmail=userEmail,
            password=password,  # Note: In production, use proper password hashing
            confirmPass=confirmPass,
            addresh=addresh,
            contact=contact,
            profilePic=profilePic if profilePic else None
        )
        user.save()
        messages.success(request, "Registration successful!")
        return redirect('login')  # Redirect to login page after successful registration
    return render(request, 'userRegistration.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        data=userModel.objects.filter(userEmail=email,password=password).exists()
        if data:
            data1=userModel.objects.get(userEmail=email)
            request.session['email']=email
            request.session['login']='user'
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')
    return render(request, 'login.html')

def adminLogin(request):
    if request.method == 'POST':
        adminEmail = request.POST.get('email')
        password = request.POST.get('password')
        if adminEmail == 'admin@gmail.com' and password == 'admin':
            request.session['email']='admin@gmail.com'
            request.session['login']='admin'
            return redirect('home')
    return render(request, 'adminLogin.html')

def about(request):
    return render(request, 'about.html')

def logout(request):
    del request.session['login']
    del request.session['email']
    return redirect('index')

def addPlaces(request):
    login = request.session['login']
    if request.method == 'POST':
        placeName = request.POST.get('placeName')
        placeLocation = request.POST.get('placeLocation')
        country = request.POST.get('country')
        description = request.POST.get('description')
        picture = request.FILES['picture']
        state = request.POST.get('state')
        placeType = request.POST.get('placetype')
        tourPlaces.objects.create(
            placeName=placeName,
            placeLocation=placeLocation,
            Country=country,
            placePic=picture,
            description=description,
            state=state,
            placeType=placeType
        )
        messages.success(request, 'Place added successfully')
        return render(request, 'addPlaces.html', {'login':login})
    return render(request, 'addPlaces.html', {'login':login})

def appPlans(request):
    login = request.session['login']
    if request.method == 'POST':
        From = request.POST.get('From')
        TO = request.POST.get('TO')
        datetime_str = request.POST.get('time')
        print('fffffffff',datetime_str)
        state = request.POST.get('state')
        country = request.POST.get('country')
        fName = request.POST.get('fName')
        picture = request.FILES['picture']
        price = request.POST.get('price')

        addFlightsModel.objects.create(
            From=From,
            To=TO,
            state=state,
            Country=country,
            ticketPrice=price,
            flightName=fName,
            time=datetime_str,
            flightPic=picture

        )
        messages.success(request, 'Flight added successfully')
        return render(request, 'appPlans.html', {'login':login})
    return render(request, 'appPlans.html', {'login':login})

def addHotels(request):
    login = request.session['login']
    if request.method == 'POST':
        Name = request.POST.get('Name')
        Location = request.POST.get('Location')
        state = request.POST.get('state')
        country = request.POST.get('country')
        Price = request.POST.get('Price')
        picture = request.FILES['picture']
        addHotelsModel.objects.create(
            hotelName=Name,
            Location=Location,
            Country=country,
            hotelPic=picture,
            price=Price,
            state=state
        )
        messages.success(request, 'Hotel added successfully')
        return render(request, 'addHotels.html', {'login':login})
    return render(request, 'addHotels.html', {'login':login})


def addCars(request):
    login = request.session['login']
    if request.method == 'POST':
        Name = request.POST.get('Name')
        Location = request.POST.get('Location')
        state = request.POST.get('state')
        country = request.POST.get('country')
        Price = request.POST.get('Price')
        picture = request.FILES['picture']
        carModel.objects.create(
            carCompany=Name,
            state=state,
            Location=Location,
            Country=country,
            carPic=picture,
            price=Price,
        )
        messages.success(request, 'Vehicle added successfully')
        return render(request, 'addCars.html', {'login':login})
    return render(request, 'addCars.html', {'login':login})

def addHospitals(request):
    login = request.session['login']
    if request.method == 'POST':
        Name = request.POST.get('Name')
        Location = request.POST.get('Location')
        state = request.POST.get('state')
        country = request.POST.get('country')
        picture = request.FILES['picture']
        emergency_mail = request.POST.get('emergencyMail')
        address = request.POST.get('address')
        HospitalModel.objects.create(
            hospitalName=Name,
            state=state,
            Location=Location,
            Country=country,
            hospitalPic=picture,
            h_emergency_mail=emergency_mail,
            Address=address
        )
        messages.success(request, 'Hospital added successfully')
        return render(request, 'addHospitals.html', {'login':login})
    return render(request, 'addHospitals.html', {'login':login})

def viewUsers(request):
    login = request.session['login']
    allUsers = userModel.objects.all()
    # Set up pagination (e.g., 6 users per page)
    paginator = Paginator(allUsers, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'viewAllUsers.html', {'allUsers': page_obj, 'login':login})

def removeUser(request, id):
    getUser = userModel.objects.get(userID=id)
    if getUser:
        getUser.delete()
        messages.success(request, 'User removed successfully')
        return redirect('viewUsers')
    else:
        messages.success(request, 'User not found')
        return redirect('viewUsers')
    
def userProfile(request):
    userMail = request.session['email']
    login = request.session['login']
    userInfo = userModel.objects.get(userEmail=userMail)
    return render(request, 'userProfile.html', {'user':userInfo, 'login':login})

def viewPlaces(request):
    login = request.session.get('login')
    destination = request.POST.get('destination') if request.method == 'POST' else None

    if destination:
        places_list = tourPlaces.objects.filter(placeName__iexact=destination).order_by('Country')
    else:
        places_list = tourPlaces.objects.all().order_by('Country')

    paginator = Paginator(places_list, 3)  # Show 3 places per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'login': login,
        'page_obj': page_obj,
        'search_query': destination  # pass search text for showing if needed
    }
    return render(request, 'viewPlaces.html', context)

def viewFlights(request):
    userMail = request.session['email']
    login = request.session['login']
    request.session['Payment_for'] = 'Flight_Booking'
    flights = addFlightsModel.objects.filter(status='Available')
    if request.method == "POST":
        startsFrom = request.POST.get('from')
        to = request.POST.get('to')
        passengers = request.POST.get('passengers')
        print('ddddddddddd')
        flights = addFlightsModel.objects.filter(From__iexact=startsFrom, To__iexact=to, status='Available')
        return render(request, 'viewFlights.html', {'login':login, 'flights':flights})
    return render(request, 'viewFlights.html', {'login':login, 'flights':flights})

def view_and_book_cars(request):
    userMail = request.session['email']
    login = request.session['login']
    all_Vehicles = carModel.objects.all()
    request.session['Payment_for'] = 'Cab_Booking'
    if request.method == 'POST':
        pickUpLocation = request.POST.get('pickup')
        passengers = request.POST.get('passengers')
        Vehicles = carModel.objects.filter(Location__iexact=pickUpLocation)
        return render(request, 'carBookings.html', {'login':login, 'all_Vehicles':Vehicles})

    return render(request, 'carBookings.html', {'login':login, 'all_Vehicles':all_Vehicles})


def viewHotels(request):
    userMail = request.session['email']
    login = request.session['login']
    hotels = addHotelsModel.objects.all()
    request.session['Payment_for'] = 'Hotel_Booking'
    if request.method == "POST":
        location = request.POST.get('Location')
        price = request.POST.get('price')
        hotels = addHotelsModel.objects.filter(Location__iexact=location)
        return render(request, 'viewHotels.html', {'login':login, 'hotels':hotels})
    return render(request, 'viewHotels.html', {'login':login, 'hotels':hotels})

def viewHospitals(request):
    login = request.session['login']
    hospitals = HospitalModel.objects.all()
    if request.method == 'POST':
        hLocation = request.POST.get('location')
        hospitals = HospitalModel.objects.filter(Location__icontains=hLocation)
        return render(request, 'viewHospitals.html', {'login':login, 'hospitals':hospitals})
    return render(request, 'viewHospitals.html', {'login':login, 'hospitals':hospitals})

def destinations(request):
    login = request.session['login']
    destination = request.POST.get('destination', '')
    
    if destination:
        places_list = tourPlaces.objects.filter(placeName__iexact=destination).order_by('Country')
    else:
        places_list = tourPlaces.objects.all().order_by('Country')
    paginator = Paginator(places_list, 6)  # Show 3 places per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'destinations.html',{'login':login, 'page_obj':page_obj})

def destdetails(request, placeID):
    login = request.session['login']
    place = tourPlaces.objects.filter(placeID=placeID)
    return render(request, 'destination_details.html',{'place':place, 'login':login})


def addsubplaces(request, placeID):
    login = request.session['login']
    place = tourPlaces.objects.get(placeID=placeID)
    
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        image = request.FILES['image']
        placetype = request.POST.get('placetype')
        # Save the image in the static folder (be careful with user-uploaded files)
        # image_paths=[]
        # Ensure the places_images directory exists inside the static directory
        places_images_dir = os.path.join(settings.BASE_DIR, 'static', 'places_images')
        os.makedirs(places_images_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Save each uploaded image and add its path to the image_paths list
       
            # Create the image path relative to static/places_images/
        image_path = os.path.join('static/places_images/', image.name)  # Path relative to static
        print(image_path)
        # n=random.randint(1111,9999)
        # Save the image in the static folder (be careful with user-uploaded files)
        with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
            for chunk in image.chunks():
                img_file.write(chunk)

            # Add the image path to the list (stored as a string in JSONField)
        # image_paths.append({'imgpath':image_path})

        # Create a new Place with the saved image paths
        place.places.append({'placename': name , 'location':location, 'desc':desc, 'img':image_path, 'placetype':placetype})
        
        place.save()
       

        messages.success(request, 'Tourism Place added successfully!')
        return redirect('addsubplaces', placeID)
        
    return render(request, 'addsubplaces.html',{'login':login, 'id':id})


def addfoods(request, placeID):
    login = request.session['login']
    place = tourPlaces.objects.get(placeID=placeID)
 
    if request.method == 'POST':
        restname = request.POST['restname']
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        image = request.FILES['image']
        
        # Save the image in the static folder (be careful with user-uploaded files)
        # image_paths=[]
        # Ensure the places_images directory exists inside the static directory
        places_images_dir = os.path.join(settings.BASE_DIR, 'static', 'places_images')
        os.makedirs(places_images_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Save each uploaded image and add its path to the image_paths list
       
            # Create the image path relative to static/places_images/
        image_path = os.path.join('static/places_images/', image.name)  # Path relative to static
        print(image_path)
        # n=random.randint(1111,9999)
        # Save the image in the static folder (be careful with user-uploaded files)
        with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
            for chunk in image.chunks():
                img_file.write(chunk)

            # Add the image path to the list (stored as a string in JSONField)
        # image_paths.append({'imgpath':image_path})

        # Create a new Place with the saved image paths
        place.restaurants.append({'restname':restname,'foodname': name , 'location':location, 'desc':desc, 'img':image_path})
        place.save()
       

        messages.success(request, 'Food or Restaurent added successfully!')
        return redirect('addfoods', placeID)
    return render(request, 'addfoods.html',{'login':login,'id':id})


def deleteplace(request, id, jid):
    login = request.session['login']
    place = tourPlaces.objects.get(placeID=id)
    data = place.places
    del data[int(jid-1)]
    
    place.save()
    messages.success(request, 'Place Deleted Successfully!')
    return redirect('destdetails', id)

def deletefoods(request, id, jid):
    login = request.session['login']
    food = tourPlaces.objects.get(placeID=id)
    data = food.restaurants
    del data[int(jid-1)]
    
    food.save()
    messages.success(request, 'Restaurents or Food Deleted Successfully!')
    return redirect('destdetails', id)

def placesingledest(request, placeID, jid):
    login=request.session['login']
    place=tourPlaces.objects.get(placeID=placeID)
    
    data = place.places[int(jid-1)]
    print('ffffff', data)
    # del data['']
    return render(request, 'placesingledest.html',{'login':login, 'data':data})

def foodsingledest(request, placeID, jid):
    login=request.session['login']
    place=tourPlaces.objects.get(placeID=placeID)
    data = place.restaurants[int(jid-1)]
    return render(request, 'foodsingledest.html',{'login':login, 'data':data})

def payment(request, id):
    # Retrieve session data
    login = request.session.get('login')
    email = request.session.get('email')
    payment_for = request.session.get('Payment_for')

    try:
        getUserDetails = userModel.objects.get(userEmail=email)
    except userModel.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')  
    if request.method == 'POST':
        amount = request.POST.get('amount')
        card_number = request.POST.get('cardNumber')  

        # Debug or store info
        print("Payment received from:", email)
        print("Amount:", amount)
        print("Card Last 4 Digits:", card_number)

        PaymentModel.objects.create(
            payment_for=payment_for,
            Booking_ID=id,
            paymenter_name=getUserDetails.userName,
            paymenter_mail=email,
            card_no=card_number,
            paid_amount=amount
        )
        messages.success(request, f'Payment of ${amount} submitted successfully.')
        return render(request, 'payment.html', {'login': login, 'id':id})

    return render(request, 'payment.html', {'login': login, 'id':id})



def chatbot_page(request):
    return render(request, 'chatbot.html')


import json, re

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '').lower()
        print('User said:', user_input)

        hospitals_locations = HospitalModel.objects.values_list('Location', flat=True)

        # Helper for regex exact word match
        def match_words(words):
            return any(re.search(rf'\b{re.escape(word)}\b', user_input) for word in words)

        # Rule-based replies
        if match_words(['hi','hii', 'hello', 'good morning', 'good evening']):
            reply = " Hello!...."

        elif "how are you" in user_input:
            reply = "I am Good, Thanks for Asking. How can I help You?"

        elif match_words([
            "i have a high body temperature and headache",
            "hey, i'm feeling very tio and tired",
            "my health condition is not good at all",
            "i have fever today",
            "just a little tired, no fever",
            "fever",
            "i have high body temperature"
        ]):
            reply = "I can understand that. Tell me more about your symptoms?"

        elif "restless" in user_input or "ankle pain" in user_input:
            reply = "It seems you have akathisia. Consult a nearby hospital immediately. You may consider mirtazapine or trazodone."

        elif "irritable" in user_input or "no sleep" in user_input:
            reply = "These are bipolar disorder symptoms. In emergency, consult a psychiatrist. Medications like antipsychotics and anticonvulsants may help."

        elif "racing heart" in user_input or "chest pain" in user_input:
            reply = "You may be having a panic attack. Try to stay calm and take antidepressants after food if prescribed. Want hospital suggestions?"

        elif "headache" in user_input or "stress" in user_input or "cold" in user_input or "throat infection" in user_input:
            reply = "You may have anxiety disorder. Relax, and please consult a psychiatrist."

        elif "hospital" in user_input and "near" in user_input:
            reply = "Please share your city or area for nearby hospital details."

        elif any(loc.lower() in user_input for loc in hospitals_locations):
            matched_location = next((loc for loc in hospitals_locations if loc.lower() in user_input), None)
            if matched_location:
                near_hospitals = HospitalModel.objects.filter(Location__iexact=matched_location)
                addresses = list(near_hospitals.values_list('Address', flat=True))
                if addresses:
                    reply_lines = [f"{idx+1}. {addr}" for idx, addr in enumerate(addresses)]
                    reply = f"Here are the hospitals in {matched_location}:\n" + "\n".join(reply_lines)
                else:
                    reply = f"Sorry, I couldn't find hospitals in {matched_location}."
            else:
                reply = "Location matched but failed to retrieve details."

        elif match_words([
            "hotel", "hotel address", "i need best hotel near me", "hotels near me",
            "can you find me a hotel near me?", "tell me hotel address nearby",
            "best hotels around here", "any hotels close to me?", "suggest some nearby hotels",
            "hotel suggestion in this area", "need hotel info in my location",
            "hotels nearby", "cheap hotel near me", "luxury hotel near me",
            "hotel options near my area"
        ]):
            reply = "Please share your city or area for nearby hotel details."

        elif match_words([
            "show me hills", "i want to visit hills", "suggest some beaches", "take me to the beach",
            "i love nature spots", "give me nature places", "i want to go to the desert", "desert destinations?",
            "suggest historic places", "any historic sites nearby?", "where can i find beaches?",
            "best hills to travel", "places with nature views", "nature and scenic places",
            "show me desert attractions", "tell me historic monuments", "i want a beach trip",
            "desert safari options?", "good hills for hiking?", "any natural destinations?"
        ]):
            place_type_mapping = {
                "hill": ["hill", "hills", "mountain", "hill station"],
                "beach": ["beach", "beaches", "sea", "coast"],
                "nature": ["nature", "natural", "scenic", "greenery"],
                "desert": ["desert", "dunes", "sand", "arid"],
                "historic": ["historic", "monument", "heritage", "ancient"]
            }

            matched_type = None
            for type_name, keywords in place_type_mapping.items():
                if match_words(keywords):
                    matched_type = type_name
                    break

            if matched_type:
                suggestions = tourPlaces.objects.filter(placeType__icontains=matched_type).order_by('?')[:3]
                if suggestions.exists():
                    reply = f"Here are some recommended {matched_type} places:\n"
                    for idx, place in enumerate(suggestions, start=1):
                        reply += f"{idx}. {place.placeName} in {place.placeLocation} - {place.description[:80]}...\n"
                else:
                    reply = f"Sorry, no {matched_type} places found in our database."
            else:
                reply = "Please mention what kind of place you're looking for: hills, beaches, nature, desert, or historic."

        else:
            reply = "Sorry, I didn't understand that. Could you rephrase or share more info?"

        return JsonResponse({'reply': reply})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



def RemoveFlight(request, id):
    getFlight = addFlightsModel.objects.get(flightId=id)
    getFlight.delete()
    messages.success(request, 'flight removed successfully')
    return redirect(viewFlights)

def removeVehicles(request, id):
    getVehicle = carModel.objects.get(carId=id)
    getVehicle.delete()
    messages.success(request, 'Vehicle removed successfully')
    return redirect(view_and_book_cars )

def removeHospitals(request, id):
    getHospital = HospitalModel.objects.get(hospitalId=id)
    getHospital.delete()
    messages.success(request, 'hospital removed successfully')
    return redirect(viewHospitals)

def viewEmargencyMails(request, hospital_mail):
    login = request.session.get('login')
    email = request.session.get('email')
    getUser = userModel.objects.get(userEmail=email)
    subject = "🚨 Emergency Alert Notification"
    message = "This is an automated emergency alert. Please take immediate action."
    recipients = [hospital_mail]
    send_mail(subject, message, settings.EMAIL_HOST_USER,recipients)
    emergencyMail.objects.create(
        hospitalMail=hospital_mail,
        userEmail=email
    )
    messages.success(request, 'mail sended successfully')
    return redirect('viewHospitals')

def viewAllEmergencyMails(request):
    login = request.session.get('login')
    allEmergencyMails = emergencyMail.objects.all()
    return render(request, 'viewEmergencyMails.html', {'login':login, 'emergency_mails':allEmergencyMails})

def deleteTourPlaces(request, id):
    getTourPlace = tourPlaces.objects.get(placeID=id)
    getTourPlace.delete()
    messages.success(request, 'Tour places deleted successfully')
    return redirect(destinations)
