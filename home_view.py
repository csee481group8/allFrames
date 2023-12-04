import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import PhotoImage
from Page_view import CollectPage, Settings_page


class HomeView(ttk.Frame):
    def __init__(self,master,**kw):
        super().__init__(master,**kw)

        # Key: account menu list names
        # Value: Page object
        self.pages = {}

        # leave enough room to row 0 and column 1
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(1,weight=1)

        self.create_widgets()
        
        self.create_frame_treeview().grid(row=0,column=0,sticky="nwse")
        self.frame_treeview.pack_forget()

        self.create_frame_page().grid(row=0,column=0)

    def create_widgets(self) -> ttk.Frame:
        """
        Create the frame that will show the current home page
        
        :return: ttk.Frame
        """
        self.widges_frame = ttk.Frame(self)

        # Load the image
        self.image = PhotoImage(file="resizeduser.png")
        

        def toggle_frame_pack(frame):
            global frame_visible
            frame_visible = False
            
            if frame_visible == True:
                frame.pack_forget()
                frame_visible = False
                frame.pack(expand=True, before = btnToggle)
            else:
                frame.pack()
                frame_visible = True

        frame_visible = True
        btnToggle = ttk.Button(self, text = 'Account',
                                command=lambda:toggle_frame_pack(self.frame_treeview), 
                                image=self.image).place(relx=.01,rely=0,relheight=0.05,relwidth=0.15)
        
        Chat_frame = ttk.Frame(self)
        btnChat = ttk.Button(self, text = "Voice Chat", padding=(25,50),
                        command=[Chat_frame.lift(),self.widges_frame.pack_forget()]).place(relx=0.1,rely=0.1,relheight=0.35,relwidth=0.35)
        Video_frame = ttk.Frame(self)
        btnCall = ttk.Button(self, text = "Video Call", padding=(25,50),
                            command=lambda:Video_frame.tkraise()).place(relx=0.5,rely=0.1,relheight=0.35,relwidth=0.35)
        Game_frame = ttk.Frame(self)
        btnGame = ttk.Button(self, text = "Game", padding=(25,50),
                            command=lambda:Game_frame.tkraise()).place(relx=0.1,rely=0.55,relheight=0.35,relwidth=0.35)
        Other_frame = ttk.Frame(self)
        btnOther = ttk.Button(self, text = "Other functions", padding=(25,50),
                            command=lambda:Other_frame.tkraise()).place(relx=0.5,rely=0.55,relheight=0.35,relwidth=0.35)
        return self.widges_frame
        
    
    def create_frame_page(self) -> ttk.Frame:
        """
        Create the frame that will show the current account list page
        
        :return: ttk.Frame
        """
        self.frame_page = ttk.Frame(self)

        return self.frame_page
    
    def create_frame_treeview(self) -> ttk.Frame:
        """
        Create the frame that will hold the account treeview widget
        and also instantiate the AccountTreeview class
        
        :return: ttk.Frame
        """

        self.frame_treeview = ttk.Frame(self)

        self.treeview_list = AccountTreeView(self.frame_treeview)
        self.treeview_list.bind("<<TreeviewSelect>>",self.on_treeview_selection_changed)
        self.treeview_list.pack(fill=tk.BOTH, expand=True)

        return self.frame_treeview
        
    def on_treeview_selection_changed(self,event):
        """
        Switch to the frame related to the newly selected account list.

        :param event:
        :return: None

        """
        selected_item = self.treeview_list.focus()
        list_name = self.treeview_list.item(selected_item).get("text")

        self.show_page(list_name)

    def show_page(self,list_name:str):
        """
        pack_forget() all pages and pack the given page name
        
        :param list_name: the selected/page to show
        :return: None
        """
        for page_name in self.pages.keys():
            self.pages[page_name].pack_forget()
        
        self.pages[list_name].pack(fill=tk.BOTH, expand=True)

    def add_page(self, image_path:str,list_name:str,page):
        """
        Instantiate a page frame and add it to the pages dictionary
        
        :param image_path: a path to an image file
        :param list_name: str
        :param page: a Page class
        :return: None
        """

        # Load the image and convert it to a photo image
        with Image.open(image_path) as img:
            # Convert it to a photo image
            photo_image = ImageTk.PhotoImage(img)

        # Add page to dictionary so we can show it when needed
        self.pages[list_name] = page(self.frame_page)

        # Keep a reference to the image so that it doesn't get garbage collected
        self.pages[list_name].image = photo_image

        # Insert the account list name into the account treeview
        self.treeview_list.add_List(section_text=list_name)
        


class AccountTreeView(ttk.Treeview):
    def __init__(self,master,**kw):
        super().__init__(master,**kw)

        self.heading("#0",text='1',image='resizeduser.png')


    def add_List(self,section_text:str):
        """
        Insert a row
        
        :param section_text:str
        :return: None
        """

        self.insert(parent="",
                    index=tk.END,
                    text=section_text)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")

    home = HomeView(root,relief="flat")
    
    home.add_page(image_path="resizeduser.png",
                    list_name="Collected data",
                    page=CollectPage)
    home.add_page(image_path="resizedsetting.png",
                    list_name="Settings",
                      page=CollectPage)

    # # Read the Image
    # image = Image.open("settings.png")
    
    # # Resize the image using resize() method
    # resize_image = image.resize((15, 18))
    
    # resize_image.save("resizedsetting.png")


    home.pack(fill=tk.BOTH,expand=True)
    home.mainloop()

    
