import tkinter as tk 
import numpy as np

class Title:
    def __init__(self,master):
        self.master = master
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=0)
        self.frame = tk.Frame(self.master,bg='black')
        self.label = tk.Label(self.master,text="PTT Instrument Project",font=('Helvetica',10),bg="deep sky blue",width=40)
        self.label.grid(row=0,column=0,columnspan=8,padx=0,pady=0,sticky='nsew')
class Setup:
    
    def __init__(self,master):
        self.master = master
        self.start_freq = tk.DoubleVar()
        self.start_freq.set(2.4)
        self.stop_freq = tk.DoubleVar()
        self.stop_freq.set(3.2)
        self.frame = tk.Frame(self.master).grid(row=1,column=0)
        self.label1 = tk.Label(self.frame,text="Start Frequency(GHz)")
        self.label2 = tk.Label(self.frame,text="Stop Frequency(GHz)")
        self.entry1 = tk.Entry(self.frame,textvariable=self.start_freq,font=('Helvetica',10),width=20)
        self.entry2 = tk.Entry(self.frame,textvariable=self.stop_freq,font=('Helvetica',10),width=20)
        self.button1 = tk.Button(self.frame,text='set',command=self.Start_click,bd=3)
        self.button2 = tk.Button(self.frame,text='set',command=self.Stop_click,bd=3)
    
    #Grid set up
        self.label1.grid(row=1,column=0)
        self.label2.grid(row=2,column=0)
        self.entry1.grid(row=1,column=1)
        self.entry2.grid(row=2,column=1)
        self.button1.grid(row=1,column=2)
        self.button2.grid(row=2,column=2)


       
        
    def Start_click(self):
        self.start_value= self.start_freq.get()*10e9
        #self.entry1.delete(0,'end')
        print(self.start_value)
        

    def Stop_click(self):
        self.stop_value=self.stop_freq.get()*10e9
        #self.entry2.delete(0,'end')
        print(self.stop_value)

class Storedata:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master).grid(row=1,column=3)
        self.label1 = tk.Label(self.frame,text="1st Solution ")
        self.label2 = tk.Label(self.frame,text="2nd Solution ")
        self.label3 = tk.Label(self.frame,text="3rd Solution ")
        self.button1 = tk.Button(self.frame,text='store',bd=5,command=self.store_function1)
        self.button2 = tk.Button(self.frame,text='store',bd=5,command=self.store_function2)
        self.button3 = tk.Button(self.frame,text='store',bd=5,command=self.store_function3)
        self.button = tk.Button(self.frame,text="reset store",command=self.reset,bd=2,bg="firebrick1",font=("Helvetica", 10))
        
    #Grid position 
        self.label1.grid(row=1,column=3)
        self.label2.grid(row=2,column=3)
        self.label3.grid(row=3,column=3)
        self.button1.grid(row=1,column=4)
        self.button2.grid(row=2,column=4)
        self.button3.grid(row=3,column=4)
        self.button.grid(row=5,column=4,stick='w')

    def store_function1(self):
        self.store1 = 1
        self.button1 = tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=1,column=4)
        
    
    def store_function2(self):
        self.store2 = 2
        print('store2')
        self.button2 = tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=2,column=4)

    
    def store_function3(self):
        self.store3 = 4 
        print(self.store3)
        self.button3 = tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=3,column=4)
    
    def reset(self):
        print('reset')
        self.button1 = tk.Button(self.frame,text='store',command=self.store_function1,bd=5).grid(row=1,column=4)
        self.button2 = tk.Button(self.frame,text='store',command=self.store_function2,bd=5).grid(row=2,column=4)
        self.button3 = tk.Button(self.frame,text='store',command=self.store_function3,bd=5).grid(row=3,column=4)

class Comment:
    def __init__(self,master):
        self.master = master
        self.text_comment = tk.StringVar()
        self.percentage_amine = tk.DoubleVar()
        self.frame = tk.Frame(self.master).grid(row=2,column=1)
        self.label = tk.Label(self.frame,text='Comment')
        self.label2 = tk.Label(self.frame,text="Percentage Amine(%)")
        self.entry = tk.Entry(self.frame,textvariable=self.text_comment,borderwidth=2,highlightcolor="blue",width=20,font=('Helvetica',10))
        self.entry2 = tk.Entry(self.frame,textvariable=self.percentage_amine,width=10)
        self.button = tk.Button(self.frame,text='save',command=self.save)
    
    # #Grid set up 
   
        self.label.grid(row=3,column=0)
        self.label2.grid(row=4,column=0)
        self.entry.grid(row=3,column=1)
        self.entry2.grid(row=4,column=1,stick='w')
        self.button.grid(row=3,column=2)

    def save(self):
        self.operation_comment=self.text_comment.get()
        print(self.operation_comment)
        self.percentage = self.percentage_amine.get()
        print('percentage: %.1f '%(self.percentage))
        self.entry.delete(0, 'end')
        self.entry2.delete(0, 'end')
    
    
     
    
