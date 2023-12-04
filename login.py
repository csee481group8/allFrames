import tkinter as tk #py 3.x
from tkinter import *
import Authentication as auth
import SignUp as sgn


def signup_frame(Signup_frame):
     ########## sign up page content
     # set the label geometry and font size in the sign in page
    lb_0 = Label(Signup_frame, text="AGELink Sign Up",width=20,font=("bold", 20))  
    lb_0.place(x=90,y=53)
    lb_0.pack()

    # set the username label
    lb_2 = Label(Signup_frame, text="User Name",width=35,font=("bold", 15))  
    lb_2.place(x=120,y=180) 
    # the username entry box
    etr_01 = Entry(Signup_frame)  
    etr_01.place(x=120,y=220)
    enty1 = etr_01.get()
    lb_2.pack() 
    etr_01.pack()
    # set the password label
    lb_3 = Label(Signup_frame, text="Password",width=35,font=("bold", 15))  
    lb_3.place(x=140,y=180)  
    # the password entry box
    etr_02 = Entry(Signup_frame)  
    etr_02.place(x=140,y=220)
    enty2 = etr_02.get()
    lb_3.pack()
    etr_02.pack()
    # set the email label
    lb_4 = Label(Signup_frame, text="email",width=35,font=("bold", 15))  
    lb_4.place(x=160,y=180)  
    # the email entry box
    etr_03 = Entry(Signup_frame)  
    etr_03.place(x=160,y=220)
    enty3 = etr_03.get()
    lb_4.pack()
    etr_03.pack()
    # pass the user entry to sign up function
    Register_btn=Button(Signup_frame,text='Register',bd='5',width=15,bg='yellow',fg='black',
                command=lambda:sgn.sign_up(enty1,enty2,enty3)).place(x=240,y=230)
    
    Signup_frame.pack()
    Signup_frame.mainloop()

def login():
    # initialize a base window with title AGELink and size 800*800, has sign-in form
    login = tk.Tk()
    login.geometry('800x800')
    login.title("AGELink/Login")

    SignUp_frame =Frame(login) #signup frame
    Home_frame = Frame (login) #home frame

    ########## login page content
    # set the label geometry and font size in the sign in page
    labl_0 = Label(login, text="AGELink",width=20,font=("bold", 20))  
    labl_0.place(x=90,y=53)
    labl_0.pack()
    # set the notice label
    labl_1 = Label(login, text="Notice: AGELink follows the AI bill of rights.",width=100,font=("bold", 10))  
    labl_1.place(x=100,y=180)
    labl_1.pack()
    # set the username label
    labl_2 = Label(login, text="User Name",width=35,font=("bold", 15))  
    labl_2.place(x=120,y=180) 
    # the username entry box
    entry_01 = Entry(login)  
    entry_01.place(x=120,y=220)
    en1 = entry_01.get()
    labl_2.pack() 
    entry_01.pack()
    # set the password label
    labl_3 = Label(login, text="Password",width=35,font=("bold", 15))  
    labl_3.place(x=140,y=180)  
    # the password entry box
    entry_02 = Entry(login)  
    entry_02.place(x=140,y=220)
    en2 = entry_02.get()
    labl_3.pack()
    entry_02.pack()
   
    # initialize the radiobutton variable with a default 0 
    var = IntVar()
    # initialize variable acknowledge
    global ack_clicked
    ack_clicked = 0

    # define function that stores the updated var radio button status
    def on_acknowledge_click():
        ack_clicked = var.get()
        print("Acknowledgment Status:", ack_clicked)

    # create a radio button with text and geometry
    Radiobutton(login,text="I acknowledge",padx = 5, variable=var, value=1, command=on_acknowledge_click).place(x=100,y=130)

    ########## home page content
    # initialize other function frames
    Chat_frame = Frame(Home_frame) #chat
    Video_frame = Frame(Home_frame) #video call
    Other_frame = Frame(Home_frame) #Other
    Game_frame = Frame(Home_frame) #game

    # A Label
    lb1  = Label(Home_frame,text ="This is the home window").place(x=0)
        # content widgets such as chatbot and chat functions
        # with data center being a hidden side bar
        # until cursor hovers over/finger taps on the left corner
        
    btnAI = Button(Home_frame, text = "Voice Chat", width= 40, height=15, padx=10,pady=10,
                        command=lambda:Chat_frame.tkraise()).place(x=50,y=50)
    btnCall = Button(Home_frame, text = "Video Call", width= 40,height=15,padx=10,pady=10,
                            command=lambda:Video_frame.tkraise()).place(x=450,y=50)
    btnDrop = Button(Home_frame, text = "Game", width= 40, height=15, padx=10,pady=10,
                            command=lambda:Game_frame.tkraise()).place(x=50,y=350)
    btnMood = Button(Home_frame, text = "Mood Prediction", width= 40, height=15,padx=10,pady=10,
                            command=lambda:Other_frame.tkraise()).place(x=450,y=350)
    
    Home_frame.pack(pady=10)
    # call authentication and store returned value in this variable
    matched = auth.auth(en1,en2)

    # define match_ack with paramenter match and parameter ack_clicked
    # if meet, return True
    def matched_acked(match,ack):
        if match==True & ack == 1:
            print("matched and acked.")
            Home_frame.lift()
        else:
            print("wrong user account/password entered or not ackknoledged.")

    # create a button that opens home page, if condition meets
    Go_btn=Button(login,text='Let\'''s go',bd='5',width=15,bg='yellow',fg='blue',
                command=lambda:matched_acked(matched,ack_clicked)).place(x=240,y=200)

    # open sign up page if sign up is clicked
    SignUp_btn=Button(login,text='Sign Up',bd='5',width=15,bg='brown',fg='black',
                command=lambda:signup_frame(SignUp_frame)).place(x=240,y=230)
    Home_frame.mainloop()
    login.mainloop()

login()