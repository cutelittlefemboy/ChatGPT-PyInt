import customtkinter
import openai
import threading

class App:
    
    def __init__(self):   
        
        self.api_key = None        
        self.is_running = True
        self.current_prompt = None
        self.current_reply = None
        
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        
        self.root = customtkinter.CTk()
        self.root.geometry("700x700+200+200")
        self.root.minsize(600, 600)
        
        self.root.title("ChatGPT GUI Interface")
        try:
            self.root.iconbitmap("app_logo.ico")
        except Exception as e:
            print("Icon not found:\n", e)
        
        #Main frame
        self.main_label = customtkinter.CTkLabel(self.root, text="ChatGPT GUI Interface", font=("Arial", 25))
        self.main_label.pack(fill=customtkinter.X, padx=20, pady=20)
        
        self.main_frame = customtkinter.CTkFrame(self.root)
        self.main_frame.pack(fill=customtkinter.BOTH, expand=True, padx=5, pady=5)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        #Top frame
        self.top_frame = customtkinter.CTkFrame(self.main_frame)
        self.top_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
        self.top_frame.grid_rowconfigure(0, weight=0)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=0)
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        self.prompt_message = customtkinter.CTkLabel(self.top_frame, text="Your prompt:", font=("Arial", 15))
        self.prompt_message.grid(column=0, row=0, padx=5, pady=0, sticky="w")
        
        self.prompt_textbox = customtkinter.CTkTextbox(self.top_frame, width=400, height = 200, font=("Arial", 14))
        self.prompt_textbox.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        
        self.submit_button = customtkinter.CTkButton(self.top_frame, text="Submit", command=self.submit_prompt)
        self.submit_button.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")
        
        #Bottom frame
        self.bottom_frame = customtkinter.CTkFrame(self.main_frame)
        self.bottom_frame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
        self.bottom_frame.grid_rowconfigure(0, weight=0)
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        
        self.prompt_message = customtkinter.CTkLabel(self.bottom_frame, text="Response:", font=("Arial", 15))
        self.prompt_message.grid(column=0, row=0, padx=5, pady=0, sticky="w")
        
        self.response_textbox = customtkinter.CTkTextbox(self.bottom_frame, width=400, height = 200, state="disabled", font=("Arial", 14))
        self.response_textbox.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

    def run(self):
        self.root.mainloop()

    def submit_prompt(self):
        if self.api_key == None:
            self.set_api_key()
        textbox_content = self.prompt_textbox.get("0.0", "end")
        self.current_prompt=[{"role": "user", "content": textbox_content}]
        
        #Creates a thread that queries chatgpt and then periodically checks if a response was recieved
        thread = threading.Thread(target=self.get_response)
        thread.start()
        self.root.after(5000, self.check_response)
    
    def check_response(self):
        if self.current_reply == None:
            self.root.after(2000, self.check_response) #reschedule if no response
            return
        self.display_response()
        
        
    def display_response(self):
        self.response_textbox.configure(state="normal")
        self.response_textbox.insert("0.0", self.current_reply)
        self.response_textbox.configure(state="disabled")
        self.current_reply = None
        
    def get_response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.current_prompt
        )
        self.current_reply = response["choices"][0]["message"]["content"]
        self.current_prompt = None

    def set_api_key(self):
        #Tries to read a file with the api key
        try:
            with open("api_key.txt", "r") as file:
                content=file.read().strip("\n")
                openai.api_key = content
                self.api_key = content
        #if it doesn't exist asks for the api key with a dialog
        except Exception as e:
            dialog = customtkinter.CTkInputDialog(text="Type your openAI API key:", title="API key")
            text = dialog.get_input()
            self.api_key = text
            openai.api_key = text
            #and tries to create a file with the api key
            try:
                with open("api_key.txt", "w") as file:
                    file.write(text)
            except Exception as e:
                return
        
main = App()
main.run()