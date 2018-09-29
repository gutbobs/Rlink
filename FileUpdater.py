#########################################################################
#
#	adds RS Monitor slots to exported .bin file
#
#########################################################################
import re
import os
import tkinter as tk
import tkinter.filedialog as tkfiledialog

def ShowChoice():
	print(v.get())

def getinputfile():
	root.filename_in =  tkfiledialog.askopenfilename(initialdir = "/",
		title = "Select file",filetypes = (("bin files","*.bin"),("all files","*.*")))
	Button_Process.place(x=25,y=530)
	Button_SelectFile_Var.set("File selected: {}".format(root.filename_in))

def loadtobuffer(filename):
	# load file to buffer
	with open(filename, 'rb') as content_file:
	    content = content_file.read()

	offset = 0
	display_output = [0]
	output_buffer = []
	for char in content:
		offset+=1
		display_output.append(hex(char))
		if offset % 16 == 0:
			#print (display_output)
			display_output=[hex(offset)]
		output_buffer.append(char)
	return output_buffer
	
def process():

	car_select = v.get()
	if car_select == 0: RSMonitor="01"
	elif car_select == 1: RSMonitor="02"

	slot1 = Text_Slot1.get(1.0, tk.END)[:-1]
	slot2 = Text_Slot2.get(1.0, tk.END)[:-1]

	print(slot1)
	print(slot2)
	print(RSMonitor)

	searched_offsets = {"0xB11":RSMonitor,"0xB12":slot1,"0xC02":slot2}

	try:
		print(root.filename_in)
		filename_in_exists = True
	except:
		filename_in_exists = False

	if filename_in_exists: 
		print(root.filename_in)
		output_buffer = loadtobuffer(root.filename_in)
		path, filename = os.path.split(root.filename_in)
		filename_out = os.path.join(path,"UPDATED_{}".format(filename))
		print(filename_out)

		for key in searched_offsets:
			print(key)
			searched_offset_int = int(key,16)
			insert_str = searched_offsets[key]

			# convert insert_str to list of 2 byte chunks
			insert = re.findall('..?',insert_str)

			for index,char in enumerate(insert):
				buffer_index = searched_offset_int+index
				old_char = output_buffer[buffer_index]
				print (hex(buffer_index),old_char,char)
				output_buffer[buffer_index] = int(char,16)


		output = open(filename_out,'wb')
		binary_format = bytearray(output_buffer)
		output.write(binary_format)
		output.close()

		result = "File output to: {}".format(filename_out)
		Label_Result_Var.set('Result: {}'.format(result))

	else:
		result = "Nothing to process"
		Label_Result_Var.set('Result: {}'.format(result))

	#print(v.get())


	#print(entries['Slot 1'].get())
	#print(entries['Slot 2'].get())



if __name__=="__main__":
	# set the variables
	cars = [("Megane 3 (X95)",1),("Clio 4 (X98)",2)]
	WindowTitle = "EEPROM File Updater"
	WindowGeometry = "500x600"
	Label_SelectCar_txt = "Car Selection"
	Label_SlotTitle_txt = "Slot Data"
	Label_Slot1_txt = "Slot 1:"
	Label_Slot2_txt = "Slot 2:"
	Label_SelectFile_txt = "Select input file"
	Label_SelectedFile_txt = "Selected File: No File Selected"
	Label_Result_txt = "Result: n/a"
	Button_SelectFile_txt = Label_SelectFile_txt
	Button_Process_txt = "Modify File"

	# build the GUI

	root = tk.Tk()
	root.title(WindowTitle)
	root.geometry(WindowGeometry)

	v = tk.IntVar()
	v.set(0)  # initializing the choice, i.e. Meg

	Label_SelectCar_Var = tk.StringVar()
	Label_SlotTitle_Var = tk.StringVar()
	Label_Slot1_Var = tk.StringVar()
	Label_Slot2_Var = tk.StringVar()
	Label_SelectFile_Var = tk.StringVar()
	Label_SelectedFile_Var = tk.StringVar()
	Label_Result_Var = tk.StringVar()

	Button_SelectFile_Var = tk.StringVar()
	Button_Process_Var = tk.StringVar()

	Label_SelectCar_Var.set(Label_SelectCar_txt)
	Label_SlotTitle_Var.set(Label_SlotTitle_txt)
	Label_Slot1_Var.set(Label_Slot1_txt)
	Label_Slot2_Var.set(Label_Slot2_txt)
	Label_SelectFile_Var.set(Label_SelectFile_txt)
	Label_SelectedFile_Var.set(Label_SelectedFile_txt)
	Label_Result_Var.set(Label_Result_txt)

	Button_SelectFile_Var.set(Button_SelectFile_txt)
	Button_Process_Var.set(Button_Process_txt)

	

	Label_SelectCar = tk.Label(root,textvariable=Label_SelectCar_Var,justify = tk.LEFT,	 padx = 20).pack()


	for val, car in enumerate(cars):
		tk.Radiobutton(root, 
			text=car[0],
			padx = 20, 
			variable=v, 
			command=ShowChoice,
			value=val).pack(anchor=tk.W)

	# Place Labels
	Label_SlotTile = tk.Label(root,textvariable=Label_SlotTitle_Var, justify = tk.LEFT,	 padx = 20).pack()
	Label_Slot1 = tk.Label(root,textvariable=Label_Slot1_Var)
	Label_Slot2 = tk.Label(root,textvariable=Label_Slot2_Var)
	Label_SelectFile = tk.Label(root,textvariable=Label_SelectFile_Var)
	Label_SelectedFile = tk.Label(root,textvariable=Label_SelectedFile_Var)
	Label_Result = tk.Label(root,textvariable=Label_Result_Var)


	Label_Slot1.place(x=25,y=170)
	Label_Slot2.place(x=25,y=370)
	Label_Result.place(x=25,y=578)
	#Label_SelectFile.place(x=25,y=500)
	#Label_SelectedFile.place(x=25,y=520)

	# place text entry fields
	Text_Slot1 = tk.Text(root,width=48,height=10)
	Text_Slot1.place(x=75,y=100)
	Text_Slot2 = tk.Text(root,width=48,height=10)
	Text_Slot2.place(x=75,y=300)	

	# Place buttons
	Button_SelectFile = tk.Button(textvariable=Button_SelectFile_Var,command=getinputfile,width = 62)
	Button_Process = tk.Button(textvariable=Button_Process_Var,command=process,width = 62)
	
	Button_SelectFile.place(x=25,y=497)
	Button_Process.pack_forget()

	#label3 = 
	#label4 = 



	root.mainloop()