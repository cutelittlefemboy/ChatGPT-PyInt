import customtkinter
import openai
import threading
import os

class Request:
    def __init__(self) -> None:
        self.request_running = False
        self.prompt = None
        self.reply = None
        self.invalid_key = False

class App:
    
    def __init__(self):
        self.request = Request()
        
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
        if self.request.request_running == True:
            self.generate_popup("One request at a time!")
            return
        if openai.api_key == None:
            self.set_api_key()
        textbox_content = self.prompt_textbox.get("0.0", "end")
        self.request.prompt=[{"role": "user", "content": textbox_content}]

        #Creates a thread that queries chatgpt and then periodically checks if a response was recieved
        self.response_textbox.configure(state="normal")
        self.response_textbox.delete("0.0", "end")
        self.response_textbox.insert("0.0", "Waiting for response...")
        self.response_textbox.configure(state="disabled")
        
        thread = threading.Thread(target=self.get_response)
        thread.start()
        self.root.after(2000, self.check_response)
        
    def get_response(self):
        self.request.request_running = True
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.request.prompt
            )
        except Exception as e:
            openai.api_key = None
            self.request.invalid_key = True
            self.request.reply = "Invalid API Key"
            return
        self.request.reply = response["choices"][0]["message"]["content"]
    
    def check_response(self):
        if self.request.reply == None:
            self.root.after(2000, self.check_response) #reschedule if no response
            return
        self.request.request_running = False
        self.display_response()
        
    def display_response(self):
        self.response_textbox.configure(state="normal")
        self.response_textbox.delete("0.0", "end")
        self.response_textbox.insert("0.0", self.request.reply)
        self.response_textbox.configure(state="disabled")

        self.current_reply = None

    def set_api_key(self):
        #Tries to read a file with the api key
        if os.path.exists("api_key.txt") and self.request.invalid_key:
            os.remove("api_key.txt")
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r") as file:
                content=file.read().strip("\n")
                print(content)
                openai.api_key = content
        #if it doesn't exist asks for the api key with a dialog
        else:
            dialog = customtkinter.CTkInputDialog(text="Type your openAI API key:", title="API key")
            text = dialog.get_input()
            openai.api_key = text
            #and tries to create a file with the api key
            try:
                with open("api_key.txt", "w") as file:
                    file.write(text)
            except Exception as e:
                self.generate_popup("Cannot create apikey.txt. Not critical. Continuing...")
                return
    
    def generate_popup(self, message):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        popup = customtkinter.CTkToplevel()
        popup.resizable(False, False)
        popup.geometry(f"200x100+{screen_width//2-100}+{screen_height//2-50}")
        popup.title(message)
        customtkinter.CTkLabel(popup, text=message, font=("Arial", 12)).pack(padx=5, pady=5)
        customtkinter.CTkButton(popup, text="Ok", command=popup.destroy).pack(padx=5, pady=5)
        popup.attributes("-topmost", True)

main = App()
main.run()