class Vna_option:
    
    def __init__(self,master):
        self.master = master
        self.single_value =1
        self.auto_value =1 
        self.frame = tk.Frame(self.master).grid(row=5,column=0)
        self.label = tk.Label(self.frame,text='Option',font=('Helvetica',10)).grid(row=5,column=0,sticky='nesw')
        self.button = tk.Button(self.frame,text='Sweep frequency',command=self.sweep_operation,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=1,stick='nesw')
        self.button1 = tk.Button(self.frame,text='Single',command=self.freezvalue,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=2,stick='nesw')
        self.button2 = tk.Button(self.frame,text='Auto',command=self.coutinuous,bg='deep sky blue',bd=2,font=('Helvetica',10),width=10).grid(row=5,column=3,stick='nesw')
        self.button3 = tk.Button(self.frame,text='Start Calibration',command=self.calibration,bd=2,bg='deep sky blue').grid(row=6,column=1,stick='nesw')

    def sweep_operation(self):
    
        pass
    
    
    def freezvalue(self):
        
        if self.single_value % 2 == 1:
            self.button1 = tk.Button(self.frame,text='Single',command=self.freezvalue,bg='red',bd=2,font=('Helvetica',10)).grid(row=5,column=2,stick='nesw')
            self.button2 = tk.Button(self.frame,text='Auto',command=self.coutinuous,state='disabled',bg='deep sky blue',bd=2,font=('Helvetica',10),width=10).grid(row=5,column=3,stick='nesw')
            
            #some task 
            self.single_value +=1
        elif self.single_value % 2 == 0:
            self.button1 = tk.Button(self.frame,text='Single',command=self.freezvalue,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=2,stick='nesw')
            self.button2 = tk.Button(self.frame,text='Auto',command=self.coutinuous,bg='deep sky blue',bd=2,font=('Helvetica',10),width=10).grid(row=5,column=3,stick='nesw')
            
            #some task 
            self.single_value +=1
        
    def coutinuous(self):
        if self.auto_value % 2 == 1:
            self.button2 = tk.Button(self.frame,text='Auto',command=self.coutinuous,bg='red',bd=2,font=('Helvetica',10)).grid(row=5,column=3,stick='nesw')
            self.button1 = tk.Button(self.frame,text='Single',command=self.freezvalue,state='disabled',bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=2,stick='nesw')
            
            #some task 
            self.auto_value +=1
        elif self.auto_value % 2 == 0:
            self.button2 = tk.Button(self.frame,text='Auto',command=self.coutinuous,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=3,stick='nesw')
            self.button1 = tk.Button(self.frame,text='Single',command=self.freezvalue,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=2,stick='nesw')
            
            #some task 
            self.auto_value +=1
    
    def calibration(self):
        
        pass 

class Comparison:
    def __init__(self,master):
        self.master = master
       
        self.frame = tk.Frame(self.master).grid(row=1,column=5)
        self.canvas1 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas2 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas3 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas4 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas5 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas6 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas7 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas8 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas9 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        
    #Grid position 
        self.canvas1.grid(row=1,column=5,padx=2)
        self.canvas2.grid(row=1,column=6,padx=2)
        self.canvas3.grid(row=1,column=7,padx=2)
        self.canvas4.grid(row=2,column=5,padx=2)
        self.canvas5.grid(row=2,column=6,padx=2)
        self.canvas6.grid(row=2,column=7,padx=2)
        self.canvas7.grid(row=3,column=5,padx=2)
        self.canvas8.grid(row=3,column=6,padx=2)
        self.canvas9.grid(row=3,column=7,padx=2)
        
        
        

    def solution_compare(self):
        self.value_store1 = Storedata.self.store1
        print('aa')
        pass        

def main():
    root=tk.Tk()
    root.title("PTT Instrument Project")
    title =Title(root)
    setup=Setup(root)
    storedata=Storedata(root)
    comment=Comment(root)
    vna=Vna_option(root)
    comparison=Comparison(root)
    
    root.mainloop()
if __name__=='__main__':
    main()
    

            