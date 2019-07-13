#instlling tkinter module into system
from tkinter import *
#for dialog box
from tkinter import messagebox
#for database access
import pymysql
#if like to save into file
import os

#components of window :
#creating an object
root = Tk()

#defining size to window
root.geometry('1200x720')

#prevents resizing the window
root.resizable(False,False)

#title to window
root.title("Hospital Management System")

#creating database connection
db = pymysql.connect("localhost","root","root","HMS",port=8889)

#making cursor to keep track for queries
cur=db.cursor()


# labels & entries

#creating left frame for labels and entries
left_frame = Frame(root, width=800, height=720)
left_frame.pack(side=LEFT)

#creating right frame for displaying appointments
right_frame = Frame(root, width=400, height=720, bg='steelblue')
right_frame.pack(side=RIGHT)


#inserting image to window
photo = PhotoImage(file="abcd2.png")
label_image= Label(left_frame, image=photo)
label_image.pack()


#creating heading in left frame
heading = Label(left_frame, text="Royal Hospital & Heart Center",font=("arial 35 bold ") , fg='orangered2' )
heading.place(x=140,y=10)


#creating label for name
label_name = Label(left_frame, text="Patient's Name", font=('arial 20 bold'), fg='darkgreen' )
label_name.place(x=100, y=150)

#creating entry for name
entry_name = Entry(left_frame, width=30)
entry_name.place(x=350,y=150)


#creating label for age
label_age = Label(left_frame, text="Age", font=('arial 20 bold'),fg='darkgreen')
label_age.place(x=100,y=200)

#creating entry for age
entry_age = Entry(left_frame, width=30)
entry_age.place(x=350,y=200)


#creating label for gender
label_gender = Label(left_frame, text="Gender", font=('arial 20 bold'),fg='darkgreen')
label_gender.place(x=100,y=250)

#creating dropdown option for gender
var = StringVar()
list1=['Male','Female','Transgender']
drop_list = OptionMenu(left_frame, var , *list1)
var.set("Select Gender")
drop_list.config(width=20)
drop_list.place(x=350, y=250)


#creating label for phone number
label_phone_no = Label(left_frame, text = "Phone Number", font=('arial 20 bold'),fg='darkgreen')
label_phone_no.place(x=100,y=300)

#creating entry for phone number
entry_phone_no = Entry(left_frame,width=30)
entry_phone_no.place(x=350,y=300)

#creating label for location
label_location = Label(left_frame, text="Location", font=('arial 20 bold'),fg='darkgreen')
label_location.place(x=100,y=350)

#creating entry for loaction
entry_location = Entry(left_frame,width=30)
entry_location.place(x=350,y=350)

#creating label for appointment time
label_time = Label(left_frame, text = "Appointment Time", font=('arial 20 bold'), fg='darkgreen')
label_time.place(x=100,y=400)

#creating entry for appointment time
entry_time = Entry(left_frame, width=30)
entry_time.place(x=350,y=400)



#creating an empty list to append appointments later on to display
ids = []

#creating box for displaying entries
box = Text(right_frame, width=50, height=40)
box.place(x=20,y=50)

label_box = Label(right_frame, text = "Logs :",font=('arial 20 bold'), fg="lightgreen",bg="steelblue")
label_box.place(x=15,y=15)


#getting number of appointments fixed from server
sql2 = "SELECT id FROM Patient_details"
cur.execute(sql2)
result = cur.fetchall()
# to print number of rows
for row in result :
    id_to_add = row[0]
    ids.append(id_to_add)


#ordering ids in ascending order
id_sort = sorted(ids)
final_id = id_sort[len(ids)-1]

#printing number of appointments till now
box.insert(END,"Total appointment till now : " + str(final_id) )
box.insert(END,"\n")


#fucntions to call when add button is clicked
def submit():
    name=entry_name.get()
    age=entry_age.get()
    gender=var.get()
    phone=entry_phone_no.get()
    location=entry_location.get()
    time=entry_time.get()

    #throwing error if any blanks is null
    if (name=="" or age=="" or  phone=="" or location=="" or time=="") :
        messagebox.showerror("Character_Error","Please fill in all the boxes")
        print("You haven't filled all the blanks")
    #checking the appointment time in database, if same time is inserted, throws warning
    else:
        #searching in database for exisitng timing
        sql="SELECT * FROM Patient_details WHERE appt_time ='{}'".format(time)
        #executing above query
        cur.execute(sql)
        #keep counting all all rows with above query
        cur.fetchall()
        #fetching number of count of exisitng appt time
        data = cur.rowcount 
        print("Number of same entry available = ",data)
        #if row count is zero, then add the deatils into database
        if (data == 0) :
            sql1 = "INSERT INTO Patient_details(patient_name,age,gender,phone_number,location,appt_time) VALUES('{}','{}','{}','{}','{}','{}')".format(name,age,gender,phone,location,time)

            try :
                cur.execute(sql1)
                db.commit()
                messagebox.showinfo("Done","{}'s appointment is fixed with Dr. Akshit at {}".format(name,time))

            except :
                db.rollback()

            #getting number of appointments fixed from server
            sql2 = "SELECT id FROM Patient_details"
            cur.execute(sql2)
            result = cur.fetchall()
            # to print number of rows
            for row in result :
                id_to_add = row[0]
                ids.append(id_to_add)


            #ordering ids in ascending order
            id_sort = sorted(ids)
            final_id = id_sort[len(ids)-1]

            #adding appointments into the text box after fixing the appt time
            box.insert(END, "\nAppointment fixed for {} at {}".format(name,time))      
             
        #if rowcount is not equal to zero, that means appointment aready exists at that time
        else :
            messagebox.showwarning("Already Exists","Sorry {}, Dr. Akshit is not available at {}".format(name,time))



