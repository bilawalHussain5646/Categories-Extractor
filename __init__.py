import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import tkinter as tk
import tkinter.font as tkFont
import threading
import json
import re

# def InfiniteScrolling(driver):
#         last_height = driver.execute_script("return document.body.scrollHeight")
#         while True:
#             # Scroll down to bottom
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#             # Wait to load page
#             time.sleep(4)

#             # Calculate new scroll height and compare with last scroll height
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height



def Categories_Extractor(driver,url,i,labels):
        # output_df = pd.DataFrame(columns=['Model','LG'])
        # print(url)
        url = str(url)
        if url == "null" or url == "nan":
            url = "/ae/null"
        data = []
        driver.get("https://www.lg.com"+str(url))
        try:
        # Use XPath to locate the script element
            script_element = driver.find_element(By.XPATH, '//script[contains(text(),"var standardData")]')

            # Extract the text content of the script element
            script_text = script_element.get_attribute('text')
            

            # Import the json library to parse the JSON data
            all_data = {}

            # Split the JavaScript string into lines
            lines = script_text.split('\n')

            # Iterate through each line and look for lines with key-value pairs
            for line in lines:
                # Remove leading and trailing whitespace
                line = line.strip()
                
                # Check if the line contains a key-value pair
                if line.startswith('"') and ':' in line:
                    # Split the line into key and value based on the colon
                    key, value = line.split(':', 1)
                    
                    # Remove surrounding quotes and trim whitespace
                    key = key.strip('" ').strip()
                    value = value.strip('" ').strip(',')
                    
                    # Add the key-value pair to the dictionary
                    all_data[key] = value

            # Print the resulting dictionary
            # print(all_data)

            
            if i == 0:
                for key,values in all_data.items():
                    labels.append(key)
                    
                # print("")
                i+=1
            for x in range(1,len(labels)):
                data.append(all_data[labels[x]])
            # print(labels)
            # print(data)
            
            return labels,data,i
        except:
            return labels,data,i

        # Initialize an empty dictionary
        # result_dict = {}

        # # Use regular expressions to find and extract variable assignments
        # assignments = re.findall(r'(\w+)\s*=\s*{([^}]+)}', script_text)
        
        # # Loop through the assignments and convert them to Python dictionary entries
        # for variable, value in assignments:
        #     print(value)
        #     print(variable)
        #     # Convert the JSON-style string to a Python dictionary
        #     value_dict = eval("{" + value + "}")
        #     result_dict[variable] = value_dict

        # # Display the resulting Python dictionary
        # print(result_dict)



        # data = json.loads(json_data)

        # print(data)
        time.sleep(5)
       
                
                


                

        # with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
        #     output_df.to_excel(writer)
        


def Run_Script():

    data = pd.read_excel("pages.xlsx",sheet_name="Sheet2")
    
    driver = webdriver.Chrome()
    list_of_urls = data["Page"]
    # print(list_of_urls)
    i=0
    labels = ["url"]
    data_df = []
    for url in list_of_urls:
        
        labels,data,i=Categories_Extractor(driver,url,i,labels)
        # Merge the array of link with another array of data and send that array to data df 
        url_array = [str(url)]
        merged_array = url_array+data
        data_df.append(merged_array)
        # print(merged_array)
        df = pd.DataFrame(data_df, columns=labels)
        df.to_excel("output.xlsx")
        
    # df = pd.DataFrame(data_df, columns=labels)
    # df.to_excel("output.xlsx")
    
    # print(df)
    
    # time.sleep(100)

                 
         

# Main App 
class App:

    def __init__(self, root):
        #setting title
        root.title("Categories Extractor")
        ft = tkFont.Font(family='Arial Narrow',size=13)
        #setting window size
        width=640
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg='black')

        ClickBtnLabel=tk.Label(root)
       
      
        
        ClickBtnLabel["font"] = ft
        
        ClickBtnLabel["justify"] = "center"
        ClickBtnLabel["text"] = "Extract the data"
        ClickBtnLabel["bg"] = "black"
        ClickBtnLabel["fg"] = "white"
        ClickBtnLabel.place(x=120,y=190,width=150,height=70)
    

        
        Lulu=tk.Button(root)
        Lulu["anchor"] = "center"
        Lulu["bg"] = "#009841"
        Lulu["borderwidth"] = "0px"
        
        Lulu["font"] = ft
        Lulu["fg"] = "#ffffff"
        Lulu["justify"] = "center"
        Lulu["text"] = "START"
        Lulu["relief"] = "raised"
        Lulu.place(x=375,y=190,width=150,height=70)
        Lulu["command"] = self.start_func




  

    def ClickRun(self):

        running_actions = [
            Run_Script,          
         
        ]

        thread_list = [threading.Thread(target=func) for func in running_actions]

        # start all the threads
        for thread in thread_list:
            thread.start()

        # wait for all the threads to complete
        for thread in thread_list:
            thread.join()
    
    def start_func(self):
        thread = threading.Thread(target=self.ClickRun)
        thread.start()

    
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


# Run()
