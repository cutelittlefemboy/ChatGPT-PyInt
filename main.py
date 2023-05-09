import customtkinter
import openai

class App:
    
    def __init__(self):   
        self.api_key = None
        
        self.is_running = True
        
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        
        self.root = customtkinter.CTk()
        self.root.title("ChatGPT GUI Interface")
        
        try:
            self.root.iconbitmap("app_logo.ico")
        except Exception as e:
            print("Icon not found")
        
        self.main_label = customtkinter.CTkLabel(self.root, text="ChatGPT GUI Interface", font=("Arial", 18))
        self.main_label.pack(padx=20, pady=20)
        self.prompt_message = customtkinter.CTkLabel(self.root, text="Your prompt:", font=("Arial", 15))
        self.prompt_message.pack(padx=10, pady=5)
        self.prompt_textbox = customtkinter.CTkTextbox(self.root, width=400)
        self.prompt_textbox.pack(padx=20, pady=20)
        self.submit_button = customtkinter.CTkButton(self.root, text="Submit", command=self.submit_prompt)
        self.submit_button.pack(padx=20, pady=10)
        self.quit_button = customtkinter.CTkButton(self.root, text="Quit", command=self.stop)
        self.quit_button.pack(padx=20, pady=10)

    def loop(self):
        while self.is_running:
            self.root.update()

    def stop(self):
        self.is_running = False

    def submit_prompt(self):
        if self.api_key == None:
            print("No api_key")
            return
        prompt=self.prompt_textbox.get("0.0", "end")
        print(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            message=prompt
        )
        
    def set_api_key(self):
        key = "test"
        api_key = key
        
main = App()
main.loop()