#creating button for add appointment
submit_button = Button(left_frame, text="Add  Appointment",font=("arial 15 bold"), width=20, height=3,highlightbackground="lightgreen" ,fg="black",command=submit)
submit_button.place(x=300,y=480)


#additional labels
label_1 = Label(left_frame, text="Your Family Superspeciality Hospital", font="Helvetica 20 italic", fg='purple')
label_1.place(x=210,y=60)


#exiting the window
def quit():
    root.quit()

button_2 = Button(left_frame, text="X",width=3, height=2, command=quit)
button_2.place(x=775,y=0)

# function to define to clear all entries once uploaded to server
def clear():
    entry_name.delete(0,END)
    entry_age.delete(0,END)
    var.set("Select Gender")
    entry_phone_no.delete(0,END)
    entry_location.delete(0,END)
    entry_time.delete(0,END)

#creating clear button to delete all data once stored into server
button_3 = Button(left_frame, text="CLEAR_All",width=15,font=("arial 15 bold"),highlightbackground="grey" ,fg="black",command=clear)
button_3.place(x=650,y=150)


#defining function to search data by entering name in entry_name
def search_for():
    intput = entry_name.get()
    #print(intput)
    sql3 ="SELECT * FROM Patient_details WHERE patient_name LIKE %s" 
    cur.execute(sql3,(intput,))
    data = cur.fetchall()
    #print(data)
    count = cur.rowcount
    #print(count)

    if count == 0 :
        messagebox.showwarning("Not Found","{} does not exists in our database".format(intput))

    else :    
        for row in data :
            _age_ = row[2]
            _gender_ = row[3]
            _phone_ = row[4]
            _loc_ = row[5]
            _time_ = row[6]
        #printing the data in entry
        entry_age.insert(END, str(_age_))
        var.set(_gender_)
        entry_phone_no.insert(END, (_phone_))
        entry_location.insert(END, str(_loc_))
        entry_time.insert(END, str(_time_))

        #printing the data found after the search
        box.insert(END, "\n")
        box.insert(END, "\nPatient's Details :")
        box.insert(END, "\nName : "+str(row[1]))
        box.insert(END, "\nAge : "+str(_age_))
        #box.insert(END, "\nGender : "+str(row[1]))
        box.insert(END, "\nPhone Number : "+str(_phone_))
        box.insert(END, "\nLocation: "+str(_loc_))
        box.insert(END, "\nAppointment Time : "+str(_time_)) 
        box.insert(END, "\n")                       

#creating button to search
button_6 = Button(left_frame,text="SEARCH", width=20,font=("arial 15 bold"),highlightbackground="lightgreen" ,fg="black",command=search_for)
button_6.place(x=60,y=600)


#defining update function where, name enter by user gets update by every field of entries
def update_all():
    updated_name = entry_name.get()                 #updated name
    updated_age = entry_age.get()                   #updated age
    updated_phone = entry_phone_no.get()            #updated phone number
    updated_location = entry_location.get()         #updated location
    updated_time = entry_time.get()                 #updated appointment time

    sql4 = "UPDATE Patient_details SET patient_name=%s , age=%s , phone_number=%s , location=%s , appt_time=%s WHERE patient_name LIKE %s"
    cur.execute(sql4, (updated_name, updated_age, updated_phone, updated_location, updated_time, entry_name.get(), ))
    data = cur.fetchall()
    db.commit()
    messagebox.showinfo("Success","Data has been updated successfully for {}".format(updated_name))

    box.insert(END, "\n")
    box.insert(END, "Updated Data of {}".format(updated_name))
    box.insert(END, "\nName : {}".format(updated_name))
    box.insert(END, "\nAge : {}".format(updated_age))
    #box.insert(END, "\nGender : {}".format(var.set())
    box.insert(END, "\nPhone Number : {}".format(updated_phone))
    box.insert(END, "\nLocation: {}".format(updated_location))
    box.insert(END, "\nAppointment Time : {}".format(updated_time))  
    box.insert(END,"\n")             

#creating update button 
button_5 = Button(left_frame, text="UPDATE",width=20,font=("arial 15 bold"),highlightbackground="lightgreen" ,fg="black",command=update_all)
button_5.place(x=320,y=600)


#creating function to delete particular entry from database
def delete_all():
    #delete appointment query
    intput_1 = entry_name.get()
    sql5 = "DELETE FROM Patient_details WHERE patient_name LIKE %s"
    
    try :
        cur.execute(sql5, (intput_1,))
        db.commit()
        print("Deleted Successfully")
        messagebox.showinfo("Deleted","{}'s appointment has been canceled".format(intput_1))

        #clear all entries once appointment is deleted
        entry_name.delete(0,END)
        entry_age.delete(0,END)
        var.set("Select Gender")
        entry_phone_no.delete(0,END)
        entry_location.delete(0,END)
        entry_time.delete(0,END)

        #printing in box
        box.insert(END,"\n")
        box.insert(END,"Apointment has been cancelled")

    except :
        db.rollback()

#button to cancel appointment
button_4 = Button(left_frame,text="DELETE", width=20,font=("arial 15 bold"),highlightbackground="lightgreen" ,fg="black",command=delete_all)
button_4.place(x=580,y=600)

#binding all functions and running
root.mainloop()