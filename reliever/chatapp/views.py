from django.shortcuts import render
from .models import ChatSave
# Create your views here.
from myapp.models import Doctor,UserSave

def index(request,doc_user=None):
	if request.method == "POST":
		message = request.POST['message']
		from_user = request.user

		is_doctor = Doctor.objects.filter(username=from_user)
		if is_doctor:
			is_doctor =True
		else:
			is_doctor = False

		to_user = doc_user
		print(is_doctor)
		ChatSave(from_user=from_user,to_user=to_user,message=message,is_doctor=is_doctor).save()
		#same user right
		total_mess = []
		my_messages = fetch_10_message(from_user,to_user)
		op_messages= fetch_10_message(to_user,from_user)
		for i in my_messages:
			i.append(True)
			total_mess.append(i)
		for i in op_messages:
			i.append(False)
			total_mess.append(i)
		total_mess.sort()
		
		context = {
			'curr_user': from_user,
			'username':from_user,
			'total_mess':total_mess,
			'other_user': to_user,
			}
		return render(request,'chatapp/chatview.html',context)
	else:
		from_user = request.user
		to_user = doc_user
		total_mess = []
		my_messages = fetch_10_message(from_user,to_user)
		op_messages= fetch_10_message(to_user,from_user)
		for i in my_messages:
			i.append(True)
			total_mess.append(i)
		for i in op_messages:
			i.append(False)
			total_mess.append(i)
		total_mess.sort()

		context = {
			'curr_user': from_user,
			'username':from_user,
			'total_mess':total_mess,
			'other_user': to_user,
			}
		return render(request,'chatapp/chatview.html',context)



def fetch_10_message(from_user,to_user):
	message = []
	cho = list(ChatSave.objects.filter(from_user=from_user, to_user=to_user))[-10:]
	for i in cho:
		message.append([str(i.current_time)[:19],i.message])
	return message